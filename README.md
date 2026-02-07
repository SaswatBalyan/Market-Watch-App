# Market Watch Dashboard - Stage 1

A professional financial analysis and visualization platform built with Python. This dashboard provides interactive tools for analyzing stock market data, comparing multiple assets, and generating investment insights.

## 🎯 Project Overview

This is **Stage 1** of the Market Watch Dashboard project, implementing the complete data pipeline for financial analysis:

### Phases Implemented

- **Phase 1: Data Ingestion & Structuring**
  - Load CSV files for 90+ stocks
  - Convert dates to datetime objects
  - Set datetime as DataFrame index for time-series operations
  - Create helper functions to extract specific ticker data

- **Phase 2: Financial Feature Engineering**
  - Daily Returns: Percentage changes showing volatility/risk
  - Cumulative Returns: Growth metric showing "If I invested $1 at start, how much is it worth now?"
  - Moving Averages: 20-day, 50-day, and 200-day smoothing for trend analysis
  - Additional metrics: Volatility, Annual Return, Sharpe Ratio

- **Phase 3: Interactive Visualizations**
  - Candlestick charts with moving average overlays
  - Volume bar charts aligned to price
  - Price vs Cumulative Returns dual-axis charts
  - Daily returns distribution histograms
  - Rolling volatility charts

- **Phase 4: Comparative Analysis**
  - Correlation matrix heatmaps (identify stocks that move together)
  - Risk vs Return scatter plots (find "Holy Grail" stocks)
  - Multi-stock cumulative returns comparison

- **Phase 5: Streamlit Deployment**
  - Interactive web dashboard
  - Real-time ticker selection
  - Date range filtering
  - Technical indicator configuration
  - Multi-stock comparison

## 📊 Project Structure

```
90sStock/
├── archive/                      # CSV data files for 90+ stocks
│   ├── AAPL_stock_market_data.csv
│   ├── MSFT_stock_market_data.csv
│   └── ... (88 more stocks)
├── data_handler.py               # Phase 1 & 2: Data loading & feature engineering
├── visualizations.py             # Phase 3 & 4: Interactive charts
├── app.py                        # Phase 5: Streamlit dashboard
├── requirements.txt              # Python dependencies
├── marketWatch.py                # (Legacy - will be replaced)
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or conda for package management

### Installation

1. **Clone/Navigate to the project directory:**
```bash
cd /home/saswat-balyan/devStuff/90sStock
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python data_handler.py
```

You should see output like:
```
============================================================
Market Watch Dashboard - Data Handler Test
============================================================

✓ Discovered 90 tickers

