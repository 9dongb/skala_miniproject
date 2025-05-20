# agent/agent_keyword.py

from utils.state import TrendState  
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

class KeywordAgent:
    def extract_main_keywords_tfidf(self, state: TrendState, top_k: int = 5) -> list:
        texts = []
        if state.arxiv_data:
            texts += [item["title"] + " " + item["summary"] for item in state.arxiv_data]
        if state.news_data:
            texts += [item["title"] + " " + item.get("snippet", "") for item in state.news_data]
        if not texts:
            return []
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words="english",
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b\w+\b"
        )
        X = vectorizer.fit_transform(texts)
        tfidf_sum = np.asarray(X.sum(axis=0)).flatten()
        top_indices = tfidf_sum.argsort()[::-1][:top_k]
        feature_names = np.array(vectorizer.get_feature_names_out())
        keywords = feature_names[top_indices].tolist()
        return keywords

    def keyword_date_stats(self, state: TrendState, keywords):
        data_rows = []
        for item in (state.arxiv_data or []):
            for kw in keywords:
                if kw.lower() in (item["title"] + item["summary"]).lower():
                    data_rows.append({"date": item["date"], "keyword": kw})
        for item in (state.news_data or []):
            for kw in keywords:
                if kw.lower() in (item["title"] + item.get("snippet", "")).lower():
                    data_rows.append({"date": item["date"], "keyword": kw})
        if not data_rows:
            return pd.DataFrame()
        df = pd.DataFrame(data_rows)
        stats = df.groupby(["date", "keyword"]).size().unstack(fill_value=0)
        return stats

    def count_market_event_articles(self, state: TrendState, event_keywords=None):
        if event_keywords is None:
            event_keywords = ["투자", "인수", "특허", "출시", "상장", "M&A"]
        count = 0
        for news in (state.news_data or []):
            if any(kw in (news["title"] + news.get("snippet", "")) for kw in event_keywords):
                count += 1
        return count

    def run(self, state: TrendState, top_k=5, event_keywords=None) -> TrendState:
        keywords = self.extract_main_keywords_tfidf(state, top_k=top_k)
        trend_stats = self.keyword_date_stats(state, keywords)
        market_event_count = self.count_market_event_articles(state, event_keywords=event_keywords)
        return state.model_copy(update={
            "keywords": keywords,
            "trend_stats": trend_stats,
            "market_event_count": market_event_count
        })