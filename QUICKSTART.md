# Quick Start Guide - Market Watch Dashboard

## Get Started in 3 Minutes

### Step 1: Install Dependencies
```bash
cd /home/saswat-balyan/devStuff/90sStock
pip install -r requirements.txt
```

### Step 2: Verify Data
```bash
python data_handler.py
```

Expected output:
```
✓ Discovered 95 tickers
...
Annual Return: 18.96%
Sharpe Ratio: 0.57
```

### Step 3: Launch Dashboard
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## Using the Dashboard

### Single Stock Analysis

1. **Select a ticker** from the sidebar (default: AAPL)
2. **Set date range** for your analysis
3. **Choose technical indicators**:
   - 20-Day MA: Short-term trend
   - 50-Day MA: Medium-term trend
   - 200-Day MA: Long-term trend

4. **View charts**:
   - **Candlestick Chart**: See price action with volume
   - **Price vs Returns**: Dual-axis view
   - **Daily Returns Distribution**: See risk profile
   - **Rolling Volatility**: Identify risky periods

### Comparative Analysis

1. **Choose analysis type**: "Multiple Stocks"
2. **Select 2+ stocks** to compare
3. **View insights**:
   - **Correlation Matrix**: Which stocks move together?
   - **Risk vs Return**: Find "Holy Grail" stocks (high return, low risk)
   - **Relative Performance**: Compare cumulative returns

---

## Key Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **Daily Return** | (Price_today - Price_yesterday) / Price_yesterday | Percentage change each day |
| **Cumulative Return** | (1 + daily_returns).cumprod() - 1 | Total growth from initial investment |
| **Annual Return** | Geometric mean of daily returns × 252 | Yearly performance |
| **Volatility** | Std Dev of daily returns × √252 | Annual risk magnitude |
| **Sharpe Ratio** | (Return - Risk-Free Rate) / Volatility | Return per unit of risk |
| **Correlation** | Covariance / (StdDev1 × StdDev2) | How stocks move together (-1 to +1) |

---

## Example Analyses

### Find Hidden Gems (Low Risk, High Return)
1. Select "Multiple Stocks" comparison
2. Choose 10-15 stocks
3. Look for stocks in the **top-left** of the Risk vs Return chart
4. These are "Holy Grail" stocks with good return/risk ratio

### Build Diversified Portfolio
1. View Correlation Matrix for your selected stocks
2. Look for stocks with **low correlation** (blue colors)
3. Combine them to reduce portfolio risk

### Identify Trend Changes
1. Look at the Candlestick chart
2. When price breaks above **200-day MA** = potential uptrend
3. When price breaks below **50-day MA** = potential downtrend

### Assess Stock Volatility
1. Check the Rolling Volatility chart
2. High peaks = risky periods
3. Low valleys = stable periods
4. Choose based on your risk tolerance

---

## Customization

### Add More Stocks
Ensure CSV file follows the pattern: `{TICKER}_stock_market_data.csv` in the `archive/` folder

### Modify Technical Indicators
Edit `data_handler.py`, function `add_technical_indicators()`:
```python
if ma_windows is None:
    ma_windows = [10, 20, 50, 100, 200]  # Add your windows here
```

### Change Date Range in Code
```python
aapl = handler.load_stock_data("AAPL")
aapl_recent = aapl['2020-01-01':'2023-12-31']  # Time-series slicing
```

---

## Keyboard Shortcuts in Dashboard

| Action | Keys |
|--------|------|
| Download chart | Hover & click camera icon |
| Pan/Zoom | Click & drag on chart |
| Zoom box | Box select tool in toolbar |
| Reset zoom | Double-click |
| Save dashboard state | Streamlit caches automatically |

---

## Pro Tips

1. **Weekly Analysis**: Set date range to recent 52 weeks to see current trends
2. **Sector Comparison**: Load related tickers (e.g., all tech stocks) to compare sectors
3. **Crisis Analysis**: Set historical date ranges to study market crashes
4. **Compare with Benchmarks**: Add spy, QQQ, VTI for benchmark comparison

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Chart won't load | Refresh browser (Ctrl+R) |
| "Ticker not found" | Check available tickers with `python data_handler.py` |
| Slow performance | Use smaller date ranges or fewer stocks |
| Import errors | Run `pip install -r requirements.txt` again |

---

## Support

Check `README.md` for detailed documentation and code examples.

**Test command to verify everything works:**
```bash
python -c "from data_handler import StockDataHandler; h = StockDataHandler(); print('✓ All systems operational')"
```

---

**Happy analyzing!**
