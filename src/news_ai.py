import json
import os
import re
from typing import Dict, List, Tuple
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from src.logger import logger

load_dotenv()


def _get_ollama_base_url() -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip().rstrip("/")
    if base_url == "http://localhost:11434":
        return "http://127.0.0.1:11434"
    return base_url


def _normalize_ticker(stock_query: str) -> str:
    ticker = stock_query.strip().upper()
    if not ticker:
        return ticker
    if ticker.startswith("^") or ticker.endswith(".NS") or ticker.endswith(".BO"):
        return ticker
    return f"{ticker}.NS"


def _clean_json_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _parse_json_payload(text: str) -> Dict:
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
            obj = json.loads(cleaned[start:end + 1])
            return obj if isinstance(obj, dict) else {}
        except Exception:
            pass

    raise ValueError("Unable to parse JSON payload from Ollama response")


def _generate_with_ollama(prompt: str) -> str:
    base_url = _get_ollama_base_url()
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1")
    endpoint = f"{base_url}/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1},
    }

    headers = {"Content-Type": "application/json"}
    
    # Inject Ollama Cloud API Key if present in .env
    api_key = os.getenv("OLLAMA_API_KEY", "").strip()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        body = response.read().decode("utf-8")
    parsed = json.loads(body)
    return str(parsed.get("response", "")).strip()


def _get_category(title: str) -> str:
    text = title.lower()
    if any(w in text for w in ["deal", "order", "contract", "win", "stake"]):
        return "deal"
    if any(w in text for w in ["policy", "court", "government", "cpi", "rbi", "budget", "results"]):
        return "current_affairs"
    return "latest"


def fetch_ai_stock_news(
    stock_query: str,
    limit: int = 10,
) -> Tuple[str, List[Dict[str, str]], str, List[str], bool]:
    ticker = _normalize_ticker(stock_query)
    stock_name = stock_query.strip().upper().replace(".NS", "").replace(".BO", "")

    ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
    if not ollama_model:
        logger.warning("OLLAMA_MODEL not set in .env")
        return ticker, [], "Ollama model is not configured in .env", [], False

    logger.info("Asking Ollama for top %s news for %s", limit, stock_name)

    prompt = (
        f"You are a financial analyst with deep knowledge of Indian stock markets. "
        f"Generate the top {limit} latest and most important stock news headlines for {stock_name} "
        f"(NSE India listed company). "
        f"For each news item provide: a realistic headline title, publication date in DD-Mon-YY format, "
        f"source name (Reuters, Economic Times, Moneycontrol, Business Standard, Livemint, Bloomberg), "
        f"a real and plausible source URL, "
        f"and one sentence explaining why it matters for the stock price or investors. "
        f"Also write a short overall AI summary paragraph and 4-5 short actionable investor next steps. "
        f"Return JSON only in this exact format with no extra text: "
        f'{{\"summary\":\"...\",\"next_steps\":[\"...\",\"...\"],'
        f'\"highlights\":[{{\"title\":\"...\",\"published_at\":\"...\",\"source\":\"...\",\"url\":\"...\",\"why_it_matters\":\"...\"}}]}}'
    )

    try:
        response_text = _generate_with_ollama(prompt)
        payload = _parse_json_payload(response_text)

        summary = str(payload.get("summary", "")).strip()
        next_steps = [str(s).strip() for s in payload.get("next_steps", []) if s]
        highlights = payload.get("highlights", [])
        items: List[Dict[str, str]] = []

        for item in highlights if isinstance(highlights, list) else []:
            if not isinstance(item, dict):
                continue
            items.append({
                "title": str(item.get("title", "Untitled")).strip(),
                "source": str(item.get("source", "Unknown")).strip(),
                "url": str(item.get("url", "")).strip(),
                "published_at": str(item.get("published_at", "N/A")).strip(),
                "why_it_matters": str(item.get("why_it_matters", "")).strip(),
                "category": _get_category(str(item.get("title", ""))),
            })

        if not summary:
            summary = f"AI-generated news analysis for {stock_name}."

        return ticker, items[:limit], summary, next_steps, True

    except Exception as exc:
        logger.warning("Ollama news generation failed for %s: %s", stock_query, exc)
        return ticker, [], f"Could not generate news for {stock_name}. Check Ollama connection.", [], False
