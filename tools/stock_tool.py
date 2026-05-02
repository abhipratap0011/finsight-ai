import yfinance as yf
import pandas as pd

def get_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    # yfinance uses different keys depending on the stock
    current_price = (
        info.get("currentPrice") or
        info.get("regularMarketPrice") or
        info.get("previousClose") or
        "N/A"
    )

    market_cap = info.get("marketCap", "N/A")
    if market_cap != "N/A":
        market_cap = f"${market_cap:,.0f}"

    return {
        "company": info.get("longName", ticker),
        "ticker": ticker.upper(),
        "current_price": current_price,
        "market_cap": market_cap,
        "pe_ratio": info.get("trailingPE") or info.get("forwardPE") or "N/A",
        "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
        "revenue": info.get("totalRevenue", "N/A"),
        "profit_margin": info.get("profitMargins", "N/A"),
        "recommendation": info.get("recommendationKey", "N/A"),
        "summary": info.get("longBusinessSummary", "N/A")
    }

def get_stock_history(ticker: str, period: str = "1mo") -> str:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    
    if hist.empty:
        return "No historical data found."
    
    hist = hist[["Open", "High", "Low", "Close", "Volume"]].round(2)
    return hist.tail(10).to_string()

import yfinance as yf

def search_ticker(company_name: str) -> str:
    try:
        search = yf.Search(company_name, max_results=1)
        quotes = search.quotes
        if quotes:
            return quotes[0].get("symbol", "")
        return ""
    except Exception as e:
        return ""