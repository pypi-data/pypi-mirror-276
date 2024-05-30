from pathlib import Path
from typing import List, Sequence

from pydantic import BaseModel
from strictyaml import load

import sentiment_analysis_model

# Project Directories
PACKAGE_ROOT = Path(sentiment_analysis_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
LOG_DIR = PACKAGE_ROOT / "logs"

class TrainingConfig(BaseModel):
    batch_size: int
    epochs: int
    learning_rate: float

class ModelConfig(BaseModel):
    name: str
    version: str

class DataConfig(BaseModel):
    dataset_path: str
    test_size: float

class AppConfig(BaseModel):
    model: ModelConfig
    training: TrainingConfig
    data: DataConfig

def fetch_config_from_yaml(cfg_path: str) -> AppConfig:
    with open(cfg_path, 'r') as conf_file:
        config_data = conf_file.read()
    cfg = load(config_data)
    return AppConfig(
        model=ModelConfig(**cfg['model'].data),
        training=TrainingConfig(**cfg['training'].data),
        data=DataConfig(**cfg['data'].data),
    )
