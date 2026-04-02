import yfinance as yf
import pandas as pd
import numpy as np
import joblib
import os
import streamlit as st

from src.logger import logging
from src.config import (
    SHORT_TERM_MODEL_PATH,
    LONG_TERM_MODEL_PATH,
    POPULAR_STOCKS,
    CACHE_TTL_MARKET_DATA,
    CACHE_TTL_FUNDAMENTALS,
    CACHE_TTL_SHAREHOLDING,
    ML_MIN_DATA_POINTS,
    SHAREHOLDING_PATTERN
)

@st.cache_data(ttl=CACHE_TTL_MARKET_DATA)
def fetch_indices():
    logging.info("Fetching market indices")
    indices = {
        "^NSEI": "NIFTY 50",
        "^BSESN": "SENSEX",
        "^NSEBANK": "BANK NIFTY"
    }
    data = {}
    for ticker, name in indices.items():
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            previous = hist['Close'].iloc[-2]
            change = current - previous
            change_percent = (change / previous) * 100
            data[name] = {"price": current, "change": change, "change_percent": change_percent}
        else:
            data[name] = None
    return data

@st.cache_data(ttl=CACHE_TTL_MARKET_DATA)
def fetch_data(ticker, period):
    logging.info("Fetching historical data for %s with period %s", ticker, period)
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    if not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        if 'Volume' in df.columns:
            df = df[df['Volume'] > 0]
        return df
    return None

def predict_horizons(df):
    logging.info("Running horizon prediction on dataframe with %s rows", len(df))
    if os.path.exists(SHORT_TERM_MODEL_PATH) and os.path.exists(LONG_TERM_MODEL_PATH) and len(df) >= ML_MIN_DATA_POINTS:
        try:
            model_short = joblib.load(SHORT_TERM_MODEL_PATH)
            model_long = joblib.load(LONG_TERM_MODEL_PATH)
            
            # Calculate features for the latest data point
            # Mom_5d, Mom_20d, Mom_60d, Volatility_20d
            df['Mom_5d'] = df['Close'].pct_change(periods=5)
            df['Mom_20d'] = df['Close'].pct_change(periods=20)
            df['Mom_60d'] = df['Close'].pct_change(periods=60)
            df['Volatility_20d'] = df['Close'].pct_change().rolling(window=20).std()
            
            latest = df.iloc[-1]
            if pd.isna(latest['Mom_60d']) or pd.isna(latest['Volatility_20d']):
                return None, None
                
            features = [[
                float(np.squeeze(latest['Mom_5d'])), 
                float(np.squeeze(latest['Mom_20d'])), 
                float(np.squeeze(latest['Mom_60d'])), 
                float(np.squeeze(latest['Volatility_20d']))
            ]]
            
            pred_short_return = model_short.predict(features)[0]
            pred_long_return = model_long.predict(features)[0]
            
            # Calculate predicted prices
            current_price = float(np.squeeze(latest['Close']))
            pred_short_price = current_price * (1 + float(pred_short_return))
            pred_long_price = current_price * (1 + float(pred_long_return))
            
            return pred_short_price, pred_long_price
        except Exception as e:
            print(f"Error predicting horizons: {e}")
            return None, None
    return None, None


def _format_indian_number(value: int) -> str:
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


def _format_market_cap_cr(market_cap: float):
    if market_cap is None:
        return "N/A"
    try:
        market_cap_cr = round(float(market_cap) / 1e7)
        if market_cap_cr <= 0:
            return "N/A"
        return f"{_format_indian_number(market_cap_cr)}Cr"
    except Exception:
        return "N/A"


@st.cache_data(ttl=CACHE_TTL_FUNDAMENTALS)
def fetch_stock_fundamentals(ticker):
    """Fetch stock fundamentals used in Stock Detail with live yfinance fallbacks."""
    logging.info("Fetching fundamentals for %s", ticker)
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        fast_info = getattr(stock, "fast_info", {}) or {}
        
        # 1-Year Return
        hist_1y = stock.history(period="1y")
        year_return = None
        if len(hist_1y) >= 2:
            start_price = hist_1y['Close'].iloc[0]
            end_price = hist_1y['Close'].iloc[-1]
            year_return = ((end_price - start_price) / start_price) * 100

        pe_ratio = info.get("trailingPE")
        if pe_ratio is None:
            pe_ratio = info.get("forwardPE")

        current_price = info.get("currentPrice")
        if current_price is None:
            current_price = fast_info.get("last_price")

        if pe_ratio is None:
            eps_ttm = info.get("epsTrailingTwelveMonths")
            if isinstance(current_price, (int, float)) and isinstance(eps_ttm, (int, float)) and eps_ttm != 0:
                pe_ratio = current_price / eps_ttm

        book_value = info.get("bookValue")
        if book_value is None:
            price_to_book = info.get("priceToBook")
            if isinstance(current_price, (int, float)) and isinstance(price_to_book, (int, float)) and price_to_book != 0:
                book_value = current_price / price_to_book

        if year_return is None:
            wk_52_change = info.get("52WeekChange")
            if isinstance(wk_52_change, (int, float)):
                year_return = wk_52_change * 100

        market_cap = info.get("marketCap")
        if market_cap is None:
            market_cap = fast_info.get("market_cap")

        dividend_yield = info.get("dividendYield")
        if isinstance(dividend_yield, (int, float)):
            if dividend_yield <= 0.2:
                dividend_yield = round(dividend_yield * 100, 2)
            elif dividend_yield > 20:
                dividend_yield = round(dividend_yield / 100, 2)
            else:
                dividend_yield = round(dividend_yield, 2)
        else:
            dividend_yield = "N/A"

        sector = info.get("sector") or info.get("industryDisp") or info.get("industry") or "N/A"
        
        fundamentals = {
            "pe_ratio": round(pe_ratio, 2) if isinstance(pe_ratio, (int, float)) else "N/A",
            "book_value": round(book_value, 2) if isinstance(book_value, (int, float)) else "N/A",
            "year_return": round(year_return, 2) if year_return is not None else "N/A",
            "sector": sector,
            "market_cap": _format_market_cap_cr(market_cap),
            "dividend_yield": dividend_yield,
        }
        return fundamentals
    except Exception as e:
        print(f"Error fetching fundamentals: {e}")
        return None


@st.cache_data(ttl=CACHE_TTL_SHAREHOLDING)
def fetch_shareholding_pattern(ticker):
    """Fetch shareholding pattern (mock data for now - replace with real API if available)."""
    logging.info("Fetching shareholding pattern for %s", ticker)
    shareholding = SHAREHOLDING_PATTERN.copy()
    quarter_info = {
        "quarter": "Q4 FY2026",
        "date": "31-Mar-2026",
        "arrow": "↑ Updated",
    }
    return shareholding, quarter_info


# POPULAR_STOCKS is now imported from src.config