--- Loading AAPL ---
Shape: (11368, 8)
Date range: 1980-12-12 00:00:00 to 2024-01-01 00:00:00
...
```

### Running the Dashboard

**Start the Streamlit app:**
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📈 Key Features

### Single Stock Analysis

1. **Key Metrics Display**
   - Current Price with intraday change
   - Annual Return percentage
   - Sharpe Ratio (risk-adjusted returns)
   - Annual Volatility

2. **Candlestick Chart**
   - OHLC (Open, High, Low, Close) candlesticks
   - Configurable moving averages (20, 50, 200-day)
   - Volume bar chart below
   - Fully interactive with zoom, pan, hover details

3. **Price & Returns Chart**
   - Dual-axis visualization
   - Left: Close price trend
   - Right: Cumulative returns percentage
   - Shows growth relative to initial investment

4. **Risk Analysis**
   - Daily returns distribution histogram
   - Rolling volatility trend chart
   - Identifies periods of high/low risk

### Comparative Analysis

1. **Correlation Matrix**
   - Heatmap showing how stocks move together
   - Red = positive correlation (move together)
   - Blue = negative correlation (move opposite)
   - Essential for portfolio diversification

2. **Risk vs Return Scatter**
   - X-Axis: Risk (daily volatility)
   - Y-Axis: Annual return
   - Color: Sharpe Ratio
   - Find "Holy Grail" stocks (top-left: high return, low risk)

3. **Multi-Stock Comparison**
   - Normalized cumulative returns
   - Compare relative performance across stocks
   - Identify outperforming/underperforming assets

## 💻 Code Modules

### `data_handler.py`

**Key Classes:**

- `StockDataHandler`: Load and manage stock data
  - `load_stock_data(ticker)`: Load single stock with proper datetime indexing
  - `load_multiple_stocks(tickers)`: Batch load multiple stocks
  - `load_all_stocks()`: Load all 90 stocks

- `FeatureEngineer`: Compute financial metrics
  - `compute_daily_returns(df)`: Daily percentage changes
  - `compute_cumulative_returns(df)`: Growth from initial investment
  - `compute_moving_average(df, window)`: Trend smoothing
  - `add_technical_indicators(df)`: Add all metrics at once
  - `compute_volatility(df, window)`: Rolling standard deviation
  - `compute_annual_return(df)`: Total annualized return
  - `compute_sharpe_ratio(df)`: Risk-adjusted return metric

- `ComparativeAnalysis`: Multi-stock analysis
  - `compute_correlation_matrix(stock_data_dict)`: Stock correlations
  - `create_risk_return_profile(stock_data_dict)`: Risk/return metrics for all stocks

### `visualizations.py`

**Key Classes:**

- `FinancialCharts`: Single-stock visualizations
  - `create_candlestick_with_volume()`: OHLC + MA + Volume
  - `create_price_and_returns_chart()`: Dual-axis price/returns
  - `create_daily_returns_histogram()`: Distribution chart
  - `create_volatility_chart()`: Rolling volatility trend

- `ComparativeCharts`: Multi-stock visualizations
  - `create_correlation_heatmap()`: Stock correlation heatmap
  - `create_risk_return_scatter()`: Risk vs Return scatter plot
  - `create_multi_stock_returns_chart()`: Normalized returns comparison

### `app.py`

Main Streamlit application with:
- Sidebar configuration (ticker selection, date range, indicators)
- Single stock analysis section
- Comparative analysis section
- Responsive layout and error handling

## 📚 Usage Examples

### Example 1: Load and Analyze a Single Stock

```python
from data_handler import StockDataHandler, FeatureEngineer

# Initialize handler
handler = StockDataHandler(archive_dir="archive")

# Load AAPL data
aapl = handler.load_stock_data("AAPL")

# Add technical indicators
aapl = FeatureEngineer.add_technical_indicators(aapl)

# Compute metrics
annual_return = FeatureEngineer.compute_annual_return(aapl)
sharpe = FeatureEngineer.compute_sharpe_ratio(aapl)

print(f"AAPL Annual Return: {annual_return:.2%}")
print(f"AAPL Sharpe Ratio: {sharpe:.2f}")
```

### Example 2: Compare Multiple Stocks

```python
from data_handler import StockDataHandler, FeatureEngineer, ComparativeAnalysis

handler = StockDataHandler(archive_dir="archive")

# Load 5 stocks
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
stocks = handler.load_multiple_stocks(tickers)

# Add indicators
for ticker in stocks:
    stocks[ticker] = FeatureEngineer.add_technical_indicators(stocks[ticker])

# Compute correlation
corr_matrix = ComparativeAnalysis.compute_correlation_matrix(stocks)
print(corr_matrix)

# Risk-Return profile
profile = ComparativeAnalysis.create_risk_return_profile(stocks)
print(profile)
```

### Example 3: Create and Display Charts

```python
from data_handler import StockDataHandler, FeatureEngineer
from visualizations import FinancialCharts, ComparativeCharts

handler = StockDataHandler(archive_dir="archive")
msft = handler.load_stock_data("MSFT")
msft = FeatureEngineer.add_technical_indicators(msft)

