import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure the logs directory exists
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create a logger
logger = logging.getLogger("sdk_logger")
logger.setLevel(logging.DEBUG)

# Console handler for info and error
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_format)

# File handler for all logs
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "app.log"), maxBytes=5 * 1024 * 1024, backupCount=3
)
file_handler.setLevel(logging.WARNING)
file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_format)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
