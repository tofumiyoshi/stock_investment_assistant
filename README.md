# 株投資アシスタント

## プロジェクト概要
個人投資家向けにAIを活用した投資支援ツールを提供し、専門知識がなくても最適な投資判断ができるようにするチャットボット形式のアプリケーションです。

## 主な機能
- Yahoo Financeデータ連携による株価/財務指標取得
- 業界ニュース収集（Google News API/Reuters RSS）
- LLMによる分析・推奨機能
- チャットボット形式のユーザーインターフェース

## 技術スタック
- **フロントエンド**: Python Tkinter/Streamlit
- **バックエンド**: Python
- **データベース**: ローカルSQLite
- **主要ライブラリ**:
  - yfinance (Yahoo Finance APIクライアント)
  - pandas (データ分析)
  - MCP Agent (推論エンジン)

## インストール方法
1. リポジトリをクローン:
   ```bash
   git clone [リポジトリURL]
   ```
2. 依存関係をインストール:
   ```bash
   uv pip install -r requirements.txt
   ```
3. 設定ファイルを編集:
   `config.yaml`に必要なAPIキーを設定

## 使用方法
1. アプリケーションを起動:
   ```bash
   python src/mcp_agent.py
   ```
2. チャットボットに質問を入力（例: 「成長株おすすめ」）
3. AIが分析結果と推奨を表示

## ライセンス
[MIT License](LICENSE)

## 連絡先
質問や問題がある場合は、[issueを登録](issues)してください。
