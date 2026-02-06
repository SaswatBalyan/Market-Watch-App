import streamlit as st

GLOSSARY = {
    "ticker": {
        "brief": "A unique symbol representing a company's stock on the market (e.g., AAPL for Apple)",
        "url": "https://www.investopedia.com/terms/t/tickersymbol.asp"
    },
    "close": {
        "brief": "The final price at which a stock trades at the end of the trading day",
        "url": "https://www.investopedia.com/terms/c/closingprice.asp"
    },
    "open": {
        "brief": "The price at which a stock begins trading when the market opens",
        "url": "https://www.investopedia.com/terms/o/openingprice.asp"
    },
    "high": {
        "brief": "The highest price a stock reaches during a trading day",
        "url": "https://www.investopedia.com/terms/h/high.asp"
    },
    "low": {
        "brief": "The lowest price a stock reaches during a trading day",
        "url": "https://www.investopedia.com/terms/l/low.asp"
    },
    "volume": {
        "brief": "The total number of shares traded during a period. Higher volume = more trading activity",
        "url": "https://www.investopedia.com/terms/v/volume.asp"
    },
    
    # Returns
    "annual_return": {
        "brief": "The percentage gain or loss of your investment over one year",
        "url": "https://www.investopedia.com/terms/a/annualized-total-return.asp"
    },
    "cumulative_return": {
        "brief": "The total percentage change in investment value from start to end date",
        "url": "https://www.investopedia.com/terms/c/cumulative-return.asp"
    },
    "daily_return": {
        "brief": "The percentage change in stock price from one day to the next",
        "url": "https://www.investopedia.com/terms/d/daily-return.asp"
    },
    
    # Risk Metrics
    "volatility": {
        "brief": "How much a stock's price fluctuates. Higher volatility = more price swings = riskier",
        "url": "https://www.investopedia.com/terms/v/volatility.asp"
    },
    "sharpe_ratio": {
        "brief": "Measures risk-adjusted returns. Higher is better - shows returns per unit of risk taken",
        "url": "https://www.investopedia.com/terms/s/sharperatio.asp"
    },
    "risk": {
        "brief": "The chance that an investment's value will decrease or not meet expectations",
        "url": "https://www.investopedia.com/terms/r/risk.asp"
    },
    "standard_deviation": {
        "brief": "A measure of how spread out prices are. Higher = more unpredictable movements",
        "url": "https://www.investopedia.com/terms/s/standarddeviation.asp"
    },
    
    # Technical Analysis
    "moving_average": {
        "brief": "Average price over a period (e.g., 50-day MA = average of last 50 days). Shows trends",
        "url": "https://www.investopedia.com/terms/m/movingaverage.asp"
    },
    "ma20": {
        "brief": "20-Day Moving Average - average price of last 20 days. Shows short-term trend",
        "url": "https://www.investopedia.com/terms/m/movingaverage.asp"
    },
    "ma50": {
        "brief": "50-Day Moving Average - average price of last 50 days. Shows medium-term trend",
        "url": "https://www.investopedia.com/terms/m/movingaverage.asp"
    },
    "ma200": {
        "brief": "200-Day Moving Average - average price of last 200 days. Shows long-term trend",
        "url": "https://www.investopedia.com/terms/m/movingaverage.asp"
    },
    "candlestick": {
        "brief": "A chart showing stock price movement. Green = price went up, Red = price went down",
        "url": "https://www.investopedia.com/terms/c/candlestick.asp"
    },
    "technical_indicator": {
        "brief": "A tool used to predict future price movements based on past price and volume data",
        "url": "https://www.investopedia.com/terms/t/technicalindicator.asp"
    },
    
    # Comparative Analysis
    "correlation": {
        "brief": "How two stocks move together. +1 = move together, -1 = move opposite, 0 = no relationship",
        "url": "https://www.investopedia.com/terms/c/correlation.asp"
    },
    "portfolio_diversification": {
        "brief": "Spreading investments across different stocks to reduce risk",
        "url": "https://www.investopedia.com/terms/d/diversification.asp"
    },
    "risk_adjusted_return": {
        "brief": "Returns earned compared to the amount of risk taken. Better if higher returns for same risk",
        "url": "https://www.investopedia.com/terms/r/risk-adjusted-return.asp"
    },
    
    # Market Terms
    "bullish": {
        "brief": "Expecting prices to go up. Positive market sentiment",
        "url": "https://www.investopedia.com/terms/b/bullmarket.asp"
    },
    "bearish": {
        "brief": "Expecting prices to go down. Negative market sentiment",
        "url": "https://www.investopedia.com/terms/b/bearmarket.asp"
    },
    "trend": {
        "brief": "The general direction a stock price is moving - uptrend (rising) or downtrend (falling)",
        "url": "https://www.investopedia.com/terms/t/trend.asp"
    },
}


