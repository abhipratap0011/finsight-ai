from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.research_agent import research_agent
from agents.analyst_agent import analyst_agent
from agents.summarizer_agent import summarizer_agent


class FinSightState(TypedDict):
    ticker: str
    research_report: Optional[str]
    analyst_report: Optional[str]
    final_summary: Optional[str]
    error: Optional[str]


def run_research(state: FinSightState) -> FinSightState:
    try:
        print(f"🔍 Researching {state['ticker']}...")
        report = research_agent(state["ticker"])
        return {**state, "research_report": report}
    except Exception as e:
        return {**state, "error": str(e)}


def run_analyst(state: FinSightState) -> FinSightState:
    try:
        print(f"📊 Analyzing {state['ticker']}...")
        report = analyst_agent(state["ticker"], state["research_report"])
        return {**state, "analyst_report": report}
    except Exception as e:
        return {**state, "error": str(e)}


def run_summarizer(state: FinSightState) -> FinSightState:
    try:
        print(f"📝 Summarizing {state['ticker']}...")
        summary = summarizer_agent(
            state["ticker"],
            state["research_report"],
            state["analyst_report"]
        )
        return {**state, "final_summary": summary}
    except Exception as e:
        return {**state, "error": str(e)}


def check_error(state: FinSightState) -> str:
    if state.get("error"):
        return "end"
    return "continue"


def build_graph():
    graph = StateGraph(FinSightState)

    graph.add_node("researcher", run_research)
    graph.add_node("analyst", run_analyst)
    graph.add_node("summarizer", run_summarizer)

    graph.set_entry_point("researcher")

    graph.add_conditional_edges(
        "researcher",
        check_error,
        {"continue": "analyst", "end": END}
    )
    graph.add_conditional_edges(
        "analyst",
        check_error,
        {"continue": "summarizer", "end": END}
    )
    graph.add_edge("summarizer", END)

    return graph.compile()


finsight_graph = build_graph()


def run_finsight(ticker: str) -> dict:
    initial_state = {
        "ticker": ticker.upper(),
        "research_report": None,
        "analyst_report": None,
        "final_summary": None,
        "error": None
    }
    result = finsight_graph.invoke(initial_state)
    return result