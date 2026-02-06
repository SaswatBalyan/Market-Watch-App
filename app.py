"""
Stage 1: Market Watch Dashboard - Streamlit Application

Phase 5: Deployment

This Streamlit app provides an interactive dashboard where users can:
- Select a ticker from a dropdown
- View interactive candlestick charts with moving averages
- See correlation heatmaps
- Analyze risk vs return metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Import custom modules
from data_handler import StockDataHandler, FeatureEngineer, ComparativeAnalysis
from visualizations import FinancialCharts, ComparativeCharts
from glossary import display_term_with_help, add_glossary_section, GLOSSARY

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Market Watch Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

@st.cache_resource
def initialize_data_handler():
    """Initialize the data handler (cached to avoid reloading)."""
    return StockDataHandler(archive_dir="archive")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

st.sidebar.markdown("# ⚙️ Market Watch Configuration")
st.sidebar.markdown("---")

# Help section for beginners
with st.sidebar.expander("📚 Need Help? Start Here!"):
    st.markdown("""
    **New to investing?** Check out our **Beginner's Guide**!
    
    The guide explains:
    - 📊 What different terms mean
    - 📈 How to read the charts
    - 💡 Tips for analyzing stocks
    - ❓ Common questions answered
    
    **Quick tips:**
    - Hover over metric labels to see explanations
    - Click "?" icons next to charts for help
    - Scroll down to see the Financial Glossary
    - Click any term to learn more on Investopedia
    """)
    
    # Create a link-like button info
    st.info("📖 See BEGINNERS_GUIDE.md in the project root for a complete guide!", icon="ℹ️")

st.sidebar.markdown("---")

handler = initialize_data_handler()

# Ticker selection
selected_ticker = st.sidebar.selectbox(
    "📊 Select Stock Ticker",
    options=handler.available_tickers,
    index=0 if handler.available_tickers else None,
    help="Select a stock ticker to analyze"
)

st.sidebar.markdown("---")

# Date range selection - constrained by available data
st.sidebar.markdown("### 📅 Date Range")

# Load selected ticker data to get available date range
try:
    ticker_data = handler.load_stock_data(selected_ticker)
    min_date = ticker_data.index.min().date()
    max_date = ticker_data.index.max().date()
    
    # Set default to last 1 year within available range
    default_start = max(min_date, max_date - timedelta(days=365))
    default_end = max_date
except Exception as e:
    st.sidebar.error(f"Error loading date range: {str(e)}")
    min_date = datetime.now().date() - timedelta(days=365*10)
    max_date = datetime.now().date()
    default_start = max(min_date, max_date - timedelta(days=365))
    default_end = max_date

col1, col2 = st.sidebar.columns(2)

with col1:
    start_date_input = st.date_input(
        "Start Date",
        value=default_start,
        min_value=min_date,
        max_value=max_date,
        help=f"Select start date for analysis (between {min_date} and {max_date})"
    )

with col2:
    end_date_input = st.date_input(
        "End Date",
        value=default_end,
        min_value=min_date,
        max_value=max_date,
        help=f"Select end date for analysis (between {min_date} and {max_date})"
    )

# Validate date range
if start_date_input > end_date_input:
    st.sidebar.error("Start date must be before end date!")
    date_range = (default_start.strftime('%Y-%m-%d'), default_end.strftime('%Y-%m-%d'))
else:
    date_range = (start_date_input.strftime('%Y-%m-%d'), end_date_input.strftime('%Y-%m-%d'))

st.sidebar.markdown("---")

# Technical indicators configuration
st.sidebar.markdown("### 📈 Technical Indicators")
st.sidebar.info("💡 **Technical Indicators** are tools to identify trends. Hover over each indicator for details.", icon="ℹ️")

show_ma20 = st.sidebar.checkbox(
    "20-Day MA", 
    value=True,
    help=GLOSSARY.get('ma20', {}).get('brief', '')
)
show_ma50 = st.sidebar.checkbox(
    "50-Day MA", 
    value=True,
    help=GLOSSARY.get('ma50', {}).get('brief', '')
)
show_ma200 = st.sidebar.checkbox(
    "200-Day MA", 
    value=False,
    help=GLOSSARY.get('ma200', {}).get('brief', '')
)

moving_averages = []
if show_ma20:
    moving_averages.append('MA20')
if show_ma50:
    moving_averages.append('MA50')
if show_ma200:
    moving_averages.append('MA200')

st.sidebar.markdown("---")

# Comparative analysis selection
st.sidebar.markdown("### 🔄 Comparative Analysis")

comparison_mode = st.sidebar.radio(
    "Analysis Type",
    options=["Single Stock", "Multiple Stocks"],
    help="Choose between analyzing a single stock or comparing multiple stocks"
)

if comparison_mode == "Multiple Stocks":
    num_compare = st.sidebar.slider(
        "Number of stocks to compare",
        min_value=2,
        max_value=10,
        value=5,
        help="Select how many stocks to include in comparative analysis"
    )
    
    compare_tickers = st.sidebar.multiselect(
        "Select stocks to compare",
        options=handler.available_tickers,
        default=handler.available_tickers[:num_compare],
        help="Select multiple stocks for correlation and risk analysis"
    )
else:
    compare_tickers = [selected_ticker]

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

st.markdown('<p class="main-header">📈 Market Watch Dashboard</p>', unsafe_allow_html=True)
st.markdown("**Interactive financial analysis for beginners and experienced investors**")

# Beginner-friendly welcome info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Tickers Available", len(handler.available_tickers))
with col2:
    st.metric("📅 Data Span", "1980 - 2026")
with col3:
    st.metric("💡 Help", "Click sidebar help")

st.info(
    "**👋 Welcome!** This dashboard helps you understand stock market trends. "
    "All technical terms have tooltips (hover) and links to Investopedia (click). "
    "Start by selecting a stock on the left! 👈",
    icon="ℹ️"
)

st.markdown("---")

# ============================================================================
# SECTION 1: SINGLE STOCK ANALYSIS
# ============================================================================

st.markdown("## 📊 Single Stock Analysis")

try:
    # Load and process data
    with st.spinner(f"Loading data for {selected_ticker}..."):
        stock_data = handler.load_stock_data(selected_ticker)
        stock_data = FeatureEngineer.add_technical_indicators(stock_data)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = stock_data['Close'].iloc[-1]
        prev_close = stock_data['Close'].iloc[-2]
        price_change = current_price - prev_close
        price_change_pct = (price_change / prev_close) * 100
        
        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}",
            delta=f"{price_change_pct:+.2f}%",
            help=GLOSSARY.get('close', {}).get('brief', '')
        )
    
    with col2:
        annual_return = FeatureEngineer.compute_annual_return(stock_data)
        st.metric(
            label="Annual Return",
            value=f"{annual_return:.2%}",
            help=GLOSSARY.get('annual_return', {}).get('brief', '')
        )
    
    with col3:
        sharpe_ratio = FeatureEngineer.compute_sharpe_ratio(stock_data)
        st.metric(
            label="Sharpe Ratio",
            value=f"{sharpe_ratio:.2f}",
            help=GLOSSARY.get('sharpe_ratio', {}).get('brief', '')
        )
    
    with col4:
        volatility = stock_data['Close'].pct_change().std() * np.sqrt(252) * 100
        st.metric(
            label="Annual Volatility",
            value=f"{volatility:.2f}%",
            help=GLOSSARY.get('volatility', {}).get('brief', '')
        )
    
    st.markdown("---")
    
    # Candlestick chart with volume
    col_title, col_help = st.columns([0.85, 0.15])
    with col_title:
        st.subheader(f"🕯️ {selected_ticker} - Candlestick Chart")
    with col_help:
        st.markdown(f"[?](https://www.investopedia.com/terms/c/candlestick.asp)", 
                   help=GLOSSARY.get('candlestick', {}).get('brief', ''))
    
    st.info(
        "📍 **What you're looking at**: Each candle shows Open, High, Low, Close prices. "
        "Green = price up, Red = price down. Colored lines are moving averages showing trends.",
        icon="ℹ️"
    )
    
    candlestick_fig = FinancialCharts.create_candlestick_with_volume(
        stock_data,
        selected_ticker,
        moving_averages=moving_averages if moving_averages else ['MA50'],
        date_range=date_range
    )
    st.plotly_chart(candlestick_fig, use_container_width=True)
    
    # Price vs Cumulative Returns
    col_title, col_help = st.columns([0.75, 0.25])
    with col_title:
        st.subheader(f"💹 {selected_ticker} - Price vs Cumulative Returns")
    with col_help:
        st.markdown(f"[?](https://www.investopedia.com/terms/c/cumulative-return.asp)", 
                   help=GLOSSARY.get('cumulative_return', {}).get('brief', ''))
    
    st.info(
        "📍 **Left axis**: Stock price. **Right axis**: Total return from day 1. "
        "Shows how your $100 investment would grow over time.",
        icon="ℹ️"
    )
    
    price_returns_fig = FinancialCharts.create_price_and_returns_chart(
        stock_data,
        selected_ticker,
        date_range=date_range
    )
    st.plotly_chart(price_returns_fig, use_container_width=True)
    
    # Daily Returns Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        col_title, col_help = st.columns([0.8, 0.2])
        with col_title:
            st.subheader(f"📉 {selected_ticker} - Daily Returns Distribution")
        with col_help:
            st.markdown(f"[?](https://www.investopedia.com/terms/d/daily-return.asp)", 
                       help=GLOSSARY.get('daily_return', {}).get('brief', ''))
        st.caption("Shows how often the stock had small vs big price changes")
        returns_hist = FinancialCharts.create_daily_returns_histogram(stock_data, selected_ticker)
        st.plotly_chart(returns_hist, use_container_width=True)
    
    with col2:
        col_title, col_help = st.columns([0.8, 0.2])
        with col_title:
            st.subheader(f"🌊 {selected_ticker} - Rolling Volatility")
        with col_help:
            st.markdown(f"[?](https://www.investopedia.com/terms/v/volatility.asp)", 
                       help=GLOSSARY.get('volatility', {}).get('brief', ''))
        st.caption("Measures how risky/unpredictable the stock is over time")
        volatility_fig = FinancialCharts.create_volatility_chart(
            stock_data,
            selected_ticker,
            window=30,
            date_range=date_range
        )
        st.plotly_chart(volatility_fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data for {selected_ticker}: {str(e)}")
    st.info("Please ensure the CSV file exists in the archive folder.")

st.markdown("---")

# ============================================================================
# SECTION 2: COMPARATIVE ANALYSIS
# ============================================================================

st.markdown("## 🔄 Comparative Analysis")

if len(compare_tickers) >= 2:
    try:
        with st.spinner("Loading comparative data..."):
            multi_stock_data = handler.load_multiple_stocks(compare_tickers)
            
            # Add technical indicators to all stocks
            for ticker in multi_stock_data:
                multi_stock_data[ticker] = FeatureEngineer.add_technical_indicators(
                    multi_stock_data[ticker]
                )
        
        # Correlation Matrix
        col_title, col_help = st.columns([0.85, 0.15])
        with col_title:
            st.subheader("🔗 Correlation Matrix")
        with col_help:
            st.markdown(f"[?](https://www.investopedia.com/terms/c/correlation.asp)", 
                       help=GLOSSARY.get('correlation', {}).get('brief', ''))
        
        st.markdown("""
        **How to read this chart:**
        - **Red (close to 1)**: Stocks move together strongly → not good for diversification
        - **Blue (close to -1)**: Stocks move opposite directions → good for diversification
        - **White (close to 0)**: No relationship
        
        **💡 Tip**: For a safe portfolio, mix stocks with low/negative correlation.
        """)
        
        corr_matrix = ComparativeAnalysis.compute_correlation_matrix(multi_stock_data)
        corr_fig = ComparativeCharts.create_correlation_heatmap(
            corr_matrix,
            title=f"Correlation Matrix - {', '.join(compare_tickers[:5])}{'...' if len(compare_tickers) > 5 else ''}"
        )
        st.plotly_chart(corr_fig, use_container_width=True)
        
        st.markdown("---")
        
        # Risk vs Return Scatter Plot
        col_title, col_help = st.columns([0.85, 0.15])
        with col_title:
            st.subheader("⚖️ Risk vs Return Analysis")
        with col_help:
            st.markdown(f"[?](https://www.investopedia.com/terms/r/risk-adjusted-return.asp)", 
                       help=GLOSSARY.get('risk_adjusted_return', {}).get('brief', ''))
        
        st.markdown("""
        **Understanding the chart:**
        - **X-Axis**: Risk (how unpredictable the stock is)
        - **Y-Axis**: Annual Return (profit percentage per year)
        - **Color**: Sharpe Ratio (brighter = better returns for the risk taken)
        
        **🎯 What you want**: Top-left = High return with low risk (rare gems!)
        """)
        
        risk_return_df = ComparativeAnalysis.create_risk_return_profile(multi_stock_data)
        risk_return_fig = ComparativeCharts.create_risk_return_scatter(
            risk_return_df,
            title=f"Risk vs Return - {', '.join(compare_tickers[:5])}{'...' if len(compare_tickers) > 5 else ''}"
        )
        st.plotly_chart(risk_return_fig, use_container_width=True)
        
        # Risk-Return Profile Table
        st.subheader("📋 Risk-Return Profile")
        
        display_df = risk_return_df[[
            'Ticker', 'Risk', 'Annual_Return', 'Sharpe'
        ]].copy()
        
        display_df['Risk'] = (display_df['Risk'] * 100).round(2).astype(str) + '%'
        display_df['Annual_Return'] = (display_df['Annual_Return'] * 100).round(2).astype(str) + '%'
        display_df['Sharpe'] = display_df['Sharpe'].round(2)
        
        display_df.columns = ['Ticker', 'Daily Volatility', 'Annual Return', 'Sharpe Ratio']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Multi-Stock Returns Comparison
        st.subheader("📈 Cumulative Returns Comparison")
        st.markdown("Normalized comparison starting from 0% - shows relative performance of all stocks.")
        
        multi_returns_fig = ComparativeCharts.create_multi_stock_returns_chart(
            multi_stock_data,
            date_range=date_range
        )
        st.plotly_chart(multi_returns_fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error in comparative analysis: {str(e)}")
else:
    st.info("Select at least 2 stocks in the sidebar for comparative analysis.")

# ============================================================================
# FOOTER & GLOSSARY
# ============================================================================

st.markdown("---")

# Add interactive glossary
add_glossary_section()

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem 0;">
    <p><small>Market Watch Dashboard - Stage 1 | Data sourced from archive</small></p>
    <p><small>Built with Streamlit, Pandas, and Plotly</small></p>
    <p><small>💡 New to investing? Click on the <strong>Financial Glossary</strong> section above to learn key terms!</small></p>
</div>
""", unsafe_allow_html=True)
