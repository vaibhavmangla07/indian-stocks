"""
Stocksy - Advanced Market Analysis & Machine Learning Predictions
A Streamlit application for analyzing Indian stocks with real-time data and ML forecasts.
"""

from src.exception import StocksyException
from src.logger import logger
from src.config import APP_NAME, APP_VERSION
from src import utils
from src import data
from src import models

__version__ = APP_VERSION
__all__ = ["StocksyException", "logger", "utils", "data", "models"]

