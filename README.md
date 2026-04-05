# Stocksy

Stocksy is a Streamlit app for Indian stock analysis. It focuses on live market data, fundamentals, news, and lightweight forecasting support using pre-trained models stored in the project.

## What the app does

- Shows live market indices for NIFTY 50, SENSEX, and BANK NIFTY
- Lets you explore 60+ popular Indian stocks
- Displays historical price charts, return trends, and volatility
- Shows stock fundamentals such as market cap, book value, P/E, and more
- Fetches stock news and AI-style summaries through the shared news pipeline
- Provides a contact form that stores messages locally

## Project layout

```text
indian-stocks-project/
├── frontend/
│   ├── app.py
│   └── views/
├── src/
│   ├── config.py
│   ├── data_manager.py
│   ├── exception.py
│   ├── logger.py
│   └── news_ai.py
├── notebook/
│   ├── ai.ipynb
│   ├── eda.ipynb
│   ├── stock_news.ipynb
│   └── train_model.ipynb
├── model/
│   ├── model_short_term.pkl
│   └── model_long_term.pkl
├── messages/
├── logs/
├── Dockerfile
├── requirements.txt
├── run.txt
└── README.md
```

## Core files

- [frontend/app.py](frontend/app.py): main Streamlit router
- [src/data_manager.py](src/data_manager.py): live market data, fundamentals, and prediction helper
- [src/news_ai.py](src/news_ai.py): stock news fetcher plus Ollama summary fallback
- [src/config.py](src/config.py): app constants, stock lists, model paths, and cache settings
- [src/logger.py](src/logger.py): logging configuration

## Requirements

- Python 3.11+
- pip
- Internet access for yfinance and news lookup
- Optional: Ollama running locally if you want AI summaries for stock news

## Environment variables

Create a `.env` file if you want to use Ollama for AI summaries:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:270m
```

If Ollama is unavailable, the stock news page falls back to raw headlines.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run frontend/app.py --server.port=8501
```

Open:

```text
http://localhost:8501
```

## Docker

Build and run the container:

```bash
docker build -t stocksy:latest .

docker run --rm -p 8501:8501 \
  --env-file .env \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=gemma3:270m \
  stocksy:latest
```

On macOS, `host.docker.internal` lets the container reach Ollama on your host machine.

## Notebook files

- `notebook/eda.ipynb`: quick exploratory analysis
- `notebook/stock_news.ipynb`: simple news fetcher using the shared news pipeline
- `notebook/ai.ipynb`: Ollama-based AI stock news notebook
- `notebook/train_model.ipynb`: model training notebook that saves `.pkl` files into `model/`

## Model files

The app loads these files from `model/`:

- `model/model_short_term.pkl`
- `model/model_long_term.pkl`

## Deployment options

Recommended options for this project:

1. Render for the Streamlit app in a container or Python web service
2. Streamlit Community Cloud for the quickest demo deployment
3. Any Docker-compatible platform if you want full control

## Troubleshooting

- If the app does not start, confirm port 8501 is free or change the port.
- If news summaries fail, make sure Ollama is running and the model is installed.
- If model-based predictions are missing, confirm the `.pkl` files exist in `model/`.
- If charts or data are blank, check your network connection.

## Notes

- The app is for educational and analysis use only.
- It is not financial advice.
- Contact messages are stored locally in `messages/`.

## Author

Vaibhav Mangla
