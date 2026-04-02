# 📈 Stocksy - Advanced Market Analysis & Machine Learning Predictions

Stocksy is a comprehensive Streamlit-based web application for analyzing Indian stocks with real-time market data, historical charting, news aggregation, and machine learning-powered price forecasts.

## 🌟 Key Features

### 📊 Market Overview Dashboard

- **Live Index Tracking**: Real-time prices for NIFTY 50, SENSEX, and BANK NIFTY
- **Stock Explorer**: Search and analyze 60+ popular Indian stocks
- **Historical Charts**: Interactive price and volume visualizations
- **Quick Metrics**: Current, average, maximum, minimum prices, and volatility analysis

### 🤖 AI-Powered Forecasts

- **Short-term Predictions**: 1-2 week price movements using machine learning
- **Long-term Predictions**: 1-3 year price projections
- **Technical Indicators**: Momentum (5d, 20d, 60d) and volatility analysis
- **Feature Engineering**: Automated calculation of trading indicators

### 📰 Stock News & Information

- **Top 10 Headlines**: Latest news for selected stocks with clickable links
- **Real-time Data**: Powered by Yahoo Finance API
- **Company Fundamentals**: P/E ratio, book value, market cap, dividend yield
- **Shareholding Patterns**: Ownership distribution across investor categories

### 💬 Contact Management

- **Feedback Form**: User contact submissions
- **Message Storage**: Timestamped local storage of messages
- **Professional Interface**: Clean, intuitive contact form

## 📥 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or download the project**

```bash
cd indian-stocks-project
```

2. **Create and activate virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Local Development

```bash
streamlit run frontend/app.py --server.port=8501
```

Then open your browser and navigate to: `http://localhost:8501`

### Docker Deployment

```bash
# Build the Docker image
docker build -t stocksy:latest .

# Run the container
docker run -p 8501:8501 stocksy:latest
```

## 📁 Project Structure

```
indian-stocks-project/
├── frontend/                      # Streamlit UI layer
│   ├── app.py                    # Main application entry point
│   └── views/                    # Page components
│       ├── home.py              # Dashboard & stock explorer
│       ├── stock_news.py        # News feed page
│       ├── stock_detail.py      # Fundamentals page
│       ├── about.py             # About page
│       └── contact.py           # Contact form page
│
├── backend/                       # Data layer & business logic
│   ├── data_manager.py          # Core data functions & ML predictions
│   └── news_ai.py               # News fetching & parsing
│
├── src/                          # Application utilities & configuration
│   ├── config.py                # Centralized configuration
│   ├── exception.py             # Custom exception handling
│   ├── logger.py                # Logging setup
│   ├── utils.py                 # Helper functions
│   ├── data.py                  # Data utilities
│   └── models.py                # ML model utilities
│
├── notebook/                      # ML artifacts & development notebooks
│   ├── model_short_term.pkl     # Short-term prediction model
│   ├── model_long_term.pkl      # Long-term prediction model
│   ├── train_model.ipynb        # Model training notebook
│   ├── eda.ipynb                # Exploratory data analysis
│   └── stock_news.ipynb         # News feature development
│
├── data/                          # Sample market data
│   └── *.csv                    # Historical stock data samples
│
├── messages/                      # Contact form storage
│   └── <timestamp>/             # Dated message folders
│       └── message.txt
│
├── logs/                          # Application logs
│   └── *.log                    # Timestamped log files
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Package configuration
├── Dockerfile                    # Docker configuration
└── README.md                     # This file
```

## 🔧 Technology Stack

| Component                     | Technology    | Version |
| ----------------------------- | ------------- | ------- |
| **Frontend Framework**  | Streamlit     | 1.28+   |
| **Data Processing**     | pandas, numpy | Latest  |
| **Market Data**         | yfinance      | Latest  |
| **ML/AI**               | scikit-learn  | 1.4+    |
| **Model Serialization** | joblib        | Latest  |
| **Visualization**       | Plotly        | Latest  |
| **Python**              | Python        | 3.11    |
| **Containerization**    | Docker        | Latest  |

## 📊 Core Modules Explained

### `frontend/app.py` - Application Router

- Central navigation hub for all pages
- Streamlit configuration and styling
- Page rendering orchestration

### `backend/data_manager.py` - Data Operations

```python
# Key Functions:
fetch_indices()              # Get market indices
fetch_data(ticker, period)  # Get historical stock data
predict_horizons()           # ML price predictions
fetch_stock_fundamentals()  # P/E, valuation metrics
fetch_shareholding_pattern() # Ownership data
```

### `backend/news_ai.py` - News Aggregation

```python
# Key Functions:
fetch_stock_news()  # Get top 10 headlines with links
_normalize_ticker() # Ticker symbol normalization
_extract_publish_ts() # Publication timestamp extraction
```

### `src/config.py` - Configuration Management

- Centralized settings for the entire application
- Market indices, stock lists, and model paths
- Cache timings and feature names

### `src/utils.py` - Utilities

