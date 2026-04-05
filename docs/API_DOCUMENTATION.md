# API Documentation

## 1. API Layer Overview
This project uses both external APIs and internal function APIs.

External APIs:
1. Yahoo Finance via yfinance
2. Google News RSS
3. Ollama Local API (optional)

Internal APIs:
- Python functions in backend/data_manager.py
- Python functions in backend/news_ai.py

## 2. External APIs

### A) Yahoo Finance (yfinance)
Used for:
- Index values
- Historical stock data
- Company fundamentals
- News fallback

Main code locations:
- backend/data_manager.py
- backend/news_ai.py

### B) Google News RSS
Used for:
- Fast latest stock headlines

Main code location:
- backend/news_ai.py in _fetch_google_news()

### C) Ollama API
Used for:
- AI-selected top headlines
- Per-headline short summary text

Main code location:
- backend/news_ai.py in fetch_ai_stock_news()

Required environment variables:
- OLLAMA_BASE_URL (optional; default http://localhost:11434)
- OLLAMA_MODEL (for example: llama3.1)

Fallback behavior:
- If model not configured, Ollama not running, or API fails:
	- function returns normal latest headlines
	- used_ai is False

## 3. Internal Function APIs

### data_manager.py

fetch_indices() -> dict
- Returns major index metrics used on home page

fetch_data(ticker, period) -> DataFrame or None
- Returns cleaned historical data for chart and analysis

predict_horizons(df) -> (short_price, long_price) or (None, None)
- Uses two trained model files to return forecast prices

fetch_stock_fundamentals(ticker) -> dict or None
- Returns fundamentals used on stock detail page

fetch_shareholding_pattern(ticker) -> (dict, dict)
- Returns shareholding data and quarter metadata

### news_ai.py

fetch_stock_news(stock_query, limit=10) -> (ticker, list)
- Returns plain latest headlines without AI summaries

fetch_ai_stock_news(stock_query, limit=10, candidate_limit=30)
-> (ticker, list, summary, used_ai)
- Tries Ollama summary flow first after collecting candidate news
- Returns fallback news when AI is not available

## 4. API Flow for News (Simple)
1. User selects stock in frontend news page
2. Frontend calls fetch_ai_stock_news()
3. Backend fetches candidate headlines
5. Ollama is called (if model is configured)
6. If Ollama succeeds: AI summary + categorized items are returned
6. If Ollama fails: latest normal headlines are returned

## 5. Real Status from Current Verification
Date verified: 4 April 2026

Observed behavior before migration:
- News fetch was working
- AI summary call can fail if Ollama is not running or model is not available
- Fallback output was working

Current expected behavior after migration:
- News fetch works as before
- AI summary depends on local Ollama availability
- If Ollama is unavailable, fallback output still works

## 6. Troubleshooting

### Problem: used_ai is always False
Check:
1. OLLAMA_MODEL is present in .env
2. OLLAMA_BASE_URL is correct
3. Ollama server is running
4. Selected model is downloaded locally

### Problem: No news returned
Check:
1. Valid ticker input
2. Google News RSS temporarily unavailable
3. yfinance fallback response availability

## 7. Security and Best Practice Notes
1. Keep API key in .env only
2. Do not commit secrets to git
3. Keep fallback behavior enabled so UI does not break
