# utils/logger.py
import logging
import os

# Create logs folder
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "automation.log")

# Configure logger
logging.basicConfig(
    level=logging.INFO,  # Use DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),     # Save logs to file
        logging.StreamHandler()            # Also show logs in terminal
    ]
)

def get_logger(name):
    """Returns a logger with the given name"""
    return logging.getLogger(name)
