"""
Stage 1: Market Watch Dashboard - Interactive Visualizations Module

Phase 3 & 4: Create financial charts using Plotly
- Candlestick charts with moving averages
- Volume bars
- Correlation heatmaps
- Risk vs Return scatter plots
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
from typing import Optional, Tuple


class FinancialCharts:
    """
    Phase 3: Interactive Financial Visualizations using Plotly
    """
    
    @staticmethod
    def create_candlestick_with_volume(
        df: pd.DataFrame, 
        ticker: str,
        moving_averages: list = None,
        date_range: Tuple[str, str] = None,
        show_volume: bool = True
    ) -> go.Figure:
        """
        Create a "Trader's View" candlestick chart with:
        - Top Panel: Candlestick chart (Open, High, Low, Close) + Moving Average lines
        - Bottom Panel: Bar chart for Volume
        
        Args:
            df: DataFrame with OHLCV data and optional MA columns
            ticker: Stock ticker symbol for title
            moving_averages: List of MA column names to plot (default ['MA20', 'MA50', 'MA200'])
            date_range: Tuple of (start_date, end_date) for filtering
            show_volume: Whether to show volume subplot
            
        Returns:
            Plotly Figure object
        """
        
        if moving_averages is None:
            moving_averages = ['MA20', 'MA50', 'MA200']
        
        # Filter date range if specified
        if date_range:
            start_date, end_date = date_range
            df = df.loc[start_date:end_date]
        
        # Create subplots: 2 rows if showing volume, 1 row if not
        rows = 2 if show_volume else 1
        row_heights = [0.7, 0.3] if show_volume else [1.0]
        
        fig = make_subplots(
            rows=rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=row_heights,
            subplot_titles=(f"{ticker} - Candlestick Chart with Moving Averages",
                          "Volume" if show_volume else None)
        )
        
        # ===== Top Panel: Candlestick Chart =====
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Candlestick',
                increasing_line_color='#26a69a',  # Green
                decreasing_line_color='#ef553b',  # Red
            ),
            row=1, col=1
        )
        
        # Add moving averages
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
        for i, ma_col in enumerate(moving_averages):
            if ma_col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[ma_col],
                        name=ma_col,
                        mode='lines',
                        line=dict(color=colors[i % len(colors)], width=2),
                        hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>'
                    ),
                    row=1, col=1
                )
        
        # ===== Bottom Panel: Volume =====
        if show_volume:
            colors_volume = ['#ef553b' if df['Close'].iloc[i] < df['Open'].iloc[i] else '#26a69a' 
                           for i in range(len(df))]
            
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['Volume'],
                    name='Volume',
                    marker_color=colors_volume,
                    hovertemplate='<b>Volume</b><br>Date: %{x|%Y-%m-%d}<br>Volume: %{y:,.0f}<extra></extra>'
                ),
                row=2, col=1
            )
        
        # ===== Layout Configuration =====
        fig.update_xaxes(title_text="Date", row=rows, col=1)
        fig.update_yaxes(title_text=f"{ticker} Price ($)", row=1, col=1)
        
        if show_volume:
            fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        fig.update_layout(
            title=f"<b>{ticker} - Interactive Candlestick Chart</b>",
            xaxis_rangeslider_visible=False,  # Hide range slider for cleaner look
            template="plotly_white",
            height=700,
            hovermode='x unified',
            font=dict(size=11),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    @staticmethod
    def create_price_and_returns_chart(
        df: pd.DataFrame,
        ticker: str,
        date_range: Tuple[str, str] = None
    ) -> go.Figure:
        """
        Create a dual-axis chart showing:
        - Left axis: Close price
        - Right axis: Cumulative returns (percentage)
        
        Args:
            df: DataFrame with 'Close' and 'Cum_Ret' columns
            ticker: Stock ticker symbol
            date_range: Tuple of (start_date, end_date) for filtering
            
        Returns:
            Plotly Figure object
        """
        
        if date_range:
            start_date, end_date = date_range
            df = df.loc[start_date:end_date]
        
        fig = go.Figure()
        
        # Price line
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['Close'],
                name='Close Price',
                mode='lines',
                line=dict(color='#1f77b4', width=2),
                yaxis='y1',
                hovertemplate='<b>Close Price</b><br>Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>'
            )
        )
        
        # Cumulative returns
        if 'Cum_Ret' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['Cum_Ret'] * 100,  # Convert to percentage
                    name='Cumulative Return %',
                    mode='lines',
                    line=dict(color='#ff7f0e', width=2),
                    yaxis='y2',
                    hovertemplate='<b>Cumulative Return</b><br>Date: %{x|%Y-%m-%d}<br>Return: %{y:.2f}%<extra></extra>'
                )
            )
        
        # Layout with dual axes
        fig.update_layout(
            title=f"<b>{ticker} - Price vs Cumulative Returns</b>",
            xaxis_title="Date",
            yaxis=dict(
                title=dict(text="Close Price ($)", font=dict(color='#1f77b4')),
                tickfont=dict(color='#1f77b4'),
            ),
            yaxis2=dict(
                title=dict(text="Cumulative Return (%)", font=dict(color='#ff7f0e')),
                tickfont=dict(color='#ff7f0e'),
                overlaying='y',
                side='right'
            ),
            template="plotly_white",
            height=500,
            hovermode='x unified',
            font=dict(size=11),
            margin=dict(l=60, r=60, t=80, b=50)
        )
        
        return fig
    
    @staticmethod
    def create_daily_returns_histogram(
        df: pd.DataFrame,
        ticker: str
    ) -> go.Figure:
        """
        Create histogram of daily returns showing risk distribution.
        
        Args:
            df: DataFrame with 'Daily_Ret' column
            ticker: Stock ticker symbol
            
        Returns:
            Plotly Figure object
        """
        
        daily_ret = (df['Daily_Ret'] * 100).dropna()  # Convert to percentage
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Histogram(
                x=daily_ret,
                nbinsx=50,
                name='Daily Returns',
                marker_color='#1f77b4',
                opacity=0.7,
                hovertemplate='<b>Return Range</b><br>Frequency: %{y}<br>Return: %{x:.2f}%<extra></extra>'
            )
        )
        
        # Add mean line
        mean_ret = daily_ret.mean()
        fig.add_vline(
            x=mean_ret,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {mean_ret:.2f}%",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title=f"<b>{ticker} - Daily Returns Distribution</b>",
            xaxis_title="Daily Return (%)",
            yaxis_title="Frequency",
            template="plotly_white",
            height=450,
            font=dict(size=11),
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_volatility_chart(
        df: pd.DataFrame,
        ticker: str,
        window: int = 30,
        date_range: Tuple[str, str] = None
    ) -> go.Figure:
        """
        Create a chart showing rolling volatility over time.
        
        Args:
            df: DataFrame with 'Close' column
            ticker: Stock ticker symbol
            window: Rolling window size (default 30 days)
            date_range: Tuple of (start_date, end_date) for filtering
            
        Returns:
            Plotly Figure object
        """
        
        if date_range:
            start_date, end_date = date_range
            df = df.loc[start_date:end_date]
        
        daily_ret = df['Close'].pct_change()
        volatility = daily_ret.rolling(window=window).std() * 100  # Daily volatility as percentage
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=volatility.index,
                y=volatility,
                name=f'{window}-Day Rolling Volatility',
                mode='lines',
                line=dict(color='#d62728', width=2),
                fill='tozeroy',
                hovertemplate='<b>Volatility</b><br>Date: %{x|%Y-%m-%d}<br>Volatility: %{y:.2f}%<extra></extra>'
            )
        )
        
        fig.update_layout(
            title=f"<b>{ticker} - {window}-Day Rolling Volatility</b>",
            xaxis_title="Date",
            yaxis_title="Daily Volatility (%)",
            template="plotly_white",
            height=450,
            hovermode='x unified',
            font=dict(size=11),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig


class ComparativeCharts:
    """
    Phase 4: Comparative Analysis Charts
    """
    
    @staticmethod
    def create_correlation_heatmap(
        corr_matrix: pd.DataFrame,
        title: str = "Stock Correlation Matrix"
    ) -> go.Figure:
        """
        Create an interactive heatmap showing correlation between stocks.
        
        Goal: See which stocks move together. This is vital for ML feature 
        selection later (to avoid multicollinearity).
        
        Args:
            corr_matrix: Correlation DataFrame (tickers x tickers)
            title: Chart title
            
        Returns:
            Plotly Figure object
        """
        
        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.index,
                colorscale='RdBu_r',
                zmid=0,
                zmin=-1,
                zmax=1,
                colorbar=dict(title="Correlation"),
                hovertemplate='<b>Correlation</b><br>%{y} vs %{x}<br>Correlation: %{z:.3f}<extra></extra>'
            )
        )
        
        fig.update_layout(
            title=f"<b>{title}</b>",
            xaxis_title="Stock Ticker",
            yaxis_title="Stock Ticker",
            template="plotly_white",
            width=900,
            height=800,
            font=dict(size=10),
            margin=dict(l=100, r=50, t=80, b=100)
        )
        
        return fig
    
    @staticmethod
    def create_risk_return_scatter(
        risk_return_df: pd.DataFrame,
        title: str = "Risk vs Return Analysis"
    ) -> go.Figure:
        """
        Create scatter plot of Risk (X-Axis) vs Return (Y-Axis).
        
        Insight: Stocks in the top-left are "Holy Grails" (High Return, Low Risk).
        Stocks in the bottom-right are bad investments.
        
        Args:
            risk_return_df: DataFrame with columns:
                - Ticker: Stock ticker
                - Risk: Standard deviation of daily returns
                - Annual_Return: Annualized return
                - Sharpe: Sharpe Ratio (optional, for color)
                
        Returns:
            Plotly Figure object
        """
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=risk_return_df['Risk'] * 100,  # Convert to percentage
                y=risk_return_df['Annual_Return'] * 100,  # Convert to percentage
                mode='markers+text',
                marker=dict(
                    size=10,
                    color=risk_return_df['Sharpe'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Sharpe Ratio"),
                    line=dict(width=1, color='white')
                ),
                text=risk_return_df['Ticker'],
                textposition="top center",
                textfont=dict(size=10, color='black'),
                hovertemplate='<b>%{text}</b><br>Risk: %{x:.2f}%<br>Annual Return: %{y:.2f}%<br>Sharpe: %{marker.color:.2f}<extra></extra>'
            )
        )
        
        # Add quadrant lines
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.update_layout(
            title=f"<b>{title}</b>",
            xaxis_title="Risk (Daily Volatility %)",
            yaxis_title="Annual Return (%)",
            template="plotly_white",
            width=900,
            height=600,
            hovermode='closest',
            font=dict(size=11),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_multi_stock_returns_chart(
        stock_data_dict: dict,
        date_range: Tuple[str, str] = None
    ) -> go.Figure:
        """
        Create a normalized comparison chart of cumulative returns for multiple stocks.
        
        All stocks start at 0% to allow fair comparison.
        
        Args:
            stock_data_dict: Dictionary of {ticker: DataFrame}
            date_range: Tuple of (start_date, end_date) for filtering
            
        Returns:
            Plotly Figure object
        """
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set2
        
        for i, (ticker, df) in enumerate(stock_data_dict.items()):
            if date_range:
                start_date, end_date = date_range
                df = df.loc[start_date:end_date]
            
            # Compute cumulative returns if not present
            if 'Cum_Ret' not in df.columns:
                df = df.copy()
                daily_ret = df['Close'].pct_change()
                df['Cum_Ret'] = (1 + daily_ret).cumprod() - 1
            
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['Cum_Ret'] * 100,  # Convert to percentage
                    name=ticker,
                    mode='lines',
                    line=dict(color=colors[i % len(colors)], width=2),
                    hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%Y-%m-%d}<br>Return: %{y:.2f}%<extra></extra>'
                )
            )
        
        fig.update_layout(
            title="<b>Multi-Stock Cumulative Returns Comparison</b>",
            xaxis_title="Date",
            yaxis_title="Cumulative Return (%)",
            template="plotly_white",
            height=550,
            hovermode='x unified',
            font=dict(size=11),
            margin=dict(l=60, r=50, t=80, b=50)
        )
        
        return fig


if __name__ == "__main__":
    # Example usage
    from data_handler import StockDataHandler, FeatureEngineer, ComparativeAnalysis
    
    print("Testing visualizations...")
    
    handler = StockDataHandler(archive_dir="archive")
    
    # Load and process single stock
    aapl = handler.load_stock_data("AAPL")
    aapl = FeatureEngineer.add_technical_indicators(aapl)
    
    # Create visualizations
    print("Creating candlestick chart...")
    fig1 = FinancialCharts.create_candlestick_with_volume(aapl, "AAPL", date_range=('2023-01-01', '2023-12-31'))
    fig1.show()
    
    print("Creating price vs returns chart...")
    fig2 = FinancialCharts.create_price_and_returns_chart(aapl, "AAPL", date_range=('2023-01-01', '2023-12-31'))
    fig2.show()
    
    # Load multiple stocks for comparative analysis
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
    multi_stocks = handler.load_multiple_stocks(tickers)
    for ticker in multi_stocks:
        multi_stocks[ticker] = FeatureEngineer.add_technical_indicators(multi_stocks[ticker])
    
    # Correlation heatmap
    print("Creating correlation heatmap...")
    corr_matrix = ComparativeAnalysis.compute_correlation_matrix(multi_stocks)
    fig3 = ComparativeCharts.create_correlation_heatmap(corr_matrix)
    fig3.show()
    
    # Risk vs Return
    print("Creating risk-return scatter...")
    profile = ComparativeAnalysis.create_risk_return_profile(multi_stocks)
    fig4 = ComparativeCharts.create_risk_return_scatter(profile)
    fig4.show()
    
    print("All visualizations created successfully!")
