"""
Data Transformation Component

Cleansing, validation, and preprocessing of stock market data.
Handles missing values, feature scaling, and prepares data for ML training.
"""

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import ML_FEATURE_NAMES
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    """Configuration paths for transformation artifacts."""
    preprocessor_obj_file_path: str = os.path.join('artifacts', "preprocessor.pkl")

class DataTransformation:
    """
    Transforms raw stock data into ML-ready format.
    
    This component:
    - Handles missing values (imputation)
    - Scales numerical features to standard range
    - Separates features from target variable
    - Saves preprocessing pipeline for inference
    """
    
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Create preprocessing pipeline for numerical stock features.
        
        Pipeline:
        1. Impute missing values (median strategy prevents data loss)
        2. Scale features to mean=0, std=1 (ensures fair model training)
        
        Returns:
            ColumnTransformer with numerical preprocessing pipeline
        """
        try:
            # Stock market features: prices, volumes, technical indicators
            numerical_columns = ML_FEATURE_NAMES  # From config: Mom_5d, Mom_20d, Mom_60d, Volatility_20d
            
            logging.info(f"Numerical features: {numerical_columns}")
            
            # Build preprocessing pipeline for numerical features
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Handle NaN values
                    ("scaler", StandardScaler())  # Normalize to standard scale
                ]
            )

            # Combine all transformers
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns)
                ]
            )

            logging.info("Preprocessing pipeline created successfully")
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path: str, test_path: str) -> tuple:
        """
        Execute full data transformation pipeline.
        
        Steps:
        1. Load train and test CSV files
        2. Create preprocessing pipeline
        3. Fit preprocessor on training data
        4. Transform both train and test data
        5. Combine features with target variable
        6. Save preprocessor for later inference
        
        Args:
            train_path: Path to training data CSV
            test_path: Path to test data CSV
            
        Returns:
            (train_arr, test_arr, preprocessor_path) tuple for next component
        """
        logging.info("Starting data transformation process")
        try:
            # Load raw data from CSV
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info(f"Loaded training data: {train_df.shape}, test data: {test_df.shape}")

            # Get preprocessing pipeline
            logging.info("Creating preprocessing pipeline")
            preprocessing_obj = self.get_data_transformer_object()

            # Separate features and target
            # Assuming last column is the target (Close price or price change)
            target_column_name = train_df.columns[-1]  # Last column is target
            logging.info(f"Target variable: {target_column_name}")

            # Extract features and target for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Extract features and target for test data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Fitting preprocessor on training data and transforming both sets")
            
            # Fit on training data, transform both sets to ensure consistency
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine features with target for supervised learning
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            
            logging.info(f"Transformed arrays - Train: {train_arr.shape}, Test: {test_arr.shape}")

            # Save preprocessing pipeline for inference
            logging.info(f"Saving preprocessor to {self.data_transformation_config.preprocessor_obj_file_path}")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            logging.info("Data transformation completed successfully")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            raise CustomException(e, sys)
