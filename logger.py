"""
Logging configuration for the Investment Agent application.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from config import DEBUG_MODE

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logger
logger = logging.getLogger("investment_agent")
logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = LOG_DIR / f"investment_agent_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def log_function_call(func_name: str, **kwargs):
    """Log a function call with its parameters."""
    params = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
    logger.debug(f"Calling {func_name}({params})")


def log_error(error: Exception, context: str = ""):
    """Log an error with context."""
    error_msg = f"Error in {context}: {str(error)}" if context else str(error)
    logger.error(error_msg, exc_info=True)


def log_performance(operation: str, duration: float):
    """Log performance metrics."""
    logger.info(f"Performance: {operation} took {duration:.2f} seconds")


def get_logger(name: str = None):
    """Get a logger instance."""
    if name:
        return logging.getLogger(f"investment_agent.{name}")
    return logger
