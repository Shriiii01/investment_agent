import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
import plotly.graph_objects as go
import plotly.express as px
from utils import validate_stock_symbol, format_currency, calculate_percentage_change
from config import DEFAULT_MODEL, DEFAULT_ANALYSIS_DAYS

# Page configuration
st.set_page_config(
    page_title="AI Investment Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    openai_api_key = st.text_input(
        "OpenAI API Key", 
        type="password",
        help="Enter your OpenAI API key to enable the AI agent",
        value=st.session_state.get('api_key', '')
    )
    
    if openai_api_key:
        st.session_state.api_key = openai_api_key
        st.session_state.api_key_set = True
        st.success("✅ API Key Set")
    
    st.divider()
    
    st.subheader("📊 Analysis Options")
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Quick Comparison", "Detailed Analysis", "Portfolio Analysis", "Trend Analysis"],
        help="Choose the type of analysis you want to perform"
    )
    
    time_period = st.selectbox(
        "Time Period",
        ["1D", "5D", "1M", "3M", "6M", "1Y", "2Y", "5Y", "MAX"],
        index=5,
        help="Select the time period for historical data"
    )
    
    st.divider()
    
    st.subheader("📚 Recent Analyses")
    if st.session_state.analysis_history:
        for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
            with st.expander(f"{analysis['timestamp']} - {analysis['stocks']}"):
                st.write(f"**Type:** {analysis['type']}")
                if st.button(f"View", key=f"view_{i}"):
                    st.session_state.selected_analysis = analysis
    else:
        st.info("No analysis history yet")

# Main content
st.markdown('<div class="main-header">AI Investment Agent 📈🤖</div>', unsafe_allow_html=True)
st.caption("Advanced AI-powered stock analysis and comparison tool with real-time data and insights")

if not st.session_state.api_key_set:
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to begin analysis.")
    st.info("""
    **Features:**
    - 📊 Real-time stock price comparison
    - 🤖 AI-powered investment analysis
    - 📈 Interactive charts and visualizations
    - 💡 Analyst recommendations
    - 📋 Fundamental analysis
    - 📚 Analysis history tracking
    """)
