# utils/parse_date.py
from datetime import datetime, timedelta
import re

def parse_news_date(date_str: str) -> str:
    """
    Serper.dev의 뉴스 'date' 값을 YYYY-MM-DD로 변환합니다.
    """
    now = datetime.now()
    date_str = date_str.strip().lower()
    if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
        # 이미 날짜 포맷
        return date_str
    elif "hour" in date_str:
        hours = int(re.search(r"(\d+) hour", date_str).group(1))
        dt = now - timedelta(hours=hours)
        return dt.strftime("%Y-%m-%d")
    elif "minute" in date_str:
        minutes = int(re.search(r"(\d+) minute", date_str).group(1))
        dt = now - timedelta(minutes=minutes)
        return dt.strftime("%Y-%m-%d")
    elif "day" in date_str:
        days = int(re.search(r"(\d+) day", date_str).group(1))
        dt = now - timedelta(days=days)
        return dt.strftime("%Y-%m-%d")
    elif "yesterday" in date_str:
        dt = now - timedelta(days=1)
        return dt.strftime("%Y-%m-%d")
    else:
        return date_str  # 변환 불가 시 원본 반환
