import os
from dotenv import load_dotenv
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

class StockMarketInfo:
    """
    Utility class to fetch stock market information using Alpha Vantage.
    """

    def __init__(self):
        load_dotenv()
        os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv("ALPHAVANTAGE_API_KEY")
        self.alpha = AlphaVantageAPIWrapper()

    def get_latest_price(self, symbol: str) -> dict:
        """
        Fetch the latest price/quote for a given stock symbol.
        """
        data = self.alpha._get_stock_quote(symbol)
        q = data.get("Global Quote", {})
        return {
            "symbol": q.get("01. symbol"),
            "price": q.get("05. price"),
            "open": q.get("02. open"),
            "high": q.get("03. high"),
            "low": q.get("04. low"),
            "volume": q.get("06. volume"),
            "previous_close": q.get("08. previous close"),
            "change_percent": q.get("10. change percent")
        }

    def get_daily_summary(self, symbol: str) -> dict:
        """
        Fetch daily OHLC time series (returns last 5 days for brevity).
        """
        data = self.alpha._get_time_series_daily(symbol)
        series = data.get("Time Series (Daily)", {})
        return dict(list(series.items())[:5])

    def get_company_overview(self, symbol: str) -> dict:
        """
        Fetch key company fundamentals.
        """
        info = self.alpha._get_company_overview(symbol)
        keys = [
            "Name", "Sector", "Industry",
            "MarketCapitalization", "PERatio", "DividendYield",
            "Description"
        ]
        return {k: info.get(k) for k in keys if k in info}
