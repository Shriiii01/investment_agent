# AI Investment Agent 📈🤖

A powerful, AI-driven investment analysis tool built with Streamlit, Agno, and OpenAI. Compare stocks, analyze fundamentals, and get AI-powered investment insights.

## Features

- 🤖 **AI-Powered Analysis**: Get comprehensive stock comparisons powered by GPT-4
- 📊 **Real-Time Data**: Access live stock prices, fundamentals, and analyst recommendations
- 📈 **Interactive Charts**: Visualize price trends and trading volumes with Plotly
- 💡 **Analyst Recommendations**: View recent analyst ratings and price targets
- 📋 **Fundamental Analysis**: Compare key metrics like P/E ratio, market cap, and more
- 📚 **Analysis History**: Track your previous analyses for reference
- 🎨 **Modern UI**: Beautiful, responsive interface built with Streamlit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shriiii01/investment_agent.git
cd investment_agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run agent.py
```

## Usage

1. **Enter API Key**: Input your OpenAI API key in the sidebar
2. **Select Stocks**: Enter two stock symbols (e.g., AAPL, MSFT)
3. **Choose Analysis Type**: Select from Quick Comparison, Detailed Analysis, Portfolio Analysis, or Trend Analysis
4. **Set Time Period**: Choose the historical data period (1D to MAX)
5. **Analyze**: Click the "Analyze" button to get AI-powered insights

## Features Breakdown

### 🤖 AI Analysis Tab
- Comprehensive stock comparison
- Performance metrics
- Risk assessment
- Investment recommendations
- Key differentiators

### 📈 Charts Tab
- Price comparison over time
- Trading volume analysis
- Performance metrics
- Interactive visualizations

### 📊 Fundamentals Tab
- Side-by-side metric comparison
- P/E ratios, market cap, dividend yield
- Revenue growth and profit margins
- Beta and volatility metrics

### 💡 Recommendations Tab
- Recent analyst recommendations
- Price targets
- Rating changes over time

## Project Structure

```
investment_agent/
├── agent.py              # Main Streamlit application
├── utils.py              # Utility functions
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Dependencies

- `streamlit`: Web application framework
- `agno`: AI agent framework
- `yfinance`: Yahoo Finance data access
- `plotly`: Interactive charts
- `pandas`: Data manipulation

## Configuration

Edit `config.py` to customize:
- Default OpenAI model
- Analysis options
- UI settings
- Feature flags

## API Keys

You'll need an OpenAI API key to use the AI analysis features. Get one at [OpenAI Platform](https://platform.openai.com/).

## Disclaimer

⚠️ **This tool is for informational purposes only and does not constitute financial advice.** Always do your own research and consult with a financial advisor before making investment decisions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Built by Shriiii01

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

