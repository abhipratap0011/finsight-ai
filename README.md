# 📈 FinSight AI — Multi-Agent Financial Research Assistant

[![Live Demo](https://img.shields.io/badge/🤗_HuggingFace-Live_Demo-FFD21E?style=for-the-badge)](https://huggingface.co/spaces/Abhi001999/finsight-ai)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/abhipratap0011/finsight-ai)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF6B6B?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1_8B-F55036?style=for-the-badge)](https://groq.com)

> **An end-to-end agentic AI system** that autonomously researches, analyzes, and summarizes any publicly traded stock using a 3-agent LangGraph pipeline powered by Groq's ultra-fast LLaMA 3.1 inference.

---

## 🎯 What It Does

Enter any stock ticker **or company name** and FinSight AI deploys 3 specialized AI agents that work sequentially to produce a professional-grade investment report in under 60 seconds.

```
User Input: "Tesla" or "TSLA"
      ↓
🔍 Research Agent   →   fetches live stock data, price history, latest news
      ↓
📊 Analyst Agent    →   performs valuation, financial health scoring, price targeting  
      ↓
📝 Summarizer Agent →   generates executive summary with investment verdict
      ↓
Output: Full Investment Report with Buy/Sell/Hold recommendation
```

---

## 🏗️ Architecture

```
finsight-ai/
│
├── agents/
│   ├── research_agent.py      # Fetches & summarizes stock data + news
│   ├── analyst_agent.py       # Financial analysis & valuation assessment
│   └── summarizer_agent.py    # Executive summary generation
│
├── tools/
│   ├── stock_tool.py          # yFinance integration (price, metrics, history)
│   ├── news_tool.py           # Real-time news & market sentiment
│   └── pdf_tool.py            # FAISS-based financial document Q&A
│
├── graph.py                   # LangGraph StateGraph pipeline
├── app.py                     # Streamlit UI
├── Dockerfile                 # Docker deployment config
└── requirements.txt
```

---

## ✨ Key Features

| Feature | Details |
|---|---|
| 🤖 **Multi-Agent System** | 3 specialized agents (Research → Analyst → Summarizer) orchestrated via LangGraph |
| 🔍 **Smart Search** | Accepts both ticker symbols (`AAPL`) and company names (`Apple`) |
| 📊 **Live Market Data** | Real-time prices, P/E ratio, 52-week high/low via yFinance |
| 📰 **News Analysis** | Latest news sentiment & analyst recommendations |
| 📄 **PDF Q&A** | Upload financial reports and ask questions via FAISS vector search |
| ⚡ **Ultra-Fast Inference** | Groq LPU hardware delivers sub-second LLM responses |
| 🐳 **Production Ready** | Dockerized and deployed on HuggingFace Spaces |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/abhipratap0011/finsight-ai.git
cd finsight-ai
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Add your Groq API key to .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🧠 Tech Stack

| Component | Technology |
|---|---|
| **LLM** | Groq LLaMA 3.1 8B Instant |
| **Agent Orchestration** | LangGraph (StateGraph) |
| **LLM Framework** | LangChain + LangChain-Groq |
| **Market Data** | yFinance |
| **Vector Search** | FAISS + HuggingFace sentence-transformers |
| **Embeddings** | all-MiniLM-L6-v2 |
| **UI** | Streamlit |
| **Deployment** | Docker + HuggingFace Spaces |

---

## 📸 Demo

### Stock Analysis Mode
- Enter any ticker or company name
- Get real-time metrics (price, P/E, 52W high/low)
- Receive full 3-tab report: Executive Summary, Research Report, Analyst Report

### PDF Analysis Mode
- Upload any financial report or earnings document
- Ask questions in natural language
- Get chunk-level grounded answers via FAISS retrieval

### Quick Stats Mode
- Fast lookup for price, margins, analyst recommendations
- 10-day price history

---

## 🤖 Agent Pipeline (LangGraph)

```python
# StateGraph flow
researcher → analyst → summarizer → END

# Each agent receives the full state and adds its output
FinSightState = {
    "ticker": str,
    "research_report": str,   # Added by Research Agent
    "analyst_report": str,    # Added by Analyst Agent  
    "final_summary": str,     # Added by Summarizer Agent
    "error": str
}
```

---

## 📊 Sample Output

```
🏢 Company Snapshot
Tesla, Inc. (TSLA) is a leading EV and clean energy company...

📈 Performance Highlights
• Current Price: $390.82 | 52W High: $498.83
• Strong revenue growth driven by EV adoption
• Analyst consensus: BUY with target $420

💡 Investment Thesis
Tesla's dominance in EV infrastructure combined with energy...

⚠️ Key Risks
• Intense competition from BYD and legacy automakers
• Regulatory uncertainty in key markets

✅ Final Verdict
Strong long-term hold with 8-12% upside potential

🎯 Price Target: $425 | Recommendation: BUY
```

---

## 🔒 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLM inference | ✅ Yes |

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

## 👤 Author

**Abhishek Pratap Singh**
- 🎓 M.Tech in AI — IIT Delhi
- 💼 AI Engineer at M3M India Ltd.
- 🔗 [LinkedIn](https://www.linkedin.com/in/abhishek-pratap-singh-7927bb244/)
- 🤗 [HuggingFace](https://huggingface.co/Abhi001999)
- 💻 [GitHub](https://github.com/abhipratap0011)

---

⭐ **If you found this useful, please star the repo!**
