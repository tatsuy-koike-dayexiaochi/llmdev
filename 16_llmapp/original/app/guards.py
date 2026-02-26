from functools import wraps
from flask import current_app, jsonify

def require_rag_index(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        count = current_app.extensions.get("rag_vector_count", 0)
        if count <= 0:
            if current_app.debug:
                current_app.logger.warning("RAG index is empty. Run: python -m app.rag.cli ingest")
            return jsonify({"error": "RAG index is empty."}), 409
        return fn(*args, **kwargs)
    return wrapper