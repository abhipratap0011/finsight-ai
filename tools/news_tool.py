import requests
from bs4 import BeautifulSoup
import yfinance as yf

def get_stock_news(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        news = stock.news[:5]  # Get latest 5 news

        if not news:
            return "No recent news found."

        result = []
        for i, item in enumerate(news, 1):
            content = item.get("content", {})
            title = content.get("title", "No title")
            summary = content.get("summary", "")
            provider = content.get("provider", {}).get("displayName", "Unknown")
            pub_date = content.get("pubDate", "")

            result.append(
                f"{i}. {title}\n"
                f"   Source: {provider}\n"
                f"   Date: {pub_date}\n"
                f"   Summary: {summary[:200]}..."
            )

        return "\n\n".join(result)

    except Exception as e:
        return f"Error fetching news: {str(e)}"


def get_market_sentiment(ticker: str) -> str:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        recommendation = info.get("recommendationKey", "N/A")
        target_price = info.get("targetMeanPrice", "N/A")
        current_price = info.get("currentPrice", "N/A")
        analyst_count = info.get("numberOfAnalystOpinions", "N/A")

        return (
            f"Analyst Recommendation: {recommendation.upper()}\n"
            f"Current Price: ${current_price}\n"
            f"Average Target Price: ${target_price}\n"
            f"Number of Analysts: {analyst_count}"
        )

    except Exception as e:
        return f"Error fetching sentiment: {str(e)}"