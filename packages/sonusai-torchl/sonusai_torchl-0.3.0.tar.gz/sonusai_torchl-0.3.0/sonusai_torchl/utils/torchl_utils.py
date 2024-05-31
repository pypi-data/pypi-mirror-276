from sonusai import logger
from typing import Any
from os.path import basename, splitext, exists, isfile

# Utilities for loading, checking, and converting Pytorch Lightning SonusAI models
# The steps to load a model from checkpoint:
# 1) load checkpoint, get hparams (a Pytorch Lightning .ckpt file i.e. from training)
# 2) load a litmodel (a custom Pytorch Lightning Model class .py file using SonusAI conventions)
# 3) check and override hparams if desired (i.e. batch-size, timesteps)
# 4) build the model with hparams, use training=false to build for inference/prediction

def torchl_load_ckpt(ckpt_path: str) -> Any:
    if exists(ckpt_path) and isfile(ckpt_path):
        ckpt_basename = basename(ckpt_path)
        ckpt_root = splitext(ckpt_basename)[0]
        from torch import load as torchload
        logger.info(f'Importing Pytorch checkpoint file {ckpt_basename}')
        try:
            checkpoint = torchload(ckpt_path, map_location=lambda storage, loc: storage)
            #litemodule.MyHyperModel.load_from_checkpoint(ckpt_name, map_location=lambda storage, loc: storage, training=training)
        except Exception as e:
            logger.exception(f'Error: could not load checkpoint from {ckpt_path}: {e}')
            raise SystemExit(1)
    else:
        logger.exception(f'Error: checkpoint file does not exist: {ckpt_path}')
        raise SystemExit(1)

    if 'hyper_parameters' in checkpoint:
        hparams = checkpoint['hyper_parameters']
    else:
        hparams = None
        logger.warning(f'Warning: Lightning checkpoint had no hyper-parameters saved, will attempt to build model '
                       f'with defaults.')

    return checkpoint, hparams, ckpt_basename, ckpt_root


def torchl_load_litmodel(model_path: str) -> Any:
    if exists(model_path) and isfile(model_path):
        from sonusai.utils import import_module
        model_basename = basename(model_path)
        model_root = splitext(model_basename)[0]
        logger.info(f'Importing model from {model_basename}')
        try:
            litmodel = import_module(model_path)
        except Exception as e:
            logger.exception(f'Error: could not load Lighting model from {model_path}: {e}')
            raise SystemExit(1)
    else:
        logger.exception(f'Error: model file does not exist: {model_path}')
        raise SystemExit(1)

    return litmodel, model_basename, model_root


def torchl_hparam_override(hparams: dict, batch_size=None, timesteps=None, hparams_ovr: dict = None):
    """ Override parameters in hparams if new ones are specified
        batch_size and timesteps are handled specifically and will be ignored if -1 or None
        timesteps is also ignored if hparams.timesteps is 0 (dim does not exist in model)
        and timesteps returned is set == 0 if hparams.timesteps is 0 to indicate model doesn't have that dim

        Note batch_size and timesteps can be set to -1 to indicate dynamic size, but are ignored here since
        building a model usually does not support this value.  Onnx and other model types can be updated to
        dynamic I/O after the model is built and exported.

        hparams_ovr is a dict of hyper-parameters that will all be diff'd with hparams and any different params
        will be over-written to hparams.

        batch_size and timesteps have priority over hparams_ovr
    """

    # TBD code diff hparams, hparams_ovr and overwrite non-matching values that exist in hparams

    if batch_size is not None:
        batch_size = int(batch_size)
        if batch_size == -1:
            hparams['batch_size'] = 1       # set to 1 for build, then set to dynamic in model export
        elif hparams['batch_size'] != batch_size:
            logger.info(f'Overriding hparams.batch_size of {hparams["batch_size"]} with {batch_size}')
            hparams["batch_size"] = batch_size
        else:
            logger.debug(f'Unmodified hparams.batch_size={batch_size}')
    else:
        logger.debug(f'Unmodified hparams.batch_size={batch_size}')

    if timesteps is not None and hparams["timesteps"] != 0:
        timesteps = int(timesteps)
        if timesteps <= -1:
            hparams['timesteps'] = 1       # set to 1 for build, then set to dynamic in model export
        elif hparams['timesteps'] != timesteps:
            logger.info(f'Overriding hparams.timesteps of {hparams["timesteps"]} with {timesteps}')
            hparams['timesteps'] = timesteps
        else:
            logger.debug(f'Unmodified hparams.timesteps={timesteps}')
    else:
        if hparams["timesteps"] == 0:
            logger.debug(f'hparams indicates no timestep dimension, setting timesteps = 0')
            timesteps = 0  # in case timesteps == -1 force it to zero if model doesn't have timestep dimension
        else:
            logger.debug(f'Unmodified hparams.timesteps={timesteps}')

    return hparams, timesteps


