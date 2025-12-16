import streamlit as st
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

# Page configuration
st.set_page_config(
    page_title="AI Investment Agent",
    page_icon="📈",
    layout="wide"
)

st.title("AI Investment Agent 📈🤖")
st.caption("This app allows you to compare the performance of two stocks and generate detailed reports.")

# Sidebar for API key
with st.sidebar:
    st.header("Configuration")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to use the AI agent")
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("1. Enter your OpenAI API key")
    st.markdown("2. Enter two stock symbols")
    st.markdown("3. Get detailed comparison report")

if openai_api_key:
    try:
        assistant = Agent(
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            tools=[
                YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)
            ],
            debug_mode=True,
            description="You are an investment analyst that researches stock prices, analyst recommendations, and stock fundamentals.",
            instructions=[
                "Format your response using markdown and use tables to display data where possible.",
                "Provide actionable insights and recommendations.",
                "Include risk assessment in your analysis."
            ],
        )

        col1, col2 = st.columns(2)
        with col1:
            stock1 = st.text_input("Enter first stock symbol (e.g. AAPL)", value="", placeholder="AAPL")
        with col2:
            stock2 = st.text_input("Enter second stock symbol (e.g. MSFT)", value="", placeholder="MSFT")

        if stock1 and stock2:
            if st.button("Analyze Stocks", type="primary"):
                with st.spinner(f"Analyzing {stock1.upper()} and {stock2.upper()}..."):
                    try:
                        query = f"Compare both the stocks - {stock1.upper()} and {stock2.upper()} and make a detailed report for an investor trying to invest and compare these stocks"
                        response: RunOutput = assistant.run(query, stream=False)
                        st.markdown("## Analysis Report")
                        st.markdown(response.content)
                    except Exception as e:
                        st.error(f"Error analyzing stocks: {str(e)}")
                        st.info("Please check that the stock symbols are valid and try again.")
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        st.info("Please check your API key and try again.")
else:
    st.info("👈 Please enter your OpenAI API key in the sidebar to get started.")