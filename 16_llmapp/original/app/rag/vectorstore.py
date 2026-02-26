import os
from app.config import Config
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def get_vectorstore(persist_dir: str, embed_model: str) -> Chroma:
    os.makedirs(persist_dir, exist_ok=True)
    embedding_model = OpenAIEmbeddings(
        model=embed_model,
        api_key=Config.OPENAI_API_KEY
    )
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model,
    )
