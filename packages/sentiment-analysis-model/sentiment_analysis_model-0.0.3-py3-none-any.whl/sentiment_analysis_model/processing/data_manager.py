import typing as t
from pathlib import Path

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from sentiment_analysis_model import __version__ as _version
from sentiment_analysis_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, AppConfig


def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe


