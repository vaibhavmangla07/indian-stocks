"""Logging configuration for the Stocksy application."""

import logging
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_FILE_PATH = LOG_DIR / LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(),
    ],
    force=True,
)

logger = logging.getLogger("stocksy")
logging.info("Stocksy logging initialized: %s", LOG_FILE_PATH)

if __name__ == "__main__":
    logger.info("Stocksy logging system initialized successfully.")
    logger.info("Log file created at: %s", LOG_FILE_PATH)

