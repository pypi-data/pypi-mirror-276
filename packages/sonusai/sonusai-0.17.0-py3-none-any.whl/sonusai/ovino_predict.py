"""sonusai ovino_predict

usage: ovino_predict [-hvlwr] [--include GLOB] [-i MIXID] MODEL DATA ...

options:
    -h, --help
    -v, --verbose               Be verbose.
    -l, --list-device-details   List details of all OpenVINO available devices
    -i MIXID, --mixid MIXID     Mixture ID(s) to generate if input is a mixture database. [default: *].
    --include GLOB              Search only files whose base name matches GLOB. [default: *.{wav,flac}].
    -w, --write-wav             Calculate inverse transform of prediction and write .wav files
    -r, --reset                 Reset model between each file.


Run prediction (inference) using an OpenVino model on a SonusAI mixture dataset or audio files from a regex path.

Inputs:
    MODEL       OpenVINO model .xml file (called the ov.Model format), requires accompanying .bin file
                to exist in same location with the same base filename.

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
2. BSE (batch single extension): mixture transform frame are fit into the batch dimension. This is possible only if
   timesteps=1 or there is no timestep dimension in the model (timesteps=0).
3.

Outputs the following to ovpredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    onnx_predict.log

"""

from sonusai import logger

def param_to_string(parameters) -> str:
    """Convert a list / tuple of parameters returned from OV to a string."""
    if isinstance(parameters, (list, tuple)):
        return ', '.join([str(x) for x in parameters])
    else:
        return str(parameters)


def openvino_list_device_details(core):
    logger.info('Requested details of OpenVINO available devices:')
    for device in core.available_devices:
        logger.info(f'{device} :')
        logger.info('\tSUPPORTED_PROPERTIES:')
        for property_key in core.get_property(device, 'SUPPORTED_PROPERTIES'):
            if property_key not in ('SUPPORTED_PROPERTIES'):
                try:
                    property_val = core.get_property(device, property_key)
                except TypeError:
                    property_val = 'UNSUPPORTED TYPE'
                logger.info(f'\t\t{property_key}: {param_to_string(property_val)}')
        logger.info('')



