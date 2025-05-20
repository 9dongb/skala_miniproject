# agent/agent_collect.py

from utils.state import TrendState  
from utils.parse_date import parse_news_date
import requests
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pytrends.request import TrendReq
import pandas as pd

class CollectAgent:
    def arxiv_search_structured_recent(self, query: str, max_results: int = 500, years: int = 2) -> list:
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{query}&start=0&max_results={max_results}&sortBy=lastUpdatedDate&sortOrder=descending"
        )
        res = requests.get(url)
        res.raise_for_status()
        root = ET.fromstring(res.text)
        ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
        result = []
        cutoff_date = datetime.now() - timedelta(days=years*365)
        for entry in root.findall('arxiv:entry', ns):
            published = entry.find('arxiv:published', ns).text[:10]
            pub_date = datetime.strptime(published, "%Y-%m-%d")
            if pub_date >= cutoff_date:
                result.append({
                    "title": entry.find('arxiv:title', ns).text.strip().replace('\n', ' '),
                    "date": published,
                    "summary": entry.find('arxiv:summary', ns).text.strip().replace('\n', ' '),
                    "link": entry.find('arxiv:id', ns).text.strip(),
                })
        return result

    def news_search_structured_recent(self, query: str, num: int = 500, years: int = 2) -> list:
        SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        url = "https://google.serper.dev/news"
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        data = {"q": query, "num": num}
        res = requests.post(url, json=data, headers=headers)
        if not res.ok:
            return []
        news = res.json().get("news", [])[:num]
        result = []
        cutoff_date = datetime.now() - timedelta(days=years*365)
        for item in news:
            date_str = parse_news_date(item.get("date", ""))
            try:
                news_date = datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                continue
            if news_date >= cutoff_date:
                result.append({
                    "title": item.get("title", ""),
                    "date": date_str,
                    "snippet": item.get("snippet", ""),
                    "source": item.get("source", ""),
                    "link": item.get("link", ""),
                })
        return result

    def get_google_trends(self, keywords: list, years: int = 2 , geo: str = 'KR') -> pd.DataFrame:
        timeframe = f'today {years}-y'
        pytrends = TrendReq(hl='ko', tz=540)
        pytrends.build_payload(keywords, timeframe=timeframe, geo=geo)
        df = pytrends.interest_over_time()
        if 'isPartial' in df.columns:
            df = df.drop(columns=['isPartial'])
        return df

    def run(self, state: TrendState) -> TrendState:
        query = state.query
        arxiv_results = self.arxiv_search_structured_recent(query=query, max_results=500, years=2)
        news_results = self.news_search_structured_recent(query=query, num=500, years=2)
        # google_trends_result = self.get_google_trends([query], years=2)
        return state.model_copy(update={
            "arxiv_data": arxiv_results,
            "news_data": news_results,
            # "google_trends_data": google_trends_result
        })