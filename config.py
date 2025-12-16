"""
Configuration file for Investment Agent
"""

# Default OpenAI model
DEFAULT_MODEL = "gpt-4o"

# Streamlit page config
PAGE_CONFIG = {
    "page_title": "AI Investment Agent",
    "page_icon": "📈",
    "layout": "wide"
}

# Agent instructions
AGENT_INSTRUCTIONS = [
    "Format your response using markdown and use tables to display data where possible.",
    "Provide actionable insights and recommendations.",
    "Include risk assessment in your analysis.",
    "Compare key metrics side-by-side.",
    "Highlight both strengths and weaknesses of each stock."
]

