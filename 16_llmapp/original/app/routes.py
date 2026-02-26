import uuid
from flask import Blueprint, render_template, current_app, jsonify, request, session
from langchain_core.messages import HumanMessage

from app.guards import require_rag_index

bp = Blueprint("main", __name__)

def get_thread_id() -> str:
    tid = session.get("thread_id")
    if not tid:
        tid = str(uuid.uuid4())
        session["thread_id"] = tid
    return tid

def rag_ready() -> bool:
    count = current_app.extensions.get("rag_vector_count", 0)
    return count > 0

@bp.get("/")
def index():
    return render_template("index.html")

@bp.get("/app/status")
def app_status():
    return jsonify({
        "rag_ready": rag_ready(),
        "server_epoch": current_app.config["SERVER_EPOCH"],
    })

@bp.post("/ask")
@require_rag_index
def ask():
    payload = request.json or {}
    query = (payload.get("query") or "").strip()

    if not query:
        return jsonify({"error": "query is required"}), 400

    thread_id = get_thread_id()

    graph = current_app.extensions["graph"]
    result = graph.invoke(
        {"messages": [HumanMessage(content=query)]},
        {"configurable": {"thread_id": thread_id}},
    )

    last = result["messages"][-1]
    return jsonify({
        "answer": getattr(last, "content", str(last)),
    })

@bp.post("/clear")
def clear():
    session["thread_id"] = str(uuid.uuid4())
    return jsonify({"status": "cleared"})