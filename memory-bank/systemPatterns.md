# システムパターン

## アーキテクチャ概要
```mermaid
graph TD
   A[ユーザー質問] --> B[MCP Agent]
   B --> IN
   OUT --> J[出力]
   L[Config] --> EV
   L --> OP
   L --> Tools

   %% エージェント詳細
   subgraph EvaluatorOptimizerLLM
      OP["Optimizer Agent
        - 投資家プロファイル考慮
        - 市場条件反映"]
      EV["Evaluator Agent
        - 分析レポート評価
        - 7つの評価基準"]
      IN --> OP
      OP -->|ソリューション| EV
      EV -->|Rejected + FeedBack| OP
      EV -->|Accepted| OUT
   end

   %% Tools
   subgraph Tools
      T1[webresearch]
      T2[fetch]
      T3[filesystem]
      T4[yfinance]
   end
   OP -->|MCP| Tools
   EV -->|MCP| Tools
```

## 主要コンポーネント
1. **MCPAgentコア**
   - エージェント管理 (optimizer/evaluator)
   - 処理フロー制御
   - 環境変数/設定管理
2. **Optimizer Agent**
   - 株式スクリーニング専門
   - 投資家プロファイルに基づく最適化
3. **Evaluator Agent**
   - 分析レポート評価
   - 7つの評価基準適用
4. **EvaluatorOptimizerLLM**
   - 品質評価ループ管理
   - OpenAIAugmentedLLM統合
5. **チャットボットUI** (Streamlit)
   - ユーザーインタラクション管理
   - クエリ入力/結果表示

## 設計パターン
- **モジュラー設計**: 各コンポーネントを独立して開発・テスト可能
- **MVCパターン**: UI/ロジック/データの分離
- **堅牢なエラーハンドリング**: 設定ファイル読み込み時の詳細なエラー処理
- **テスト容易性**: 環境変数によるモックレスポンス切り替え

## 統合ポイント
- **Yahoo Finance API**: RESTful API経由のデータ取得
- **Google News API**: 業界ニュース取得（無料枠）
- **Reuters RSS**: 業界ニュース取得（無料）
- **LLM MCP Agent**: 自然言語処理と推論エンジン連携
- **設定管理**: config.yamlからの認証情報取得
