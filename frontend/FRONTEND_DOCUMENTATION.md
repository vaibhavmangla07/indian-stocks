# Frontend Documentation (Interview Guide)

## 1. What the Frontend Does

The frontend is a Streamlit UI layer that:

- Orchestrates user navigation
- Triggers backend calls based on user inputs
- Formats and presents market data as metrics/charts/cards
- Handles user interaction flows with minimal latency

Main entrypoint: frontend/app.py
Feature modules: frontend/views/home.py, stock_news.py, stock_detail.py, about.py, contact.py

## 2. Routing and Composition

frontend/app.py is intentionally small:

1. Sets page config
2. Applies global CSS for branding
3. Shows top menu (Home, Stock News, Stock Detail, About, Contact Us)
4. Calls the matching render_* function from views modules

Why this design:

- Cleaner code ownership by feature
- Easier onboarding for new developers
- Lower merge conflicts because features are isolated in separate files

## 3. Home View Deep Dive

File: frontend/views/home.py

Responsibilities:

- Show market overview metrics for indices
- Provide stock + period controls in main content area
- Render quick KPI metrics (current, average, max, low, volatility)
- Show chart tabs for price action and volume
- Show ML forecast tab using backend predictions

Interview explanation:

"The Home view is a dashboard-style orchestration layer. It does not own data retrieval logic; it delegates to backend functions and only handles interaction and rendering."

## 4. Stock News View Deep Dive

File: frontend/views/stock_news.py

Responsibilities:

- Stock selector UI
- Loading state while fetching
- Ordered list of headline cards with links and metadata
- User-friendly no-data/empty-state messaging

Interview explanation:

"This page is optimized for quick context gathering. The backend returns normalized, simplified items and frontend focuses on readability and trust cues (source and timestamp)."

## 5. Stock Detail View Deep Dive

File: frontend/views/stock_detail.py

Responsibilities:

- Stock selector and normalized ticker path
- Fundamentals card UI with polished styling
- Numeric format handling for readability (percent, decimal, market cap)
- Shareholding pie chart rendering

Interview explanation:

"We designed this page to look closer to trading-app style fundamentals panels while keeping the data path provider-agnostic through backend wrappers."

## 6. About and Contact Views

about.py:

- Product narrative and feature summary
- Consistent Stocksy branding

contact.py:

- Form validation
- Writes message to timestamp-based folder in messages/
- User success/failure feedback

Interview explanation:

"About improves product clarity, while Contact provides a lightweight persistence flow without introducing a separate database."

## 7. State and UX Patterns

- Uses Streamlit widgets and built-in state behavior
- Uses spinners for user feedback during I/O
- Uses success/warning/info messages for transparent outcomes
- Uses tab and column layouts for high information density

## 8. Frontend Performance Notes

- Delegates caching to backend layer where data functions are annotated
- Avoids expensive recomputation inside UI loops
- Keeps large data table hidden in expandable section

## 9. Common Interview Questions and Answers

Q: Why split app.py into multiple files?
A: Scalability and maintainability. Single-file Streamlit apps become hard to debug and review once they cross a few hundred lines.

Q: How do you keep UI and business logic separate?
A: UI files only orchestrate rendering and user flow. Data fetching and transformation are in backend modules.

Q: How do you handle empty or partial data?
A: Use explicit fallback rendering, no-data warnings, and formatting helpers to avoid broken or unreadable UI.

Q: How is mobile/readability handled?
A: Use column layouts carefully, card-style sections, and concise metric labels; critical values are formatted for quick scanning.
