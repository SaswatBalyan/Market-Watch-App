import pandas as pd
import numpy as np
from pathlib import Path
import os


class StockDataHandler:
    def __init__(self, archive_dir: str = "archive"):
        self.archive_dir = Path(archive_dir)
        self.data_cache = {} 
        self._discover_tickers()
    
    def _discover_tickers(self):
        self.available_tickers = []
        
        if not self.archive_dir.exists():
            raise FileNotFoundError(f"Archive directory not found: {self.archive_dir}")
        
        for csv_file in sorted(self.archive_dir.glob("*_stock_market_data.csv")):
            ticker = csv_file.stem.replace("_stock_market_data", "")
            self.available_tickers.append(ticker)
        
        print(f"✓ Discovered {len(self.available_tickers)} tickers")
    
    def load_stock_data(self, ticker: str) -> pd.DataFrame:
        if ticker in self.data_cache:
            return self.data_cache[ticker].copy()
        
        csv_path = self.archive_dir / f"{ticker}_stock_market_data.csv"
        
        if not csv_path.exists():
            raise FileNotFoundError(
                f"Data not found for ticker {ticker}. "
                f"Available tickers: {', '.join(self.available_tickers[:10])}..."
            )

        df = pd.read_csv(csv_path)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        
        df['Ticker'] = ticker

        self.data_cache[ticker] = df.copy()
        
        return df
    
    def get_stock_data(self, ticker: str) -> pd.DataFrame:
        return self.load_stock_data(ticker)
    
    def load_multiple_stocks(self, tickers: list) -> dict:
        data = {}
        for ticker in tickers:
            try:
                data[ticker] = self.load_stock_data(ticker)
            except FileNotFoundError as e:
                print(f"Warning: {e}")
        return data
    
    def load_all_stocks(self) -> dict:
        return self.load_multiple_stocks(self.available_tickers)


class FeatureEngineer:
    @staticmethod
    def compute_daily_returns(df: pd.DataFrame) -> pd.Series:
        return df['Close'].pct_change()
    
    @staticmethod
    def compute_cumulative_returns(df: pd.DataFrame) -> pd.Series:
        daily_ret = FeatureEngineer.compute_daily_returns(df)
        return (1 + daily_ret).cumprod() - 1  
    
    @staticmethod
    def compute_moving_average(df: pd.DataFrame, window: int = 50) -> pd.Series:
        return df['Close'].rolling(window=window).mean()
    
    @staticmethod
    def add_technical_indicators(df: pd.DataFrame, ma_windows: list = None) -> pd.DataFrame:
        if ma_windows is None:
            ma_windows = [20, 50, 200]
        
        df = df.copy()
        
        df['Daily_Ret'] = FeatureEngineer.compute_daily_returns(df)

        df['Cum_Ret'] = FeatureEngineer.compute_cumulative_returns(df)

        for window in ma_windows:
            df[f'MA{window}'] = FeatureEngineer.compute_moving_average(df, window=window)
        
        return df
    
    @staticmethod
    def compute_volatility(df: pd.DataFrame, window: int = 30) -> pd.Series:
        daily_ret = FeatureEngineer.compute_daily_returns(df)
        return daily_ret.rolling(window=window).std()
    
    @staticmethod
    def compute_annual_return(df: pd.DataFrame) -> float:
        total_return = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]
        years = len(df) / 252  # 252 trading days per year
        annual_return = (1 + total_return) ** (1 / years) - 1
        return annual_return
    
    @staticmethod
    def compute_sharpe_ratio(df: pd.DataFrame, risk_free_rate: float = 0.02) -> float:
        daily_ret = FeatureEngineer.compute_daily_returns(df).dropna()
        excess_ret = daily_ret.mean() - (risk_free_rate / 252)  # Daily risk-free rate
        volatility = daily_ret.std()
        sharpe = (excess_ret / volatility) * np.sqrt(252)  # Annualize
        return sharpe


class ComparativeAnalysis:
    @staticmethod
    def create_returns_pivot(stock_data_dict: dict, use_close: bool = False) -> pd.DataFrame:
        column_name = 'Close' if use_close else 'Daily_Ret'
        
        for ticker in stock_data_dict:
            if 'Daily_Ret' not in stock_data_dict[ticker].columns and not use_close:
                stock_data_dict[ticker]['Daily_Ret'] = (
                    stock_data_dict[ticker]['Close'].pct_change()
                )

        pivot_data = []
        for ticker, df in stock_data_dict.items():
            pivot_data.append(df[[column_name]].rename(columns={column_name: ticker}))
        
        pivot_df = pd.concat(pivot_data, axis=1)
        return pivot_df
    
    @staticmethod
    def compute_correlation_matrix(stock_data_dict: dict) -> pd.DataFrame:
        pivot_df = ComparativeAnalysis.create_returns_pivot(stock_data_dict, use_close=False)
        return pivot_df.corr()
    
    @staticmethod
    def create_risk_return_profile(stock_data_dict: dict) -> pd.DataFrame:
        profile = []
        
        for ticker, df in stock_data_dict.items():
            daily_ret = df['Close'].pct_change().dropna()
            
            risk = daily_ret.std()  # Daily volatility
            daily_return = daily_ret.mean()
            annual_return = daily_return * 252  # Annualize
            sharpe = (daily_return / risk * np.sqrt(252)) if risk > 0 else 0
            
            profile.append({
                'Ticker': ticker,
                'Risk': risk,
                'Annual_Return': annual_return,
                'Sharpe': sharpe
            })
        
        return pd.DataFrame(profile).sort_values('Sharpe', ascending=False)


if __name__ == "__main__":
    print("Working properly")