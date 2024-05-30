import os
from pathlib import Path

import yaml
from pydantic import BaseModel


class TrainConfig(BaseModel):
    data_path: Path
    model_path: Path
    score_path: Path
    target: str


def init_train_config() -> TrainConfig:
    with open(os.environ["CONFIG_PATH"], "r") as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)
    return TrainConfig(**yaml_content["train"])
