# ⚙️ Stocksy Backend Architecture Documentation

The "Backend" of Stocksy does not run as a continuous, standalone daemon (like a Node.js or Spring Boot server). Instead, it runs as a **highly modular Python backend layer** (housed exclusively within the `src/` directory) that executes synchronously when triggered by the Streamlit frontend.

This document breaks down the core architecture and logic of these backend services.

---

## 1. Directory Structure (`src/`)

```plaintext
src/
├── config.py              # Configuration Constants (Tickers, Indices)
├── data_manager.py        # Core processing (Fetching + ML Inference + Feature Eng)
├── news_ai.py             # External LLM handling (Prompt Injection + Parsing)
├── exception.py           # Custom Error Handling architecture
└── logger.py              # Application Logging configuration 
```

---

## 2. Core Modules Breakdown

### A. `config.py` (The State Definitions)
This file represents the global configurations. It is fundamentally stateless but central to standardizing inputs across the application.
- **`POPULAR_STOCKS`**: A static array of ~60 curated Indian NSE stock tickers (e.g., RELIANCE, TCS, INFY).
- **`MARKET_INDICES`**: A dictionary mapping user-friendly names to Yahoo Finance backend tickers (e.g., `"BANK NIFTY": "^NSEBANK"`).

### B. `data_manager.py` (The Engine)
This is the heaviest and most important file in the backend. It acts as both the **ETL (Extract, Transform, Load) Pipeline** and the **ML inference router**.

- **ETL Responsibilities (`fetch_data`)**:
  - Connects to `yfinance`.
  - Downloads historic OHLCV data.
  - Automatically performs Feature Engineering: it manually computes `SMA_20` (20-day Simple Moving Average), `SMA_50` (50-day Simple Moving Average), and a 20-day standard deviation for `Volatility`.
  - Cleans NaN values (Data pre-processing).

- **ML Responsibilities (`predict_horizons`)**:
  - Validates that the pre-processed `df` possesses exactly the 5 variables expected by the model.
  - Passes the isolated feature vectors to pre-loaded `scikit-learn` Ridge models via `joblib.load()`.
  
### C. `news_ai.py` (The AI Layer)
This file abstracts away the complexities of prompting an LLM. 
- It generates a custom, heavily constrained system prompt forcing the LLM into a specific persona ("Expert financial analyst").
- Instructs the LLM to return data matching a precise JSON Schema.
- Sanitizes the raw string output from Ollama using regex (`_clean_json_text`) to strip rogue markdown formatting before securely passing it to Python's `json.loads()`.

### D. `logger.py` (The Telemetry System)
A custom wrapper around Python's built-in `logging` module.
- Generates a unique log file per day/session under the `logs/` directory.
- Sets output to a unified format: `[YYYY-MM-DD HH:MM:SS,mmm] logger_name - INFO - Message`.
- Crucial for debugging "silent" data fetching errors since Streamlit suppresses native console tracebacks for end-users.

### E. `exception.py` (The Safety Net)
Defines a custom exception class `StocksyException`, extending Python's native `Exception`.
- Captures specific stack trace contexts during runtime errors (like model prediction failures).
- Prevents the entire Streamlit UI from crashing by elegantly catching exceptions and logging them.

---

## 3. Scalability & Edge Cases

- **Caching Mechanisms**: Stocksy combats latency through heavy usage of Streamlit's `@st.cache_data`. The backend guarantees that identical queries made within a typical interval (e.g., 300 seconds for AI generations, 60 seconds for market data) will *never* re-run computationally expensive logic or re-ping external APIs.
- **Fail-overs**: `data_manager.py` and `news_ai.py` are built defensively. If Ollama is offline or Yahoo finance rate limits an IP, the backend returns empty dictionaries (`{}` snippet fallbacks), ensuring the frontend always correctly renders an "Empty State" UI rather than producing a white-screen crash.
