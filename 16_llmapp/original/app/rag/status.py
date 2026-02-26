import os
from pathlib import Path
from app.rag.vectorstore import get_vectorstore

def get_vector_count(persist_dir: str, embed_model: str) -> int:
    # Chromaのデータディレクトリが存在しない場合は0
    if not os.path.exists(persist_dir):
        return 0

    # chroma.sqlite3が存在しない場合も0
    chroma_db_path = Path(persist_dir) / "chroma.sqlite3"
    if not chroma_db_path.exists():
        return 0

    try:
        vs = get_vectorstore(persist_dir=persist_dir, embed_model=embed_model)

        col = getattr(vs, "_collection", None)
        if col is not None and hasattr(col, "count"):
            return int(col.count())

        return 0

    except Exception:
        return 0