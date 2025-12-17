"""
Data processing utilities for stock analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from logger import get_logger

logger = get_logger("data_processor")


def calculate_moving_averages(hist_data: pd.DataFrame, periods: List[int] = [20, 50, 200]) -> pd.DataFrame:
    """
    Calculate moving averages for stock data.
    
    Args:
        hist_data: Historical price data DataFrame
        periods: List of periods for moving averages
        
    Returns:
        DataFrame with moving average columns added
    """
    if hist_data.empty:
        return hist_data
    
    try:
        result = hist_data.copy()
        for period in periods:
            if len(result) >= period:
                result[f'MA_{period}'] = result['Close'].rolling(window=period).mean()
        return result
    except Exception as e:
        logger.error(f"Error calculating moving averages: {str(e)}")
        return hist_data


def detect_support_resistance(hist_data: pd.DataFrame, window: int = 20) -> Dict[str, float]:
    """
    Detect support and resistance levels.
    
    Args:
        hist_data: Historical price data DataFrame
        window: Window size for detection
        
    Returns:
        Dictionary with support and resistance levels
    """
    if hist_data.empty:
        return {'support': None, 'resistance': None}
    
    try:
        recent_data = hist_data.tail(window)
        support = recent_data['Low'].min()
        resistance = recent_data['High'].max()
        
        return {
            'support': float(support),
            'resistance': float(resistance)
        }
    except Exception as e:
        logger.error(f"Error detecting support/resistance: {str(e)}")
        return {'support': None, 'resistance': None}


def calculate_price_targets(current_price: float, support: float, resistance: float) -> Dict[str, float]:
    """
    Calculate price targets based on support and resistance.
    
    Args:
        current_price: Current stock price
        support: Support level
        resistance: Resistance level
        
    Returns:
        Dictionary with price targets
    """
    try:
        range_size = resistance - support
        targets = {
            'conservative_target': current_price + (range_size * 0.1),
            'moderate_target': current_price + (range_size * 0.25),
            'aggressive_target': current_price + (range_size * 0.5),
            'stop_loss': support * 0.95
        }
        return targets
    except Exception as e:
        logger.error(f"Error calculating price targets: {str(e)}")
        return {}


def analyze_trend(hist_data: pd.DataFrame) -> Dict[str, any]:
    """
    Analyze price trend.
    
    Args:
        hist_data: Historical price data DataFrame
        
    Returns:
        Dictionary with trend analysis
    """
    if hist_data.empty or len(hist_data) < 2:
        return {'trend': 'unknown', 'strength': 0}
    
    try:
        # Calculate short-term and long-term trends
        short_period = min(20, len(hist_data) // 2)
        long_period = min(50, len(hist_data))
        
        short_ma = hist_data['Close'].tail(short_period).mean()
        long_ma = hist_data['Close'].tail(long_period).mean()
        current_price = hist_data['Close'].iloc[-1]
        
        # Determine trend
        if current_price > short_ma > long_ma:
            trend = 'bullish'
            strength = min(100, ((current_price - long_ma) / long_ma) * 1000)
        elif current_price < short_ma < long_ma:
            trend = 'bearish'
            strength = min(100, ((long_ma - current_price) / long_ma) * 1000)
        else:
            trend = 'sideways'
            strength = 50
        
        return {
            'trend': trend,
            'strength': round(strength, 2),
            'short_ma': round(short_ma, 2),
            'long_ma': round(long_ma, 2)
        }
    except Exception as e:
        logger.error(f"Error analyzing trend: {str(e)}")
        return {'trend': 'unknown', 'strength': 0}


def calculate_correlation(hist_data1: pd.DataFrame, hist_data2: pd.DataFrame) -> float:
    """
    Calculate correlation between two stocks.
    
    Args:
        hist_data1: Historical data for first stock
        hist_data2: Historical data for second stock
        
    Returns:
        Correlation coefficient (-1 to 1)
    """
    try:
        # Align dates
        common_dates = hist_data1.index.intersection(hist_data2.index)
        
        if len(common_dates) < 2:
            return 0.0
        
        returns1 = hist_data1.loc[common_dates, 'Close'].pct_change().dropna()
        returns2 = hist_data2.loc[common_dates, 'Close'].pct_change().dropna()
        
        # Align returns
        common_returns = pd.concat([returns1, returns2], axis=1).dropna()
        
        if len(common_returns) < 2:
            return 0.0
        
        correlation = common_returns.iloc[:, 0].corr(common_returns.iloc[:, 1])
        return round(correlation, 4) if not np.isnan(correlation) else 0.0
    except Exception as e:
        logger.error(f"Error calculating correlation: {str(e)}")
        return 0.0


def calculate_drawdown(hist_data: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate maximum drawdown.
    
    Args:
        hist_data: Historical price data DataFrame
        
    Returns:
        Dictionary with drawdown metrics
    """
    if hist_data.empty:
        return {'max_drawdown': 0, 'current_drawdown': 0}
    
    try:
        # Calculate running maximum
        running_max = hist_data['Close'].expanding().max()
        
        # Calculate drawdown
        drawdown = (hist_data['Close'] - running_max) / running_max * 100
        
        max_drawdown = drawdown.min()
        current_drawdown = drawdown.iloc[-1]
        
        return {
            'max_drawdown': round(max_drawdown, 2),
            'current_drawdown': round(current_drawdown, 2)
        }
    except Exception as e:
        logger.error(f"Error calculating drawdown: {str(e)}")
        return {'max_drawdown': 0, 'current_drawdown': 0}


