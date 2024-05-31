import logging
import pandas as pd

from sklearn.model_selection import train_test_split

from sentiment_analysis_model.config.core import config
from sentiment_analysis_model.pipeline import create_pipeline
from sentiment_analysis_model.processing.data_manager import load_dataset, save_pipeline
from sentiment_analysis_model.processing.features import preprocess_text

from sentiment_analysis_model import __version__ as _version

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def train():
    logger.info("Starting training process.")
    # Read the dataset
    data = load_dataset(file_name=config.app_config.data_file)
    data.columns = ['target', 'ids', 'date', 'flag', 'user', 'text']

    # Preprocess the data
    data['text'] = data['text'].apply(preprocess_text)
    X = data['text']
    y = data['target'].replace({0: 0, 4: 1})

    logger.info("Splitting the data into training and testing sets.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.model.test_size, random_state=42)

    logger.info("Creating and training the pipeline.")
    pipeline = create_pipeline()
    pipeline.fit(X_train, y_train)

    logger.info("Saving the trained model.")
    save_pipeline(pipeline_to_persist=pipeline)
    logger.info(f"Model trained and saved as {config.app_config.package_name}_{_version}.pkl")


if __name__ == "__main__":
    train()
