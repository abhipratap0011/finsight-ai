from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tools.stock_tool import get_stock_info, get_stock_history
from tools.news_tool import get_stock_news, get_market_sentiment
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def research_agent(ticker: str) -> str:
    stock_info = get_stock_info(ticker)
    stock_history = get_stock_history(ticker)
    news = get_stock_news(ticker)
    sentiment = get_market_sentiment(ticker)

    prompt = ChatPromptTemplate.from_template("""
    You are a senior financial research analyst.
    Analyze the following data for {ticker} and provide a comprehensive research report.

    STOCK INFO:
    {stock_info}

    PRICE HISTORY (Last 10 days):
    {stock_history}

    LATEST NEWS:
    {news}

    MARKET SENTIMENT:
    {sentiment}

    Provide:
    1. Company Overview
    2. Recent Performance Analysis
    3. News Impact Assessment
    4. Key Risks & Opportunities
    """)

    chain = prompt | llm
    response = chain.invoke({
        "ticker": ticker,
        "stock_info": stock_info,
        "stock_history": stock_history,
        "news": news,
        "sentiment": sentiment
    })

    return response.content