import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from src.logger import logging

from src.config import (
    CACHE_TTL_MARKET_DATA,
    CACHE_TTL_FUNDAMENTALS,
    LONG_TERM_MODEL_PATH,
    ML_MIN_DATA_POINTS,
    POPULAR_STOCKS,
    SHORT_TERM_MODEL_PATH,
)


def _to_float(value):
    try:
        return float(value)
    except Exception:
        return None


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
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            if len(hist) < 2:
                data[name] = None
                continue

            current = _to_float(hist["Close"].iloc[-1])
            previous = _to_float(hist["Close"].iloc[-2])
            if current is None or previous in (None, 0):
                data[name] = None
                continue

            change = current - previous
            change_percent = (change / previous) * 100
            data[name] = {
                "price": current,
                "change": change,
                "change_percent": change_percent,
            }
        except Exception:
            data[name] = None

    return data


@st.cache_data(ttl=CACHE_TTL_MARKET_DATA)
def fetch_data(ticker, period):
    logging.info("Fetching historical data for %s with period %s", ticker, period)
    try:
        df = yf.Ticker(ticker).history(period=period)
        if df.empty:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()
        if "Volume" in df.columns:
            df = df[df["Volume"] > 0]
        return df
    except Exception:
        logging.warning("Failed to fetch data for %s", ticker)
        return None


def predict_horizons(df):
    logging.info("Running horizon prediction on dataframe with %s rows", len(df))
    if len(df) < ML_MIN_DATA_POINTS:
        return None, None

    if not (os.path.exists(SHORT_TERM_MODEL_PATH) and os.path.exists(LONG_TERM_MODEL_PATH)):
        return None, None

    try:
        model_short = joblib.load(SHORT_TERM_MODEL_PATH)
        model_long = joblib.load(LONG_TERM_MODEL_PATH)

        work_df = df.copy()
        work_df["Mom_5d"] = work_df["Close"].pct_change(5)
        work_df["Mom_20d"] = work_df["Close"].pct_change(20)
        work_df["Mom_60d"] = work_df["Close"].pct_change(60)
        work_df["Volatility_20d"] = work_df["Close"].pct_change().rolling(20).std()

        latest = work_df.iloc[-1]
        if pd.isna(latest["Mom_60d"]) or pd.isna(latest["Volatility_20d"]):
            return None, None

        features = [[
            float(np.squeeze(latest["Mom_5d"])),
            float(np.squeeze(latest["Mom_20d"])),
            float(np.squeeze(latest["Mom_60d"])),
            float(np.squeeze(latest["Volatility_20d"])),
        ]]

        short_return = float(model_short.predict(features)[0])
        long_return = float(model_long.predict(features)[0])
        current_price = float(np.squeeze(latest["Close"]))

        return current_price * (1 + short_return), current_price * (1 + long_return)
    except Exception:
        logging.warning("Prediction failed for horizon models")
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
    """Fetch stock fundamentals for Stock Detail page."""
    logging.info("Fetching fundamentals for %s", ticker)
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        fast_info = getattr(stock, "fast_info", {}) or {}

        hist_1y = stock.history(period="1y")
        year_return = None
        if len(hist_1y) >= 2:
            start_price = hist_1y["Close"].iloc[0]
            end_price = hist_1y["Close"].iloc[-1]
            year_return = ((end_price - start_price) / start_price) * 100

        pe_ratio = info.get("trailingPE")
        pe_ratio = pe_ratio if pe_ratio is not None else info.get("forwardPE")
        eps_ttm = info.get("epsTrailingTwelveMonths")

        current_price = info.get("currentPrice") or fast_info.get("last_price")
        previous_close = info.get("previousClose") or fast_info.get("previous_close")
        open_price = info.get("open") or fast_info.get("open")
        day_low = info.get("dayLow") or fast_info.get("day_low")
        day_high = info.get("dayHigh") or fast_info.get("day_high")
        week_52_low = info.get("fiftyTwoWeekLow") or fast_info.get("year_low")
        week_52_high = info.get("fiftyTwoWeekHigh") or fast_info.get("year_high")
        beta = info.get("beta")
        volume = info.get("volume") or fast_info.get("last_volume")
        avg_volume = info.get("averageVolume") or fast_info.get("ten_day_average_volume") or fast_info.get("three_month_average_volume")
        dividend_rate = info.get("dividendRate")
        ex_dividend_date = info.get("exDividendDate")
        target_mean_price = info.get("targetMeanPrice")
        full_time_employees = info.get("fullTimeEmployees")
        website = info.get("website")
        long_business_summary = info.get("longBusinessSummary") or info.get("summary")
        industry = info.get("industry") or info.get("industryDisp")
        fiscal_year_end = info.get("fiscalYearEnd")
        company_name = info.get("longName") or info.get("shortName") or ticker.replace(".NS", "").replace(".BO", "")

        if pe_ratio is None:
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

        return {
            "previous_close": previous_close,
            "open_price": open_price,
            "day_low": day_low,
            "day_high": day_high,
            "week_52_low": week_52_low,
            "week_52_high": week_52_high,
            "beta": beta,
            "volume": volume,
            "avg_volume": avg_volume,
            "pe_ratio": round(pe_ratio, 2) if isinstance(pe_ratio, (int, float)) else "N/A",
            "eps_ttm": round(eps_ttm, 2) if isinstance(eps_ttm, (int, float)) else "N/A",
            "dividend_rate": round(dividend_rate, 2) if isinstance(dividend_rate, (int, float)) else "N/A",
            "book_value": round(book_value, 2) if isinstance(book_value, (int, float)) else "N/A",
            "year_return": round(year_return, 2) if year_return is not None else "N/A",
            "sector": sector,
            "market_cap": _format_market_cap_cr(market_cap),
            "dividend_yield": dividend_yield,
            "ex_dividend_date": pd.to_datetime(ex_dividend_date, unit="s", errors="coerce") if ex_dividend_date else None,
            "target_mean_price": round(target_mean_price, 2) if isinstance(target_mean_price, (int, float)) else "N/A",
            "full_time_employees": int(full_time_employees) if isinstance(full_time_employees, (int, float)) else "N/A",
            "website": website or "N/A",
            "business_summary": long_business_summary or "N/A",
            "industry": industry or "N/A",
            "fiscal_year_end": fiscal_year_end or "N/A",
            "company_name": company_name or ticker,
        }
    except Exception:
        logging.warning("Failed to fetch fundamentals for %s", ticker)
        return None
