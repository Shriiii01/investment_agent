"""
Error handling utilities for better user experience.
"""

import traceback
from typing import Optional, Callable
from functools import wraps
from logger import logger, log_error


class InvestmentAgentError(Exception):
    """Base exception for Investment Agent errors."""
    pass


class StockDataError(InvestmentAgentError):
    """Exception raised when stock data cannot be retrieved."""
    pass


class APIError(InvestmentAgentError):
    """Exception raised when API calls fail."""
    pass


class ValidationError(InvestmentAgentError):
    """Exception raised when validation fails."""
    pass


def handle_errors(context: str = ""):
    """
    Decorator to handle errors gracefully.
    
    Args:
        context: Context description for error logging
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except StockDataError as e:
                logger.error(f"Stock data error in {context or func.__name__}: {e}")
                raise
            except APIError as e:
                logger.error(f"API error in {context or func.__name__}: {e}")
                raise
            except ValidationError as e:
                logger.error(f"Validation error in {context or func.__name__}: {e}")
                raise
            except Exception as e:
                log_error(e, context or func.__name__)
                raise InvestmentAgentError(f"Unexpected error: {str(e)}")
        return wrapper
    return decorator


def get_user_friendly_error_message(error: Exception) -> str:
    """
    Convert technical error messages to user-friendly ones.
    
    Args:
        error: Exception object
        
    Returns:
        User-friendly error message
    """
    error_type = type(error).__name__
    error_message = str(error)
    
    # Map common errors to user-friendly messages
    error_mappings = {
        'StockDataError': "Unable to retrieve stock data. Please check the stock symbol and try again.",
        'APIError': "API request failed. Please check your API key and internet connection.",
        'ValidationError': "Invalid input. Please check your data and try again.",
        'KeyError': "Missing required data. Please try again.",
        'TimeoutError': "Request timed out. Please try again later.",
        'ConnectionError': "Connection error. Please check your internet connection.",
    }
    
    # Check for specific error patterns
    if "API key" in error_message.lower():
        return "Invalid or missing API key. Please check your OpenAI API key in the sidebar."
    
    if "symbol" in error_message.lower() or "ticker" in error_message.lower():
        return "Invalid stock symbol. Please enter a valid ticker symbol (e.g., AAPL, MSFT)."
    
    if "rate limit" in error_message.lower():
        return "API rate limit exceeded. Please wait a moment and try again."
    
    # Return mapped message or generic one
    return error_mappings.get(error_type, f"An error occurred: {error_message}")


def safe_execute(func: Callable, default_return=None, error_message: Optional[str] = None):
    """
    Safely execute a function and return default value on error.
    
    Args:
        func: Function to execute
        default_return: Value to return on error
        error_message: Custom error message
        
    Returns:
        Function result or default_return on error
    """
    try:
        return func()
    except Exception as e:
        log_error(e, func.__name__)
        if error_message:
            logger.warning(error_message)
        return default_return

