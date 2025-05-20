# agent/agent_repory.py

from langchain_core.messages import HumanMessage
from prompt.repory_prompt import get_report_prompt
from prompt.summary_prompt import get_summary_prompt
from utils.llm import get_llm
from utils.state import TrendState  
import pandas as pd
import os
import markdown
from weasyprint import HTML

class ReportAgent:
    def forecast_imgs_markdown(self):
        forecast_img_dir = "output/forecast_img"
        forecast_imgs = [f for f in os.listdir(forecast_img_dir) if f.endswith(".png")]
        md = ""
        for img_path in forecast_imgs:
            kw = os.path.splitext(img_path)[0]
            rel_path = os.path.join(forecast_img_dir, img_path)
            md += f"### {kw} 트렌드 예측\n\n"
            md += f'<img src="{rel_path}" style="width:100%; max-width:500px;"/>\n\n'
        return md

    def markdown_to_pdf(self, md_text, pdf_path="output/pdf/final_report.pdf", table_html=None):
        html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
        # 표가 있으면, <table> 태그를 table_html로 치환
        if table_html:
            import re
            html = re.sub(r'<table[\\s\\S]*?</table>', table_html, html, flags=re.MULTILINE)

        html = f"""
        <html>
        <head>
            <style>
                @page {{
                    margin: 1cm;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    page-break-inside: avoid;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 16px 0;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #f2f2f2;
                    color: #333;
                }}
                tr:nth-child(even) {{
                    background-color: #fafafa;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        base_url = os.path.abspath(".")
        HTML(string=html, base_url=base_url).write_pdf(pdf_path, presentational_hints=True)
        return pdf_path
    
    def styled_trend_stats_html(self, df: pd.DataFrame) -> str:
        styled = (
            df.style
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('color', '#333'), ('border', '1px solid #ccc'), ('padding', '6px')]},
                {'selector': 'td', 'props': [('border', '1px solid #ccc'), ('padding', '6px')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#fafafa')]},
                {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('width', '100%')]},
            ])
            .set_properties(**{'text-align': 'center'})
        )
        return styled.to_html(escape=False, index=True)

    def run(self, state: TrendState) -> TrendState:
        llm = get_llm()
        keywords = getattr(state, "keywords", [])
        trend_summary = ""
        if isinstance(state.trend_stats, pd.DataFrame):
            ts = state.trend_stats.copy()
            ts.index = pd.to_datetime(ts.index)
            ts_month = ts.resample('ME').sum()
            # trend_summary = ts_month.to_string()
            trend_stats_html = self.styled_trend_stats_html(ts_month)

        forecast_desc = ""
        if state.forecast and isinstance(state.forecast, dict):
            for k, v in state.forecast.items():
                forecast_desc += f"\n[{k}] 예측 샘플: {v.head(3).to_string(index=False)}"

        risk_op_analysis = getattr(state, "risk_opportunity_analysis", {})
        opportunities = risk_op_analysis.get("opportunities", [])
        risks = risk_op_analysis.get("risks", [])

        summary_prompt = get_summary_prompt(state.query, keywords)
        summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
        summary_text = summary_response.content.strip()

        prompt = get_report_prompt(summary_text, state.query, keywords, trend_stats_html, self.forecast_imgs_markdown(), opportunities, risks)
        response = llm.invoke([HumanMessage(content=prompt)])

        pdf_path = self.markdown_to_pdf(response.content, table_html=trend_stats_html)
        return state.model_copy(update={"report": pdf_path})