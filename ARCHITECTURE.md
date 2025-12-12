# Architecture

## Overview

The Investment Agent is built using Streamlit for the frontend and the Agno framework for AI agent capabilities.

## Components

### Frontend (Streamlit)
- `agent.py`: Main application entry point
- Provides user interface for stock comparison
- Handles user input and displays results

### Backend (Agno)
- AI agent powered by OpenAI GPT-4o
- YFinance tools for stock data retrieval
- Processes queries and generates reports

### Utilities
- `utils.py`: Helper functions for validation
- `config.py`: Configuration settings

## Data Flow

1. User enters stock symbols
2. Agent queries YFinance for stock data
3. GPT-4o analyzes the data
4. Formatted report displayed to user

