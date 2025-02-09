from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    streaming=False,
    temperature=0.3,
)
