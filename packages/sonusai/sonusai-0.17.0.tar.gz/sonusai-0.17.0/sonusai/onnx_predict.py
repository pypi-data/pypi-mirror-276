"""sonusai onnx_predict

usage: onnx_predict [-hvlwr] [--include GLOB] [-i MIXID] MODEL DATA ...

options:
    -h, --help
    -v, --verbose               Be verbose.
    -l, --list-device-details   List details of all OpenVINO available devices
    -i MIXID, --mixid MIXID     Mixture ID(s) to generate if input is a mixture database. [default: *].
    --include GLOB              Search only files whose base name matches GLOB. [default: *.{wav,flac}].
    -w, --write-wav             Calculate inverse transform of prediction and write .wav files
    -r, --reset                 Reset model between each file.

Run prediction (inference) using an onnx model on a SonusAI mixture dataset or audio files from a regex path.
The OnnxRuntime (ORT) inference engine is used to execute the inference.

Inputs:
    MODEL       ONNX model .onnx file of a trained model (weights are expected to be in the file).

    DATA        The input data must be one of the following:
                * WAV
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

                * directory
                  Using the given SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction. The MIXID is required.


Note there are multiple ways to process model prediction over multiple audio data files:
1. TSE (timestep single extension): mixture transform frames are fit into the timestep dimension and the model run as
   a single inference call.  If batch_size is > 1 then run multiple mixtures in one call with shorter mixtures
   zero-padded to the size of the largest mixture.
2. TME (timestep multi-extension): mixture is split into multiple timesteps, i.e. batch[0] is starting timesteps, ...
   Note that batches are run independently, thus sequential state from one set of timesteps to the next will not be
   maintained, thus results for such models (i.e. conv, LSTMs, in the tstep dimension) would not match using TSE mode.

TBD not sure below make sense, need to continue ??
2. BSE (batch single extension): mixture transform frames are fit into the batch dimension. This make sense only if
   independent predictions are made on each frame w/o considering previous frames (i.e.
   timesteps=1 or there is no timestep dimension in the model (timesteps=0).
3.classification

Outputs the following to ovpredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    onnx_predict.log

"""

from sonusai import logger
from typing import Any, List, Optional, Tuple
from os.path import basename, splitext, exists, isfile
import onnxruntime as ort
import onnx
from onnx import ValueInfoProto


