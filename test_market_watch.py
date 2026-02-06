import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

from data_handler import StockDataHandler, FeatureEngineer, ComparativeAnalysis


class TestDataHandler(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.handler = StockDataHandler(archive_dir="archive")
    
    def test_discover_tickers(self):
        self.assertGreater(len(self.handler.available_tickers), 0)
        self.assertIn('AAPL', self.handler.available_tickers)
    
    def test_load_single_stock(self):
        df = self.handler.load_stock_data("AAPL")

        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

        expected_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_cols:
            self.assertIn(col, df.columns)

        self.assertIsInstance(df.index, pd.DatetimeIndex)

        self.assertIn('Ticker', df.columns)
        self.assertTrue((df['Ticker'] == 'AAPL').all())
    
    def test_load_multiple_stocks(self):
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        data = self.handler.load_multiple_stocks(tickers)
        
        self.assertEqual(len(data), 3)
        for ticker in tickers:
            self.assertIn(ticker, data)
            self.assertIsInstance(data[ticker], pd.DataFrame)
    
    def test_data_caching(self):
        df1 = self.handler.load_stock_data("AAPL")
        df2 = self.handler.load_stock_data("AAPL")
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_time_series_indexing(self):
        df = self.handler.load_stock_data("AAPL")

        sliced = df['2020-01-01':'2020-12-31']
        self.assertGreater(len(sliced), 0)
        self.assertGreaterEqual(sliced.index[0], pd.Timestamp('2020-01-01'))
        self.assertLessEqual(sliced.index[-1], pd.Timestamp('2020-12-31'))


class TestFeatureEngineer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.handler = StockDataHandler(archive_dir="archive")
        cls.df = cls.handler.load_stock_data("AAPL")
    
    def test_daily_returns(self):
        ret = FeatureEngineer.compute_daily_returns(self.df)

        self.assertIsInstance(ret, pd.Series)

        self.assertTrue(pd.isna(ret.iloc[0]))

        expected_ret = (self.df['Close'].iloc[1] - self.df['Close'].iloc[0]) / self.df['Close'].iloc[0]
        self.assertAlmostEqual(ret.iloc[1], expected_ret, places=6)
        
        self.assertTrue((ret.dropna() > -1).all())
        self.assertTrue((ret.dropna() < 1).all())
    
    def test_cumulative_returns(self):
        cum_ret = FeatureEngineer.compute_cumulative_returns(self.df)
        self.assertIsInstance(cum_ret, pd.Series)
        self.assertGreater(cum_ret.notna().sum(), 0)
        
        first_valid_idx = cum_ret.first_valid_index()
        if first_valid_idx is not None:
            first_valid = cum_ret[first_valid_idx]
            self.assertTrue(abs(first_valid) < 0.5)
    
    def test_moving_average(self):
        ma50 = FeatureEngineer.compute_moving_average(self.df, window=50)
        
        self.assertIsInstance(ma50, pd.Series)

        self.assertEqual(ma50.isna().sum(), 49)

        self.assertTrue(ma50.iloc[49] > 0)
 
        prices = self.df['Close'].iloc[0:50]
        expected_ma = prices.mean()
        self.assertAlmostEqual(ma50.iloc[49], expected_ma, places=2)
    
    def test_add_technical_indicators(self):
        df_with_indicators = FeatureEngineer.add_technical_indicators(self.df)
        
        expected_cols = ['Daily_Ret', 'Cum_Ret', 'MA20', 'MA50', 'MA200']
        for col in expected_cols:
            self.assertIn(col, df_with_indicators.columns)
        self.assertEqual(len(df_with_indicators), len(self.df))
    
    def test_volatility(self):
        vol = FeatureEngineer.compute_volatility(self.df, window=30)
        
        self.assertTrue((vol.dropna() >= 0).all())
        
        self.assertGreater(vol.notna().sum(), 0)
    
    def test_annual_return(self):
        annual_ret = FeatureEngineer.compute_annual_return(self.df)
        
        self.assertIsInstance(annual_ret, (float, np.floating))
        
        self.assertGreater(annual_ret, -1)
        self.assertLess(annual_ret, 5)
    
    def test_sharpe_ratio(self):
        sharpe = FeatureEngineer.compute_sharpe_ratio(self.df)
        
        self.assertIsInstance(sharpe, (float, np.floating))
        
        self.assertGreater(sharpe, -5)
        self.assertLess(sharpe, 5)


class TestComparativeAnalysis(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.handler = StockDataHandler(archive_dir="archive")
        cls.tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']
        cls.stock_data = cls.handler.load_multiple_stocks(cls.tickers)

        for ticker in cls.stock_data:
            cls.stock_data[ticker] = FeatureEngineer.add_technical_indicators(
                cls.stock_data[ticker]
            )
    
    def test_returns_pivot(self):
        pivot = ComparativeAnalysis.create_returns_pivot(self.stock_data)

        self.assertEqual(pivot.shape[1], len(self.tickers))

        for ticker in self.tickers:
            self.assertIn(ticker, pivot.columns)

        self.assertTrue(pivot.notna().sum().sum() > 0)
    
    def test_correlation_matrix(self):
        corr = ComparativeAnalysis.compute_correlation_matrix(self.stock_data)

        self.assertEqual(corr.shape[0], len(self.tickers))
        self.assertEqual(corr.shape[1], len(self.tickers))

        for ticker in self.tickers:
            self.assertAlmostEqual(corr.loc[ticker, ticker], 1.0, places=5)

        pd.testing.assert_frame_equal(corr, corr.T)

        self.assertTrue((corr >= -1).all().all())
        self.assertTrue((corr <= 1).all().all())
    
    def test_risk_return_profile(self):
        profile = ComparativeAnalysis.create_risk_return_profile(self.stock_data)
        
        expected_cols = ['Ticker', 'Risk', 'Annual_Return', 'Sharpe']
        for col in expected_cols:
            self.assertIn(col, profile.columns)

        self.assertEqual(len(profile), len(self.tickers))
        
        self.assertTrue((profile['Risk'] >= 0).all())
        
        self.assertTrue((profile['Sharpe'] > -5).all())
        self.assertTrue((profile['Sharpe'] < 5).all())


class TestDataIntegrity(unittest.TestCase):

    def test_no_missing_ohlc(self):
        handler = StockDataHandler(archive_dir="archive")
        df = handler.load_stock_data("AAPL")
        
        self.assertEqual(df['Open'].isna().sum(), 0)
        self.assertEqual(df['High'].isna().sum(), 0)
        self.assertEqual(df['Low'].isna().sum(), 0)
        self.assertEqual(df['Close'].isna().sum(), 0)
    
    def test_high_low_constraints(self):
        handler = StockDataHandler(archive_dir="archive")
        df = handler.load_stock_data("AAPL")
        
        df_clean = df['2000-01-01':]

        violations = (df_clean['High'] < df_clean['Low']).sum()
        self.assertLess(violations, len(df_clean) * 0.05) 
    
    def test_positive_volume(self):

        handler = StockDataHandler(archive_dir="archive")
        df = handler.load_stock_data("AAPL")
        
        df_clean = df['2000-01-01':]
        
        positive_volume = (df_clean['Volume'] > 0).sum()
        total_records = len(df_clean)

        self.assertGreater(positive_volume / total_records, 0.95)
    
    def test_sorted_index(self):
        handler = StockDataHandler(archive_dir="archive")
        df = handler.load_stock_data("AAPL")
        
        self.assertTrue(df.index.is_monotonic_increasing)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDataHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestFeatureEngineer))
    suite.addTests(loader.loadTestsFromTestCase(TestComparativeAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    
    print("=" * 70)
    print("Market Watch Dashboard - Test Suite")
    print("=" * 70)
    print()
    
    success = run_tests()
    
    print()
    print("=" * 70)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
