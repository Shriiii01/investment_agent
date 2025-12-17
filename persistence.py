"""
Data persistence utilities for analysis history.
"""

import json
import pickle
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from logger import logger

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

HISTORY_FILE = DATA_DIR / "analysis_history.json"
SETTINGS_FILE = DATA_DIR / "user_settings.json"


def save_analysis_history(history: List[Dict[str, Any]]) -> bool:
    """
    Save analysis history to file.
    
    Args:
        history: List of analysis history entries
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump({
                'history': history,
                'last_updated': datetime.now().isoformat(),
                'count': len(history)
            }, f, indent=2, default=str)
        
        logger.info(f"Saved {len(history)} analysis history entries")
        return True
    except Exception as e:
        logger.error(f"Error saving analysis history: {e}")
        return False


def load_analysis_history() -> List[Dict[str, Any]]:
    """
    Load analysis history from file.
    
    Returns:
        List of analysis history entries
    """
    if not HISTORY_FILE.exists():
        logger.info("No existing history file found")
        return []
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            history = data.get('history', [])
            logger.info(f"Loaded {len(history)} analysis history entries")
            return history
    except Exception as e:
        logger.error(f"Error loading analysis history: {e}")
        return []


def save_user_settings(settings: Dict[str, Any]) -> bool:
    """
    Save user settings to file.
    
    Args:
        settings: Dictionary of user settings
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump({
                'settings': settings,
                'last_updated': datetime.now().isoformat()
            }, f, indent=2)
        
        logger.info("User settings saved")
        return True
    except Exception as e:
        logger.error(f"Error saving user settings: {e}")
        return False


def load_user_settings() -> Dict[str, Any]:
    """
    Load user settings from file.
    
    Returns:
        Dictionary of user settings
    """
    if not SETTINGS_FILE.exists():
        logger.info("No existing settings file found")
        return {}
    
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            settings = data.get('settings', {})
            logger.info("User settings loaded")
            return settings
    except Exception as e:
        logger.error(f"Error loading user settings: {e}")
        return {}


def clear_analysis_history() -> bool:
    """
    Clear all analysis history.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        logger.info("Analysis history cleared")
        return True
    except Exception as e:
        logger.error(f"Error clearing analysis history: {e}")
        return False


def get_history_stats() -> Dict[str, Any]:
    """
    Get statistics about analysis history.
    
    Returns:
        Dictionary with history statistics
    """
    history = load_analysis_history()
    
    if not history:
        return {
            'total_analyses': 0,
            'unique_stocks': set(),
            'analysis_types': {},
            'date_range': None
        }
    
    unique_stocks = set()
    analysis_types = {}
    dates = []
    
    for entry in history:
        # Extract stocks
        stocks_str = entry.get('stocks', '')
        if stocks_str:
            stocks = [s.strip() for s in stocks_str.replace('vs', ',').split(',')]
            unique_stocks.update(stocks)
        
        # Count analysis types
        analysis_type = entry.get('type', 'Unknown')
        analysis_types[analysis_type] = analysis_types.get(analysis_type, 0) + 1
        
        # Collect dates
        timestamp = entry.get('timestamp', '')
        if timestamp:
            dates.append(timestamp)
    
    return {
        'total_analyses': len(history),
        'unique_stocks': sorted(list(unique_stocks)),
        'analysis_types': analysis_types,
        'date_range': {
            'earliest': min(dates) if dates else None,
            'latest': max(dates) if dates else None
        } if dates else None
    }