def load_ort_session(model_path, providers=['CPUExecutionProvider']):
    if exists(model_path) and isfile(model_path):
        model_basename = basename(model_path)
        model_root = splitext(model_basename)[0]
        logger.info(f'Importing model from {model_basename}')
        try:
            session = ort.InferenceSession(model_path, providers=providers)
            options = ort.SessionOptions()
        except Exception as e:
            logger.exception(f'Error: could not load onnx model from {model_path}: {e}')
            raise SystemExit(1)
    else:
        logger.exception(f'Error: model file does not exist: {model_path}')
        raise SystemExit(1)

    logger.info(f'Opened session with provider options: {session._provider_options}.')
    try:
        meta = session.get_modelmeta()
        hparams = eval(meta.custom_metadata_map["hparams"])
        logger.info(f'Sonusai hyper-parameter metadata was found in model with {len(hparams)} parameters, '
                    f'checking for required ones ...')
        # Print to log here will fail if required parameters not available.
        logger.info(f'feature         {hparams["feature"]}')
        logger.info(f'batch_size      {hparams["batch_size"]}')
        logger.info(f'timesteps       {hparams["timesteps"]}')
        logger.info(f'flatten, add1ch {hparams["flatten"]}, {hparams["add1ch"]}')
        logger.info(f'truth_mutex     {hparams["truth_mutex"]}')
    except:
        hparams = None
        logger.warning(f'Warning: onnx model does not have required SonusAI hyper-parameters.')

    inputs = session.get_inputs()
    outputs = session.get_outputs()

    #in_names = [n.name for n in session.get_inputs()]
    #out_names = [n.name for n in session.get_outputs()]

    return session, options, model_root, hparams, inputs, outputs


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    listdd = args['--list-device-details']
    writewav= args['--write-wav']
    mixids = args['--mixid']
    reset = args['--reset']
    include = args['--include']
    model_path = args['MODEL']
    datapaths = args['DATA']

    providers = ort.get_available_providers()
    logger.info(f'Loaded Onnx runtime, available providers: {providers}.')

    session, options, model_root, hparams, sess_inputs, sess_outputs = load_ort_session(model_path)
    if hparams is None:
        logger.error(f'Error: onnx model does not have required Sonusai hyper-parameters, can not proceed.')
        raise SystemExit(1)
    if len(sess_inputs) != 1:
        logger.error(f'Error: onnx model does not have 1 input, but {len(sess_inputs)}. Exit due to unknown input.')

    in0name = sess_inputs[0].name
    in0type = sess_inputs[0].type
    out0name = sess_outputs[0].name
    out_names = [n.name for n in session.get_outputs()]

    from os.path import join, dirname, isdir, normpath, realpath, abspath
    from sonusai.utils.asr_manifest_functions import PathInfo
    from sonusai.utils import braced_iglob
    from sonusai.mixture import MixtureDatabase

    mixdb_path = None
    entries = None
    if len(datapaths) == 1 and isdir(datapaths[0]):  # Assume it's a single path to sonusai mixdb subdir
        in_basename = basename(normpath(datapaths[0]))
        mixdb_path= datapaths[0]
        logger.debug(f'Attempting to load mixture database from {mixdb_path}')
        mixdb = MixtureDatabase(mixdb_path)
        logger.debug(f'Sonusai mixture db load success: found {mixdb.num_mixtures} mixtures with {mixdb.num_classes} classes')
        p_mixids = mixdb.mixids_to_list(mixids)
        if len(p_mixids) != mixdb.num_mixtures:
            logger.info(f'Processing a subset of {p_mixids} from available mixtures.')
    else:  # search all datapaths for .wav, .flac (or whatever is specified in include)
        in_basename = ''
        entries: list[PathInfo] = []
        for p in datapaths:
            location = join(realpath(abspath(p)), '**', include)
            logger.debug(f'Processing {location}')
            for file in braced_iglob(pathname=location, recursive=True):
                name = file
                entries.append(PathInfo(abs_path=file, audio_filepath=name))

    from sonusai.utils import create_ts_name
    from os import makedirs
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    output_dir = create_ts_name('opredict-' + in_basename)
    makedirs(output_dir, exist_ok=True)
    # Setup logging file
    create_file_handler(join(output_dir, 'onnx-predict.log'))
    update_console_handler(verbose)
    initial_log_messages('onnx_predict')
    # Reprint some info messages
    logger.info(f'Loaded OnnxRuntime, available providers: {providers}.')
    logger.info(f'Read and compiled onnx model from {model_path}.')
    if len(datapaths) == 1 and isdir(datapaths[0]):  # Assume it's a single path to sonusai mixdb subdir
        logger.info(f'Loaded mixture database from {datapaths}')
        logger.info(f'Sonusai mixture db: found {mixdb.num_mixtures} mixtures with {mixdb.num_classes} classes')
    else:
        logger.info(f'{len(datapaths)} data paths specified, found {len(entries)} audio files.')
    if in0type.find('float16') != -1:
        model_is_fp16 = True
        logger.info(f'Detected input of float16, converting all feature inputs to that type.')
    else:
        model_is_fp16 = False


    if mixdb_path is not None:  # mixdb input
        # Assume (of course) that mixdb feature, etc. is what model expects
        if hparams["feature"] != mixdb.feature:
            logger.warning(f'Mixture feature does not match model feature, this inference run may fail.')
        feature_mode = mixdb.feature  # no choice, can't use hparams["feature"] since it's different than the mixdb

        #if hparams["num_classes"] != mixdb.num_classes:    # needs to be i.e. mixdb.feature_parameters
        #if mixdb.num_classes != model_num_classes:
        #     logger.error(f'Feature parameters in mixture db {mixdb.num_classes} does not match num_classes in model {inp0shape[-1]}')
        #     raise SystemExit(1)

        from sonusai.utils import reshape_inputs
        from sonusai.utils import reshape_outputs
        from sonusai.mixture import get_audio_from_feature
        from sonusai.utils import write_wav
        import numpy as np
        import h5py
        if hparams["batch_size"] == 1:
            for mixid in p_mixids:
                feature, _ = mixdb.mixture_ft(mixid)  # frames x stride x feature_params
                if hparams["timesteps"] == 0:
                    tsteps = 0                        # no timestep dim, reshape will take care
                else:
                    tsteps = feature.shape[0]         # fit frames into timestep dimension (TSE mode)
                feature, _ = reshape_inputs(feature=feature,
                                            batch_size=1,
                                            timesteps=tsteps,
                                            flatten=hparams["flatten"],
                                            add1ch=hparams["add1ch"])
                if model_is_fp16:
                    feature = np.float16(feature)
                # run inference, ort session wants i.e. batch x tsteps x feat_params, outputs numpy BxTxFP or BxFP
                predict = session.run(out_names, {in0name: feature})[0]
                #predict, _ = reshape_outputs(predict=predict[0], timesteps=frames)  # frames x feat_params
                output_fname = join(output_dir, mixdb.mixtures[mixid].name)
                with h5py.File(output_fname, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset('predict', data=predict)
                if writewav:  # note only makes sense if model is predicting audio, i.e. tstep dimension exists
                    # predict_audio wants [frames, channels, feature_parameters] equiv. to tsteps, batch, bins
                    predict = np.transpose(predict, [1, 0, 2])
                    predict_audio = get_audio_from_feature(feature=predict, feature_mode=feature_mode)
                    owav_name = splitext(output_fname)[0]+'_predict.wav'
                    write_wav(owav_name, predict_audio)


    #
    #     # sampler = None
    #     # p_datagen = TorchFromMixtureDatabase(mixdb=mixdb,
    #     #                                      mixids=p_mixids,
    #     #                                      batch_size=batch_size,
    #     #                                      cut_len=0,
    #     #                                      flatten=model.flatten,
    #     #                                      add1ch=model.add1ch,
    #     #                                      random_cut=False,
    #     #                                      sampler=sampler,
    #     #                                      drop_last=False,
    #     #                                      num_workers=dlcpu)
    #
    #     # Info needed to set up inverse transform
    #     half = model.num_classes // 2
    #     fg = FeatureGenerator(feature_mode=feature,
    #                           num_classes=model.num_classes,
    #                           truth_mutex=model.truth_mutex)
    #     itf = TorchInverseTransform(N=fg.itransform_N,
    #                                 R=fg.itransform_R,
    #                                 bin_start=fg.bin_start,
    #                                 bin_end=fg.bin_end,
    #                                 ttype=fg.itransform_ttype)
    #
    #     enable_truth_wav = False
    #     enable_mix_wav = False
    #     if wavdbg:
    #         if mixdb.target_files[0].truth_settings[0].function == 'target_mixture_f':
    #             enable_mix_wav = True
    #             enable_truth_wav = True
    #         elif mixdb.target_files[0].truth_settings[0].function == 'target_f':
    #             enable_truth_wav = True
    #
    #     if reset:
    #         logger.info(f'Running {mixdb.num_mixtures} mixtures individually with model reset ...')
    #         for idx, val in enumerate(p_datagen):
    #             # truth = val[1]
    #             feature = val[0]
    #             with torch.no_grad():
    #                 ypred = model(feature)
    #             output_name = join(output_dir, mixdb.mixtures[idx].name)
    #             pdat = ypred.detach().numpy()
    #             if timesteps > 0:
    #                 logger.debug(f'In and out tsteps: {feature.shape[1]},{pdat.shape[1]}')
    #             logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
    #             with h5py.File(output_name, 'a') as f:
    #                 if 'predict' in f:
    #                     del f['predict']
    #                 f.create_dataset('predict', data=pdat)
    #
    #             if wavdbg:
    #                 owav_base = splitext(output_name)[0]
    #                 tmp = torch.complex(ypred[..., :half], ypred[..., half:]).permute(2, 0, 1).detach()
    #                 itf.reset()
    #                 predwav, _ = itf.execute_all(tmp)
    #                 # predwav, _ = calculate_audio_from_transform(tmp.numpy(), itf, trim=True)
    #                 write_wav(owav_base + '.wav', predwav.permute([1, 0]).numpy(), 16000)
    #                 if enable_truth_wav:
    #                     # Note this support truth type target_f and target_mixture_f
    #                     tmp = torch.complex(val[0][..., :half], val[0][..., half:2 * half]).permute(2, 0, 1).detach()
    #                     itf.reset()
    #                     truthwav, _ = itf.execute_all(tmp)
    #                     write_wav(owav_base + '_truth.wav', truthwav.permute([1, 0]).numpy(), 16000)
    #
    #                 if enable_mix_wav:
    #                     tmp = torch.complex(val[0][..., 2 * half:3 * half], val[0][..., 3 * half:]).permute(2, 0, 1)
    #                     itf.reset()
    #                     mixwav, _ = itf.execute_all(tmp.detach())
    #                     write_wav(owav_base + '_mix.wav', mixwav.permute([1, 0]).numpy(), 16000)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # from os import makedirs
    # from os.path import isdir
    # from os.path import join
    # from os.path import splitext
    #
    # import h5py
    # import onnxruntime as rt
    # import numpy as np
    #
    # from sonusai.mixture import Feature
    # from sonusai.mixture import Predict
    # from sonusai.utils import SonusAIMetaData
    # from sonusai import create_file_handler
    # from sonusai import initial_log_messages
    # from sonusai import update_console_handler
    # from sonusai.mixture import MixtureDatabase
    # from sonusai.mixture import get_feature_from_audio
    # from sonusai.mixture import read_audio
    # from sonusai.utils import create_ts_name
    # from sonusai.utils import get_frames_per_batch
    # from sonusai.utils import get_sonusai_metadata
    #
    # output_dir = create_ts_name('ovpredict')
    # makedirs(output_dir, exist_ok=True)
    #
    #
    #
    # model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])
    # model_metadata = get_sonusai_metadata(model)
    #
    # batch_size = model_metadata.input_shape[0]
    # if model_metadata.timestep:
    #     timesteps = model_metadata.input_shape[1]
    # else:
    #     timesteps = 0
    # num_classes = model_metadata.output_shape[-1]
    #
    # frames_per_batch = get_frames_per_batch(batch_size, timesteps)
    #
    # logger.info('')
    # logger.info(f'feature       {model_metadata.feature}')
    # logger.info(f'num_classes   {num_classes}')
    # logger.info(f'batch_size    {batch_size}')
    # logger.info(f'timesteps     {timesteps}')
    # logger.info(f'flatten       {model_metadata.flattened}')
    # logger.info(f'add1ch        {model_metadata.channel}')
    # logger.info(f'truth_mutex   {model_metadata.mutex}')
    # logger.info(f'input_shape   {model_metadata.input_shape}')
    # logger.info(f'output_shape  {model_metadata.output_shape}')
    # logger.info('')
    #
    # if splitext(entries)[1] == '.wav':
    #     # Convert WAV to feature data
    #     logger.info('')
    #     logger.info(f'Run prediction on {entries}')
    #     audio = read_audio()
    #     feature = get_feature_from_audio(audio=audio, feature_mode=model_metadata.feature)
    #
    #     predict = pad_and_predict(feature=feature,
    #                               model_name=model_name,
    #                               model_metadata=model_metadata,
    #                               frames_per_batch=frames_per_batch,
    #                               batch_size=batch_size,
    #                               timesteps=timesteps,
    #                               reset=reset)
    #
    #     output_name = splitext()[0] + '.h5'
    #     with h5py.File(output_name, 'a') as f:
    #         if 'feature' in f:
    #             del f['feature']
    #         f.create_dataset(name='feature', data=feature)
    #
    #         if 'predict' in f:
    #             del f['predict']
    #         f.create_dataset(name='predict', data=predict)
    #
    #     logger.info(f'Saved results to {output_name}')
    #     return
    #
    # if not isdir():
    #     logger.exception(f'Do not know how to process input from {entries}')
    #     raise SystemExit(1)
    #
    # mixdb = MixtureDatabase()
    #
    # if mixdb.feature != model_metadata.feature:
    #     logger.exception(f'Feature in mixture database does not match feature in model')
    #     raise SystemExit(1)
    #
    # mixids = mixdb.mixids_to_list(mixids)
    # if reset:
    #     # reset mode cycles through each file one at a time
    #     for mixid in mixids:
    #         feature, _ = mixdb.mixture_ft(mixid)
    #
    #         predict = pad_and_predict(feature=feature,
    #                                   model_name=model_name,
    #                                   model_metadata=model_metadata,
    #                                   frames_per_batch=frames_per_batch,
    #                                   batch_size=batch_size,
    #                                   timesteps=timesteps,
    #                                   reset=reset)
    #
    #         output_name = join(output_dir, mixdb.mixtures[mixid].name)
    #         with h5py.File(output_name, 'a') as f:
    #             if 'predict' in f:
    #                 del f['predict']
    #             f.create_dataset(name='predict', data=predict)
    # else:
    #     features: list[Feature] = []
    #     file_indices: list[slice] = []
    #     total_frames = 0
    #     for mixid in mixids:
    #         current_feature, _ = mixdb.mixture_ft(mixid)
    #         current_frames = current_feature.shape[0]
    #         features.append(current_feature)
    #         file_indices.append(slice(total_frames, total_frames + current_frames))
    #         total_frames += current_frames
    #     feature = np.vstack([features[i] for i in range(len(features))])
    #
    #     predict = pad_and_predict(feature=feature,
    #                               model_name=model_name,
    #                               model_metadata=model_metadata,
    #                               frames_per_batch=frames_per_batch,
    #                               batch_size=batch_size,
    #                               timesteps=timesteps,
    #                               reset=reset)
    #
    #     # Write data to separate files
    #     for idx, mixid in enumerate(mixids):
    #         output_name = join(output_dir, mixdb.mixtures[mixid].name)
    #         with h5py.File(output_name, 'a') as f:
    #             if 'predict' in f:
    #                 del f['predict']
    #             f.create_dataset('predict', data=predict[file_indices[idx]])
    #
    # logger.info(f'Saved results to {output_dir}')
    #

# def pad_and_predict(feature: Feature,
#                     model_name: str,
#                     model_metadata: SonusAIMetaData,
#                     frames_per_batch: int,
#                     batch_size: int,
#                     timesteps: int,
#                     reset: bool) -> Predict:
#     import onnxruntime as rt
#     import numpy as np
#
#     from sonusai.utils import reshape_inputs
#     from sonusai.utils import reshape_outputs
#
#     frames = feature.shape[0]
#     padding = frames_per_batch - frames % frames_per_batch
#     feature = np.pad(array=feature, pad_width=((0, padding), (0, 0), (0, 0)))
#     feature, _ = reshape_inputs(feature=feature,
#                                 batch_size=batch_size,
#                                 timesteps=timesteps,
#                                 flatten=model_metadata.flattened,
#                                 add1ch=model_metadata.channel)
#     sequences = feature.shape[0] // model_metadata.input_shape[0]
#     feature = np.reshape(feature, [sequences, *model_metadata.input_shape])
#
#     model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])
#     output_names = [n.name for n in model.get_outputs()]
#     input_names = [n.name for n in model.get_inputs()]
#
#     predict = []
#     for sequence in range(sequences):
#         predict.append(model.run(output_names, {input_names[0]: feature[sequence]}))
#         if reset:
#             model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])
#
#     predict_arr = np.vstack(predict)
#     # Combine [sequences, batch_size, ...] into [frames, ...]
#     predict_shape = predict_arr.shape
#     predict_arr = np.reshape(predict_arr, [predict_shape[0] * predict_shape[1], *predict_shape[2:]])
#     predict_arr, _ = reshape_outputs(predict=predict_arr, timesteps=timesteps)
#     predict_arr = predict_arr[:frames, :]
#
#     return predict_arr


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
