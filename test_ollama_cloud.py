import os
import logging
from src.news_ai import fetch_ai_stock_news
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
# Manually simulate cloud base URL to test the key
os.environ["OLLAMA_BASE_URL"] = "https://ollama.com"

print("--- Testing Ollama Cloud API ---")
res = fetch_ai_stock_news("RELIANCE.NS", limit=1)
print("\nResult Tuple:", res)
