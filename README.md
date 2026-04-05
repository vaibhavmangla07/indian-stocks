# 📈 Stocksy

> Advanced Market Analysis & Machine Learning Predictions for Indian Stocks

Stocksy is a professional, clean, and comprehensive Streamlit application designed for analyzing Indian stocks on the NSE and BSE. It acts as an all-in-one financial dashboard that combines real-time market data, historical charting, fundamental analysis, AI-curated news, and machine-learning-based price forecasting.

---

## 🌟 Features

- **📊 Live Market Indices:** Real-time ticker tracking for major Indian indices (NIFTY 50, SENSEX, BANK NIFTY).
- **🔎 Stock Explorer:** Deep dive into individual stocks with dynamic period-aware metrics (e.g., 5Y High/Low, Volatility).
- **📉 Historical Charting:** Interactive closing price and volume charts with multiple time-period filters (1mo, 3mo, 6mo, 1y, 2y, 5y).
- **🤖 ML Price Forecast:** Short-term and long-term future price projections powered by Ridge Regression machine learning models.
- **🧠 AI-Curated Stock News:** Fetches the top 10 latest headlines for any stock and uses **Local AI (Ollama)** to generate "Why it matters" market impact analysis and bulleted investor next steps.
- **🏢 Fundamentals Breakdown:** Key financial ratios, market cap insights, PE ratios, and company descriptions powered by Yahoo Finance.

---

## 🏗️ Project Architecture

```plaintext
indian-stocks-project/
├── frontend/                  # Streamlit UI Layer
│   ├── app.py                 # Main application entry point & routing
│   └── views/                 # Individual page modules
│       ├── home.py            # Market overview & Stock explorer
│       ├── stock_detail.py    # Fundamental analysis
│       ├── stock_news.py      # AI-powered news dashboard
│       ├── about.py           # Project details
│       └── contact.py         # Contact form module
├── src/                       # Backend Logic & Integrations
│   ├── data_manager.py        # Core data fetching (yfinance) & ML inference
│   ├── news_ai.py             # Pure Ollama AI integration for news generation
│   ├── config.py              # Centralized tickers, indices, and constants
│   ├── logger.py              # Custom logging configuration
│   └── exception.py           # Custom exception handling
├── model/                     # Pre-trained Machine Learning Models
│   ├── model_short_term.pkl   # Ridge Regression (short horizon: 20 days)
│   └── model_long_term.pkl    # Ridge Regression (long horizon: 60 days)
├── notebook/                  # R&D Jupyter Notebooks
│   ├── eda.ipynb              # Exploratory Data Analysis for Indian Market
│   ├── train_model.ipynb      # ML Model Training Pipeline
│   ├── ai.ipynb               # Prototyping Ollama integration
│   └── stock_news.ipynb       # News scraping prototype sandbox
├── messages/                  # Local storage for Contact Us submissions
├── logs/                      # Log files generated per session
├── docs/                      # (Empty directory reserved for future docs)
├── requirements.txt           # Python package dependencies
├── setup.py                   # Package setup for 'src' module
├── Dockerfile                 # Containerization instructions
├── .env                       # Environment variables (Ollama config)
└── README.md                  # Project documentation
```

---

## 🦾 Data & AI Stack

1. **Market Data**: Sourced live via `yfinance` API (Tickers suffixed with `.NS` for National Stock Exchange of India).
2. **Machine Learning**: `scikit-learn` Ridge Regression models utilizing historical Simple Moving Averages (SMA_20, SMA_50) and Rolling Volatility features.
3. **News Intelligence**: Deep integration with **Ollama** running locally on your hardware. We ping the `gpt-oss:120b-cloud` (or custom configured model) to act as a financial analyst, curating news and providing "Why it matters" statements completely offline and without rate limitations.

---

## 🚀 Getting Started

### Prerequisites

1.  **Python 3.8+**
2.  **Ollama** (for local AI features) installed and running.

### Installation

1. **Clone the repository & navigate to the directory:**

    ```bash
    git clone https://github.com/vaibhavmangla07/indian-stocks.git
    cd indian-stocks-project
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**
    Create a `.env` file in the root directory (or edit the existing one) to configure your local AI:

    ```env
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=gpt-oss:120b-cloud  # Or whichever model you have pulled, e.g., llama3.1
    ```

### Running the App

To start the Streamlit dashboard, run:

```bash
streamlit run frontend/app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 🤖 AI Configuration (Ollama)

Stocksy's **Stock News Intelligence** feature runs entirely locally using Ollama, ensuring privacy and speed.

- To use this feature, ensure the Ollama daemon is running in the background.
- Verify your model string in the `.env` file matches exactly with a model you have installed (`ollama list`).
- If Ollama is unavailable, the application degrades gracefully.

---

## 📈 Machine Learning Details

The project utilizes `scikit-learn` Ridge Regression models (`model_short_term.pkl` and `model_long_term.pkl`) to attempt future price projections based on historical moving averages and volatility features extracted via `yfinance`.

*Note: Models are for educational and structural demonstration purposes only. They do not constitute financial advice.*

---

## 📄 Disclaimer

This project is built for **educational purposes** as a demonstration of integrating Python, Streamlit, Machine Learning, and Local LLMs. It is not intended for live trading or financial decision-making. Always consult a certified financial advisor before making investment decisions.
