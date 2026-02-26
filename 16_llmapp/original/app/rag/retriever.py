from langchain_core.retrievers import BaseRetriever
from .vectorstore import get_vectorstore

def build_retriever(
    persist_dir: str,
    embed_model: str,
    k: int = 4,
) -> BaseRetriever:
    vs = get_vectorstore(persist_dir=persist_dir, embed_model=embed_model)
    return vs.as_retriever(search_kwargs={"k": k})