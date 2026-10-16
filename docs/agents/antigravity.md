# Google Antigravity + AI Studio (`gemini-4-argon`) Rules

このリポジトリで動作するすべてのスキルおよびエージェント（Google Antigravity GUI / IDE / CLI `agy`）は、以下の3つの必須ルールとクロスプラットフォーム仕様に従うこと。

## 1. 完全日本語対応

ユーザーへの質問、選択肢の提示、解説、回答、および生成するすべてのドキュメント（仕様書・チケット・ADR・用語集・コードレビュー結果など）は、**すべて日本語で記述すること**。

## 2. 質問ツールの強制使用 (`ask_question`)

ユーザーに確認や質問を行う際（インタビュー系スキルを含むすべての対話）は、通常のチャットテキスト出力で質問を投げて済ませるのではなく、**必ず1問ずつ Antigravity 組み込みの `ask_question` ツールを呼び出してユーザーの回答を待つこと**。

## 3. 複雑な問題における `gemini-4-argon` 外部スクリプト呼び出し

アーキテクチャの深い設計、難解なバグの原因特定、複数モジュールに跨る仕様策定など「複雑な問題」だと判断した場合、自身のループだけで解決しようとせず、**`GEMINI_API_KEY` の記述場所を確認した上で、`gemini-4-argon` を呼び出す Python スクリプト（`.agents/scripts/call_argon.py`）を `run_command` ツール経由で実行し、その推論結果を取得して活用すること**。

### `GEMINI_API_KEY` の探索優先順位（クロスプラットフォーム対応）

`.agents/scripts/call_argon.py` およびエージェントは、以下の優先順位で `GEMINI_API_KEY` を探索・参照する:

1. **プロジェクトルートの `.env` ファイル**: `./.env` 内の `GEMINI_API_KEY`
2. **OSの環境変数**: `GEMINI_API_KEY`（Linux の `export GEMINI_API_KEY=...` または Windows のユーザー/システム環境変数）
3. **ユーザーホーム配下のグローバル設定**: `~/.gemini/.env`（`pathlib.Path.home() / ".gemini" / ".env"`、すなわち Windows では `C:\Users\<User>\.gemini\.env`、Linux では `/home/<user>/.gemini/.env`）内の `GEMINI_API_KEY`

APIキーが設定されているか事前確認する場合は、以下のコマンドを実行できる:

- **Linux / macOS**: `python3 .agents/scripts/call_argon.py --check-key`（または `uv run .agents/scripts/call_argon.py --check-key`）
- **Windows**: `python .agents/scripts/call_argon.py --check-key`（または `uv run .agents/scripts/call_argon.py --check-key`）

### `.agents/scripts/call_argon.py` の呼び出し方法

パス表記は OS を問わずスラッシュ（`/`）区切りの相対パス `.agents/scripts/call_argon.py` に統一する。`run_command` ツールから以下のいずれかの方法で実行すること:

- **uv が利用可能な環境（Windows / Linux 共通・推奨）**:
  ```bash
  uv run .agents/scripts/call_argon.py "アーキテクチャ上の課題と質問内容" -f src/module.ts -f GLOSSARY.md
  ```
- **Linux / macOS**:
  ```bash
  python3 .agents/scripts/call_argon.py "アーキテクチャ上の課題と質問内容" -f src/module.ts
  ```
- **Windows**:
  ```bash
  python .agents/scripts/call_argon.py "アーキテクチャ上の課題と質問内容" -f src/module.ts
  ```
