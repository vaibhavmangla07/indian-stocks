# Notebook Documentation

## 1. Why This Folder Exists
Notebook files are used for experimentation, analysis, and training support.

They help in:
1. Understanding stock data behavior
2. Building and validating ML features
3. Training model artifacts
4. Prototyping news and AI summary logic

Current files:
- notebook/eda.ipynb
- notebook/train_model.ipynb
- notebook/stock_news.ipynb
- notebook/ai.ipynb

## 2. Notebook Details

### A) eda.ipynb
Purpose:
- Exploratory Data Analysis

Typical activities:
- Check price trends
- Check missing values
- Compare stock movement patterns
- Validate basic assumptions before model work

### B) train_model.ipynb
Purpose:
- Train prediction models used by app backend

Feature style used:
- Momentum features
- Volatility feature

Algorithm used:
- Ridge Regression

Final output files:
- notebook/model_short_term.pkl
- notebook/model_long_term.pkl

How app uses these outputs:
- backend/data_manager.py loads these two files in predict_horizons()

### C) stock_news.ipynb
Purpose:
- News parsing and normalization experiments

Typical activities:
- Test news source response format
- Test title/source/url extraction
- Validate sorting and display-friendly structure

### D) ai.ipynb
Purpose:
- Ollama summary experimentation

Needs:
- OLLAMA_BASE_URL and OLLAMA_MODEL in environment

Important note:
- If Ollama server is not running, AI calls fail and no AI summary is returned

## 3. Notebook vs Production Code
Notebooks are not the live serving layer.

Production logic lives in:
- backend/news_ai.py
- backend/data_manager.py
- frontend views

Notebooks are reference and development support.

## 4. Safe Usage Guidelines
1. Use notebooks for experiments only
2. Keep production code changes in .py files
3. Save model artifacts in notebook folder with expected names
4. Re-test backend prediction after any model retraining

## 5. Quick Checks
- Open notebooks:
	- jupyter notebook
- Confirm model files exist:
	- notebook/model_short_term.pkl
	- notebook/model_long_term.pkl
