from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def summarizer_agent(ticker: str, research_report: str, analyst_report: str) -> str:

    prompt = ChatPromptTemplate.from_template("""
    You are a financial report writer for a top investment firm.
    Combine the research and analyst reports into one clean, 
    professional executive summary for {ticker}.

    RESEARCH REPORT:
    {research_report}

    ANALYST REPORT:
    {analyst_report}

    Create a concise executive summary with:
    1. 🏢 Company Snapshot (3-4 lines)
    2. 📈 Performance Highlights (bullet points)
    3. 💡 Investment Thesis (why invest or not)
    4. ⚠️ Key Risks (2-3 points)
    5. ✅ Final Verdict (one clear sentence)
    6. 🎯 Price Target & Recommendation

    Keep it professional, clear and actionable.
    Format it nicely with headers and bullet points.
    """)

    chain = prompt | llm
    response = chain.invoke({
        "ticker": ticker,
        "research_report": research_report,
        "analyst_report": analyst_report
    })

    return response.content