import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# 実行中のスクリプトのパスを取得
current_script_path = os.path.abspath(__file__)
# 実行中のスクリプトが存在するディレクトリを取得 (app/)
current_directory = os.path.dirname(current_script_path)
# originalディレクトリを取得
base_directory = os.path.dirname(current_directory)

class Config:
    SECRET_KEY = "dev-secret-test-key"

    OPENAI_API_KEY = os.getenv("API_KEY", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

    OPENAI_CHAT_MODEL = "gpt-4o-mini"
    OPENAI_EMBED_MODEL = "text-embedding-3-small"

    CHROMA_DIR = f"{base_directory}/data/chroma_db"
    PDF_DIR = f"{base_directory}/data/pdf"

    SERVER_EPOCH = os.urandom(8).hex()
