import time
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load from backend/.env if it exists
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(env_path)

API_KEY = os.getenv("OPENAI_API_KEY")

def get_embeddings_model():
    key = os.getenv("OPENAI_API_KEY")
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=key
    )

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a batch of texts using LangChain's OpenAIEmbeddings (text-embedding-3-small).
    """
    if not texts:
        return []
        
    embeddings_model = get_embeddings_model()
    for attempt in range(4):
        try:
            return embeddings_model.embed_documents(texts)
        except Exception as e:
            print(f"  LangChain OpenAI Embedding Error on attempt {attempt+1}: {e}")
            time.sleep(2 * (attempt + 1))
            
    raise Exception("Failed to generate embeddings after 4 attempts.")