# Create candlestick chart for 2023
fig = FinancialCharts.create_candlestick_with_volume(
    msft, 
    "MSFT",
    moving_averages=['MA20', 'MA50'],
    date_range=('2023-01-01', '2023-12-31')
)
fig.show()
```

## 🔧 Configuration

### Sidebar Options

1. **Stock Ticker**: Select from 90+ available stocks
2. **Date Range**: Filter analysis to specific dates
3. **Technical Indicators**: Toggle 20-day, 50-day, 200-day moving averages
4. **Analysis Mode**: Single stock vs Multiple stocks comparison
5. **Comparison Stocks**: Select which stocks to include in comparative analysis

## 📊 Data Format

Input CSV files contain the following columns:
- `Date`: Trading date
- `Open`: Opening price
- `High`: Highest price of the day
- `Low`: Lowest price of the day
- `Close`: Closing price
- `Volume`: Number of shares traded
- `Stock Splits`: Stock split information (mostly 0.0)

**Processed DataFrame columns after feature engineering:**
- All original OHLCV columns
- `Daily_Ret`: Daily return percentage
- `Cum_Ret`: Cumulative return from start
- `MA20`, `MA50`, `MA200`: Moving averages
- `Ticker`: Stock symbol (added for multi-stock analysis)

## 🎓 Financial Concepts Explained

### Daily Returns
Formula: (Price_today - Price_yesterday) / Price_yesterday

Shows the percentage change from one day to the next. A histogram reveals the risk distribution.

### Cumulative Returns
Formula: (1 + daily_returns).cumprod() - 1

Shows the growth: "If I invested $1 at the start, how much would it be worth now?"

This metric allows fair comparison of stocks at different price points (e.g., Amazon at $150 vs Ford at $10).

### Moving Averages
A smoothed version of the price that removes noise and shows the true direction:
- **20-day MA**: Short-term trend
- **50-day MA**: Medium-term trend
- **200-day MA**: Long-term trend

### Volatility
Standard deviation of daily returns. Higher volatility = higher risk.

### Sharpe Ratio
Return per unit of risk. Higher Sharpe = better risk-adjusted returns.

Formula: (Average Daily Return - Risk Free Rate) / Daily Volatility × √252

### Correlation
Measure of how two stocks move together:
- **+1.0**: Perfect positive correlation (move together)
- **0.0**: No relationship
- **-1.0**: Perfect negative correlation (move opposite)

## 🚨 Troubleshooting

### "FileNotFoundError: Data not found for ticker X"

**Solution**: Ensure the CSV file `{TICKER}_stock_market_data.csv` exists in the `archive/` directory.

### "ImportError: No module named 'plotly'"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### "Streamlit command not found"

**Solution**: Install and run Streamlit:
```bash
pip install streamlit
streamlit run app.py
```

### Charts not displaying in Streamlit

**Solution**: Clear Streamlit cache and restart:
```bash
streamlit run app.py --logger.level=debug
```

## 📈 Performance Metrics

Dataset coverage:
- **90+ stocks** from various sectors
- **Date range**: 1980-2024 (44+ years of historical data)
- **Average rows per stock**: ~11,000 trading days
- **Total data points**: ~1,000,000+ OHLCV records

## 🔮 Future Enhancements (Stage 2+)

- **Machine Learning Integration**: Predictive models for stock prices
- **Portfolio Optimization**: Markowitz efficient frontier analysis
- **Real-time Data**: Live market data integration
- **Advanced Indicators**: RSI, MACD, Bollinger Bands
- **Backtesting Engine**: Test trading strategies
- **Report Generation**: Export analysis as PDF

## 📝 Notes

- All data is historical and sourced from CSV files
- Prices are adjusted for stock splits
- No dividends adjustment applied in this version
- Time series analysis assumes trading days (weekends/holidays excluded)

## 📄 License

This project is provided as-is for educational and personal use.

## 👨‍💼 Author

Built as an educational project demonstrating:
- Financial data engineering
- Time-series analysis
- Interactive data visualization
- Full-stack Python application development

---

**Last Updated**: February 2026
**Version**: 1.0 (Stage 1 Complete)

