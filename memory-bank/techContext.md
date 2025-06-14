# 技術コンテキスト

## 技術スタック
- フロントエンド: チャットボットUI (Streamlit)
- バックエンド: Python
- コアエンジン: OpenAIAugmentedLLM (GPT-4o)
- データベース: ローカルSQLite
- インフラ: ローカル実行環境
- ロギング: richライブラリ
- 設定管理: python-dotenv + config.yaml

## 開発環境
- 主要ツール: VSCode, Git
- ビルドシステム: setuptools
- テストフレームワーク: pytest
- 仮想環境: UVツール
- 依存管理: UVツール

## 依存関係
- yfinance (Yahoo Finance APIクライアント)
- pandas (データ分析)
- MCP Agent (推論エンジン)
- httpx (HTTPクライアント)
- python-dotenv (環境変数管理)
- rich (リッチなコンソール出力)
- EvaluatorOptimizerLLM (品質評価ループ)
- RequestParams (LLMリクエストパラメータ管理)

## デプロイメント
- ローカルマシン向け実行ファイル
- Pythonスクリプトとして配布

## 技術的制約
- Yahoo Finance APIの無料利用制限
- GPT-4oモデルのトークン制限とコスト管理
- 環境変数のセキュアな管理 (.envファイル)
- ロギング出力のリッチテキストフォーマット制限
- テストモード実装による外部API依存の解消
