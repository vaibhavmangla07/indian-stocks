# 🖥️ Stocksy Frontend Architecture Documentation

The UI layer for Stocksy is built entirely using **Streamlit**, an open-source Python framework for crafting custom machine learning and data science web apps. This document explains the routing logic, state management, and visual construction of the frontend components based in the `frontend/` directory.

---

## 1. Directory Structure (`frontend/`)

```plaintext
frontend/
├── app.py                 # The master router & layout configuration (st.set_page_config)
└── views/                 # Modular page scripts imported by app.py
    ├── about.py           # Static information & project explanation
    ├── contact.py         # Form submission builder via st.form
    ├── home.py            # Primary dashboard: indices, stock explorer, & charting
    ├── stock_detail.py    # Extracts and plots JSON structures from Yahoo Finance 
    └── stock_news.py      # Controls the loading states for AI generation
```

---

## 2. Global Routing & Layout (`app.py`)

`app.py` enforces the global visual standard for the entire application. It acts as the singular entry point.

### Key Behaviors:
- **Environment Pathing**: Modifies `sys.path.append(...)` to ensure the `frontend/` layer can securely import modules from the sister `src/` backend directory without dependency hell.
- **Master UI Config**: Executes `st.set_page_config()` immediately upon mount, forcing `layout="wide"` to afford the charts maximum monitor real estate.
- **Custom CSS Parsing**: Injects `<style>` tags via Streamlit's `st.markdown(unsafe_allow_html=True)` parameter to adjust global header typography and center the radio buttons used for navigation.
- **Navigation Router**: Employs an `st.radio` widget horizontally (`horizontal=True`) masquerading as a minimalist top-level navigation bar. Based on the selected state string, it triggers the execution of modular function wrappers imported from the `views/` directory.

---

## 3. The `views/` Modules

Each view is encapsulated inside a standard `render_` Python function. This ensures page assets are only requested from the backend when the user actively navigates to them, maintaining rapid load times and low memory footprints.

### A. `home.py` (Market Overview & Explorer)
- Consists of a three-tab Layout (`st.tabs`):
  1. **📋 Quick Overview**: Displays 5 column `st.metric` widgets featuring dynamic delta colors (e.g., green for positive change, red for negative) comparing current price against the absolute High/Low of the selected time period.
  2. **📈 Price Action & Volume**: Houses dual `st.line_chart` and `st.bar_chart` components tracking "Close Price" and "Trading Volume".
  3. **🤖 ML Forecast**: Employs `st.spinner` to indicate inference processing overhead, and then dynamically overlays forecasted line trajectories resulting from `src.data_manager.predict_horizons()`.

### B. `stock_detail.py` (Fundamental Analysis)
- Extracts the sprawling `dict` of data from Yahoo Finance and formats it linearly via Streamlit rows.
- **Edge-Case Formatting**: Imports formatting functions (`_format_indian_number`) to natively translate scientific notation into Indian numerical formatting (e.g., Millions into ₹ Crores). 
- Handles the `Empty State` UI natively: if `fundamentals` returns false, renders an `st.warning()`.

### C. `stock_news.py` (AI Intelligence Dashboard)
- Controls the most intensive loading state in the application using `st.status`.
- **Progressive UI Rendering**:
  1. First sets `"Fetching latest headlines from Google News/Yahoo..."`
  2. Updates to `"🤖 Running Ollama AI analysis — picking top headlines..."`
  3. Culminates in `"Analysis complete!"`
- Employs standard markdown to construct tabular data resulting from the Ollama backend hook.

### D. `contact.py` (Local Database Mock)
- Defines a Streamlit Context Manager (`with st.form("contact_form", clear_on_submit=True):`) handling text inputs to prevent reload loops. 
- Connects directly to the OS file system to save forms inside `messages/TIMESTAMP/message.txt`, executing an `st.success()` or `st.error()` notification pipeline.

### E. `about.py` (Project Overview)
- A highly optimized, purely static script running un-cached `st.markdown()` blocks to define the goals and feature set of the application.

---

## 4. State Management & Interaction Handling

- **No `st.session_state` Reliance**: Rather than relying on Streamlit's volatile session state dictionary, Stocksy ties user intent directly to the persistent keys in `selectbox` inputs (e.g. `key="home_stock_select"`). 
- **Memoization as State**: The application substitutes traditional state manipulation with `@st.cache_data`. When a user toggles between tabs or resizes their window (triggering a Streamlit full-page reload script), Python does not re-compute logic; it instantly renders the memoized UI layout.
