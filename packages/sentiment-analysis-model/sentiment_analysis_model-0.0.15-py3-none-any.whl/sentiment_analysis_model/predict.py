from joblib import load
from sentiment_analysis_model import __version__ as _version
from sentiment_analysis_model import config
from sentiment_analysis_model.processing.data_manager import load_pipeline


pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
model = load_pipeline(file_name=pipeline_file_name)


def predict(texts):
    predictions = model.predict(texts)
    sentiment_map = {0: 'negative', 1: 'positive'}
    return [sentiment_map[pred] for pred in predictions]
