"""
Utility functions for the Investment Agent application.
"""

import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime
from exceptions import DataFetchError
from cache import cache_manager
from logger import get_logger

logger = get_logger("utils")


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
    
    # Check cache first
    cache_key = f"validate_{symbol}"
    cached_result = cache_manager.get(cache_key)
    if cached_result is not None:
        return cached_result
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        # Check if we got valid data (not empty dict)
        is_valid = info is not None and len(info) > 0 and 'symbol' in info
        cache_manager.set(cache_key, is_valid)
        return is_valid
    except Exception as e:
        logger.debug(f"Validation error for {symbol}: {str(e)}")
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


def get_stock_info(symbol: str, use_cache: bool = True) -> dict:
    """
    Get comprehensive stock information.
    
    Args:
        symbol: Stock ticker symbol
        use_cache: Whether to use cached data
        
    Returns:
        Dictionary containing stock information
    """
    cache_key = f"stock_info_{symbol}"
    
    if use_cache:
        cached_info = cache_manager.get(cache_key)
        if cached_info is not None:
            logger.debug(f"Using cached stock info for {symbol}")
            return cached_info
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        if use_cache and info:
            cache_manager.set(cache_key, info)
        
        return info
    except Exception as e:
        error_msg = f"Error fetching stock info for {symbol}: {str(e)}"
        logger.error(error_msg)
        raise DataFetchError(error_msg) from e


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


def calculate_volatility(hist_data: pd.DataFrame, period: int = 30) -> float:
    """
    Calculate volatility (standard deviation of returns) for a stock.
    
    Args:
        hist_data: Historical price data DataFrame
        period: Number of days for calculation
        
    Returns:
        Volatility as a percentage
    """
    if hist_data.empty or len(hist_data) < 2:
        return 0.0
    
    try:
        # Calculate daily returns
        returns = hist_data['Close'].pct_change().dropna()
        
        # Use last N days if available
        if len(returns) > period:
            returns = returns.tail(period)
        
        # Calculate annualized volatility
        volatility = returns.std() * (252 ** 0.5) * 100  # Annualized, as percentage
        return round(volatility, 2)
    except Exception as e:
        logger.error(f"Error calculating volatility: {str(e)}")
        return 0.0


def calculate_sharpe_ratio(hist_data: pd.DataFrame, risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe ratio for a stock.
    
    Args:
        hist_data: Historical price data DataFrame
        risk_free_rate: Risk-free rate (default 2%)
        
    Returns:
        Sharpe ratio
    """
    if hist_data.empty or len(hist_data) < 2:
        return 0.0
    
    try:
        # Calculate daily returns
        returns = hist_data['Close'].pct_change().dropna()
        
        if len(returns) == 0:
            return 0.0
        
        # Calculate excess returns
        excess_returns = returns - (risk_free_rate / 252)
        
        # Calculate Sharpe ratio
        if excess_returns.std() == 0:
            return 0.0
        
        sharpe = (excess_returns.mean() / excess_returns.std()) * (252 ** 0.5)
        return round(sharpe, 2)
    except Exception as e:
        logger.error(f"Error calculating Sharpe ratio: {str(e)}")
        return 0.0


def calculate_rsi(hist_data: pd.DataFrame, period: int = 14) -> float:
    """
    Calculate Relative Strength Index (RSI) for a stock.
    
    Args:
        hist_data: Historical price data DataFrame
        period: Period for RSI calculation (default 14)
        
    Returns:
        RSI value (0-100)
    """
    if hist_data.empty or len(hist_data) < period + 1:
        return 50.0  # Neutral RSI
    
    try:
        delta = hist_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        if loss.iloc[-1] == 0:
            return 100.0
        
        rs = gain.iloc[-1] / loss.iloc[-1]
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)
    except Exception as e:
        logger.error(f"Error calculating RSI: {str(e)}")
        return 50.0


def get_technical_indicators(symbol: str, period: str = "6mo") -> Dict[str, float]:
    """
    Get technical indicators for a stock.
    
    Args:
        symbol: Stock ticker symbol
        period: Time period for historical data
        
    Returns:
        Dictionary with technical indicators
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return {}
        
        indicators = {
            'volatility': calculate_volatility(hist),
            'sharpe_ratio': calculate_sharpe_ratio(hist),
            'rsi': calculate_rsi(hist),
            'current_price': float(hist['Close'].iloc[-1]),
            'price_change_pct': calculate_percentage_change(
                hist['Close'].iloc[0],
                hist['Close'].iloc[-1]
            )
        }
        
        return indicators
    except Exception as e:
        logger.error(f"Error getting technical indicators for {symbol}: {str(e)}")
        return {}


def compare_stocks_metrics(stocks: List[str]) -> pd.DataFrame:
    """
    Compare multiple stocks across key metrics.
    
    Args:
        stocks: List of stock symbols
        
    Returns:
        DataFrame with comparison metrics
    """
    comparison_data = []
    
    for symbol in stocks:
        try:
            info = get_stock_info(symbol)
            indicators = get_technical_indicators(symbol)
            
            stock_data = {
                'Symbol': symbol,
                'Current Price': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                'Market Cap': info.get('marketCap', 'N/A'),
                'P/E Ratio': info.get('trailingPE', 'N/A'),
                'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else 'N/A',
                'Beta': info.get('beta', 'N/A'),
                'Volatility': indicators.get('volatility', 'N/A'),
                'RSI': indicators.get('rsi', 'N/A'),
                'Risk Score': calculate_risk_score(symbol)
            }
            
            comparison_data.append(stock_data)
        except Exception as e:
            logger.error(f"Error comparing stock {symbol}: {str(e)}")
            continue
    
    return pd.DataFrame(comparison_data)


def normalize_stock_data(hist_data: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize stock price data to start at 100 for easier comparison.
    
    Args:
        hist_data: Historical price data DataFrame
        
    Returns:
        Normalized DataFrame
    """
    if hist_data.empty:
        return hist_data
    
    try:
        normalized = hist_data.copy()
        first_price = normalized['Close'].iloc[0]
        normalized['Close'] = (normalized['Close'] / first_price) * 100
        return normalized
    except Exception as e:
        logger.error(f"Error normalizing stock data: {str(e)}")
        return hist_data


def get_stock_summary(symbol: str) -> Dict[str, any]:
    """
    Get a comprehensive summary for a stock.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary with stock summary
    """
    try:
        info = get_stock_info(symbol)
        indicators = get_technical_indicators(symbol)
        
        summary = {
            'symbol': symbol,
            'name': info.get('longName', info.get('shortName', 'N/A')),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'current_price': info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
            'market_cap': format_currency(info.get('marketCap')),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'dividend_yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else 'N/A',
            'beta': info.get('beta', 'N/A'),
            '52_week_high': format_currency(info.get('fiftyTwoWeekHigh')),
            '52_week_low': format_currency(info.get('fiftyTwoWeekLow')),
            'volatility': indicators.get('volatility', 'N/A'),
            'rsi': indicators.get('rsi', 'N/A'),
            'risk_score': calculate_risk_score(symbol),
            'description': info.get('longBusinessSummary', 'N/A')[:200] + '...' if info.get('longBusinessSummary') else 'N/A'
        }
        
        return summary
    except Exception as e:
        logger.error(f"Error getting stock summary for {symbol}: {str(e)}")
        return {'error': str(e)}

