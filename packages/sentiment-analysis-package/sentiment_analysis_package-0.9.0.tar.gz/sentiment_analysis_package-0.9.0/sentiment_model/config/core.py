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


import os
import yaml


def fetch_config_from_yaml(cfg_path):
    sentiment_model_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    config_path = os.path.join(sentiment_model_path, cfg_path)
    with open(config_path, 'r') as conf_file:
        config = yaml.safe_load(conf_file)
    return config