def get_term_tooltip(term_key: str) -> str:
    return GLOSSARY.get(term_key.lower(), {}).get("brief", "")


def get_term_url(term_key: str) -> str:
    return GLOSSARY.get(term_key.lower(), {}).get("url", "")


def create_term_link(term: str, term_key: str = None) -> str:
    if term_key is None:
        term_key = term.lower().replace(" ", "_")
    
    brief = get_term_tooltip(term_key)
    url = get_term_url(term_key)
    
    if not url:
        return term
    
    html = f"""
    <span style="border-bottom: 2px dotted #1f77b4; cursor: help; position: relative;">
        <a href="{url}" target="_blank" style="color: #1f77b4; text-decoration: none; font-weight: 500;">
            {term}
        </a>
        <span style="visibility: hidden; width: 250px; background-color: #333; color: #fff; text-align: center; 
                     border-radius: 6px; padding: 8px; position: absolute; z-index: 1; bottom: 125%; left: 50%; 
                     margin-left: -125px; opacity: 0; transition: opacity 0.3s; font-size: 12px; line-height: 1.4;">
            {brief}
        </span>
    </span>
    """
    return html


def display_term_with_help(term: str, term_key: str = None):
    if term_key is None:
        term_key = term.lower().replace(" ", "_")
    
    brief = get_term_tooltip(term_key)
    url = get_term_url(term_key)
    
    if url:
        st.markdown(
            f"[{term}]({url})" + 
            (f" {st.tooltip(brief)}" if brief else ""),
            unsafe_allow_html=False
        )
    else:
        st.write(term)


def create_info_box_with_terms(content: str, terms_dict: dict = None) -> str:
    if terms_dict is None:
        terms_dict = {}
    
    result = content
    for display_term, glossary_key in terms_dict.items():
        html_term = create_term_link(display_term, glossary_key)
        result = result.replace(display_term, html_term)
    
    return result


def add_glossary_section():
    with st.expander("📚 Financial Glossary - Learn Terms"):
        st.markdown("### Common Financial Terms")
        
        categories = {
            "📈 Stock Basics": ["ticker", "open", "close", "high", "low", "volume"],
            "💹 Returns": ["annual_return", "cumulative_return", "daily_return"],
            "⚠️ Risk Metrics": ["volatility", "sharpe_ratio", "risk", "standard_deviation"],
            "🔍 Technical Analysis": ["moving_average", "ma20", "ma50", "ma200", "candlestick", "technical_indicator"],
            "🔄 Comparative Analysis": ["correlation", "portfolio_diversification", "risk_adjusted_return"],
            "📊 Market Terms": ["bullish", "bearish", "trend"]
        }
        
        for category, terms in categories.items():
            st.markdown(f"**{category}**")
            
            cols = st.columns(2)
            for idx, term in enumerate(terms):
                col = cols[idx % 2]
                brief = get_term_tooltip(term)
                url = get_term_url(term)
                
                if url:
                    col.markdown(
                        f"**[{term.replace('_', ' ').title()}]({url})**: {brief}",
                        unsafe_allow_html=True
                    )
                else:
                    col.markdown(f"**{term.replace('_', ' ').title()}**: {brief}")
            
            st.markdown("") 
