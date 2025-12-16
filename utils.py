"""
Utility functions for the Investment Agent application.
"""

def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate if a stock symbol is in the correct format.
    
    Args:
        symbol: Stock symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not symbol:
        return False
    
    # Basic validation: should be uppercase letters and numbers, 1-5 characters
    symbol = symbol.strip().upper()
    return symbol.isalnum() and 1 <= len(symbol) <= 5


def format_stock_symbol(symbol: str) -> str:
    """
    Format stock symbol to uppercase and remove whitespace.
    
    Args:
        symbol: Stock symbol to format
        
    Returns:
        str: Formatted stock symbol
    """
    return symbol.strip().upper() if symbol else ""

