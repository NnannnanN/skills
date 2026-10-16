# 要件定義書：mattpocock/skills の Google Antigravity + AI Studio 最適化カスタマイズ（クロスプラットフォーム対応版）

## 1. プロジェクトの目的
本リポジトリ（`mattpocock/skills`）のスキル群を、**Windows および Linux（Antigravity CLI `agy` 含む）のマルチプラットフォーム環境**で動作する **Google Antigravity** と **Google AI Studio (`gemini-4-argon` API)** のハイブリッド開発環境に最適化して移植・改修する。
メインエージェントのクォータを節約しつつ、高度な推論が必要な局面でのみ Google AI Studio の API 枠（`gemini-4-argon`）をスクリプト経由で呼び出す構成を構築する。

---

## 2. 全体要件：全スキルの Antigravity 適合化とクロスプラットフォーム対応
`skills/` 配下（または `.agents/skills/`）にあるすべてのスキル（`SKILL.md` および関連ファイル）を走査・確認し、Antigravity（GUI / IDE / CLI）で動作するのに適した形へ修正すること。

### 2.1 ディレクトリ構成と Frontmatter の最適化
- **配置先:** Antigravity の標準仕様である `.agents/skills/<skill-name>/SKILL.md` の構造に準拠させること。
- **YAML Frontmatter の検証:** 各 `SKILL.md` の先頭に `name` と `description` が正しく定義されているか確認し、Antigravity のモデルが自律発火（Progressive Disclosure）しやすい明確な `description` に調整すること。不要な Claude Code 専用のプラグイン設定（`.claude-plugin` 等への依存）や Codex 専用メタデータがあれば、Antigravity の動作を阻害しないよう整理すること。

### 2.2 Antigravity 組み込みツールへのマッピング置換
各スキルの指示文（プロンプト）内で、他社エージェント固有のツール名やコマンドが記述されている箇所を、Antigravity の組み込みツール（`BuiltinTools`）に置き換えること。
- ファイル・ディレクトリ操作：`list_directory`, `search_directory`, `find_file`, `view_file`, `create_file`, `edit_file`
- コマンド実行：`run_command`
- サブエージェント起動：`start_subagent`
- ユーザーへの質問：**必ず `ask_questions`（Antigravity 組み込みの `ask_question`）ツールを使用すること**

### 2.3 クロスプラットフォーム（Windows / Linux）の互換性確保
- **パス表記の統一:** スキル内の指示やスクリプト参照パスは、OSを問わず機能するようスラッシュ（`/`）区切りの相対パス（例：`.agents/scripts/call_argon.py`）で統一すること。ホームディレクトリを参照する場合は、Python の `pathlib.Path.home()` 等を用いて Windows（`C:\Users\<User>`）と Linux（`/home/<user>`）の双方で解決できるようにすること。
- **シェルコマンドの中立化:** `run_command` で実行を指示するコマンドは、特定のシェル（PowerShell専用構文やBash専用構文）に過度に依存しないように記述するか、OSに応じた実行方法（`python` または `python3` / `uv run` 等）を柔軟に選択できるよう明記すること。

### 2.4 ドキュメント参照先と用語の統一
- `CLAUDE.md` への参照・書き込み指示がある場合は、`AGENTS.md` または `GEMINI.md` を優先するように修正すること。
- v1.3 以降の仕様に合わせ、`CONTEXT.md` への参照が残っている場合はすべて `GLOSSARY.md` に統一すること。
- インタビュー系プリミティブスキル（`grilling`、`grill-me`、`grill-with-docs`、`to-spec`、`triage` 等）において、チャットテキストで直接質問を投げるのではなく、**必ず1問ずつ `ask_questions`（`ask_question`）ツールを呼び出してユーザーの回答を待つ**ように書き換えること。

---

## 3. 個別要件：`setup-matt-pocock-skills` の拡張仕様
初期セットアップを担う `setup-matt-pocock-skills`（`setup-mattpocock`）スキルの `SKILL.md` を改修し、リポジトリのセットアップ実行時（`AGENTS.md` / `GEMINI.md` や `docs/agents/` 配下の生成時）に、以下の **3つの必須ルール** をプロジェクトの共通規約として書き込むようにすること。

### 追加記述する3つの必須ルール
1. **完全日本語対応:**
   - ユーザーへの質問、選択肢の提示、解説、回答、および生成するドキュメント（仕様書・チケット・ADR・用語集など）は**すべて日本語で記述すること**。
2. **質問ツールの強制使用:**
   - ユーザーに確認や質問を行う際は、通常のテキスト出力で済ませず、**必ず `ask_questions`（Antigravity 組み込みの `ask_question`）ツールを使用すること**。
