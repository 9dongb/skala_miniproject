# agent/agent_risk.py

from langchain_core.messages import HumanMessage
from utils.llm import get_llm
from utils.state import TrendState  
import pandas as pd
import json 


class RiskAgent:
    def run(self, state: TrendState) -> TrendState:
        llm = get_llm()
        trend_summary = ""
        if isinstance(state.trend_stats, pd.DataFrame):
            if len(state.trend_stats) > 30:
                ts = state.trend_stats.copy()
                ts.index = pd.to_datetime(ts.index)
                ts_month = ts.resample('ME').sum()
                trend_summary = ts_month.to_string()
            else:
                trend_summary = state.trend_stats.to_string()
        else:
            trend_summary = "트렌드 데이터 없음"

        forecast_desc = ""
        if state.forecast and isinstance(state.forecast, dict):
            for k, v in state.forecast.items():
                forecast_desc += f"\n[{k}] 예측 샘플: {v.head(3).to_string(index=False)}"

        market_news = []
        if state.news_data:
            for news in state.news_data:
                if any(kw in (news["title"] + news.get("snippet", "")) for kw in ["투자", "제휴", "위기", "규제", "경쟁", "시장"]):
                    market_news.append(news["title"] + ": " + news.get("snippet", ""))
                if len(market_news) >= 5:
                    break
        market_news_text = "\n".join(market_news)

        prompt = f"""
아래는 최근 2년 AI 트렌드 통계(월별), 예측 결과, 시장 반응 기사 입니다.

[2년치 트렌드 요약]
{trend_summary}

[예측 결과 샘플]
{forecast_desc}

[시장 반응 기사 예시]
{market_news_text}

위 정보를 바탕으로 1~3년 내 주요 '기회'(성장 가능성, 신시장, 적용 분야)와 '리스크'(규제, 경쟁, 한계, 과도한 hype 등)를 각 3가지씩 구체적으로 뽑아줘. 
각 항목에 설명을 붙여 json 객체로 반환해.
예시:
{{
  "opportunities": [{{"title": "예시", "desc": "설명"}}...],
  "risks": [{{"title": "예시", "desc": "설명"}}...]
}}
"""
        response = llm.invoke([HumanMessage(content=prompt)])
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {"opportunities": [], "risks": [], "raw": response.content}
        return state.model_copy(update={"risk_opportunity_analysis": analysis})