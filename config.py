"""
Configuration settings for the Investment Agent application.
"""

# OpenAI Model Configuration
DEFAULT_MODEL = "gpt-4o"  # Default OpenAI model to use
MODEL_OPTIONS = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]

# Analysis Configuration
DEFAULT_ANALYSIS_DAYS = 30  # Default number of days for analysis
MAX_STOCKS_TO_COMPARE = 5  # Maximum number of stocks to compare at once

# UI Configuration
PAGE_TITLE = "AI Investment Agent"
PAGE_ICON = "📈"
LAYOUT = "wide"

# API Configuration
API_TIMEOUT = 30  # Timeout in seconds for API calls
MAX_RETRIES = 3  # Maximum number of retries for failed API calls

# Data Configuration
CACHE_DURATION = 300  # Cache duration in seconds (5 minutes)
HISTORICAL_DATA_PERIODS = ["1D", "5D", "1M", "3M", "6M", "1Y", "2Y", "5Y", "MAX"]

# Analysis Types
ANALYSIS_TYPES = [
    "Quick Comparison",
    "Detailed Analysis",
    "Portfolio Analysis",
    "Trend Analysis",
    "Risk Analysis",
    "Valuation Analysis"
]

# Display Configuration
MAX_HISTORY_ITEMS = 10  # Maximum number of analysis history items to display
CHART_HEIGHT = 500  # Default height for charts
CHART_TEMPLATE = "plotly_white"  # Plotly chart template

# Feature Flags
ENABLE_CHARTS = True
ENABLE_FUNDAMENTALS = True
ENABLE_RECOMMENDATIONS = True
ENABLE_HISTORY = True
DEBUG_MODE = True

