"""
ML model utilities for Stocksy application.
Handles model loading, predictions, and performance tracking.
"""

import os
import sys
from typing import Tuple, Optional
import numpy as np
import pandas as pd

from src.exception import StocksyException
from src.logger import logger
from src.utils import load_object
from src.config import SHORT_TERM_MODEL_PATH, LONG_TERM_MODEL_PATH, ML_MIN_DATA_POINTS, ML_FEATURE_NAMES


def load_prediction_models() -> Tuple[Optional[object], Optional[object]]:
    """
    Load short-term and long-term prediction models.
    
    Returns:
        Tuple of (short_term_model, long_term_model) or (None, None) if load fails
    """
    try:
        short_model = None
        long_model = None
        
        if os.path.exists(SHORT_TERM_MODEL_PATH):
            short_model = load_object(SHORT_TERM_MODEL_PATH)
            logger.info(f"Short-term model loaded: {SHORT_TERM_MODEL_PATH}")
        else:
            logger.warning(f"Short-term model not found: {SHORT_TERM_MODEL_PATH}")
        
        if os.path.exists(LONG_TERM_MODEL_PATH):
            long_model = load_object(LONG_TERM_MODEL_PATH)
            logger.info(f"Long-term model loaded: {LONG_TERM_MODEL_PATH}")
        else:
            logger.warning(f"Long-term model not found: {LONG_TERM_MODEL_PATH}")
        
        return short_model, long_model
    
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return None, None


def prepare_prediction_features(df: pd.DataFrame) -> Optional[list]:
    """
    Prepare features for ML prediction.
    
    Args:
        df: DataFrame with technical indicators already calculated
        
    Returns:
        List of feature values or None if insufficient data
    """
    try:
        if df is None or len(df) < ML_MIN_DATA_POINTS:
            logger.warning(f"Insufficient data for prediction. Required: {ML_MIN_DATA_POINTS}, Got: {len(df)}")
            return None
        
        latest = df.iloc[-1]
        
        # Check if all required features exist
        for feature in ML_FEATURE_NAMES:
            if feature not in df.columns or pd.isna(latest[feature]):
                logger.warning(f"Missing or invalid feature: {feature}")
                return None
        
        # Extract features for the latest data point
        features = [[
            float(np.squeeze(latest["Mom_5d"])),
            float(np.squeeze(latest["Mom_20d"])),
            float(np.squeeze(latest["Mom_60d"])),
            float(np.squeeze(latest["Volatility_20d"]))
        ]]
        
        logger.info(f"Prediction features prepared: {features}")
        return features
    
    except Exception as e:
        logger.error(f"Error preparing prediction features: {str(e)}")
        return None


def make_predictions(
    df: pd.DataFrame,
    short_model: object,
    long_model: object
) -> Tuple[Optional[float], Optional[float]]:
    """
    Make price predictions using trained models.
    
    Args:
        df: DataFrame with Close prices and indicators
        short_model: Trained short-term prediction model
        long_model: Trained long-term prediction model
        
    Returns:
        Tuple of (predicted_short_term_price, predicted_long_term_price) or (None, None)
    """
    try:
        if None in [short_model, long_model]:
            logger.warning("One or more models are not available")
            return None, None
        
        # Prepare features
        features = prepare_prediction_features(df)
        if features is None:
            return None, None
        
        # Get current price
        if "Close" not in df.columns or len(df) == 0:
            return None, None
        
        current_price = float(np.squeeze(df["Close"].iloc[-1]))
        
        # Make predictions
        pred_short_return = short_model.predict(features)[0]
        pred_long_return = long_model.predict(features)[0]
        
        # Calculate predicted prices
        pred_short_price = current_price * (1 + float(pred_short_return))
        pred_long_price = current_price * (1 + float(pred_long_return))
        
        logger.info(
            f"Predictions made - Short: ₹{pred_short_price:.2f}, Long: ₹{pred_long_price:.2f}"
        )
        
        return pred_short_price, pred_long_price
    
    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        return None, None


def validate_model_outputs(
    short_price: Optional[float],
    long_price: Optional[float],
    current_price: float
) -> bool:
    """
    Validate that model predictions are reasonable.
    
    Args:
        short_price: Short-term predicted price
        long_price: Long-term predicted price
        current_price: Current stock price
        
    Returns:
        True if predictions are valid, False otherwise
    """
    try:
        if short_price is None or long_price is None:
            return False
        
        if short_price <= 0 or long_price <= 0 or current_price <= 0:
            logger.warning("Invalid prices for validation")
            return False
        
        # Check for unrealistic predictions (e.g., > 500% change)
        max_change = 5.0  # 500% max change
        
        short_change = abs((short_price - current_price) / current_price)
        long_change = abs((long_price - current_price) / current_price)
        
        if short_change > max_change or long_change > max_change:
            logger.warning(
                f"Predictions seem unrealistic. "
                f"Short change: {short_change*100:.1f}%, Long change: {long_change*100:.1f}%"
            )
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Error validating model outputs: {str(e)}")
        return False


if __name__ == "__main__":
    logger.info("Model utilities module loaded successfully.")