3. **複雑な問題における `gemini-4-argon` 外部スクリプト呼び出し:**
   - アーキテクチャの深い設計、難解なバグの原因特定、複数モジュールに跨る仕様策定など「複雑な問題」だとエージェントが判断した場合、自身のループだけで解決しようとせず、**`GEMINI_API_KEY` の記述場所を確認した上で、それを用いて `gemini-4-argon` を呼び出す Python スクリプト（`.agents/scripts/call_argon.py`）を `run_command` ツール経由で実行し、その推論結果を取得して活用すること**。

---

## 4. 追加実装要件：`gemini-4-argon` 呼び出し用 Python スクリプトの作成
上記の「ルール3」を Windows / Linux 両環境の全スキルから共通して実行できるよう、以下の仕様でヘルパースクリプトを作成し、`setup-matt-pocock-skills` のセットアップ項目に組み込むこと。

### 4.1 APIキー（`GEMINI_API_KEY`）の記述場所の定義（クロスプラットフォーム対応）
スクリプトおよびエージェントは以下の優先順位で `GEMINI_API_KEY` を探索・参照するものとし、その旨を `AGENTS.md`（または `docs/agents/` 内の設定ファイル）に明記すること。
1. プロジェクトルートの `.env` ファイル内の `GEMINI_API_KEY`
2. OSの環境変数 `GEMINI_API_KEY`（Linux の `export GEMINI_API_KEY=...` や Windows のユーザー環境変数）
3. ユーザーホーム配下のグローバル設定 `~/.gemini/.env`（`pathlib.Path.home() / ".gemini" / ".env"`）内の `GEMINI_API_KEY`

### 4.2 スクリプトの配置と仕様
- **配置パス:** `.agents/scripts/call_argon.py`
- **クロスプラットフォーム対応:**
  - ファイル先頭に `#!/usr/bin/env python3`（Shebang）を記述し、改行コードは `LF` とすること。
  - Linux 環境では実行権限（`chmod +x`）の付与または `python3 .agents/scripts/call_argon.py`、Windows 環境では `python .agents/scripts/call_argon.py` で実行できるよう、呼び出し手順をスキル内に明記すること。
  - 標準入出力のエンコーディングは OS に依存せず UTF-8 で統一すること（`sys.stdout.reconfigure(encoding='utf-8')` 等を実装）。
- **使用ライブラリ:** Google 公式 SDK `google-genai`（`from google import genai`）および `python-dotenv` を使用すること。（※ `uv run` が使える環境にも対応できるよう、PEP 723 のインラインスクリプトメタデータ `# /// script` で依存パッケージ `google-genai`, `python-dotenv` をファイル先頭に記載しておくとなお良い）
- **モデル指定:** `gemini-4-argon` を指定すること。
- **入出力仕様:**
  - コマンドライン引数（プロンプト文字列、またはコンテキストファイルのパス）を受け取る。
  - システムプロンプトとして「日本語で論理的かつ詳細な設計・解決策を回答すること」を設定する。
  - 標準出力に `gemini-4-argon` の回答を出力し、呼び出し元の Antigravity エージェント（Desktop / IDE / CLI `agy`）が結果を読み取れるようにする。

---

## 5. エージェントへの作業手順（実行ステップ）
この要件定義書を読み込んだ Antigravity エージェントは、以下の順序で作業を進めること。

1. **現状調査:** リポジトリ内の全スキル一覧と `setup-matt-pocock-skills` の内容を確認する。
2. **不明点の確認:** 作業方針に疑問がある場合は、早速 **日本語で `ask_questions`（`ask_question`）ツールを使って** ユーザーに確認する。
3. **Python スクリプトの実装:** `.agents/scripts/call_argon.py` をクロスプラットフォーム仕様で作成し、動作確認を行う。
4. **`setup-matt-pocock-skills` の改修:** 本要件の3つのルールとスクリプト呼び出し手順が `AGENTS.md` / `GEMINI.md` および `docs/agents/` に出力されるよう `SKILL.md` を更新する。
5. **全スキルのレビューと一括改修:** 各スキルの `SKILL.md` を巡回し、Antigravity 用ツール名への置換、日本語化指示、`ask_questions`（`ask_question`）の強制、OS非依存のパス表記への修正、および複雑タスク時の `call_argon.py` 呼び出しフック（特に `improve-codebase-architecture`、`diagnosing-bugs`、`to-spec`、`grill-with-docs` 等の高負荷スキル）を追記する。
6. **完了報告:** 変更したファイルの一覧と、Windows / Linux（CLI）双方での使い方を日本語で報告する。
