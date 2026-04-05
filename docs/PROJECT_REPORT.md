# 📊 Stocksy: Comprehensive Project Report & Overview

## 1. Project Title
**Stocksy**: Advanced Market Analysis & Machine Learning Predictions for Indian Stocks.

## 2. Objective
The primary objective of this project is to build an end-to-end, full-stack financial dashboard tailored for the Indian Equity Market (NSE/BSE). This application aims to democratize institutional-grade financial telemetry by combining real-time market data, technical indicator charting, machine learning forecasting, and Local Large Language Model (LLM) news intelligence into a single, highly performant web interface.

---

## 3. Problem Statement
Retail investors often face information fragmentation. To make informed decisions, they must hop between:
1. Brokerage apps (for live prices and charts).
2. Financial portals (for P/E ratios and market caps).
3. News aggregators (for market sentiment).
4. Trading algorithms (for statistical forecasting).

**The Solution**: Stocksy attempts to solve this fragmentation by unifying all four pillars into an intuitive Streamlit dashboard. Furthermore, it addresses data-privacy concerns by processing AI market sentiment locally using open-weights models (via Ollama) rather than transmitting queries to proprietary cloud API endpoints.

---

## 4. Key Features Delivered

1. **Live Market Pulse**: Instant ticker tracking of the `NIFTY 50`, `SENSEX`, and `BANK NIFTY`.
2. **Deep History & Technicals**: Interactive visualization of closing prices, trading volume, and dynamic "Period-Aware" performance metrics (e.g., automatically calculating the 5-Year True High/Low and percentage deltas from the current price).
3. **Machine Learning Projections**: Integrates `scikit-learn` Ridge Regression models. By calculating historical Simple Moving Averages (`SMA_20`, `SMA_50`) and standard deviation (`Volatility`) dynamically, the application projects potential 20-day and 60-day price trajectories natively inside the historical chart.
4. **Local AI News Intelligence**: A groundbreaking feature running entirely on offline hardware. Stocksy fetches generic URL headlines and passes them through a highly constrained JSON prompt to a local **Ollama** Daemon. The LLM acts as an expert analyst, outputting structured "Why it matters" statements and "Investor Next Steps" without token costs or data leakage.
5. **Fundamental Screeners**: Instant extraction of company descriptions, actual market capitalization formatting (in ₹ Crores), and Trailing P/E metrics directly from Yahoo Finance data streams.

---

## 5. Technology Stack

| Domain | Technology / Library | Role in Project |
| :--- | :--- | :--- |
| **Frontend UI** | `Streamlit` | Core user interface, routing, layout rendering, and caching. |
| **Data Ingestion** | `yfinance` | Rapid querying of historical arrays and fundamental dictionaries. |
| **Machine Learning** | `scikit-learn`, `pandas`, `joblib` | Feature engineering (SMAs/Volatility) and Ridge Regression modeling. |
| **Artificial Intelligence** | `Ollama` | Local LLM inference engine generating JSON financial summaries. |
| **Environment / Ops** | `python-dotenv`, `Docker` | Secure variable management and containerized deployment paths. |

---

## 6. Project Architecture Overview

Stocksy implements a highly modular structure to separate concerns:

1. **The Presentation Layer (`frontend/`)**: Houses discrete scripts for each tab (`home.py`, `stock_news.py`, etc.). Employs `@st.cache_data` heavily to preserve computational overhead during state changes.
2. **The Logic Engine (`src/`)**: Acts as the backend proxy. Contains routing for ML serializers (`data_manager.py`) and complex JSON web-scraping sanitizers (`news_ai.py`).
3. **The Data Hub (`model/` & `.env`)**: Secures pre-trained model weights (`.pkl` files) and ensures local port integration for external background tasks (Ollama daemons).

*(For deep technical specifics, refer to `API_DOCUMENTATION.md`, `BACKEND_DOCUMENTATION.md`, and `FRONTEND_DOCUMENTATION.md` in this directory).*

---

## 7. Challenges Overcome

- **LLM Output Sanitization**: Initial versions of the local AI generated unstructured markdown blobs that broke Streamlit UI tables. This was solved by engineering a strict systemic prompt that forces Ollama to reply exclusively in valid JSON format, combined with a Python Regex sanitizer to strip rogue formatting blocks.
- **Data Latency**: Fetching 5 years of daily string data while simultaneously generating ML trajectories initially caused 4-5 second page freezes. Implemented intelligent caching to ensure that once a ticker is queried, subsequent tab switches are instantaneous.
- **Scientific Notation Parsing**: Yahoo Finance returns massive integers for Market Cap (e.g., `18500000000000`), forcing the creation of a custom math parser `_format_indian_number` to dynamically convert and display the standard Indian readable format (e.g., `₹18.5 lakh Cr`).

---

## 8. Future Scope & Enhancements

1. **User Authentication & Portfolios**: Allowing users to log in, save a basket of watched tickers, and calculate cumulative portfolio ROI against the Nifty 50.
2. **Deep Learning Upgrades**: Upgrading the rudimentary Ridge Regression models to state-of-the-art LSTM (Long Short-Term Memory) or Transformer-based time-series architectures for more accurate horizon predictions.
3. **Automated Trading Hooks**: Creating Webhook triggers allowing the platform to execute mock paper-trades based on sentiment shifts detected by the Local LLM in the `news_ai.py` array.
