import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from sentiment_analysis_model import __version__ as _version
from sentiment_analysis_model.config.core import DATASET_DIR,TRAINED_MODEL_DIR, config


def load_dataset(*, file_name: str) -> pd.DataFrame:
   data1 = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"), encoding='ISO-8859-1', header=None, nrows=20000)
   data2 = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"), encoding='ISO-8859-1', header=None, skiprows=798622, nrows=20000)
   data = pd.concat([data1, data2])
   return data


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    file_path = TRAINED_MODEL_DIR / file_name
    trained_model = joblib.load(filename=file_path)
    return trained_model


def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
