# 📓 Stocksy Notebook Documentation

The `notebook/` directory serves as the R&D (Research & Development) workspace for Stocksy. It contains Jupyter Notebooks utilized for initial exploratory data analysis, algorithm prototyping, and machine learning model training before logic is formalized and abstracted into the `src/` backend.

---

## 1. Directory Structure (`notebook/`)

```plaintext
notebook/
├── eda.ipynb              # Deep dive visual analytics of Indian Equities
├── train_model.ipynb      # ML feature engineering and Ridge model serialization
├── ai.ipynb               # Prompt engineering & payload tuning for local LLMs
└── stock_news.ipynb       # Scraping experiments and data-source validation
```

---

## 2. Notebook Summaries & Use Cases

### A. `eda.ipynb` (Exploratory Data Analysis)
This is the data science exploration notebook specifically targeting National Stock Exchange (`.NS`) datasets via `yfinance`. 

**Core Objectives:**
- **Distribution Analysis**: Mapping daily returns to define standard deviations and spot market anomalies (tail risks).
- **Cumulative Returns**: Visualizing long-term asset growth to contextualize multi-year stock performance.
- **Rolling Volatility**: Plotting 20-day and 50-day rolling standard deviations to identify historically turbulent market periods.
- **Seasonality & Holding Patterns**: Developing visual intuition around monthly trading volume spikes and institutional shareholding data patterns.
- *Status:* Contains rendered data-visualization outputs (Matplotlib/Seaborn/Plotly).

### B. `train_model.ipynb` (Machine Learning Pipeline)
This notebook acts as the factory for the Machine Learning models deployed in the live application.

**Core Objectives:**
- **Feature Engineering**: Formulates the primary predictors used in the live backend—specifically, taking basic `Close` sequences and generating `SMA_20` (Short Moving Average), `SMA_50` (Long Moving Average), and `Volatility` metrics.
- **Data Splitting**: Fragments training and testing arrays natively using `scikit-learn`'s `train_test_split`.
- **Model Training**: Initiates a `sklearn.linear_model.Ridge` regression array configured to minimize overfitting on noisy financial data.
- **Serialization**: Executes `joblib.dump()` to construct `model_short_term.pkl` and `model_long_term.pkl`. These `.pkl` files are ported directly to the root `model/` directory for consumption by the Streamlit application.

### C. `ai.ipynb` (LLM Prototyping)
A standalone sandbox dedicated strictly to testing Ollama inference routing.

**Core Objectives:**
- **Connection Validation**: Testing initial HTTP `POST` protocols against `http://localhost:11434/api/generate`.
- **System Prompt Tuning**: Establishing the initial JSON schema requirements and identifying prompt weaknesses (e.g., stopping the LLM from outputting unparsed markdown blobs alongside required JSON variables).
- *Status:* Experimental sandbox. Not actively utilized by the runtime application but acts as a regression-test environment if prompt syntax breaks in the future.

### D. `stock_news.ipynb` (News Scraping Sandbox)
An environment dedicated to parsing open-web financial news sources to supply context logic.

**Core Objectives:**
- **Data Mapping**: Initially utilized to test `yfinance` native news arrays and reverse-engineer Google News RSS structures.
- **Summarization Hooks**: Evaluates text body extraction (scraping payloads via `BeautifulSoup`) to identify which components actually provide valuable analysis content for the local LLM to digest.

---

## 3. Best Practices for Modifying Notebooks

1. **Avoid Hardcoding Secrets**: Do not store private API keys locally inside these notebooks. If external API integrations are tested, load them via `python-dotenv`.
2. **Environment Synchronization**: Ensure that `pandas`, `scikit-learn`, and `yfinance` versions within your notebook environment mirror the exact versions requested in the central `requirements.txt` to prevent serialization bugs when moving `.pkl` files to production.
