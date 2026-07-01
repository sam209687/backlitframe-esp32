"""
logger.py
Central logging setup. Writes to logs/app.log and also to console.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

_configured = False


def get_logger(name: str = "smartshowroom") -> logging.Logger:
    global _configured
    logger = logging.getLogger(name)

    if not _configured:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )

        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=2_000_000, backupCount=5
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        _configured = True

    return logger
