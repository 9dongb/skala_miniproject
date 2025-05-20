# utils/state.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
import pandas as pd

# 상태 정의
class TrendState(BaseModel):
    query: str                                         # 사용자의 질문

    arxiv_data: Optional[List[Dict[str, Any]]] = None  # arXiv 논문 구조화 데이터
    news_data: Optional[List[Dict[str, Any]]] = None   # 뉴스 구조화 데이터
    google_trends_data: Optional[pd.DataFrame] = None  # 구글 트렌드 데이터
    trend_stats: Optional[Any] = None                  # 키워드별 집계/시계열 DataFrame 등
    keywords: Optional[List[str]] = None               #
    forecast: Optional[Any] = None                     # 예측(Prophet 결과, DataFrame, plot 등)
    forecast_imgs:Optional[str] = None                 # 예측 결과 이미지 경로
    report: Optional[str] = None                       # 최종 보고서(자연어)
    model_config = ConfigDict(arbitrary_types_allowed=True)