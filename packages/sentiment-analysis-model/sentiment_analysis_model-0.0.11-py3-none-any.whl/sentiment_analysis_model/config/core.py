from pydantic import BaseModel
from strictyaml import load


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