else:
    # Initialize agent
    try:
        assistant = Agent(
            model=OpenAIChat(id=DEFAULT_MODEL, api_key=openai_api_key),
            tools=[
                YFinanceTools(
                    stock_price=True, 
                    analyst_recommendations=True, 
                    stock_fundamentals=True
                )
            ],
            debug_mode=True,
            description="You are an expert investment analyst that researches stock prices, analyst recommendations, and stock fundamentals. Provide detailed, actionable insights.",
            instructions=[
                "Format your response using markdown and use tables to display data where possible.",
                "Include specific numbers, percentages, and metrics in your analysis.",
                "Provide clear buy/hold/sell recommendations with reasoning.",
                "Compare stocks across multiple dimensions: price, fundamentals, analyst sentiment, and growth potential."
            ],
        )
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        st.stop()

    # Main input section
    st.header("🔍 Stock Comparison")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        stock1 = st.text_input(
            "First Stock Symbol", 
            placeholder="e.g., AAPL",
            help="Enter the ticker symbol for the first stock"
        ).upper().strip()
    with col2:
        stock2 = st.text_input(
            "Second Stock Symbol", 
            placeholder="e.g., MSFT",
            help="Enter the ticker symbol for the second stock"
        ).upper().strip()
    with col3:
        st.write("")  # Spacing
        analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)

    # Quick stats display
    if stock1 or stock2:
        st.subheader("📊 Quick Stats")
        quick_cols = st.columns(max(2, len([s for s in [stock1, stock2] if s])))
        
        for idx, stock in enumerate([stock1, stock2]):
            if stock and validate_stock_symbol(stock):
                try:
                    ticker = yf.Ticker(stock)
                    info = ticker.info
                    current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
                    
                    with quick_cols[idx]:
                        st.metric(
                            label=f"{stock}",
                            value=format_currency(current_price) if isinstance(current_price, (int, float)) else current_price,
                            delta=f"{info.get('regularMarketChangePercent', 0):.2f}%" if 'regularMarketChangePercent' in info else None
                        )
                except Exception as e:
                    st.error(f"Error fetching data for {stock}: {str(e)}")

    # Perform analysis
    if analyze_button and stock1 and stock2:
        # Validate stock symbols
        if not validate_stock_symbol(stock1):
            st.error(f"Invalid stock symbol: {stock1}")
        elif not validate_stock_symbol(stock2):
            st.error(f"Invalid stock symbol: {stock2}")
        else:
            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Analysis", "📈 Charts", "📊 Fundamentals", "💡 Recommendations"])
            
            with tab1:
                with st.spinner(f"🤖 AI is analyzing {stock1} and {stock2}... This may take a moment."):
                    try:
                        query = f"""
                        Perform a comprehensive {analysis_type.lower()} comparing {stock1} and {stock2}.
                        Include:
                        1. Current price comparison
                        2. Performance metrics over the {time_period} period
                        3. Fundamental analysis (P/E ratio, market cap, revenue, etc.)
                        4. Analyst recommendations and price targets
                        5. Risk assessment
                        6. Investment recommendation with clear reasoning
                        7. Key differentiators between the two stocks
                        
                        Format the response with clear sections, use tables for data, and provide actionable insights.
                        """
                        
                        response: RunOutput = assistant.run(query, stream=False)
                        
                        # Display AI response
                        st.markdown("### 🤖 AI Investment Analysis")
                        st.markdown(response.content)
                        
                        # Save to history
                        analysis_entry = {
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'stocks': f"{stock1} vs {stock2}",
                            'type': analysis_type,
                            'response': response.content
                        }
                        st.session_state.analysis_history.append(analysis_entry)
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        st.exception(e)
            
            with tab2:
                st.subheader("📈 Price Comparison Charts")
                try:
                    # Fetch historical data
                    ticker1 = yf.Ticker(stock1)
                    ticker2 = yf.Ticker(stock2)
                    
                    hist1 = ticker1.history(period=time_period)
                    hist2 = ticker2.history(period=time_period)
                    
                    if not hist1.empty and not hist2.empty:
                        # Price comparison chart
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=hist1.index,
                            y=hist1['Close'],
                            mode='lines',
                            name=stock1,
                            line=dict(color='#1f77b4', width=2)
                        ))
                        
                        fig.add_trace(go.Scatter(
                            x=hist2.index,
                            y=hist2['Close'],
                            mode='lines',
                            name=stock2,
                            line=dict(color='#ff7f0e', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"Price Comparison: {stock1} vs {stock2}",
                            xaxis_title="Date",
                            yaxis_title="Price ($)",
                            hovermode='x unified',
                            height=500,
                            template="plotly_white"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Volume comparison
                        fig_vol = go.Figure()
                        fig_vol.add_trace(go.Bar(
                            x=hist1.index,
                            y=hist1['Volume'],
                            name=stock1,
                            marker_color='#1f77b4',
                            opacity=0.7
                        ))
                        fig_vol.add_trace(go.Bar(
                            x=hist2.index,
                            y=hist2['Volume'],
                            name=stock2,
                            marker_color='#ff7f0e',
                            opacity=0.7
                        ))
                        
                        fig_vol.update_layout(
                            title="Trading Volume Comparison",
                            xaxis_title="Date",
                            yaxis_title="Volume",
                            barmode='group',
                            height=400,
                            template="plotly_white"
                        )
                        
                        st.plotly_chart(fig_vol, use_container_width=True)
                        
                        # Performance metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                f"{stock1} Performance",
                                f"{calculate_percentage_change(hist1['Close'].iloc[0], hist1['Close'].iloc[-1]):.2f}%"
                            )
                        with col2:
                            st.metric(
                                f"{stock2} Performance",
                                f"{calculate_percentage_change(hist2['Close'].iloc[0], hist2['Close'].iloc[-1]):.2f}%"
                            )
                    else:
                        st.warning("Unable to fetch historical data for one or both stocks.")
                        
                except Exception as e:
                    st.error(f"Error creating charts: {str(e)}")
            
            with tab3:
                st.subheader("📊 Fundamental Analysis")
                try:
                    ticker1 = yf.Ticker(stock1)
                    ticker2 = yf.Ticker(stock2)
                    
                    info1 = ticker1.info
                    info2 = ticker2.info
                    
                    # Create comparison table
                    comparison_data = {
                        'Metric': [
                            'Current Price',
                            'Market Cap',
                            'P/E Ratio',
                            'Forward P/E',
                            'Dividend Yield',
                            '52 Week High',
                            '52 Week Low',
                            'Beta',
                            'Revenue Growth',
                            'Profit Margin'
                        ],
                        stock1: [
                            format_currency(info1.get('currentPrice', info1.get('regularMarketPrice', 'N/A'))),
                            format_currency(info1.get('marketCap', 'N/A')),
                            f"{info1.get('trailingPE', 'N/A')}",
                            f"{info1.get('forwardPE', 'N/A')}",
                            f"{info1.get('dividendYield', 0) * 100:.2f}%" if info1.get('dividendYield') else 'N/A',
                            format_currency(info1.get('fiftyTwoWeekHigh', 'N/A')),
                            format_currency(info1.get('fiftyTwoWeekLow', 'N/A')),
                            f"{info1.get('beta', 'N/A')}",
                            f"{info1.get('revenueGrowth', 'N/A')}",
                            f"{info1.get('profitMargins', 0) * 100:.2f}%" if info1.get('profitMargins') else 'N/A'
                        ],
                        stock2: [
                            format_currency(info2.get('currentPrice', info2.get('regularMarketPrice', 'N/A'))),
                            format_currency(info2.get('marketCap', 'N/A')),
                            f"{info2.get('trailingPE', 'N/A')}",
                            f"{info2.get('forwardPE', 'N/A')}",
                            f"{info2.get('dividendYield', 0) * 100:.2f}%" if info2.get('dividendYield') else 'N/A',
                            format_currency(info2.get('fiftyTwoWeekHigh', 'N/A')),
                            format_currency(info2.get('fiftyTwoWeekLow', 'N/A')),
                            f"{info2.get('beta', 'N/A')}",
                            f"{info2.get('revenueGrowth', 'N/A')}",
                            f"{info2.get('profitMargins', 0) * 100:.2f}%" if info2.get('profitMargins') else 'N/A'
                        ]
                    }
                    
                    df_comparison = pd.DataFrame(comparison_data)
                    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
                    
                except Exception as e:
                    st.error(f"Error fetching fundamental data: {str(e)}")
            
            with tab4:
                st.subheader("💡 Analyst Recommendations")
                try:
                    ticker1 = yf.Ticker(stock1)
                    ticker2 = yf.Ticker(stock2)
                    
                    rec1 = ticker1.recommendations
                    rec2 = ticker2.recommendations
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**{stock1} Recommendations**")
                        if rec1 is not None and not rec1.empty:
                            st.dataframe(rec1.tail(10), use_container_width=True)
                        else:
                            st.info("No recent recommendations available")
                    
                    with col2:
                        st.write(f"**{stock2} Recommendations**")
                        if rec2 is not None and not rec2.empty:
                            st.dataframe(rec2.tail(10), use_container_width=True)
                        else:
                            st.info("No recent recommendations available")
                            
                except Exception as e:
                    st.error(f"Error fetching recommendations: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Built with ❤️ using Streamlit, Agno, and OpenAI</p>
        <p>⚠️ This tool is for informational purposes only. Not financial advice.</p>
    </div>
""", unsafe_allow_html=True)