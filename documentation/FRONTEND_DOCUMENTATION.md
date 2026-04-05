# Frontend Documentation

## 1. What Frontend Does
Frontend is built using Streamlit and handles all user interaction.

It allows users to:
1. View live market indices
2. Analyze selected stock with charts and metrics
3. Read stock news
4. View fundamentals and shareholding information
5. Send contact message

Main entry file:
- frontend/app.py

View files:
- frontend/views/home.py
- frontend/views/stock_news.py
- frontend/views/stock_detail.py
- frontend/views/about.py
- frontend/views/contact.py

## 2. Routing and Navigation
In frontend/app.py:
1. Streamlit page config is set
2. Header and menu are rendered
3. Menu selection decides which render function runs

This keeps app.py clean and simple.

## 3. Page-Wise Details

### A) Home Page
File:
- frontend/views/home.py

What user sees:
- Index cards (NIFTY, SENSEX, BANK NIFTY)
- Stock selector
- Time period selector
- Charts and summary metrics
- Forecast output section

Backend calls used:
- fetch_indices()
- fetch_data()
- predict_horizons()

### B) Stock News Page
File:
- frontend/views/stock_news.py

What user sees:
- Stock selector
- Top headlines with links, source, and publish time
- Optional AI summary if Ollama call succeeds

Backend call used:
- fetch_ai_stock_news()

Fallback behavior:
- If Ollama fails or is unavailable, latest headlines are still shown

### C) Stock Detail Page
File:
- frontend/views/stock_detail.py

What user sees:
- Fundamentals cards
- Shareholding pattern chart

Backend calls used:
- fetch_stock_fundamentals()
- fetch_shareholding_pattern()

### D) About Page
File:
- frontend/views/about.py

What user sees:
- Project overview
- Feature highlights
- Tech stack snapshot

Note on model statement:
- "2 Trained Models" means:
  - notebook/model_short_term.pkl
  - notebook/model_long_term.pkl

### E) Contact Page
File:
- frontend/views/contact.py

What user sees:
- Name, email, and message form

What happens on submit:
- Data is saved to messages folder in timestamped subfolder

## 4. Frontend Design Principles
1. Keep UI code in view files only
2. Keep API/data logic in backend files
3. Show clear user feedback (success/warning/info)
4. Avoid heavy processing in frontend

## 5. Common Warnings and Notes
- Streamlit can show label warning if radio label is empty
- This warning does not stop app execution

## 6. Quick Verification
- Run app:
  - streamlit run frontend/app.py
- Compile frontend files:
  - python -m compileall frontend
