import argparse
from app.config import Config
from app.rag.ingest import ingest_pdfs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["ingest"])
    args = parser.parse_args()

    if args.command == "ingest":
        stats = ingest_pdfs(
            pdf_dir=Config.PDF_DIR,
            persist_dir=Config.CHROMA_DIR,
            embed_model=Config.OPENAI_EMBED_MODEL,
            chat_model=Config.OPENAI_CHAT_MODEL,
        )
        print(stats)

if __name__ == "__main__":
    main()