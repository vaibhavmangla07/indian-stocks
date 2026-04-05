# 🔌 Stocksy API Documentation

While Stocksy does not run a standalone backend web server (e.g., FastAPI, Django), it acts as an orchestration engine that interfaces with a robust set of internal methods and external endpoints. This document outlines the core data-fetching mechanisms, machine learning inference points, and LLM integrations that power the application.

---

## 1. Market Data Integrations (`src/data_manager.py`)

All financial data ingestion relies heavily on the `yfinance` Python library, wrapping Yahoo Finance's undocumented API endpoints.

### `fetch_indices()`
- **Purpose**: Retrieves real-time pricing and daily change metrics for major Indian market indices.
- **Under the hood**: Pings Yahoo Finance for `^NSEI` (NIFTY 50), `^BSESN` (SENSEX), and `^NSEBANK` (BANK NIFTY).
- **Returns**: A nested dictionary containing Current Price, Absolute Change, and Percentage Change for each index.
- **Caching**: `@st.cache_data(ttl=60)` — updates every 60 seconds.

### `fetch_data(ticker: str, period: str = "1mo")`
- **Purpose**: Extracts historical OHLCV (Open, High, Low, Close, Volume) dataframe records for a chosen stock.
- **Parameters**: 
  - `ticker`: Expected to have the `.NS` (National Stock Exchange) suffix for standard Indian stocks.
  - `period`: Granularity level (`1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`).
- **Processing**: Features engineering occurs live here. Simple Moving Averages (`SMA_20`, `SMA_50`) and standard deviation parameters (`Volatility`) are dynamically injected into the pandas DataFrame.
- **Caching**: `@st.cache_data(ttl=60)`

### `fetch_stock_fundamentals(ticker: str)`
- **Purpose**: Extracts specific fundamental keys from the massive `Ticker.info` JSON object provided by Yahoo Finance.
- **Returns**: A Dictionary object parsing `longName` (Company Name), `industry`, `sector`, `marketCap`, `trailingPE`, `dividendYield`, and `longBusinessSummary`. Fallback logic applies `N/A` for missing nodes.

---

## 2. Machine Learning Inference API (`src/data_manager.py`)

### `predict_horizons(df: pd.DataFrame)`
- **Purpose**: Acts as an internal endpoint routing live pandas DataFrames to pre-serialized `scikit-learn` Ridge Regression models.
- **Process**: 
  1. Receives the engineered `df` array from `fetch_data()`.
  2. Extracts the exact columns matching model training (Close arrays, SMAs, Volume, Volatility).
  3. Deserializes `/model/model_short_term.pkl` and `/model/model_long_term.pkl`.
  4. Yields future projection floats.
- **Returns**: Tuple `(short_term_prediction: float, long_term_prediction: float)`

---

## 3. Local AI Integration API (`src/news_ai.py`)

Instead of pinging a paid API like OpenAI, Stocksy interacts seamlessly with a local **Ollama** Daemon over HTTP.

### `fetch_ai_stock_news(stock_name: str, limit: int = 10)`
- **Purpose**: Orchestrates the fetching of background stock data and routes it into an LLM context window to extract intelligent, structured news formats.
- **Ollama Endpoint Used**: `POST http://localhost:11434/api/generate` (Configured via `.env` parameter `OLLAMA_BASE_URL`).
- **Payload Schema**:
  ```json
  {
    "model": "gpt-oss:120b-cloud",  // or whatever is in .env 
    "format": "json",
    "stream": false,
    "prompt": "You are a professional financial analyst. Generate exactly 10 latest highly realistic news headlines..."
  }
  ```
- **Response Handling**: The application forces a strict `format: "json"` constraint on the LLM. The resulting string is parsed in python via `json.loads()` and dynamically rendered into a standard dictionary.
- **Fallback**: Continues to operate utilizing hardcoded emergency backup summaries if the HTTP connection to Ollama fails or times out.
- **Caching**: `@st.cache_data(ttl=300)` — aggressively cached for 5 minutes to prevent redundant LLM inference overhead and ensure rapid page loads for repeated lookups.

---

## 4. Environment Variables Map

The API connectivity parameters of Stocksy are configurable via standard environment variables:

| Variable | Description | Default Target |
|:---|:---|:---|
| `OLLAMA_BASE_URL` | The HTTP URI routing to the Ollama Daemon | `http://127.0.0.1:11434` |
| `OLLAMA_MODEL` | The specific model tag stored locally | `gpt-oss:120b-cloud` |
