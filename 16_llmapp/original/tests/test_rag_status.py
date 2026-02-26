from unittest.mock import MagicMock, patch
from app.rag.status import get_vector_count


def test_get_vector_count_returns_zero_when_dir_not_exists(tmp_path):
    """ディレクトリが存在しない場合は0を返す"""
    non_existent_dir = str(tmp_path / "non_existent")
    count = get_vector_count(non_existent_dir, "text-embedding-3-small")
    assert count == 0


def test_get_vector_count_returns_zero_when_db_file_not_exists(tmp_path):
    """chroma.sqlite3が存在しない場合は0を返す"""
    empty_dir = tmp_path / "empty_chroma"
    empty_dir.mkdir()
    count = get_vector_count(str(empty_dir), "text-embedding-3-small")
    assert count == 0


def test_get_vector_count_returns_zero_on_exception(tmp_path):
    """例外が発生した場合は0を返す"""
    # chroma.sqlite3を作成してディレクトリチェックをパス
    chroma_dir = tmp_path / "chroma"
    chroma_dir.mkdir()
    (chroma_dir / "chroma.sqlite3").touch()

    # get_vectorstoreが例外を投げるようにモック
    with patch("app.rag.status.get_vectorstore") as mock_vs:
        mock_vs.side_effect = Exception("Test exception")
        count = get_vector_count(str(chroma_dir), "text-embedding-3-small")
        assert count == 0


def test_get_vector_count_returns_collection_count(tmp_path):
    """_collectionが正常に動作する場合はその値を返す"""
    # chroma.sqlite3を作成
    chroma_dir = tmp_path / "chroma"
    chroma_dir.mkdir()
    (chroma_dir / "chroma.sqlite3").touch()

    # モックのvectorstoreを作成
    mock_collection = MagicMock()
    mock_collection.count.return_value = 42

    mock_vectorstore = MagicMock()
    mock_vectorstore._collection = mock_collection

    with patch("app.rag.status.get_vectorstore") as mock_vs:
        mock_vs.return_value = mock_vectorstore
        count = get_vector_count(str(chroma_dir), "text-embedding-3-small")
        assert count == 42


def test_get_vector_count_returns_zero_when_collection_is_none(tmp_path):
    """_collectionがNoneの場合は0を返す"""
    # chroma.sqlite3を作成
    chroma_dir = tmp_path / "chroma"
    chroma_dir.mkdir()
    (chroma_dir / "chroma.sqlite3").touch()

    # _collectionがNoneのvectorstoreをモック
    mock_vectorstore = MagicMock()
    mock_vectorstore._collection = None

    with patch("app.rag.status.get_vectorstore") as mock_vs:
        mock_vs.return_value = mock_vectorstore
        count = get_vector_count(str(chroma_dir), "text-embedding-3-small")
        assert count == 0
