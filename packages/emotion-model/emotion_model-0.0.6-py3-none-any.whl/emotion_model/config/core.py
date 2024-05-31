from pathlib import Path
from typing import List

from pydantic import BaseModel
from strictyaml import YAML, load

import emotion_model

# Project Directories
PACKAGE_ROOT = Path(emotion_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config/config.yaml"
DATASET_DIR = PACKAGE_ROOT / "dataset"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
LOG_DIR = PACKAGE_ROOT / "logs"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    clf_save_file: str


class NNConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    emotions: List[str]
    image_size: List[int]
    image_reshape_params: List[int]
    layer1: dict
    layer2: dict
    layer3: dict
    layer4: dict
    layer5: dict
    layer6: dict
    layer7: dict
    layer8: dict
    optimizer: str
    loss: str
    metrics: List[str]
    epochs: int
    batch_size: int
    test_size: float
    random_state: int


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    nn_config: NNConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        nn_config=NNConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()

config.nn_config.layer1['params']['filters'] = int(config.nn_config.layer1['params']['filters'])
config.nn_config.layer1['params']['kernel_size'] = tuple(
    map(int, list(config.nn_config.layer1['params']['kernel_size'])))
config.nn_config.layer1['params']['input_shape'] = tuple(
    map(int, list(config.nn_config.layer1['params']['input_shape'])))

config.nn_config.layer2['params']['filters'] = int(config.nn_config.layer2['params']['filters'])
config.nn_config.layer2['params']['kernel_size'] = tuple(
    map(int, list(config.nn_config.layer2['params']['kernel_size'])))

config.nn_config.layer3['params']['pool_size'] = tuple(
    map(int, list(config.nn_config.layer3['params']['pool_size'])))

config.nn_config.layer4['params']['filters'] = int(config.nn_config.layer4['params']['filters'])
config.nn_config.layer4['params']['kernel_size'] = tuple(
    map(int, list(config.nn_config.layer4['params']['kernel_size'])))

config.nn_config.layer5['params']['pool_size'] = tuple(
    map(int, list(config.nn_config.layer5['params']['pool_size'])))

config.nn_config.layer7['params']['units'] = int(config.nn_config.layer7['params']['units'])

config.nn_config.layer8['params']['units'] = int(config.nn_config.layer8['params']['units'])
