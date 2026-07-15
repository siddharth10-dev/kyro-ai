import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=os.environ.get("GEMINI_API_KEY", "")
)

def clean_content(content) -> str:
    if not content:
        return ""
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
            elif isinstance(part, str):
                text_parts.append(part)
        return "".join(text_parts).strip()
    elif isinstance(content, str):
        return content.strip()
    return str(content).strip()