# main.py
from langgraph.graph import StateGraph, END

import matplotlib.pyplot as plt

from utils.state import TrendState
from utils.state import TrendState
from agent.agent_collect import CollectAgent
from agent.agent_keywords import KeywordAgent
from agent.agent_prophet import ProphetAgent
from agent.agent_risk import RiskAgent
from agent.agent_report import ReportAgent


collect_agent = CollectAgent()
keyword_agent = KeywordAgent()
prophet_agent = ProphetAgent()
risk_agent = RiskAgent()
report_agent = ReportAgent()


# LangGraph 프로세스 빌더
builder = StateGraph(TrendState)

# 노드 등록
builder.add_node("collect_data", collect_agent.run)
builder.add_node("preprocess_analyze", keyword_agent.run)
builder.add_node("forecast_trend", prophet_agent.run)
builder.add_node("risk_opportunity", risk_agent.run)
builder.add_node("generate_report", report_agent.run)

builder.set_entry_point("collect_data")
builder.add_edge("collect_data", "preprocess_analyze")
builder.add_edge("preprocess_analyze", "forecast_trend")
builder.add_edge("forecast_trend", "risk_opportunity")
builder.add_edge("risk_opportunity", "generate_report")
builder.add_edge("generate_report", END)

# LangGraph 컴파일
app = builder.compile()


# 그래프 시각화
app.get_graph().draw_mermaid_png(output_file_path="output/graph/graph.png")

if __name__ == "__main__":
    user_query = input()
    init_state = TrendState(query=user_query)
    result_state = app.invoke(init_state)
    print("보고서 경로: " + result_state["report"])