"""
Utility functions for Stocksy application.
Provides model serialization, number formatting, and data processing helpers.
"""

import os
import sys
import joblib
import pandas as pd
from typing import Any, Optional

from src.exception import StocksyException
from src.logger import logger


def save_object(file_path: str, obj: Any) -> None:
    """
    Serialize and save a Python object to disk using joblib.
    
    Args:
        file_path: Path where the object will be saved
        obj: Python object to serialize
        
    Raises:
        StocksyException: If save operation fails
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        joblib.dump(obj, file_path)
        logger.info(f"Object saved successfully at: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save object at {file_path}: {str(e)}")
        raise StocksyException(e, sys)


def load_object(file_path: str) -> Any:
    """
    Load and deserialize a Python object from disk using joblib.
    
    Args:
        file_path: Path to the serialized object file
        
    Returns:
        Deserialized Python object
        
    Raises:
        StocksyException: If load operation fails
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Object file not found at: {file_path}")
        obj = joblib.load(file_path)
        logger.info(f"Object loaded successfully from: {file_path}")
        return obj
    except Exception as e:
        logger.error(f"Failed to load object from {file_path}: {str(e)}")
        raise StocksyException(e, sys)


def format_indian_number(value: int) -> str:
    """
    Format an integer in Indian numbering system (e.g., 10,00,000).
    
    Args:
        value: Integer to format
        
    Returns:
        Formatted string in Indian number system
    """
    s = str(int(value))
    if len(s) <= 3:
        return s
    
    last_three = s[-3:]
    remaining = s[:-3]
    parts = []
    
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    
    if remaining:
        parts.insert(0, remaining)
    
    return ",".join(parts + [last_three])


def format_market_cap(market_cap: Optional[float]) -> str:
    """
    Format market cap value in crores (Cr).
    
    Args:
        market_cap: Market cap value
        
    Returns:
        Formatted market cap string
    """
    if market_cap is None or market_cap <= 0:
        return "N/A"
    
    try:
        market_cap_cr = round(float(market_cap) / 1e7)
        if market_cap_cr > 0:
            return f"{format_indian_number(market_cap_cr)}Cr"
    except Exception:
        pass
    
    return "N/A"


def validate_dataframe(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validate that a DataFrame has required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        True if valid, False otherwise
    """
    if df is None or df.empty:
        logger.warning("DataFrame is empty or None")
        return False
    
    missing = set(required_columns) - set(df.columns)
    if missing:
        logger.warning(f"Missing required columns: {missing}")
        return False
    
    return True


if __name__ == "__main__":
    logger.info("Stocksy utilities module loaded successfully.")
