# utils/save_plot.py
import matplotlib.pyplot as plt
from prophet import Prophet
import pandas as pd
import os

plt.rcParams["font.family"] = "AppleGothic"

def save_trend_plot(df, keyword, output_dir="output"):
    import os
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10,4))
    plt.plot(df["date"], df[keyword], marker="o")
    plt.title(f"'{keyword}' 트렌드 변화")
    plt.xlabel("날짜")
    plt.ylabel("빈도수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    save_path = os.path.join(output_dir, f"trend_{keyword}.png")
    plt.savefig(save_path, dpi=150)
    plt.close()  # 메모리 누수 방지
    return save_path


def forecast_and_save_plot(state, keyword, periods=30, output_dir="output"):

    os.makedirs(output_dir, exist_ok=True)

    if not isinstance(state.trend_stats, pd.DataFrame) or keyword not in state.trend_stats.columns:
        return None

    df = state.trend_stats[[keyword]].reset_index().rename(columns={"date": "ds", keyword: "y"})
    df["ds"] = pd.to_datetime(df["ds"])
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)

    # Prophet의 plot 메서드는 Figure를 반환
    fig = m.plot(forecast)
    fig.savefig(os.path.join(output_dir, f"prophet_{keyword}.png"), dpi=150)
    plt.close(fig)
    return forecast