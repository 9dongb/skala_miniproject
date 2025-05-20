# utils/llm.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
def get_llm():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    return llm