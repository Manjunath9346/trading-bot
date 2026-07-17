import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")

# Log format
FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def setup_logging(console_level=logging.INFO, file_level=logging.DEBUG):
    """
    Configure root logger with console and rotating file handlers.

    Args:
        console_level: Logging level for console output.
        file_level: Logging level for file output.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture everything

    # Remove any existing handlers to avoid duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(FORMATTER)
    root_logger.addHandler(console_handler)

    # File handler with rotation (max 5 MB, keep 3 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(FORMATTER)
    root_logger.addHandler(file_handler)