def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring
    import openvino as ov

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    listdd = args['--list-device-details']
    writewav= args['--write-wav']
    mixids = args['--mixid']
    reset = args['--reset']
    include = args['--include']
    model_name = args['MODEL']
    datapaths = args['DATA']


    core = ov.Core()   # Create runtime
    avail_devices = core.available_devices # simple report of available devices
    logger.info(f'Loaded OpenVINO runtime, available devices: {avail_devices}.')
    if listdd is True:   # print
        openvino_list_device_details(core)

    from os.path import abspath, join, realpath, basename, isdir, normpath, splitext
    from sonusai.utils.asr_manifest_functions import PathInfo
    from sonusai.utils import braced_iglob
    from sonusai.mixture import MixtureDatabase
    from typing import Any

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

    logger.info(f'Reading and compiling model from {model_name}.')
    compiled_model = core.compile_model(model_name, "AUTO")
    logger.info(f'Compiled model using default OpenVino compile settings.')

    from sonusai.utils import create_ts_name
    from os import makedirs
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    output_dir = create_ts_name('ovpredict-' + in_basename)
    makedirs(output_dir, exist_ok=True)
    # Setup logging file
    create_file_handler(join(output_dir, 'ovino_predict.log'))
    update_console_handler(verbose)
    initial_log_messages('ovino_predict')
    logger.info(f'Read and compiled OpenVINO model from {model_name}.')
    if len(datapaths) == 1 and isdir(datapaths[0]):  # Assume it's a single path to sonusai mixdb subdir
        logger.info(f'Loaded mixture database from {datapaths}')
        logger.info(f'Sonusai mixture db: found {mixdb.num_mixtures} mixtures with {mixdb.num_classes} classes')
    else:
        logger.info(f'{len(datapaths)} data paths specified, found {len(entries)} audio files.')
    if listdd is True:   # print
        openvino_list_device_details(core)

    if len(compiled_model.inputs) != 1 or len(compiled_model.outputs) != 1:
        logger.warning(f'Model has incorrect i/o, expected 1,1 but got {len(compiled_model.inputs)}, {len(compiled_model.outputs)}.')
        logger.warning(f'Using the first input and output.')
    else:
        logger.info(f'Model has 1 input and 1 output as expected.')

    inp0shape = compiled_model.inputs[0].partial_shape #compiled_model.inputs[0].shape   # fails on dynamic
    # out0shape = compiled_model.outputs[0].shape  # fails onb dynamic
    logger.info(f'Model input0 shape: {inp0shape}')
    # model_num_classes = inp0shape[-1]
    # logger.info(f'Model input0 shape {inp0shape}')
    # logger.info(f'Model output0 shape {out0shape}')


    # Check/calculate key Sonusai hyper-params
    # model_num_classes = inp0shape[-1]
    # batch_size = inp0shape[0]           # note batch dim can be used for frames dim if no timestep dimension
    # if batch_size != 1:
    #     logger.warning(f'Model batch size is not 1, but {batch_size}.')
    #
    # if len(inp0shape) > 2:
    #     if len(inp0shape) == 3:
    #         tsteps = inp0shape[1]       # note tstep dim can be used for frames dim if it exists
    #     else:
    #         logger.debug(f'Model input has more than 3 dims, assuming timestep dimension is 0 (does not exist).')
    #         tsteps = 0
    # else:
    #     logger.debug(f'Model input has 2 dims, timestep dimension is 0 (does not exist).')
    #     tsteps = 0
    #
    # flattened = True  # TBD get from model
    # add1ch = False

    if mixdb_path is not None:  # mixdb input
        # Assume (of course) that mixdb feature, etc. is what model expects
        feature_mode = mixdb.feature
        # if mixdb.num_classes != model_num_classes:
        #     logger.error(f'Feature parameters in mixture db {mixdb.num_classes} does not match num_classes in model {inp0shape[-1]}')
        #     raise SystemExit(1)
        # TBD add custom parameters in OpenVino model file? Then add feature, tsteps, truth mutex

        # note simple compile and prediction run:
        # compiled_model = ov.compile_model(ov_model, "AUTO")   # compile model
        import numpy as np
        inp_sample_np = np.ones([1,1,402], dtype=np.single)
        #inp_sample_t = torch.rand(1, 1, 402)
        shared_in = ov.Tensor(array=inp_sample_np, shared_memory=True)  # Create tensor, external memory, from numpy
        infer_request = compiled_model.create_infer_request()
        infer_request.set_input_tensor(shared_in)  # Set input tensor for model with one input
        input_tensor = infer_request.get_input_tensor()  # for debug
        output_tensor = infer_request.get_output_tensor()  # for debug

        infer_request.start_async()
        infer_request.wait()
        output = infer_request.get_output_tensor()  # Get output tensor for model with one output
        output_buffer = output.data  # output_buffer[] - accessing output tensor data




        from sonusai.utils import reshape_inputs
        from sonusai.utils import reshape_outputs
        from sonusai.mixture import get_audio_from_feature
        from sonusai.utils import write_wav
        import h5py
        for mixid in p_mixids:
            feature, _ = mixdb.mixture_ft(mixid)                # frames x stride x feature_params
            feature, _ = reshape_inputs(feature=feature,
                                        batch_size=1,
                                        timesteps=feature.shape[0],
                                        flatten=flattened,
                                        add1ch=add1ch)

            predict = compiled_model(feature) # run inference, model wants i.e. batch x tsteps x feat_params
            #TBD convert to numpy
            predict, _ = reshape_outputs(predict=predict, timesteps=tsteps)
            output_name = join(output_dir, mixdb.mixtures[mixid].name)
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset('predict', data=predict)
            if writewav:
                predict_audio = get_audio_from_feature(feature=predict, feature_mode=feature_mode)
                write_wav()



        # sampler = None
        # p_datagen = TorchFromMixtureDatabase(mixdb=mixdb,
        #                                      mixids=p_mixids,
        #                                      batch_size=batch_size,
        #                                      cut_len=0,
        #                                      flatten=model.flatten,
        #                                      add1ch=model.add1ch,
        #                                      random_cut=False,
        #                                      sampler=sampler,
        #                                      drop_last=False,
        #                                      num_workers=dlcpu)

        # Info needed to set up inverse transform
        half = model.num_classes // 2
        fg = FeatureGenerator(feature_mode=feature,
                              num_classes=model.num_classes,
                              truth_mutex=model.truth_mutex)
        itf = TorchInverseTransform(N=fg.itransform_N,
                                    R=fg.itransform_R,
                                    bin_start=fg.bin_start,
                                    bin_end=fg.bin_end,
                                    ttype=fg.itransform_ttype)

        enable_truth_wav = False
        enable_mix_wav = False
        if wavdbg:
            if mixdb.target_files[0].truth_settings[0].function == 'target_mixture_f':
                enable_mix_wav = True
                enable_truth_wav = True
            elif mixdb.target_files[0].truth_settings[0].function == 'target_f':
                enable_truth_wav = True

        if reset:
            logger.info(f'Running {mixdb.num_mixtures} mixtures individually with model reset ...')
            for idx, val in enumerate(p_datagen):
                # truth = val[1]
                feature = val[0]
                with torch.no_grad():
                    ypred = model(feature)
                output_name = join(output_dir, mixdb.mixtures[idx].name)
                pdat = ypred.detach().numpy()
                if timesteps > 0:
                    logger.debug(f'In and out tsteps: {feature.shape[1]},{pdat.shape[1]}')
                logger.debug(f'Writing predict shape {pdat.shape} to {output_name}')
                with h5py.File(output_name, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset('predict', data=pdat)

                if wavdbg:
                    owav_base = splitext(output_name)[0]
                    tmp = torch.complex(ypred[..., :half], ypred[..., half:]).permute(2, 0, 1).detach()
                    itf.reset()
                    predwav, _ = itf.execute_all(tmp)
                    # predwav, _ = calculate_audio_from_transform(tmp.numpy(), itf, trim=True)
                    write_wav(owav_base + '.wav', predwav.permute([1, 0]).numpy(), 16000)
                    if enable_truth_wav:
                        # Note this support truth type target_f and target_mixture_f
                        tmp = torch.complex(val[0][..., :half], val[0][..., half:2 * half]).permute(2, 0, 1).detach()
                        itf.reset()
                        truthwav, _ = itf.execute_all(tmp)
                        write_wav(owav_base + '_truth.wav', truthwav.permute([1, 0]).numpy(), 16000)

                    if enable_mix_wav:
                        tmp = torch.complex(val[0][..., 2 * half:3 * half], val[0][..., 3 * half:]).permute(2, 0, 1)
                        itf.reset()
                        mixwav, _ = itf.execute_all(tmp.detach())
                        write_wav(owav_base + '_mix.wav', mixwav.permute([1, 0]).numpy(), 16000)

















    from os import makedirs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import h5py
    import onnxruntime as rt
    import numpy as np

    from sonusai.mixture import Feature
    from sonusai.mixture import Predict
    from sonusai.utils import SonusAIMetaData
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_feature_from_audio
    from sonusai.mixture import read_audio
    from sonusai.utils import create_ts_name
    from sonusai.utils import get_frames_per_batch
    from sonusai.utils import get_sonusai_metadata

    output_dir = create_ts_name('ovpredict')
    makedirs(output_dir, exist_ok=True)



    model = rt.InferenceSession(model_name, providers=['CPUExecutionProvider'])
    model_metadata = get_sonusai_metadata(model)

    batch_size = model_metadata.input_shape[0]
    if model_metadata.timestep:
        timesteps = model_metadata.input_shape[1]
    else:
        timesteps = 0
    num_classes = model_metadata.output_shape[-1]

    frames_per_batch = get_frames_per_batch(batch_size, timesteps)

    logger.info('')
    logger.info(f'feature       {model_metadata.feature}')
    logger.info(f'num_classes   {num_classes}')
    logger.info(f'batch_size    {batch_size}')
    logger.info(f'timesteps     {timesteps}')
    logger.info(f'flatten       {model_metadata.flattened}')
    logger.info(f'add1ch        {model_metadata.channel}')
    logger.info(f'truth_mutex   {model_metadata.mutex}')
    logger.info(f'input_shape   {model_metadata.input_shape}')
    logger.info(f'output_shape  {model_metadata.output_shape}')
    logger.info('')

    if splitext(entries)[1] == '.wav':
        # Convert WAV to feature data
        logger.info('')
        logger.info(f'Run prediction on {entries}')
        audio = read_audio()
        feature = get_feature_from_audio(audio=audio, feature_mode=model_metadata.feature)

        predict = pad_and_predict(feature=feature,
                                  model_name=model_name,
                                  model_metadata=model_metadata,
                                  frames_per_batch=frames_per_batch,
                                  batch_size=batch_size,
                                  timesteps=timesteps,
                                  reset=reset)

        output_name = splitext()[0] + '.h5'
        with h5py.File(output_name, 'a') as f:
            if 'feature' in f:
                del f['feature']
            f.create_dataset(name='feature', data=feature)

            if 'predict' in f:
                del f['predict']
            f.create_dataset(name='predict', data=predict)

        logger.info(f'Saved results to {output_name}')
        return

    if not isdir():
        logger.exception(f'Do not know how to process input from {entries}')
        raise SystemExit(1)

    mixdb = MixtureDatabase()

    if mixdb.feature != model_metadata.feature:
        logger.exception(f'Feature in mixture database does not match feature in model')
        raise SystemExit(1)

    mixids = mixdb.mixids_to_list(mixids)
    if reset:
        # reset mode cycles through each file one at a time
        for mixid in mixids:
            feature, _ = mixdb.mixture_ft(mixid)

            predict = pad_and_predict(feature=feature,
                                      model_name=model_name,
                                      model_metadata=model_metadata,
                                      frames_per_batch=frames_per_batch,
                                      batch_size=batch_size,
                                      timesteps=timesteps,
                                      reset=reset)

            output_name = join(output_dir, mixdb.mixtures[mixid].name)
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset(name='predict', data=predict)
    else:
        features: list[Feature] = []
        file_indices: list[slice] = []
        total_frames = 0
        for mixid in mixids:
            current_feature, _ = mixdb.mixture_ft(mixid)
            current_frames = current_feature.shape[0]
            features.append(current_feature)
            file_indices.append(slice(total_frames, total_frames + current_frames))
            total_frames += current_frames
        feature = np.vstack([features[i] for i in range(len(features))])

        predict = pad_and_predict(feature=feature,
                                  model_name=model_name,
                                  model_metadata=model_metadata,
                                  frames_per_batch=frames_per_batch,
                                  batch_size=batch_size,
                                  timesteps=timesteps,
                                  reset=reset)

        # Write data to separate files
        for idx, mixid in enumerate(mixids):
            output_name = join(output_dir, mixdb.mixtures[mixid].name)
            with h5py.File(output_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset('predict', data=predict[file_indices[idx]])

    logger.info(f'Saved results to {output_dir}')


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