def torchl_build_model(litmodel, hparams, training: bool = False, ckpt=None):
    """
    Build a lightning model from an imported litmodel and set of hyper-parameters hparams.
    The training hparam is overridden by the training arg provided (True or False).
    Check built model for SonusAI hparams compatibility and return an updated hparams that possibly has additional
    parameters (flatten, add1ch, and input_shape, num_classes) that were missing in the hparams arg provided.
    Note the model is not rebuilt with the new hparams.
    Optionally load weights from a lightning checkpoint ckpt. If Training=False then train-only module weights
    are removed to match the built model.
    """

    logger.info(
        f'Building model for inference with batch_size={hparams["batch_size"]}, timesteps={hparams["timesteps"]}')
    hparams["training"] = training  # Sonusai convention to ignore training-only objects like GAN and loss models
    model = litmodel.MyHyperModel(**hparams)

    # Add SonusAI required params that didn't get saved (or were derived) in previous versions.
    if "num_classes"  in model.__dict__:
        hparams["num_classes"] = model.num_classes
        logger.debug(f'Updated hparams with num_classes.')
    if "flatten" in model.__dict__:
        hparams["flatten"] = model.flatten
        logger.debug(f'Updated hparams with flatten.')
    if "add1ch" in model.__dict__:
        hparams["add1ch"] = model.add1ch
        logger.debug(f'Updated hparams with add1ch.')
    if "truth_mutex" in model.__dict__:
        hparams["truth_mutex"] = model.add1ch
        logger.debug(f'Updated hparams with truth_mutex.')
    if "input_shape" in model.__dict__:
        hparams["input_shape"] = model.input_shape
        logger.debug(f'Updated hparams with input_shape.')

    if ckpt is not None:
        if training is False:
            # Remove weights that pertain to custom loss or GAN models (discriminator) - not needed for prediction
            # The build model will/should also not have these when training hparam is set to False
            logger.info(f'Removing weights that pertain to custom loss or gan models (discriminator)'
                        f' - not needed for inference.')
            klist = list(ckpt["state_dict"].keys())
            for key in klist:
                if key.startswith("per_loss"):
                    ckpt["state_dict"].pop(key)
                    logger.debug(f'Removed key {key}.')
                if key.startswith("discr"):
                    ckpt["state_dict"].pop(key)
                    logger.debug(f'Removed key {key}.')

        logger.info(f'Loading weights from checkpoint with training = {training} ...')
        model.load_state_dict(ckpt["state_dict"])

    return model, hparams


# Deprecated
def load_torchl_ckpt_model(model_name: str,
                           ckpt_name: str,
                           batch_size: int = None,
                           timesteps: int = None,
                           training: bool = False) -> Any:
    import torch

    from sonusai import logger
    from sonusai.utils import import_module

    # Load checkpoint first to get hparams if available
    try:
        checkpoint = torch.load(ckpt_name, map_location=lambda storage, loc: storage)
    except Exception as e:
        logger.exception(f'Error: could not load checkpoint from {ckpt_name}: {e}')
        raise SystemExit(1)

    # Import model definition file
    logger.info(f'Importing {model_name}')
    torchl_module = import_module(model_name)

    if 'hyper_parameters' in checkpoint:
        logger.info(f'Found checkpoint file with hyper-parameters')
        hparams = checkpoint['hyper_parameters']
        if batch_size is not None and ['batch_size'] != batch_size:
            if batch_size != 1 and not training:
                batch_size = 1
                logger.warning('Prediction only supports batch_size = 1, forcing to 1')
            logger.info(f'Overriding model default batch_size of {hparams["batch_size"]} with {batch_size}')
            hparams["batch_size"] = batch_size

        if timesteps is not None:
            if hparams['timesteps'] == 0 and timesteps != 0:
                timesteps = 0
                logger.warning(f'Model does not contain timesteps; ignoring override')

            if hparams['timesteps'] != 0 and timesteps == 0:
                timesteps = hparams['timesteps']
                logger.warning(f'Using model default timesteps of {timesteps}')

            if hparams['timesteps'] != timesteps:
                logger.info(f'Overriding model default timesteps of {hparams["timesteps"]} with {timesteps}')
                hparams['timesteps'] = timesteps

        logger.info(f'Building model with hyper-parameters and batch_size={batch_size}, timesteps={timesteps}')
        try:
            model = torchl_module.MyHyperModel(**hparams, training=training)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_name} failed: {e}')
            raise SystemExit(1)
    else:
        logger.info(f'Found checkpoint file with no hyper-parameters')
        logger.info(f'Building model with defaults')
        try:
            tmp = torchl_module.MyHyperModel(training=training)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_name} failed: {e}')
            raise SystemExit(1)

        if batch_size is not None:
            if tmp.batch_size != batch_size:
                logger.info(f'Overriding model default batch_size of {tmp.batch_size} with {batch_size}')
        else:
            batch_size = tmp.batch_size

        if timesteps is not None:
            if tmp.timesteps == 0 and timesteps != 0:
                logger.warning(f'Model does not contain timesteps; ignoring override')
                timesteps = 0

            if tmp.timesteps != 0 and timesteps == 0:
                logger.warning(f'Using model default timesteps of {timesteps}')
                timesteps = tmp.timesteps

            if tmp.timesteps != timesteps:
                logger.info(f'Overriding model default timesteps of {tmp.timesteps} with {timesteps}.')
        else:
            timesteps = tmp.timesteps

        model = torchl_module.MyHyperModel(timesteps=timesteps, batch_size=batch_size, training=training)

    logger.info(f'Loading weights from {ckpt_name}')

    if training is False:
        # Remove weights that pertain to custom loss or gan models (discriminator) - not needed for prediction
        logger.info('Removing weights that are not needed for inference.')
        for key in checkpoint['state_dict'].copy().keys():
            if key.startswith('per_loss'):
                checkpoint['state_dict'].pop(key)
            elif key.startswith('discr'):
                checkpoint['state_dict'].pop(key)

    model.load_state_dict(checkpoint['state_dict'])
    return model
