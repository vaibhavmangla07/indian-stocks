import os
import sys
from dataclasses import dataclass
from glob import glob

import pandas as pd

from src.config import DATA_DIR
from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def _load_stock_data(self) -> pd.DataFrame:
        try:
            csv_files = glob(os.path.join(DATA_DIR, "*.csv"))
            
            if not csv_files:
                raise FileNotFoundError(f"No CSV files found in {DATA_DIR}")
            
            logging.info(f"Found {len(csv_files)} stock data files")
            
            # Load and combine all CSV files
            dataframes = []
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    dataframes.append(df)
                    logging.info(f"Loaded {os.path.basename(csv_file)} with shape {df.shape}")
                except Exception as e:
                    logging.warning(f"Failed to load {csv_file}: {e}")
                    continue
            
            if not dataframes:
                raise ValueError("Could not load any valid CSV files")
            
            # Combine all dataframes
            combined_df = pd.concat(dataframes, ignore_index=True)
            logging.info(f"Combined dataset shape: {combined_df.shape}")
            
            return combined_df
            
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> tuple:
        logging.info("Starting data ingestion process")
        try:
            # Load stock data from CSV files
            df = self._load_stock_data()
            logging.info(f'Loaded dataset with shape: {df.shape}')

            # Create artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save raw combined data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(f"Raw data saved to {self.ingestion_config.raw_data_path}")

            # Perform train-test split (80% train, 20% test)
            logging.info("Performing train-test split (80-20)")
            from sklearn.model_selection import train_test_split
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save train and test sets
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            
            logging.info(f"Train data: {train_set.shape}, Test data: {test_set.shape}")
            logging.info("Data ingestion completed successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    # Step 1: Data Ingestion - Load and split data
    data_ingestion = DataIngestion()
    train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

    # Step 2: Data Transformation - Clean and preprocess data
    from src.components.data_transformation import DataTransformation
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data_path, test_data_path
    )

    # Step 3: Model Training - Train ML model
    from src.components.model_trainer import ModelTrainer
    model_trainer = ModelTrainer()
    result = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(f"\nTraining Complete. Result: {result}")
