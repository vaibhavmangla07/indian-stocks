"""
Prediction Pipeline Module

Makes stock price predictions using trained models and preprocessing pipelines.
Handles data preparation, preprocessing, and model inference.
"""

import os
import sys

import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

class PredictPipeline:
    """
    Makes predictions on new stock data using trained model and preprocessor.
    
    This class:
    - Loads trained ML model from artifacts
    - Loads preprocessing pipeline (scaler, imputer, etc.)
    - Transforms input features using same preprocessing as training
    - Returns price predictions
    """
    
    def __init__(self):
        """Initialize prediction pipeline (no state needed)."""
        pass

    def predict(self, features: pd.DataFrame) -> list:
        """
        Make price predictions on input features.
        
        Process:
        1. Load trained model from artifacts/model.pkl
        2. Load preprocessor from artifacts/preprocessor.pkl
        3. Transform input features using preprocessor (same scaling as training)
        4. Generate predictions using model
        
        Args:
            features: DataFrame with stock features (Mom_5d, Mom_20d, Mom_60d, Volatility_20d)
            
        Returns:
            List of predicted values (stock prices or price changes)
            
        Raises:
            CustomException: If model/preprocessor not found or prediction fails
        """
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
            
            logging.info(f"Loading model from {model_path} and preprocessor from {preprocessor_path}")
            
            # Load artifacts
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            logging.info("Model and preprocessor loaded successfully")
            
            # Transform features using same preprocessing as training
            logging.info("Preprocessing input features")
            data_scaled = preprocessor.transform(features)
            
            # Generate predictions
            logging.info("Generating predictions")
            predictions = model.predict(data_scaled)
            
            logging.info(f"Prediction complete. Shape: {predictions.shape}")
            return predictions
        
        except Exception as e:
            raise CustomException(e, sys)

class CustomData:
    """
    Encapsulates stock market features for prediction.
    
    Converts user input (technical indicators + stock info) into a standardized
    DataFrame format for model preprocessing and prediction.
    """
    
    def __init__(
        self,
        stock_name: str,
        momentum_5d: float,
        momentum_20d: float,
        momentum_60d: float,
        volatility_20d: float
    ):
        """
        Initialize with stock technical indicators.
        
        Args:
            stock_name: Stock ticker (e.g., "RELIANCE", "TCS")
            momentum_5d: 5-day momentum indicator (price change %)
            momentum_20d: 20-day momentum indicator (price change %)
            momentum_60d: 60-day momentum indicator (price change %)
            volatility_20d: 20-day volatility (price fluctuation %)
        """
        self.stock_name = stock_name
        self.momentum_5d = momentum_5d
        self.momentum_20d = momentum_20d
        self.momentum_60d = momentum_60d
        self.volatility_20d = volatility_20d

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        Convert stock features to DataFrame format for model preprocessing.
        
        Returns:
            Single-row DataFrame with columns matching ML_FEATURE_NAMES from config
            
        Example:
            CustomData("RELIANCE", 2.5, 1.8, 0.5, 3.2).get_data_as_dataframe()
            
            Output DataFrame:
                Mom_5d  Mom_20d  Mom_60d  Volatility_20d
            0    2.5      1.8      0.5            3.2
        """
        try:
            logging.info(f"Creating DataFrame for {self.stock_name} prediction")
            
            # Create dictionary matching ML_FEATURE_NAMES order
            custom_data_dict = {
                "Mom_5d": [self.momentum_5d],
                "Mom_20d": [self.momentum_20d],
                "Mom_60d": [self.momentum_60d],
                "Volatility_20d": [self.volatility_20d],
            }
            
            df = pd.DataFrame(custom_data_dict)
            logging.info(f"DataFrame created with shape {df.shape}")
            return df

        except Exception as e:
            raise CustomException(e, sys)
