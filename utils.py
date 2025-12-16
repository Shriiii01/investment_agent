"""
Utility functions for the Investment Agent application.
"""

import yfinance as yf
from typing import Optional


def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate if a stock symbol exists and is valid.
    
    Args:
        symbol: Stock ticker symbol to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not symbol or len(symbol) == 0:
        return False
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # Check if we got valid data (not empty dict)
        return info is not None and len(info) > 0 and 'symbol' in info
    except Exception:
        return False


def format_currency(value: Optional[float]) -> str:
    """
    Format a number as currency.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted currency string
    """
    if value is None or value == 'N/A':
        return 'N/A'
    
    try:
        if abs(value) >= 1_000_000_000_000:
            return f"${value/1_000_000_000_000:.2f}T"
        elif abs(value) >= 1_000_000_000:
            return f"${value/1_000_000_000:.2f}B"
        elif abs(value) >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
        elif abs(value) >= 1_000:
            return f"${value/1_000:.2f}K"
        else:
            return f"${value:.2f}"
    except (TypeError, ValueError):
        return str(value)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Starting value
        new_value: Ending value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def get_stock_info(symbol: str) -> dict:
    """
    Get comprehensive stock information.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary containing stock information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info
    except Exception as e:
        return {'error': str(e)}


def calculate_risk_score(symbol: str) -> float:
    """
    Calculate a simple risk score based on beta and volatility.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Risk score from 0-10 (higher = more risky)
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        beta = info.get('beta', 1.0)
        if beta is None:
            beta = 1.0
        
        # Simple risk calculation based on beta
        # Beta > 1.5 = high risk, Beta < 0.5 = low risk
        if beta >= 1.5:
            risk_score = 8.0
        elif beta >= 1.2:
            risk_score = 6.0
        elif beta >= 0.8:
            risk_score = 4.0
        elif beta >= 0.5:
            risk_score = 2.0
        else:
            risk_score = 1.0
        
        return min(risk_score, 10.0)
    except Exception:
        return 5.0  # Default moderate risk


def format_large_number(value: Optional[float]) -> str:
    """
    Format large numbers with appropriate suffixes.
    
    Args:
        value: Number to format
        
    Returns:
        Formatted string
    """
    if value is None:
        return 'N/A'
    
    try:
        abs_value = abs(value)
        if abs_value >= 1_000_000_000_000:
            return f"{value/1_000_000_000_000:.2f}T"
        elif abs_value >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"
        elif abs_value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"
        elif abs_value >= 1_000:
            return f"{value/1_000:.2f}K"
        else:
            return f"{value:.2f}"
    except (TypeError, ValueError):
        return str(value)

