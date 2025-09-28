import os
from dotenv import load_dotenv
from typing import List
from langchain.tools import tool
from utils.stock_market_analyzer import StockMarketInfo

class StockTools:
    """
    LangChain tools wrapping the StockMarketInfo utilities.
    """

    def __init__(self):
        load_dotenv()
        self.stock_info = StockMarketInfo()
        self.stock_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup all stock market related tools.
        """

        @tool
        def latest_stock_price(symbol: str) -> str:
            """
            Get the latest stock price and quote details for a ticker.
            Example: "AAPL", "MSFT", "TSLA"
            """
            try:
                result = self.stock_info.get_latest_price(symbol)
                return f"Latest price data for {symbol}: {result}"
            except Exception as e:
                return f"Unable to fetch latest stock price for {symbol}: {e}"

        @tool
        def daily_stock_summary(symbol: str) -> str:
            """
            Get the last 5 days OHLC summary for a ticker.
            """
            try:
                result = self.stock_info.get_daily_summary(symbol)
                return f"Recent daily summary for {symbol}: {result}"
            except Exception as e:
                return f"Unable to fetch daily summary for {symbol}: {e}"

        @tool
        def company_overview(symbol: str) -> str:
            """
            Get fundamental company information (name, sector, market cap, etc.)
            """
            try:
                result = self.stock_info.get_company_overview(symbol)
                return f"Company overview for {symbol}: {result}"
            except Exception as e:
                return f"Unable to fetch company overview for {symbol}: {e}"

        return [latest_stock_price, daily_stock_summary, company_overview]