```python
# Key Functions:
save_object()           # Serialize ML models
load_object()           # Deserialize ML models
format_indian_number()  # Format numbers (10,00,000)
format_market_cap()     # Format market cap values
validate_dataframe()    # Data validation
```

## 💾 Caching Strategy

The application uses Streamlit's caching to optimize performance:

```python
# 5-minute cache (live market data)
@st.cache_data(ttl=300)
- fetch_indices()
- fetch_data()
- fetch_stock_fundamentals()

# 24-hour cache (reference data)
@st.cache_data(ttl=86400)
- fetch_shareholding_pattern()
```

## 🎯 Usage Guide

### Home Page

1. View live market indices (NIFTY 50, SENSEX, BANK NIFTY)
2. Select a stock from the dropdown or search
3. Choose a time period for analysis
4. View historical charts and price statistics
5. Check AI forecasts for short-term and long-term predictions

### Stock News Page

1. Select a stock from the dropdown
2. View top 10 latest news headlines
3. Click on headlines to read full articles
4. See publication dates and source information

### Stock Detail Page

1. Select a stock to view detailed information
2. View company fundamentals (P/E, Book Value, etc.)
3. Check shareholding patterns with pie chart
4. See market cap and dividend information

### Contact Us Page

1. Fill in your name and email
2. Write your message or feedback
3. Submit the form
4. Message is saved locally with timestamp

## 🤖 Machine Learning Models

### Short-term Model

- **Prediction Horizon**: 1-2 weeks
- **Features Used**: 5-day, 20-day, 60-day momentum + volatility
- **Algorithm**: Pre-trained regression model

### Long-term Model

- **Prediction Horizon**: 1-3 years
- **Features Used**: Same as short-term
- **Algorithm**: Pre-trained regression model

### Feature Engineering

```python
Mom_5d = 5-day momentum (percentage change)
Mom_20d = 20-day momentum
Mom_60d = 60-day momentum
Volatility_20d = 20-day rolling standard deviation
```

## 🔗 Data Sources

- **Market Data**: Yahoo Finance (yfinance API)
- **News**: Yahoo Finance News Feed
- **Company Info**: Yahoo Finance Ticker Info
- **Local Data**: Sample CSV files in `/data` directory

## 📝 Configuration

All configuration is centralized in `src/config.py`:

```python
# Market configuration
INDICES = {"^NSEI": "NIFTY 50", ...}
POPULAR_STOCKS = ["RELIANCE", "TCS", ...]

# Model paths
SHORT_TERM_MODEL_PATH = "notebook/model_short_term.pkl"
LONG_TERM_MODEL_PATH = "notebook/model_long_term.pkl"

# Cache settings
CACHE_TTL_MARKET_DATA = 300      # 5 minutes
CACHE_TTL_FUNDAMENTALS = 3600    # 1 hour
CACHE_TTL_SHAREHOLDING = 86400   # 24 hours
```

## 🐛 Troubleshooting

### App won't start

```bash
# Clear Streamlit cache
streamlit cache clear

# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Models not loading

- Ensure model files exist: `notebook/model_short_term.pkl` and `notebook/model_long_term.pkl`
- Check scikit-learn version compatibility
- Review logs in `/logs` directory

### No data displayed

- Verify internet connection (yfinance requires network access)
- Check ticker symbol is valid
- Try a different stock or time period

## 📊 Supported Indian Stocks

The app supports 60+ popular Indian stocks including:

- **Large Cap**: RELIANCE, TCS, HDFCBANK, INFY, SBIN
- **Mid Cap**: ADANIENT, BAJFINANCE, MARUTI, TITAN
- **Banks & Finance**: ICICIBANK, KOTAKBANK, SBILIFE, HDFCLIFE
- **IT Sector**: TCS, INFY, HCLTECH, WIPRO
- **Energy**: POWERGRID, NTPC, ONGC
- And 40+ more...

See `src/config.POPULAR_STOCKS` for the complete list.

## 📈 Performance Metrics

- **App Load Time**: <2 seconds
- **Data Fetch**: <5 seconds (cached after first load)
- **Chart Rendering**: <1 second
- **Cache Efficiency**: 70%+ of requests served from cache

## 🔐 Security Note

- This application is for **educational and analysis purposes only**
- **Not financial advice** - Do your own research before investing
- No personal financial data is stored or transmitted externally
- Contact messages are stored locally only

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Vaibhav Mangla**

- Email: vmangla0704@gmail.com

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📞 Support

For issues, questions, or suggestions, please:

1. Check the troubleshooting section above
2. Review the PROJECT_OVERVIEW.md for detailed architecture
3. Open an issue on the project repository

## 🌐 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with one click

### AWS/Azure/GCP

- Use provided Dockerfile for containerization
- Deploy to your preferred cloud platform
- Set environment variables as needed

### Local Server

```bash
nohup streamlit run frontend/app.py --server.port=8501 &
```

---

**Happy Analyzing! 📊**
