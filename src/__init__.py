"""
Stocksy - Advanced Market Analysis & Machine Learning Predictions.
"""

from src.config import APP_NAME, APP_VERSION
from src.exception import StocksyException
from src.logger import logger

__version__ = APP_VERSION
__all__ = ["APP_NAME", "APP_VERSION", "StocksyException", "logger"]

