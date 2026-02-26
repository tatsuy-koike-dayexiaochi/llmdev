from flask import Flask
from .config import Config
from .routes import bp
from .graph.builder import build_graph
from .rag.status import get_vector_count

def create_app() -> Flask:
    # Flaskアプリケーションのセットアップ
    app = Flask(__name__)
    app.config.from_object(Config)

    # グラフを作成
    app.extensions["graph"] = build_graph(app.config)

    # RAGステータスをキャッシュ（起動時に1回だけ計算）
    app.extensions["rag_vector_count"] = get_vector_count(
        app.config["CHROMA_DIR"],
        app.config["OPENAI_EMBED_MODEL"],
    )

    app.register_blueprint(bp)
    return app
