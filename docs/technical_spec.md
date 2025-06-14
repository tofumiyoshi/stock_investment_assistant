# 技術設計書

## 1. システム構成
```mermaid
classDiagram
    class 株投資アシスタント {
        +データ取得モジュール()
        +分析エンジン()
        +UIインターフェース()
    }
    class データ取得モジュール {
        +get_stock_data()
    }
    class 分析エンジン {
        +analyze_trends()
        +generate_recommendation()
    }
    株投資アシスタント --> データ取得モジュール
    株投資アシスタント --> 分析エンジン
```

## 2. 主要モジュール仕様
### データ取得モジュール
- Yahoo Finance APIを使用
- 取得データ:
  - 株価(日次/週次)
  - 財務諸表
  - 企業情報

### 分析エンジン
- LLMを使用した自然言語処理
- 技術指標計算:
  - RSI
  - 移動平均
  - ボリンジャーバンド

## 3. API仕様
```mermaid
sequenceDiagram
    participant User
    participant System
    participant YahooAPI
    User->>System: 銘柄コード入力
    System->>YahooAPI: データリクエスト
    YahooAPI-->>System: JSONデータ
    System->>System: データ分析
    System-->>User: 推奨結果表示
```

## 4. データモデル
- 銘柄マスタ
- 株価データ
- ユーザープロファイル
