import pytest
from authenticator import Authenticator

@pytest.fixture
def auth():
    return Authenticator()

@pytest.fixture
def registered_auth(auth):
    auth.register("user_name", "password")
    return auth

def test_register(auth):
    # ユーザーが正しく登録される事
    auth.register("user_name", "password")
    assert "user_name" in auth.users
    assert auth.users["user_name"] == "password"

def test_register_duplicate(registered_auth):
    # すでに存在するユーザー名で登録を試みた場合に、エラーメッセージが出力
    with pytest.raises(ValueError):
        registered_auth.register("user_name", "hogehoge")

def test_login(registered_auth):
    # 正しいユーザー名とパスワードでログインできる事
    assert "ログイン成功" == registered_auth.login("user_name", "password")

def test_login_error(registered_auth):
    # 登録されていないユーザーの場合エラーが出る事
    with pytest.raises(ValueError):
        registered_auth.login("hoge", "password")
    # 誤ったパスワードでエラーが出る事
    with pytest.raises(ValueError):
        registered_auth.login("user_name", "hogehoge")

