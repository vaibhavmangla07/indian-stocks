# Backend Documentation

## 1. What Backend Does
Backend is the main logic layer of this project.

It does four important jobs:
1. Fetch market/index data
2. Fetch stock-level data and fundamentals
3. Run model-based forecast logic
4. Fetch news and optionally create AI summaries

Main files:
- backend/data_manager.py
- backend/news_ai.py

## 2. File: backend/data_manager.py

### A) fetch_indices()
Purpose:
- Gets latest values for NIFTY 50, SENSEX, and BANK NIFTY

Output format:
- Dictionary with index name as key
- Value contains price, day change, and day change percent

Notes:
- If API call fails for any index, it returns None for that index (no app crash)

### B) fetch_data(ticker, period)
Purpose:
- Gets historical stock data from yfinance

Input:
- ticker like RELIANCE.NS
- period like 1mo, 3mo, 1y

Output:
- Clean DataFrame with OHLCV columns
- Returns None if no data is found

### C) predict_horizons(df)
Purpose:
- Creates short-term and long-term predicted prices

How it works:
1. Check minimum rows (ML_MIN_DATA_POINTS)
2. Load 2 model files
3. Create technical features:
   - Mom_5d
   - Mom_20d
   - Mom_60d
   - Volatility_20d
4. Predict return for short and long horizon
5. Convert return to predicted price

Model files used:
- notebook/model_short_term.pkl
- notebook/model_long_term.pkl

### D) fetch_stock_fundamentals(ticker)
Purpose:
- Fetches important company details for stock detail page

Typical fields returned:
- pe_ratio
- book_value
- year_return
- sector
- market_cap
- dividend_yield

### E) fetch_shareholding_pattern(ticker)
Purpose:
- Returns shareholding split shown in frontend pie chart

Current state:
- Uses configured mock split from src/config.py

## 3. File: backend/news_ai.py

### A) fetch_stock_news(stock_query, limit)
Purpose:
- Fetch latest stock news without AI summary

Source priority:
1. Google News RSS
2. yfinance fallback

Output:
- normalized ticker
- list of news items (title, source, url, published_at)

### B) fetch_ai_stock_news(stock_query, limit, candidate_limit)
Purpose:
- Fetch news and ask Ollama to shortlist/summarize

When AI is available:
- returns used_ai = True
- each item can include summary and category

When AI is unavailable or rate-limited:
- returns used_ai = False
- returns normal latest headlines safely

## 4. Logging and Error Handling
- Uses src.logger logging in all key functions
- Uses StocksyException (alias CustomException) for consistent errors
- Backend follows fail-safe style: return empty/None instead of breaking app flow

## 5. Caching and Performance
- Streamlit cache decorators are used in data functions
- TTL values are controlled from src/config.py
- This reduces repeated API calls and improves page speed

## 6. Why This Backend Design Is Good
1. Simple function-based structure
2. Clear separation between data fetch and UI rendering
3. Easy to debug because logs are added at each stage
4. Easy to extend (new endpoint/function can be added without changing UI heavily)

## 7. Quick Verification Commands
- Syntax check:
  - python -m compileall backend
- Manual smoke test:
  - import and run fetch_indices(), fetch_data(), fetch_stock_news()
