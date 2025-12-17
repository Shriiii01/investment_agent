"""
Custom exceptions for the Investment Agent application.
"""


class InvestmentAgentError(Exception):
    """Base exception for Investment Agent."""
    pass


class InvalidStockSymbolError(InvestmentAgentError):
    """Raised when an invalid stock symbol is provided."""
    pass


class APIError(InvestmentAgentError):
    """Raised when an API call fails."""
    pass


class DataFetchError(InvestmentAgentError):
    """Raised when data cannot be fetched."""
    pass


class CacheError(InvestmentAgentError):
    """Raised when cache operations fail."""
    pass


class AnalysisError(InvestmentAgentError):
    """Raised when analysis fails."""
    pass


class ConfigurationError(InvestmentAgentError):
    """Raised when configuration is invalid."""
    pass

