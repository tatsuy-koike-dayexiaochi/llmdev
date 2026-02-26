from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import tiktoken

from .vectorstore import get_vectorstore

def ingest_pdfs(
    pdf_dir: str,
    persist_dir: str,
    embed_model: str,
    chat_model: str,
) -> dict:
    vs = get_vectorstore(persist_dir=persist_dir, embed_model=embed_model)

    loader = DirectoryLoader(
        path=pdf_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    documents = loader.load()

    encoding_name = tiktoken.encoding_for_model(chat_model).name
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name=encoding_name
    )
    chunks = text_splitter.split_documents(documents)

    if chunks:
        vs.add_documents(chunks)

    return {
        "encoding_model_used_for_split": chat_model,
        "embedding_model_used_for_index": embed_model,
        "chunks_added": len(chunks),
    }