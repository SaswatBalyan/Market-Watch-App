ARCHIVE_DIR = "archive"

SECTORS = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "NVDA", "AMD", "INTC", "CSCO", "ORCL", "ADBE", "CRM"],
    "Finance": ["JPM", "BAC", "GS", "MS", "BLK", "SCHW", "AXP", "MA", "V", "DFS"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK", "AMGN", "LLY", "GILD", "BIIB"],
    "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "MPC", "PSX", "VLO", "HES", "OKE"],
    "Consumer": ["AMZN", "WMT", "HD", "MCD", "NKE", "COST", "TJX", "DIS", "SBUX", "TSLA"],
    "Industrials": ["BA", "CAT", "MMM", "DE", "LMT", "RTX", "GE", "HON", "ITW", "LUV"],
}

PRESETS = {
    "FAANG": ["AAPL", "AMZN", "GOOGL", "META", "NVDA"],
    "Tech Giants": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
    "Banks": ["JPM", "BAC", "GS", "MS", "BLK"],
    "All Sectors": ["AAPL", "JPM", "JNJ", "XOM", "AMZN", "BA"],
}

DEFAULT_MA_WINDOWS = [20, 50, 200]

DEFAULT_VOLATILITY_WINDOW = 30

RISK_FREE_RATE = 0.02

TRADING_DAYS_PER_YEAR = 252

CHART_TEMPLATE = "plotly_white"  # Options: "plotly", "plotly_white", "plotly_dark"

CANDLESTICK_COLORS = {
    "increasing": "#26a69a",  
    "decreasing": "#ef553b",  
}

MA_COLORS = {
    20: "#1f77b4",   
    50: "#ff7f0e",   
    200: "#2ca02c",  
}

CHART_HEIGHTS = {
    "candlestick": 700,
    "single_metric": 450,
    "correlation": 800,
    "risk_return": 600,
}

SIDEBAR_WIDTH = "medium"

DEFAULT_LOOKBACK_DAYS = 365

FEATURES = {
    "single_stock_analysis": True,
    "comparative_analysis": True,
    "correlation_heatmap": True,
    "risk_return_scatter": True,
    "multi_stock_comparison": True,
}

MAX_CONCURRENT_STOCKS = 15

MIN_DATE = "1980-01-01"  
MAX_DATE = "2026-01-31"  

MIN_DATA_POINTS = 50

MIN_STOCK_HISTORY = 250

CACHE_SIZE = 20

CACHE_TTL = 3600

DOWNSAMPLE_THRESHOLD = 2000 

DOWNSAMPLE_METHOD = 'resample'

DOWNSAMPLE_TARGET = 500

REPORT_SECTIONS = {
    "summary_metrics": True,
    "performance_chart": True,
    "risk_analysis": True,
    "correlation_analysis": True,
    "recommendations": True,
}

DEBUG = False

LOG_FILE = "market_watch.log"

LOG_LEVEL = 'INFO'

ALERTS = {
    "high_volatility": 0.04,  # Daily volatility > 4%
    "extreme_return": 0.10,   # Single day return > 10%
    "low_correlation": 0.3,   # For portfolio diversification
}

#WORK
REALTIME_DATA_SOURCE = None  

API_KEYS = {
    # "alpha_vantage": os.getenv('ALPHA_VANTAGE_API_KEY'),
    # "polygon": os.getenv('POLYGON_API_KEY'),
}

def get_sector_stocks(sector: str) -> list:
    return SECTORS.get(sector, [])

def get_preset_stocks(preset: str) -> list:
    return PRESETS.get(preset, [])

def get_all_stocks() -> list:
    all_stocks = []
    for stocks in SECTORS.values():
        all_stocks.extend(stocks)
    return list(set(all_stocks))

if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"Available sectors: {list(SECTORS.keys())}")
    print(f"Total stocks configured: {len(get_all_stocks())}")
    print(f"Stock presets: {list(PRESETS.keys())}")
