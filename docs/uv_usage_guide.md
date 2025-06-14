# UVパッケージマネージャー使用ガイド

## 1. インストール

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

## 2. 基本コマンド

### プロジェクト初期化
```bash
uv pip install -e .
```

### 依存関係インストール
```bash
uv pip install -r requirements.txt
```

### 依存関係凍結
```bash
uv pip freeze > requirements.txt
```

## 3. 既存プロジェクト移行

### Poetryからの移行
```bash
uv pip install $(poetry export --without-hashes)
```

### pipからの移行
```bash
uv pip install -r requirements.txt
```

## 4. ベストプラクティス

- 仮想環境と併用する

#### UVコマンドを使用する場合
```bash
uv venv --python 3.13 .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows
```

#### 従来の方法
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows
uv pip install -r requirements.txt
```

- `uv.lock`ファイルをバージョン管理に含める

## 5. トラブルシューティング

### Windows特有の問題
- PowerShellの実行ポリシー制限がある場合:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 依存関係競合が発生した場合
```bash
uv pip install --resolution=highest package_name
```

### キャッシュクリア
```bash
uv pip cache purge
```

## 6. 参考リンク
- [公式ドキュメント](https://github.com/astral-sh/uv)
- [pipからの移行ガイド](https://astral.sh/blog/uv)
