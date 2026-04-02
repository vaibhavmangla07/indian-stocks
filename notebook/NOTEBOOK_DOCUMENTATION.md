# Notebook Documentation (Interview Guide)

## 1. Notebook Folder Purpose

The notebook folder is used for experimentation and model workflow support:

- Model training and iteration
- Feature engineering experiments
- Ad hoc data validation
- Reproducible analysis steps before productionizing code

Key notebooks:

- notebook/train_model.ipynb
- notebook/stock_news.ipynb

## 2. train_model.ipynb (Typical Role)

Expected responsibilities:

1. Load historical stock data
2. Engineer features (momentum/volatility style)
3. Train regression models for target horizons
4. Validate model behavior
5. Export serialized model artifacts used by backend

Artifacts consumed later by backend/data_manager.py in predict_horizons().

Interview explanation:

"Notebook training is used as an offline ML workflow. Inference is moved to backend functions to keep runtime path stable and fast for users."

## 3. stock_news.ipynb (Typical Role)

Expected responsibilities:

1. Prototype ticker normalization logic
2. Test yfinance news payload structure
3. Validate sorting and field extraction for headline rendering

Interview explanation:

"News notebook acted as a sandbox to harden parsing logic before integrating into backend/news_ai.py."

## 4. Engineering Boundary: Notebook vs App Code

Notebook should do:

- Experiments and one-off analysis
- Model iteration and validation

Application code should do:

- Stable, reusable functions
- Error-handled production paths
- UI-ready outputs

This separation improves reliability and deployment confidence.

## 5. Reproducibility Notes

- Use pinned dependencies from requirements.txt
- Keep cell execution order logical
- Save model outputs to known paths referenced by backend
- Move mature logic from notebook to backend/frontend modules

## 6. Interview Talking Points

Q: Why keep notebooks if code exists in modules?
A: Notebooks are best for exploration and rapid iteration. Modules are best for production behavior.

Q: How do you prevent notebook drift?
A: Once logic stabilizes, migrate it to backend and keep notebook as documented experiment history.

Q: How does notebook work connect to the app?
A: Model artifacts and validated logic are integrated into backend functions consumed by the Streamlit UI.
