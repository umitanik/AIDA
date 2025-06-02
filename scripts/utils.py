"""
Utility functions for AI Documentation Assistant.
Handles logging, error handling, and other helper tasks.
"""

import logging


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


def log_message(message, level="info"):
    """
    Logs a message with the specified level.

    Args:
        message (str): The message to log.
        level (str): The log level ("info", "error", "warning").
    """
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)