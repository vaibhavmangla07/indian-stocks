import sys

from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class TrainPipeline:
    """
    Manages end-to-end ML model training for stock price prediction.
    
    This pipeline orchestrates:
    1. Data Ingestion - Load and split raw stock data
    2. Data Transformation - Clean, preprocess, and scale features
    3. Model Training - Train and select best ML model
    """
    
    def __init__(self):
        """Initialize training pipeline components."""
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def run_pipeline(self) -> float:
        logging.info("=" * 60)
        logging.info("Starting ML Training Pipeline for Stock Prediction")
        logging.info("=" * 60)
        
        try:
            # Step 1: Data Ingestion
            logging.info("\n[STEP 1/3] Data Ingestion: Loading stock data...")
            train_data_path, test_data_path = self.data_ingestion.initiate_data_ingestion()
            logging.info(f"✓ Data loaded: Train={train_data_path}, Test={test_data_path}")
            
            # Step 2: Data Transformation
            logging.info("\n[STEP 2/3] Data Transformation: Preprocessing and scaling...")
            train_arr, test_arr, _ = (
                self.data_transformation.initiate_data_transformation(
                    train_data_path, test_data_path
                )
            )
            logging.info(f"✓ Data transformed: Train shape={train_arr.shape}, Test shape={test_arr.shape}")
            
            # Step 3: Model Training
            logging.info("\n[STEP 3/3] Model Training: Training and evaluating models...")
            r2_score = self.model_trainer.initiate_model_trainer(train_arr, test_arr)
            logging.info(f"✓ Model training complete: R² Score = {r2_score:.4f}")
            
            logging.info("\n" + "=" * 60)
            logging.info(f"Training Pipeline Completed Successfully!")
            logging.info(f"Model R² Score: {r2_score:.4f}")
            logging.info("=" * 60)
            
            return r2_score

        except Exception as e:
            logging.error(f"Training Pipeline Failed: {str(e)}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    pipeline = TrainPipeline()
    final_score = pipeline.run_pipeline()
    print(f"\nFinal Model Performance: R² = {final_score:.4f}")
