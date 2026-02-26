import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from app import create_app

@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("CHROMA_DIR", str(tmp_path / "chroma_db"))
    monkeypatch.setenv("PDF_DIR", str(tmp_path / "pdfs"))
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("TAVILY_API_KEY", "test")
    a = create_app()
    a.config.update(TESTING=True)
    return a

@pytest.fixture
def client(app):
    return app.test_client()
