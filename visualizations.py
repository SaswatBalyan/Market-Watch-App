import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
from typing import Optional, Tuple


class FinancialCharts:

    @staticmethod
    def create_candlestick_with_volume(
        df: pd.DataFrame, 
        ticker: str,
        moving_averages: list = None,
        date_range: Tuple[str, str] = None,
        show_volume: bool = True
    ) -> go.Figure:

        if moving_averages is None:
            moving_averages = ['MA20', 'MA50', 'MA200']
        
        if date_range:
            start_date, end_date = date_range
            df = df.loc[start_date:end_date]
        
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

        fig.update_xaxes(title_text="Date", row=rows, col=1)
        fig.update_yaxes(title_text=f"{ticker} Price ($)", row=1, col=1)
        
        if show_volume:
            fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        fig.update_layout(
            title=f"<b>{ticker} - Interactive Candlestick Chart</b>",
            xaxis_rangeslider_visible=True,  
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
        
        if date_range:
            start_date, end_date = date_range
            df = df.loc[start_date:end_date]
        
        fig = go.Figure()
 
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

        if 'Cum_Ret' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['Cum_Ret'] * 100,
                    name='Cumulative Return %',
                    mode='lines',
                    line=dict(color='#ff7f0e', width=2),
                    yaxis='y2',
                    hovertemplate='<b>Cumulative Return</b><br>Date: %{x|%Y-%m-%d}<br>Return: %{y:.2f}%<extra></extra>'
                )
            )

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

        
        daily_ret = (df['Daily_Ret'] * 100).dropna()  
        
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

        if date_range:
            start_date, end_date = date_range
            df = df.loc[start_date:end_date]
        
        daily_ret = df['Close'].pct_change()
        volatility = daily_ret.rolling(window=window).std() * 100
        
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
    @staticmethod
    def create_correlation_heatmap(
        corr_matrix: pd.DataFrame,
        title: str = "Stock Correlation Matrix"
    ) -> go.Figure:
        
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
        
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=risk_return_df['Risk'] * 100,  
                y=risk_return_df['Annual_Return'] * 100,  
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

    print("Working properly")
