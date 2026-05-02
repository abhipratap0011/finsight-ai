import streamlit as st
from graph import run_finsight
from tools.stock_tool import get_stock_info, get_stock_history, search_ticker
from tools.pdf_tool import process_pdf, query_pdf
import tempfile
import os

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00D4AA;
        text-align: center;
    }
    .sub-header {
        font-size: 1rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #1E1E2E;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00D4AA;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📈 FinSight AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent Financial Research Assistant powered by LangGraph + Groq</p>', unsafe_allow_html=True)

st.sidebar.title("⚙️ Controls")
mode = st.sidebar.radio(
    "Select Mode",
    ["🔍 Stock Analysis", "📄 PDF Analysis", "📊 Quick Stats"]
)

def resolve_ticker(user_input: str) -> str:
    cleaned = user_input.strip()
    
    # First try it directly as a ticker
    try:
        import yfinance as yf
        test = yf.Ticker(cleaned.upper())
        info = test.info
        if info.get("currentPrice") or info.get("regularMarketPrice"):
            return cleaned.upper()
    except:
        pass
    
    # If direct lookup failed, search by company name
    found = search_ticker(cleaned)
    return found.upper() if found else ""

if mode == "🔍 Stock Analysis":
    st.subheader("🔍 AI-Powered Stock Analysis")
    st.caption("💡 You can enter a ticker symbol (e.g. AAPL) or a company name (e.g. Apple)")

    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input(
            "Enter Stock Ticker or Company Name",
            placeholder="e.g. AAPL, Tesla, Google, Microsoft",
            help="Enter a ticker symbol or full company name"
        )
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("🚀 Analyze", use_container_width=True)

    if analyze_btn and user_input:
        with st.spinner("🔍 Resolving ticker..."):
            ticker = resolve_ticker(user_input)

        if not ticker:
            st.error(f"❌ Could not find a ticker for '{user_input}'. Try entering the ticker directly like AAPL, TSLA.")
            st.stop()

        if ticker != user_input.upper().strip():
            st.info(f"🔎 Found ticker: **{ticker}** for '{user_input}'")

        with st.spinner(f"🤖 Running 3 AI agents on {ticker}... This takes ~30 seconds"):
            try:
                info = get_stock_info(ticker)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("💰 Current Price", f"${info['current_price']}")
                with col2:
                    st.metric("📊 P/E Ratio", info['pe_ratio'])
                with col3:
                    st.metric("⬆️ 52W High", f"${info['52w_high']}")
                with col4:
                    st.metric("⬇️ 52W Low", f"${info['52w_low']}")

                st.divider()

                result = run_finsight(ticker)

                if result.get("error"):
                    st.error(f"Error: {result['error']}")
                else:
                    tab1, tab2, tab3 = st.tabs([
                        "📋 Executive Summary",
                        "🔍 Research Report",
                        "📊 Analyst Report"
                    ])
                    with tab1:
                        st.markdown(result["final_summary"])
                    with tab2:
                        st.markdown(result["research_report"])
                    with tab3:
                        st.markdown(result["analyst_report"])

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

    elif analyze_btn and not user_input:
        st.warning("Please enter a ticker symbol or company name!")

elif mode == "📄 PDF Analysis":
    st.subheader("📄 Financial Document Analysis")
    st.write("Upload any financial report, annual report, or earnings document")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            vectorstore = process_pdf(tmp_path)
            st.session_state["vectorstore"] = vectorstore
            st.success(f"✅ PDF processed: {uploaded_file.name}")
            os.unlink(tmp_path)

    if "vectorstore" in st.session_state:
        question = st.text_input("Ask a question about the document")
        if st.button("🔍 Ask") and question:
            with st.spinner("Searching document..."):
                answer = query_pdf(st.session_state["vectorstore"], question)
                st.markdown("### Answer")
                st.markdown(answer)

elif mode == "📊 Quick Stats":
    st.subheader("📊 Quick Stock Statistics")
    st.caption("💡 You can enter a ticker symbol or company name")
    user_input = st.text_input("Enter Ticker or Company Name", placeholder="e.g. AAPL or Apple")

    if st.button("Get Stats") and user_input:
        with st.spinner("Fetching data..."):
            try:
                ticker = resolve_ticker(user_input)
                if not ticker:
                    st.error(f"❌ Could not find ticker for '{user_input}'")
                    st.stop()

                if ticker != user_input.upper().strip():
                    st.info(f"🔎 Found ticker: **{ticker}** for '{user_input}'")

                info = get_stock_info(ticker)
                history = get_stock_history(ticker)

                st.markdown(f"### {info['company']} ({info['ticker']})")
                st.markdown(info['summary'])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${info['current_price']}")
                    st.metric("P/E Ratio", info['pe_ratio'])
                with col2:
                    st.metric("52W High", f"${info['52w_high']}")
                    st.metric("52W Low", f"${info['52w_low']}")
                with col3:
                    st.metric("Profit Margin", info['profit_margin'])
                    st.metric("Recommendation", info['recommendation'].upper())

                st.markdown("### 📈 Price History (Last 10 Days)")
                st.code(history)

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.markdown(
    "<center>Built with LangGraph • Groq LLaMA 3.1 • FAISS • Streamlit</center>",
    unsafe_allow_html=True
)