from unittest.mock import patch
from langchain_core.messages import AIMessage


def test_index_route(client):
    """インデックスページが正常に表示される"""
    response = client.get("/")
    assert response.status_code == 200


def test_app_status_route(client):
    """アプリケーションステータスが正常に返される"""
    response = client.get("/app/status")
    assert response.status_code == 200
    data = response.json
    assert "rag_ready" in data
    assert "server_epoch" in data
    assert isinstance(data["rag_ready"], bool)
    assert isinstance(data["server_epoch"], str)


def test_ask_requires_query_field(client):
    """queryフィールドが必須であることを確認"""
    response = client.post("/ask", json={})
    assert response.status_code == 400
    assert "error" in response.json


def test_ask_requires_non_empty_query(client):
    """空のqueryは拒否されることを確認"""
    response = client.post("/ask", json={"query": ""})
    assert response.status_code == 400
    assert "error" in response.json


def test_ask_requires_rag_index(client, app):
    """RAGインデックスが未作成の場合は409を返す"""
    # RAGインデックスを明示的に0に設定
    app.extensions["rag_vector_count"] = 0

    response = client.post("/ask", json={"query": "test question"})
    assert response.status_code == 409
    assert "error" in response.json
    assert response.json["error"] == "RAG index is empty."


def test_ask_returns_answer_when_rag_ready(client, app):
    """RAGが準備できている場合は回答を返す"""
    # RAGインデックスをモック（存在することにする）
    app.extensions["rag_vector_count"] = 10

    # グラフの実行結果をモック
    mock_message = AIMessage(content="にゃー")
    mock_result = {"messages": [mock_message]}

    with patch.object(app.extensions["graph"], "invoke", return_value=mock_result):
        response = client.post("/ask", json={"query": "こんにちは"})
        assert response.status_code == 200
        assert "answer" in response.json
        assert response.json["answer"] == "にゃー"


def test_clear_route(client):
    """セッションクリアが正常に動作する"""
    # 最初のthread_idを取得
    with client.session_transaction() as sess:
        sess["thread_id"] = "original-id"

    response = client.post("/clear")
    assert response.status_code == 200
    assert response.json["status"] == "cleared"

    # thread_idが変更されたことを確認
    with client.session_transaction() as sess:
        assert sess["thread_id"] != "original-id"


def test_thread_id_persistence(client):
    """同じセッション内でthread_idが維持される"""
    with client:
        # 最初のリクエスト
        client.get("/")
        with client.session_transaction() as sess:
            first_thread_id = sess.get("thread_id")

        # 2回目のリクエスト
        client.get("/")
        with client.session_transaction() as sess:
            second_thread_id = sess.get("thread_id")

        # thread_idが同じであることを確認
        assert first_thread_id == second_thread_id
