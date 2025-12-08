# API Documentation

## Agent API

The Investment Agent uses the Agno framework to interact with OpenAI and YFinance.

### Initialization

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)]
)
```

### Running Queries

```python
response = agent.run("Compare AAPL and MSFT")
print(response.content)
```

## Utility Functions

See `utils.py` for helper functions like `validate_stock_symbol()` and `format_stock_symbol()`.

