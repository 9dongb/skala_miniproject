# prompt/report_prompt.py

def get_report_prompt(summary_text, query, keywords, trend_summary, forecast_imgs_markdown, opportunities, risks):
    return f"""
아래는 AI 트렌드 분석의 전체 결과야. 
상단에는 “SUMMARY” 단락(경영진/의사결정자용 요약)을 먼저 작성하고, 
그 뒤로 아래 순서대로 전체 보고서를 체계적으로 작성해줘.

==========
SUMMARY
{summary_text}
==========

1. 분석 주제 및 질문: {query}
2. 대표 트렌드 키워드: {keywords}
3. 2년치 트렌드 변화 요약(월별 집계):\n{trend_summary}
4. 미래 시계열 예측 요약:\n{forecast_imgs_markdown}
5. 시장 반응 기사 및 주요 이슈: (중요 기사 3~5건 간단 요약, state.news_data에서 뽑아도 됨)
6. 주요 기회(성장, 적용 분야): {opportunities}
7. 주요 리스크(위험, 한계, 규제 등): {risks}
8. 종합 인사이트(구체적 조언, 2~3문단)

보고서는 전문가 수준의 논리/구조/간결함을 유지해 작성해줘.
"""