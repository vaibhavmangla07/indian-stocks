import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            logging.info("Training pipeline started.")
            
            # Step 1: Data Ingestion
            ingestion = DataIngestion()
            train_data_path, test_data_path = ingestion.initiate_data_ingestion()
            
            # Step 2: Data Transformation
            transformation = DataTransformation()
            train_arr, test_arr, _ = transformation.initiate_data_transformation(train_data_path, test_data_path)
            
            # Step 3: Model Trainer
            trainer = ModelTrainer()
            r2_score = trainer.initiate_model_trainer(train_arr, test_arr)
            
            logging.info(f"Training pipeline completed with R2 Score: {r2_score}")
            return r2_score

        except Exception as e:
            raise CustomException(e, sys)

if __name__=="__main__":
    pipeline = TrainPipeline()
    pipeline.run_pipeline()
