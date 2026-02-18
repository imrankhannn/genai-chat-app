from groq import Groq
from app.core.config import GROQ_API_KEY

def get_groq_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY missing")
    return Groq(api_key=GROQ_API_KEY)
