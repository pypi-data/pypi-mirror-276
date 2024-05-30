import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump
from sentiment_analysis_model.config.core import fetch_config_from_yaml
from sentiment_analysis_model.pipeline import create_pipeline
from sentiment_analysis_model.processing.features import preprocess_text  

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = fetch_config_from_yaml('./sentiment_analysis_model/config.yml')

def train():
    logger.info("Starting training process.")
    # Read the dataset
    data1 = pd.read_csv(config.data.dataset_path, encoding='ISO-8859-1', header=None, nrows=5000)
    data2 = pd.read_csv(config.data.dataset_path, encoding='ISO-8859-1', header=None, skiprows=798622, nrows=5000)
    data = pd.concat([data1, data2])
    data.columns = ['target', 'ids', 'date', 'flag', 'user', 'text']

    # Preprocess the data
    data['text'] = data['text'].apply(preprocess_text)
    X = data['text']
    y = data['target'].replace({0: 0, 4: 1})

    logger.info("Splitting the data into training and testing sets.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.data.test_size, random_state=42)

    logger.info("Creating and training the pipeline.")
    pipeline = create_pipeline()
    pipeline.fit(X_train, y_train)

    logger.info("Saving the trained model.")
    dump(pipeline, f"{config.model.name}_{config.model.version}.pkl")
    logger.info(f"Model trained and saved as {config.model.name}_{config.model.version}.pkl")

if __name__ == "__main__":
    train()
