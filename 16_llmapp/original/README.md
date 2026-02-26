## セットアップ

## RAGサンプルデータの配置
講習で利用したデータを利用しました。
配置をお願いします。
```
16_llmapp
 └──  original
        └──  app
        └──  data
             └──  pdf
             └──  text
```

### PDFのインデックス作成

```bash
cd 16_llmapp/original
python -m app.rag.cli ingest
```

## 実行

```bash
cd 16_llmapp/original
python run.py
```

http://localhost:5000 にアクセス

---

## 講習コード（chatbot）との差分

### 1. インデックス作成を切り離し
起動時の初回だけでなく、作り直したいタイミングで作り直せるように

本番反映を見込むと必ず別だと思います。

それによりインデックスが作成されていない場合のエラーハンドリングを追加

### 2. メッセージの保管をローカルストレージに移動
せっかくセッションに保存しているのでリロードにも対応

しかし、サーバーが再起動するとメモリーもリセットされるのでローカルストレージのデータも削除するように実装

### 3. アーキテクチャ: 責務の整理
Flaskアプリケーションっぽく整理

```
app/
├── __init__.py          # アプリ初期化、キャッシュ設定
├── config.py            # 設定の一元管理
├── routes.py            # ルーティング
├── guards.py            # デコレータ
├── graph/               # LangGraph関連
│   ├── builder.py       # グラフ構築
│   ├── state.py         # State定義
│   └── tools.py         # ツール定義
└── rag/                 # RAG関連（責務明確）
    ├── status.py        # ステータス確認
    ├── vectorstore.py   # Chroma初期化
    ├── retriever.py     # Retriever構築
    ├── ingest.py        # PDF取り込み
    └── cli.py           # CLIコマンド
```

### 4. フロントエンド: Markdown対応
LLMの出力を見やすく表示（リスト、コードブロック等）

CSSはchatgpt利用