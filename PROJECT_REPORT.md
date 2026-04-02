# Stocksy Project Report

## 1. Objective

Build a single application for Indian stock market analysis that combines:

- Market snapshot (indices)
- Stock-level technical view
- Fundamentals and contextual data
- News feed
- ML forecast assistance

## 2. Final Scope Delivered

- Modular Streamlit frontend with dedicated view files
- Backend service layer for data retrieval and transformation
- News fetch pipeline with ticker normalization and clean output mapping
- Fundamentals view with improved display formatting
- Shareholding visualization via pie chart
- Contact form message persistence

## 3. Architecture

- Presentation layer: frontend/app.py and frontend/views/*.py
- Logic/data layer: backend/data_manager.py, backend/news_ai.py
- Model artifacts/workflow: notebook/ area
- Persistence: local folders for messages and optional CSV snapshots

## 4. Key Functional Flows

### Home flow

1. Fetch indices
2. Select stock + period
3. Retrieve historical OHLCV
4. Render KPIs and charts
5. Generate forecast outputs (if model conditions are satisfied)

### Stock News flow

1. Normalize ticker
2. Query Yahoo Finance news
3. Sort by latest publish time
4. Render top 10 with source and links

### Stock Detail flow

1. Normalize ticker
2. Fetch fundamentals from yfinance info/fast_info and fallbacks
3. Compute and format key values for UI
4. Render fundamentals cards and shareholding chart

## 5. Data and Modeling Notes

- Market and fundamentals: yfinance endpoints
- Forecasting: Ridge Regression model artifacts loaded by backend
- Some values rely on provider availability and can be N/A at times

## 6. Validation Executed

- Compiled all active Python modules
- Smoke-tested backend functions for indices, data, fundamentals, and news
- Restarted Streamlit app and validated HTTP response on port 8501

## 7. Current Limitations

- Shareholding data uses a static mocked structure
- Streamlit warnings remain for empty label and deprecated use_container_width usage
- Real-time values are source-dependent and may differ from broker apps

## 8. Recommended Next Improvements

1. Replace deprecated use_container_width usage with width='stretch'
2. Add a non-empty hidden label for top navigation radio for accessibility
3. Integrate a real shareholding data source
4. Add automated tests for backend utility functions
5. Add CI checks for py_compile and linting
