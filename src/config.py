import os
from typing import List

# Application Settings
APP_NAME = "Stocksy"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Advanced Market Analysis & Machine Learning Predictions for Indian Stocks"

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
MESSAGES_DIR = os.path.join(PROJECT_ROOT, "messages")
MODELS_DIR = os.path.join(PROJECT_ROOT, "notebook")

# Model Paths
SHORT_TERM_MODEL_PATH = os.path.join(MODELS_DIR, "model_short_term.pkl")
LONG_TERM_MODEL_PATH = os.path.join(MODELS_DIR, "model_long_term.pkl")

# Streamlit Configuration
STREAMLIT_PORT = 8501
STREAMLIT_LAYOUT = "wide"
STREAMLIT_THEME = "light"

# Data Fetching Configuration
CACHE_TTL_MARKET_DATA = 300  # 5 minutes
CACHE_TTL_FUNDAMENTALS = 3600  # 1 hour

# Market Data Configuration
INDICES = {
    "^NSEI": "NIFTY 50",
    "^BSESN": "SENSEX",
    "^NSEBANK": "BANK NIFTY"
}

# Popular Indian Stocks
POPULAR_STOCKS: List[str] = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "BHARTIARTL", 
    "SBIN", "INFY", "LICI", "ITC", "HINDUNILVR", "LT", "BAJFINANCE", 
    "HCLTECH", "MARUTI", "SUNPHARMA", "ADANIENT", "KOTAKBANK", 
    "TITAN", "ONGC", "JTLIND", "NTPC", "AXISBANK", "DMART", 
    "ADANIPORTS", "ULTRACEMCO", "ASIANPAINT", "COALINDIA", 
    "BAJAJFINSV", "BAJAJ-AUTO", "POWERGRID", "NESTLEIND", "WIPRO", 
    "M&M", "IOC", "JIOFIN", "HAL", "DLF", "ADANIGREEN", "TATASTEEL", 
    "SIEMENS", "VBL", "ZOMATO", "PIDILITind", "GRASIM", "SBILIFE", 
    "BEL", "LTIM", "TRENT", "HINDALCO", "INDUSINDBK", "GODREJCP", 
    "INDIGO", "BANKBARODA", "HDFCLIFE", "BOSCHLTD", "BPCL", "PFC", 
    "IREDA", "IRFC", "RVNL", "PNB"
]

# Stock Exchange Suffixes
STOCK_SUFFIXES = {
    "NSE": ".NS",  # National Stock Exchange
    "BSE": ".BO"   # Bombay Stock Exchange
}

# ML Model Configuration
ML_FEATURE_NAMES = ["Mom_5d", "Mom_20d", "Mom_60d", "Volatility_20d"]
ML_MIN_DATA_POINTS = 61  # Minimum historical data for ML prediction

# Time Periods for Stock Analysis
TIME_PERIODS = ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
DEFAULT_PERIOD = "1y"

# News Configuration
NEWS_LIMIT = 10  # Default number of news articles to fetch
NEWS_SOURCES_TIMEOUT = 10  # Timeout for news API calls

# Display Formats
CURRENCY_FORMAT = "₹"
PERCENTAGE_FORMAT = ".2f"

# Error Messages
ERROR_MSG_NO_DATA = "Unable to fetch data. Please try again."
ERROR_MSG_MODEL_NOT_FOUND = "ML model file not found."
ERROR_MSG_INVALID_TICKER = "Invalid ticker symbol."

if __name__ == "__main__":
    print(f"{APP_NAME} v{APP_VERSION}: {APP_DESCRIPTION}")
    print(f"Popular Stocks: {len(POPULAR_STOCKS)} stocks available")
    print(f"Models: {SHORT_TERM_MODEL_PATH}, {LONG_TERM_MODEL_PATH}")
