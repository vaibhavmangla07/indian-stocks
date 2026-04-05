import json
import os
import re
from datetime import datetime
from html import unescape
from typing import Dict, List, Tuple
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yfinance as yf
from dotenv import load_dotenv

from src.logger import logging

load_dotenv()


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


def _extract_yfinance_news(raw_news: List[Dict], limit: int) -> List[Dict[str, str]]:
    cleaned: List[Dict[str, str]] = []

    for item in sorted(raw_news, key=_extract_publish_ts, reverse=True)[:limit]:
        content = item.get("content", {}) if isinstance(item, dict) else {}

        title = "Untitled"
        if isinstance(item, dict):
            title = content.get("title") or item.get("title", "Untitled")

        source = None
        if isinstance(content, dict):
            source = content.get("provider", {}).get("displayName") or content.get("provider")
        if not source and isinstance(item, dict):
            source = item.get("publisher")
        source = source or "Unknown"

        link = None
        if isinstance(content, dict):
            link = content.get("canonicalUrl", {}).get("url") or content.get("clickThroughUrl", {}).get("url")
        if not link and isinstance(item, dict):
            link = item.get("link")
        link = link or ""

        published_at = "N/A"
        pub_date = content.get("pubDate") if isinstance(content, dict) else None
        if pub_date:
            try:
                published_at = datetime.fromisoformat(pub_date.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
            except Exception:
                published_at = "N/A"

        cleaned.append(
            {
                "title": str(title).strip(),
                "source": str(source).strip(),
                "url": str(link).strip(),
                "published_at": published_at,
            }
        )

    return cleaned


def _fetch_google_news(stock_query: str, limit: int = 10) -> List[Dict[str, str]]:
    query = quote_plus(f"{stock_query} stock news")
    rss_url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-IN&gl=IN&ceid=IN:en"

    try:
        with urlopen(rss_url, timeout=10) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
    except Exception:
        return []

    items: List[Dict[str, str]] = []
    for item in root.findall("./channel/item")[:limit]:
        title = unescape(item.findtext("title", default="Untitled"))
        link = item.findtext("link", default="")
        published_at = item.findtext("pubDate", default="N/A")

        source_node = item.find("source")
        source = unescape(source_node.text) if source_node is not None and source_node.text else "Google News"

        items.append(
            {
                "title": title,
                "source": source,
                "url": link,
                "published_at": published_at,
            }
        )
    return items


def fetch_stock_news(stock_query: str, limit: int = 10) -> Tuple[str, List[Dict[str, str]]]:
    """Fetch stock news from Google News first, then yfinance as fallback."""
    logging.info("Fetching stock news for %s with limit %s", stock_query, limit)
    ticker = _normalize_ticker(stock_query)
    if not ticker:
        return "", []

    google_news_items = _fetch_google_news(stock_query, limit=limit)
    if google_news_items:
        return ticker, google_news_items

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

    return ticker, _extract_yfinance_news(raw_news, limit=limit)


def _clean_json_text(text: str) -> str:
    cleaned_text = text.strip()
    cleaned_text = re.sub(r"^```(?:json)?\s*", "", cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"\s*```$", "", cleaned_text)
    return cleaned_text.strip()


def _parse_json_payload(text: str) -> Dict:
    """Parse JSON from model output even when extra text is present."""
    cleaned = _clean_json_text(text)

    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        pass

    try:
        decoder = json.JSONDecoder()
        obj, _ = decoder.raw_decode(cleaned)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        pass

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            obj = json.loads(cleaned[start : end + 1])
            return obj if isinstance(obj, dict) else {}
        except Exception:
            pass

    raise ValueError("Unable to parse JSON payload from Ollama response")


def _generate_with_ollama(prompt: str) -> str:
    """Call local Ollama API and return generated response text."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1")
    endpoint = f"{base_url}/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1},
    }

    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        body = response.read().decode("utf-8")
    parsed = json.loads(body)
    return str(parsed.get("response", "")).strip()


def fetch_ai_stock_news(
    stock_query: str,
    limit: int = 10,
    candidate_limit: int = 30,
) -> Tuple[str, List[Dict[str, str]], str, bool]:
    """Fetch Ollama-curated stock news and fall back to raw headlines when needed."""
    ticker, raw_news = fetch_stock_news(stock_query, limit=candidate_limit)
    if not raw_news:
        return ticker, [], "", False

    ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
    if not ollama_model:
        return ticker, raw_news[:limit], "Ollama model is not configured. Showing latest market news.", False

    prompt = (
        "Pick the 10 most important headlines for this stock and write a short summary for each one. "
        "Use only the news items below and return JSON only in this format: "
        "{\"summary\":\"...\",\"highlights\":[{\"title\":\"...\",\"source\":\"...\",\"url\":\"...\",\"published_at\":\"...\",\"summary\":\"...\"}]}. "
        f"Stock: {ticker or stock_query}\nNews items: {json.dumps(raw_news, ensure_ascii=False)}"
    )

    try:
        response_text = _generate_with_ollama(prompt)
        payload = _parse_json_payload(response_text)

        summary = str(payload.get("summary", "")).strip()
        highlights = payload.get("highlights", [])
        items: List[Dict[str, str]] = []

        for item in highlights if isinstance(highlights, list) else []:
            if not isinstance(item, dict):
                continue
            items.append(
                {
                    "title": str(item.get("title", "Untitled")).strip(),
                    "source": str(item.get("source", "Unknown")).strip(),
                    "url": str(item.get("url", "")).strip(),
                    "published_at": str(item.get("published_at", "N/A")).strip(),
                    "summary": str(item.get("summary", "")).strip(),
                    "category": _get_category(str(item.get("title", ""))),
                }
            )

        if not items:
            items = [
                {
                    **news_item,
                    "summary": "",
                    "category": _get_category(news_item.get("title", "")),
                }
                for news_item in raw_news[:limit]
            ]

        if not summary:
            summary = f"Latest market headlines for {ticker or stock_query}."

        return ticker, items[:limit], summary, True

    except Exception as exc:
        logging.warning("Ollama news generation failed for %s: %s; using fallback headlines", stock_query, exc)
        fallback_items = [
            {
                **news_item,
                "summary": "",
                "category": _get_category(news_item.get("title", "")),
            }
            for news_item in raw_news[:limit]
        ]
        return ticker, fallback_items, f"Latest market news for {ticker or stock_query}.", False


def _get_category(title: str) -> str:
    text = title.lower()
    if any(word in text for word in ["deal", "order", "orderbook", "contract", "win", "stake"]):
        return "deal"
    if any(word in text for word in ["policy", "court", "government", "cpi", "rbi", "budget", "results"]):
        return "current_affairs"
    return "latest"
