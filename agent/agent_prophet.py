# agent/agent_prophet.py

from prophet import Prophet
from utils.state import TrendState  
import pandas as pd
import os
import matplotlib.pyplot as plt

class ProphetAgent:
    def save_prophet_plot(self, m, forecast, keyword, output_dir="output/forecast_img"):
        os.makedirs(output_dir, exist_ok=True)
        fig = m.plot(forecast)
        fig.set_size_inches(6, 2)
        img_path = os.path.join(output_dir, f"{keyword}.png")
        fig.savefig(img_path, dpi=150)
        plt.close(fig)
        return img_path

    def run(self, state: TrendState, periods=365) -> TrendState:
        if not state.keywords:
            return state
        forecast_results = {}
        forecast_imgs = {}
        for kw in state.keywords:
            if isinstance(state.trend_stats, pd.DataFrame) and kw in state.trend_stats.columns:
                df = state.trend_stats[[kw]].reset_index().rename(columns={"date": "ds", kw: "y"})
                df["ds"] = pd.to_datetime(df["ds"])
                m = Prophet()
                m.fit(df)
                future = m.make_future_dataframe(periods=periods)
                forecast = m.predict(future)
                forecast_results[kw] = forecast
                img_path = self.save_prophet_plot(m, forecast, kw)
                forecast_imgs[kw] = img_path
        return state.model_copy(update={"forecast": forecast_results, "forecast_imgs": forecast_imgs})