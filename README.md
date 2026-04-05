# 📈 Stocksy

> **Advanced Market Analysis & Machine Learning Predictions for Indian Stocks**

Stocksy is a professional, clean, and comprehensive Streamlit application designed specifically for analyzing Indian stocks on the National Stock Exchange (NSE) and Bombay Stock Exchange (BSE). It serves as an all-in-one financial dashboard combining real-time market data, interactive historical charting, fundamental company analysis, AI-curated news intelligence, and machine-learning-based price forecasting.

---

## 🌟 Core Features

- **📊 Live Market Indices:** Real-time, at-a-glance ticker tracking for major Indian indices—**NIFTY 50**, **SENSEX**, and **BANK NIFTY**.
- **🔎 Period-Aware Stock Explorer:** Deep dive into individual stocks with dynamic metrics. Select a time frame (1mo to 5y) to instantly see the stock's true High/Low for that specific period, along with percentage deltas from the current price.
- **📉 Interactive Charting:** Beautiful, full-width Streamlit charts displaying historical Closing Prices alongside Trading Volume over selected time horizons.
- **🤖 ML Price Forecast:** Short-term (20-day) and long-term (60-day) future price projections powered by pre-trained Ridge Regression machine learning models utilizing Simple Moving Averages and Rolling Volatility.
- **🧠 Local AI News Intelligence:** A powerful, privacy-first news engine. Stocksy fetches the latest news context and passes it to your local **Ollama** LLM (e.g., `gpt-oss:120b-cloud`) to instantly generate a curated "Top 10" news table, explaining *"Why it matters for the stock"* and offering actionable *"Investor Next Steps."*
- **🏢 Deep Fundamentals Breakdown:** Instant extraction of crucial financial ratios, exact market cap (in ₹ Crores), P/E ratios, and detailed company descriptions directly from Yahoo Finance.

---

## 🏗️ Comprehensive Project Architecture

The repository is modularly structured to separate the UI layer from the backend data pipelines and ML inference logic.

```plaintext
indian-stocks-project/
├── frontend/                  # Streamlit User Interface Layer
│   ├── app.py                 # Main entry point and page routing engine
│   └── views/                 # Isolated modules for each dashboard page
│       ├── home.py            # Renders Market Overview, Stock Explorer & ML Charting
│       ├── stock_detail.py    # Renders the Fundamental Analysis & Financial Ratios
│       ├── stock_news.py      # Renders the Local AI-powered News Intelligence board
│       ├── about.py           # Renders Project Architecture/Details
│       └── contact.py         # Submits user messages to the local file system
├── src/                       # Backend Logic, Integrations & Utilities
│   ├── data_manager.py        # Core logic: yfinance fetching, caching, and ML inference
│   ├── news_ai.py             # Pure Ollama JSON protocol integration for stock analysis
│   ├── config.py              # Centralized list of 60+ popular NSE tickers & indices
│   ├── logger.py              # Custom rolling logger saving to the 'logs/' directory
│   └── exception.py           # Custom exception handling class (StocksyException)
├── model/                     # Serialized Pre-trained Scikit-Learn Models
│   ├── model_short_term.pkl   # Ridge Regression weights for 20-day horizon forecasts
│   └── model_long_term.pkl    # Ridge Regression weights for 60-day horizon forecasts
├── notebook/                  # Research, Development & Prototyping Environment
│   ├── eda.ipynb              # Deep-dive Exploratory Data Analysis for the Indian Market
│   ├── train_model.ipynb      # Pipeline to generate, train, and export the .pkl models
│   ├── ai.ipynb               # Sandbox for tuning Ollama prompt behavior
│   └── stock_news.ipynb       # Scraping prototype sandbox for legacy news APIs
├── messages/                  # Local storage repository for "Contact Us" submissions
├── logs/                      # Timestamped application execution logs stored per session
├── docs/                      # Directory reserved for extended HTML/PDF documentation
├── requirements.txt           # Exhaustive list of Python package dependencies
├── setup.py                   # Package setup to allow 'src' to be installed as a module
├── Dockerfile                 # Configuration for containerized production deployment
├── .env                       # Environment variables config (Ollama routing)
└── README.md                  # This documentation file
```

---

## 🦾 Data & AI Stack Deep-Dive

### 1. Market Data Pipeline
All real-time pricing and fundamental data are sourced on-the-fly using the `yfinance` library. To ensure relevance to the Indian market, Stocksy automatically appends `.NS` (National Stock Exchange) to all stock queries, guaranteeing accurate ₹ (INR) pricing and volume data. Data fetching is rigorously memoized using `@st.cache_data` to ensure a snappy user experience and prevent rate-limiting.

### 2. Machine Learning Inference
The application ships with offline `scikit-learn` Ridge Regression models. When a user requests a forecast for a stock (e.g., RELIANCE):
1. Stocksy downloads the maximum historical context for that ticker.
2. It dynamically engineers features on the fly: **SMA_20**, **SMA_50**, and **Rolling Volatility**.
3. It passes these features to the serialized models (`.pkl`) to project future price trajectories, plotting the result as a seamless extension of the historical price chart.

### 3. Edge AI (Local LLM Integration)
Stocksy prioritizes privacy and speed by leveraging **Ollama**. Instead of relying on expensive OpenAI API calls, the `news_ai.py` module constructs an elaborate JSON-schema prompt detailing the stock's context. This prompt is fired to a local Ollama daemon (configured via `.env`). The LLM returns a structured JSON payload containing highly contextualized market impact analysis, which Streamlit renders into an elegant markdown table.

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8 to 3.11**
2. **Git** for cloning the repository.
3. *(Optional but Highly Recommended)* **Ollama** installed and running on your local machine if you want to use the AI News Intelligence feature.

### Step-by-Step Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/vaibhavmangla07/indian-stocks.git
    cd indian-stocks-project
    ```

2. **Initialize a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Environment File:**
    Create a file named `.env` in the root folder. Define your Ollama parameters. Make sure the `OLLAMA_MODEL` matches exactly with a model you have pulled (you can check your models by running `ollama list` in a new terminal).
    ```env
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=gpt-oss:120b-cloud 
    ```

5. **Launch Stocksy:**
    ```bash
    streamlit run frontend/app.py
    ```
    The Streamlit console will provide a local URL (usually `http://localhost:8501`), which will automatically open in your web browser.

---

## 🗂️ How the Logging System Works

Stocksy includes a robust, production-ready logging system tailored for debugging local applications. 
- A unique log file is automatically generated in the `logs/` directory every time you start the app (e.g., `logs/2026-04-05_16-04-44.log`).
- It captures all Streamlit page navigations, tracking when the user queries data (`Fetching historical data for TCS.NS...`), and notes when the ML inference or AI generation pipelines are triggered.

---

## 📄 Disclaimer

This project is built strictly for **educational and research purposes**. It serves as an architectural demonstration of integrating full-stack Python development, Streamlit, Machine Learning pipelines, and Local Large Language Models. 

**Stocksy does not provide financial advice.** The ML projections and AI-curated news summaries are for demonstration only and should never be used for live trading or financial decision-making. Always consult a certified, licensed financial advisor before making actual investments.