def prepare_comparison_data(stock1_data: Dict, stock2_data: Dict) -> pd.DataFrame:
    """
    Prepare data for side-by-side comparison.
    
    Args:
        stock1_data: Data dictionary for first stock
        stock2_data: Data dictionary for second stock
        
    Returns:
        DataFrame ready for display
    """
    try:
        comparison = {
            'Metric': [],
            stock1_data.get('symbol', 'Stock 1'): [],
            stock2_data.get('symbol', 'Stock 2'): []
        }
        
        # Common metrics to compare
        metrics = [
            ('Current Price', 'current_price'),
            ('Market Cap', 'market_cap'),
            ('P/E Ratio', 'pe_ratio'),
            ('Dividend Yield', 'dividend_yield'),
            ('Beta', 'beta'),
            ('Volatility', 'volatility'),
            ('RSI', 'rsi'),
            ('Risk Score', 'risk_score')
        ]
        
        for metric_name, metric_key in metrics:
            comparison['Metric'].append(metric_name)
            comparison[stock1_data.get('symbol', 'Stock 1')].append(
                stock1_data.get(metric_key, 'N/A')
            )
            comparison[stock2_data.get('symbol', 'Stock 2')].append(
                stock2_data.get(metric_key, 'N/A')
            )
        
        return pd.DataFrame(comparison)
    except Exception as e:
        logger.error(f"Error preparing comparison data: {str(e)}")
        return pd.DataFrame()


def aggregate_portfolio_metrics(stocks_data: List[Dict]) -> Dict[str, any]:
    """
    Aggregate metrics for a portfolio of stocks.
    
    Args:
        stocks_data: List of stock data dictionaries
        
    Returns:
        Dictionary with aggregated portfolio metrics
    """
    if not stocks_data:
        return {}
    
    try:
        total_market_cap = 0
        total_pe = 0
        total_beta = 0
        total_risk = 0
        valid_count = 0
        
        for stock_data in stocks_data:
            # Extract numeric values (handle formatted strings)
            market_cap = stock_data.get('market_cap', 0)
            pe = stock_data.get('pe_ratio', 0)
            beta = stock_data.get('beta', 1.0)
            risk = stock_data.get('risk_score', 5.0)
            
            if isinstance(market_cap, (int, float)):
                total_market_cap += market_cap
            if isinstance(pe, (int, float)) and pe > 0:
                total_pe += pe
                valid_count += 1
            if isinstance(beta, (int, float)):
                total_beta += beta
            if isinstance(risk, (int, float)):
                total_risk += risk
        
        avg_pe = total_pe / valid_count if valid_count > 0 else 0
        avg_beta = total_beta / len(stocks_data) if stocks_data else 0
        avg_risk = total_risk / len(stocks_data) if stocks_data else 0
        
        return {
            'total_stocks': len(stocks_data),
            'total_market_cap': total_market_cap,
            'average_pe': round(avg_pe, 2),
            'average_beta': round(avg_beta, 2),
            'average_risk_score': round(avg_risk, 2),
            'portfolio_diversification': 'High' if avg_beta < 1.0 else 'Moderate' if avg_beta < 1.5 else 'Low'
        }
    except Exception as e:
        logger.error(f"Error aggregating portfolio metrics: {str(e)}")
        return {}

