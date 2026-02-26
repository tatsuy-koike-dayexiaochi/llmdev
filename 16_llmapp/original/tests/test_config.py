import os
from app.config import Config


def test_config_has_required_keys():
    """設定クラスが必要なキーを持っているか確認"""
    assert hasattr(Config, "SECRET_KEY")
    assert hasattr(Config, "OPENAI_API_KEY")
    assert hasattr(Config, "TAVILY_API_KEY")
    assert hasattr(Config, "OPENAI_CHAT_MODEL")
    assert hasattr(Config, "OPENAI_EMBED_MODEL")
    assert hasattr(Config, "CHROMA_DIR")
    assert hasattr(Config, "PDF_DIR")
    assert hasattr(Config, "SERVER_EPOCH")


def test_config_default_values():
    """デフォルト値が正しく設定されているか確認"""
    assert Config.SECRET_KEY == "dev-secret-test-key"
    assert Config.OPENAI_CHAT_MODEL == "gpt-4o-mini"
    assert Config.OPENAI_EMBED_MODEL == "text-embedding-3-small"
    assert Config.CHROMA_DIR.endswith("data/chroma_db")
    assert Config.PDF_DIR.endswith("data/pdf")


def test_config_server_epoch_is_unique():
    """SERVER_EPOCHがランダムな値であることを確認"""
    assert len(Config.SERVER_EPOCH) == 16
    assert isinstance(Config.SERVER_EPOCH, str)
