from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.core.config import HF_TOKEN

def get_embeddings():
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN missing")

    return HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2",
        task="feature-extraction",
        huggingfacehub_api_token=HF_TOKEN
    )
