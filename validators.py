"""
Data validation utilities for the Investment Agent application.
"""

import re
from typing import List, Optional, Tuple
from exceptions import InvalidStockSymbolError, ConfigurationError
from logger import get_logger

logger = get_logger("validators")


def validate_symbol_format(symbol: str) -> bool:
    """
    Validate stock symbol format (basic format check).
    
    Args:
        symbol: Stock symbol to validate
        
    Returns:
        True if format is valid
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Stock symbols are typically 1-5 uppercase letters, sometimes with dots or hyphens
    pattern = r'^[A-Z]{1,5}(\.[A-Z]+)?(-[A-Z]+)?$'
    return bool(re.match(pattern, symbol.upper()))


def validate_api_key(api_key: str) -> bool:
    """
    Validate OpenAI API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if format appears valid
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # OpenAI API keys typically start with 'sk-' and are 51 characters long
    return api_key.startswith('sk-') and len(api_key) >= 20


def validate_time_period(period: str) -> bool:
    """
    Validate time period string.
    
    Args:
        period: Time period string (e.g., "1D", "1Y", "MAX")
        
    Returns:
        True if valid
    """
    valid_periods = ["1D", "5D", "1M", "3M", "6M", "1Y", "2Y", "5Y", "MAX"]
    return period.upper() in valid_periods


def validate_stock_list(stocks: List[str], max_stocks: int = 5) -> Tuple[bool, Optional[str]]:
    """
    Validate a list of stock symbols.
    
    Args:
        stocks: List of stock symbols
        max_stocks: Maximum number of stocks allowed
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not stocks:
        return False, "No stocks provided"
    
    if len(stocks) > max_stocks:
        return False, f"Maximum {max_stocks} stocks allowed"
    
    for stock in stocks:
        if not validate_symbol_format(stock):
            return False, f"Invalid stock symbol format: {stock}"
    
    return True, None


def sanitize_input(input_str: str, max_length: int = 100) -> str:
    """
    Sanitize user input.
    
    Args:
        input_str: Input string to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not isinstance(input_str, str):
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = input_str.strip()
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        logger.warning(f"Input truncated to {max_length} characters")
    
    return sanitized


def validate_analysis_type(analysis_type: str) -> bool:
    """
    Validate analysis type.
    
    Args:
        analysis_type: Analysis type string
        
    Returns:
        True if valid
    """
    from config import ANALYSIS_TYPES
    return analysis_type in ANALYSIS_TYPES


def validate_numeric_range(value: float, min_val: float, max_val: float) -> bool:
    """
    Validate if a numeric value is within a range.
    
    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        True if within range
    """
    try:
        num_value = float(value)
        return min_val <= num_value <= max_val
    except (ValueError, TypeError):
        return False

