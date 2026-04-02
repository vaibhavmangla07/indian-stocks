"""
Data utilities and helper functions for Stocksy application.
Provides data validation, cleaning, and transformation operations.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, List

from src.logger import logger


def clean_price_data(df: pd.DataFrame, min_volume: int = 0) -> Optional[pd.DataFrame]:
    """
    Clean price data by removing invalid entries.
    
    Args:
        df: DataFrame with OHLCV data
        min_volume: Minimum volume threshold (exclude days with lower volume)
        
    Returns:
        Cleaned DataFrame or None if invalid
    """
    try:
        if df is None or df.empty:
            logger.warning("Data is empty or None")
            return None
        
        # Reset index if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df = df.reset_index()
        
        # Remove zero volume entries
        if "Volume" in df.columns and min_volume > 0:
            df = df[df["Volume"] > min_volume]
        
        # Remove NaN values
        df = df.dropna(subset=["Close"])
        
        logger.info(f"Data cleaning completed. {len(df)} valid records remaining.")
        return df
    
    except Exception as e:
        logger.error(f"Error cleaning price data: {str(e)}")
        return None


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators for ML model prediction.
    
    Args:
        df: DataFrame with Close prices
        
    Returns:
        DataFrame with calculated indicators
    """
    try:
        if df is None or len(df) < 61:
            logger.warning("Insufficient data for technical indicators calculation")
            return df
        
        # Momentum indicators
        df["Mom_5d"] = df["Close"].pct_change(periods=5)
        df["Mom_20d"] = df["Close"].pct_change(periods=20)
        df["Mom_60d"] = df["Close"].pct_change(periods=60)
        
        # Volatility
        df["Volatility_20d"] = df["Close"].pct_change().rolling(window=20).std()
        
        logger.info("Technical indicators calculated successfully")
        return df
    
    except Exception as e:
        logger.error(f"Error calculating technical indicators: {str(e)}")
        return df


def validate_stock_data(df: pd.DataFrame, required_columns: List[str] = None) -> bool:
    """
    Validate stock data DataFrame.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required columns (default: ["Date", "Close", "Volume"])
        
    Returns:
        True if valid, False otherwise
    """
    if required_columns is None:
        required_columns = ["Date", "Close", "Volume"]
    
    if df is None or df.empty:
        logger.warning("Stock data is empty")
        return False
    
    missing = set(required_columns) - set(df.columns)
    if missing:
        logger.warning(f"Missing required columns: {missing}")
        return False
    
    if (df["Close"] <= 0).any():
        logger.warning("Invalid Close prices detected")
        return False
    
    return True


def get_price_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate price statistics from stock data.
    
    Args:
        df: DataFrame with Close prices
        
    Returns:
        Dictionary with price statistics
    """
    try:
        if df is None or df.empty or "Close" not in df.columns:
            return {}
        
        close_prices = df["Close"].dropna()
        
        return {
            "current_price": float(close_prices.iloc[-1]) if len(close_prices) > 0 else None,
            "avg_price": float(close_prices.mean()),
            "max_price": float(close_prices.max()),
            "min_price": float(close_prices.min()),
            "volatility": float(close_prices.std()),
            "price_change": float(close_prices.iloc[-1] - close_prices.iloc[0]) if len(close_prices) > 1 else 0,
            "price_change_pct": float((close_prices.iloc[-1] / close_prices.iloc[0] - 1) * 100) if close_prices.iloc[0] != 0 else 0,
        }
    except Exception as e:
        logger.error(f"Error calculating price statistics: {str(e)}")
        return {}


def get_one_year_return(df: pd.DataFrame) -> Optional[float]:
    """
    Calculate one-year return percentage.
    
    Args:
        df: DataFrame with historical Close prices
        
    Returns:
        One-year return percentage or None
    """
    try:
        if df is None or len(df) < 2 or "Close" not in df.columns:
            return None
        
        close_prices = df["Close"].dropna()
        if len(close_prices) < 2:
            return None
        
        start_price = close_prices.iloc[0]
        end_price = close_prices.iloc[-1]
        
        if start_price <= 0:
            return None
        
        return ((end_price - start_price) / start_price) * 100
    
    except Exception as e:
        logger.error(f"Error calculating one-year return: {str(e)}")
        return None


if __name__ == "__main__":
    logger.info("Data utilities module loaded successfully.")
