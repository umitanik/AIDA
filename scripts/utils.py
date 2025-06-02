"""
Utility functions for AI Documentation Assistant.
Handles logging, error handling, and other helper tasks.
"""

import logging
import re


def setup_logging():
    """
    Sets up logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()

# İlerleme durumunu takip etmek için global değişkenler
current_progress = 0
current_url = ""
indexing_status = ""


def log_message(message, level="info"):
    """
    Logs a message with the specified level.

    Args:
        message (str): The message to log.
        level (str): The log level ("info", "error", "warning").
    """
    global current_progress, current_url, indexing_status

    # İlerleme yüzdesini kontrol et
    progress_match = re.search(r"Progress: (\d+\.\d+)%", message)
    if progress_match:
        current_progress = float(progress_match.group(1)) / 100

    # İndekslenen URL'yi kontrol et
    url_match = re.search(r"Indexing \d+/\d+: (.+)", message)
    if url_match:
        current_url = url_match.group(1)

    # Genel durum mesajlarını kaydet
    indexing_status = message

    # Normal loglama
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)


def get_indexing_progress():
    """
    Returns the current indexing progress.

    Returns:
        tuple: (progress_percentage, current_url, status_message)
    """
    return current_progress, current_url, indexing_status
