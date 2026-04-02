import os
import importlib
from datetime import datetime
from typing import Dict, List, Tuple

import yfinance as yf

from src.logger import logging


def _normalize_ticker(stock_query: str) -> str:
    ticker = stock_query.strip().upper()
    if not ticker:
        return ticker
    if ticker.startswith("^") or ticker.endswith(".NS") or ticker.endswith(".BO"):
        return ticker
    return f"{ticker}.NS"


def _extract_publish_ts(item: Dict) -> int:
    content = item.get("content", {}) if isinstance(item, dict) else {}

    pub_date = content.get("pubDate") if isinstance(content, dict) else None
    if pub_date:
        try:
            dt_obj = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
            return int(dt_obj.timestamp())
        except Exception:
            pass

    if isinstance(item, dict) and item.get("providerPublishTime"):
        try:
            return int(item["providerPublishTime"])
        except Exception:
            pass

    return 0


def fetch_stock_news(stock_query: str, limit: int = 10) -> Tuple[str, List[Dict[str, str]]]:
    """Fetch stock news via yfinance and return normalized ticker + simplified news list."""
    logging.info("Fetching stock news for %s with limit %s", stock_query, limit)
    ticker = _normalize_ticker(stock_query)
    if not ticker:
        return "", []

    raw_news = []
    for candidate in [ticker, stock_query.strip().upper(), f"{stock_query.strip().upper()}.BO"]:
        if not candidate:
            continue
        try:
            items = yf.Ticker(candidate).news or []
            if items:
                raw_news = items
                ticker = candidate
                break
        except Exception:
            continue

    sorted_news = sorted(raw_news, key=_extract_publish_ts, reverse=True)

    cleaned: List[Dict[str, str]] = []
    for item in sorted_news[:limit]:
        content = item.get("content", {}) if isinstance(item, dict) else {}

        title = (
            content.get("title")
            or item.get("title", "Untitled")
            if isinstance(item, dict)
            else "Untitled"
        )

        provider = content.get("provider", {}) if isinstance(content, dict) else {}
        source = (
            provider.get("displayName")
            or content.get("provider")
            or (item.get("publisher") if isinstance(item, dict) else None)
            or "Unknown"
        )

        canonical_url = content.get("canonicalUrl", {}) if isinstance(content, dict) else {}
        click_url = content.get("clickThroughUrl", {}) if isinstance(content, dict) else {}
        link = (
            canonical_url.get("url")
            or click_url.get("url")
            or (item.get("link") if isinstance(item, dict) else "")
            or ""
        )

        published_at = "N/A"
        pub_date = content.get("pubDate") if isinstance(content, dict) else None
        if pub_date:
            try:
                published_at = datetime.fromisoformat(pub_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
            except Exception:
                published_at = "N/A"
        elif isinstance(item, dict) and item.get("providerPublishTime"):
            try:
                published_at = datetime.fromtimestamp(int(item["providerPublishTime"])).strftime("%Y-%m-%d %H:%M")
            except Exception:
                published_at = "N/A"

        cleaned.append(
            {
                "title": title,
                "source": source,
                "url": link,
                "published_at": published_at,
            }
        )

    return ticker, cleaned

