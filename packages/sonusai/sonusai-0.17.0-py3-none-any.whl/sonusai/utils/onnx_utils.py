from dataclasses import dataclass

from sonusai import logger
from typing import Any  #List, Optional, Tuple
import onnxruntime as ort
from onnxruntime import InferenceSession
import onnx
from onnx import ValueInfoProto
from os.path import basename, splitext, exists, isfile


@dataclass(frozen=True)
class SonusAIMetaData:
    input_shape: list[int]
    output_shape: list[int]
    flattened: bool
    timestep: bool
    channel: bool
    mutex: bool
    feature: str


def get_and_check_inputs(model: onnx.ModelProto) -> tuple[list[ValueInfoProto], list[list[int] | str]]:
    # ignore initializer inputs (only seen in older onnx < v1.5
    initializer_names = [x.name for x in model.graph.initializer]
    onnx_inputs = [ipt for ipt in model.graph.input if ipt.name not in initializer_names]
    if len(onnx_inputs) != 1:
        logger.warning(f'Warning: onnx model does not have 1 input, but {len(onnx_inputs)}')
        #raise SystemExit(1)

    inshapes = []
    for inp in onnx_inputs:                      # iterate through inputs of the graph to find shapes
        tensor_type = inp.type.tensor_type       # get tensor type: 0, 1, 2,
        if (tensor_type.HasField("shape")):      # check if it has a shape:
            tmpshape = []
            for d in tensor_type.shape.dim:      # iterate through dimensions of the shape
                if (d.HasField("dim_value")):    # known dimension, int value
                    tmpshape.append(d.dim_value)
                elif (d.HasField("dim_param")):  # dynamic dim with symbolic name of d.dim_param
                    tmpshape.append(0)           # set size to 0
                else:                            # unknown dimension with no name
                    tmpshape.append(0)           # also set to 0
            inshapes.append(tmpshape)            # add as a list
        else:
            inshapes.append("unknown rank")

    # This one-liner works only if input has type and shape, returns a list
    #in0shape = [d.dim_value for d in onnx_inputs[0].type.tensor_type.shape.dim]

    return onnx_inputs, inshapes


def get_and_check_outputs(model: onnx.ModelProto) -> tuple[list[ValueInfoProto], list[list[int | Any] | str]]:
    onnx_outputs = [opt for opt in model.graph.output]
    if len(onnx_outputs) != 1:
        logger.warning(f'Warning: onnx model does not have 1 output, but {len(onnx_outputs)}')

    oshapes = []
    for inp in onnx_outputs:                     # iterate through inputs of the graph to find shapes
        tensor_type = inp.type.tensor_type       # get tensor type: 0, 1, 2,
        if (tensor_type.HasField("shape")):      # check if it has a shape:
            tmpshape = []
            for d in tensor_type.shape.dim:      # iterate through dimensions of the shape
                if (d.HasField("dim_value")):    # known dimension, int value
                    tmpshape.append(d.dim_value)
                elif (d.HasField("dim_param")):  # dynamic dim with symbolic name of d.dim_param
                    tmpshape.append(0)           # set size to 0
                else:                            # unknown dimension with no name
                    tmpshape.append(0)           # also set to 0
            oshapes.append(tmpshape)             # add as a list
        else:
            oshapes.append("unknown rank")

    return onnx_outputs, oshapes


def add_sonusai_metadata(model, hparams):
    """Add SonusAI hyper-parameter metadata to an ONNX model using key hparams

    :param model: ONNX model
    :hparams: dictionary of hyper-parameters, added
    Note SonusAI conventions require models to have:
      - feature: Model feature type
      - is_flattened: Model input feature data is flattened (stride + bins combined)
      - timesteps: Size of timestep dimension (0 for no dimension)
      - add1ch:   Model input has channel dimension
      - truth_mutex: Model label output is mutually exclusive
    """

    # Add hyper-parameters as metadata in onnx model under hparams key
    assert eval(str(hparams)) == hparams       # Note hparams should be a dict (i.e. extracted from checkpoint)
    meta = model.metadata_props.add()
    meta.key = "hparams"
    meta.value = str(hparams)

    return model


def get_sonusai_metadata(session: InferenceSession) -> SonusAIMetaData:
    """Get SonusAI hyper-parameter metadata from an ONNX Runtime session.
       Returns dictionary hparams
    """
    meta = session.get_modelmeta()
    hparams = eval(meta.custom_metadata_map["hparams"])

    # m = model.get_modelmeta().custom_metadata_map
    # return SonusAIMetaData(input_shape=model.get_inputs()[0].shape,
    #                        output_shape=model.get_outputs()[0].shape,
    #                        flattened=m['is_flattened'] == 'True',
    #                        timestep=m['has_timestep'] == 'True',
    #                        channel=m['has_channel'] == 'True',
    #                        mutex=m['is_mutex'] == 'True',
    #                        feature=m['feature'])

    return hparams

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