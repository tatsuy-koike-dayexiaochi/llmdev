from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults

from app.rag.retriever import build_retriever

def build_tools(config):
    retriever = build_retriever(
        persist_dir=config["CHROMA_DIR"],
        embed_model=config["OPENAI_EMBED_MODEL"],
        k=4,
    )

    rag_tool = create_retriever_tool(
        retriever,
        name="rag_search",
        description=(
            "Search and return company rules"
        ),
    )

    tavily_tool = TavilySearchResults(
        tavily_api_key=config["TAVILY_API_KEY"],
        max_results=2,
    )

    return [rag_tool, tavily_tool]