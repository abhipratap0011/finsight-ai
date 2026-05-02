from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tools.stock_tool import get_stock_info
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

def analyst_agent(ticker: str, research_report: str) -> str:
    stock_info = get_stock_info(ticker)

    prompt = ChatPromptTemplate.from_template("""
    You are an expert financial analyst and investment advisor.
    Based on the research report below, provide a detailed investment analysis.

    TICKER: {ticker}

    STOCK DATA:
    - Current Price: {current_price}
    - P/E Ratio: {pe_ratio}
    - Market Cap: {market_cap}
    - 52 Week High: {week_high}
    - 52 Week Low: {week_low}
    - Profit Margin: {profit_margin}
    - Analyst Recommendation: {recommendation}

    RESEARCH REPORT:
    {research_report}

    Provide a structured analysis with:
    1. Valuation Assessment (is it overvalued/undervalued?)
    2. Financial Health Score (1-10)
    3. Growth Potential (Short-term & Long-term)
    4. Investment Recommendation (Strong Buy / Buy / Hold / Sell / Strong Sell)
    5. Price Target (3-6 months)
    6. Key Metrics Summary
    """)

    chain = prompt | llm
    response = chain.invoke({
        "ticker": ticker,
        "current_price": stock_info["current_price"],
        "pe_ratio": stock_info["pe_ratio"],
        "market_cap": stock_info["market_cap"],
        "week_high": stock_info["52w_high"],
        "week_low": stock_info["52w_low"],
        "profit_margin": stock_info["profit_margin"],
        "recommendation": stock_info["recommendation"],
        "research_report": research_report
    })

    return response.content