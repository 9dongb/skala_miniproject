# prompts/summary_prompt.py

def get_summary_prompt(query, keywords):
    return f"""
아래 항목의 주요 내용을 한눈에 알 수 있도록, 임원/경영진용 SUMMARY 단락(5~10줄)으로 요약해줘.
- 분석 주제: {query}
- 대표 키워드: {keywords}
- 최근 2년 트렌드 및 미래 예측 요약
- 시장 반응, 주요 기회, 주요 리스크
- 결론 및 인사이트

모든 내용을 한글로, 짧고 간결하게 요약해줘.
"""
