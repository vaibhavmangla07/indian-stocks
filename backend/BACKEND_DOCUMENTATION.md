# Backend Documentation (Interview Guide)

## 1. Backend Role

The backend layer acts as a service abstraction between UI and external data providers.

Primary files:

- backend/data_manager.py
- backend/news_ai.py

It is responsible for:

- Data retrieval from yfinance
- Data normalization and fallback handling
- Feature engineering for ML inference
- Returning frontend-ready dictionaries/dataframes

## 2. data_manager.py Responsibilities

### fetch_indices()

- Pulls 5-day index history for key benchmarks
- Computes last close, absolute change, and percentage change
- Returns dictionary keyed by index name

### fetch_data(ticker, period)

- Pulls historical stock data by period
- Normalizes DataFrame columns
- Filters invalid zero-volume rows when available

### predict_horizons(df)

- Loads short-term and long-term Ridge model artifacts
- Builds momentum and volatility features
- Performs inference for short and long horizon returns
- Converts predicted returns into predicted prices

### fetch_stock_fundamentals(ticker)

- Reads yfinance info and fast_info
- Computes 1-year return from price history
- Uses multiple fallbacks for PE and Book Value
- Normalizes dividend yield and market cap display values

### fetch_shareholding_pattern(ticker)

- Returns currently mocked shareholding structure and quarter metadata
- Designed as replaceable adapter for future real data API

## 3. news_ai.py Responsibilities

Current active responsibility is news fetching only.

### fetch_stock_news(stock_query, limit)

- Normalizes ticker formats (.NS, .BO, index symbols)
- Tries multiple ticker candidates
- Sorts items by publish timestamp descending
- Maps provider payload to clean fields:
  - title
  - source
  - url
  - published_at

## 4. Caching Strategy

- Uses Streamlit cache decorators in backend functions
- TTL chosen by data type:
  - faster-changing data gets shorter TTL
  - slow-changing data gets longer TTL

Interview explanation:

"Caching is applied close to data access functions to avoid repeated network calls while keeping UI code simple and deterministic."

## 5. Error and Fallback Design

- Provider calls wrapped in try/except where needed
- Missing values converted to N/A instead of failing pages
- Fallback keys and derived calculations reduce blank fields

Interview explanation:

"The backend is defensive because finance provider schemas can be inconsistent. We prefer resilient partial rendering over hard failures."

## 6. Data Contracts to Frontend

Each function returns stable shapes expected by UI:

- fetch_indices -> dict of metric dicts
- fetch_data -> pandas DataFrame or None
- fetch_stock_fundamentals -> normalized dict
- fetch_stock_news -> (normalized_ticker, list of normalized items)

This reduces coupling and simplifies frontend testing.

## 7. Known Gaps and Improvement Plan

1. Replace mocked shareholding with real provider
2. Add structured logging instead of print for production observability
3. Add unit tests for normalization helpers
4. Add retry/backoff around provider calls
5. Centralize schema validation for provider payloads
