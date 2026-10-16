# Skills (Google Antigravity + AI Studio 対応版)

実践的なソフトウェアエンジニアリングとワークフローのためのエージェントスキル集です。**Google Antigravity CLI (`agy`)** および **Antigravity 2.0 (Desktop / IDE)** と、Google AI Studio（`gemini-4-argon`）のハイブリッド環境（Windows / Linux / macOS）に最適化されています。

---

## インストール方法（Antigravity CLI / Antigravity 2.0）

### 1. `npx skills` でインストール（推奨）

導入したいプロジェクトのディレクトリ（またはグローバル `-g`）で以下のコマンドを実行します。

```bash
npx skills@latest add NnannnanN/skills -a antigravity
```

- **Antigravity CLI (`agy`) や Antigravity 2.0 内のターミナル**で実行する場合は、環境が自動検出されるため `-a antigravity` を省略して `npx skills@latest add NnannnanN/skills` だけでもインストールできます。
- インストールするスキルを選択するプロンプトが出た場合は、初期設定用の `setup-matt-pocock-skills` を含めてください。
- **アップデート方法**:
  ```bash
  npx skills@latest update
  ```
  （※新しいスキルが追加された場合は、再度 `npx skills@latest add NnannnanN/skills -a antigravity` を実行してください。）

<details>
<summary><strong>リポジトリを直接 git clone してリンクする場合（開発・カスタマイズ向け）</strong></summary>

本リポジトリをクローンして直接編集・管理したい場合は、同梱のスクリプトで `.agents/skills/` および `~/.agents/skills/` にシンボリックリンク（Windows ではジャンクションまたはコピー）を作成できます。

```bash
git clone https://github.com/NnannnanN/skills.git
cd skills

# Linux / macOS
python3 scripts/link-skills.py

# Windows
python scripts/link-skills.py
```

</details>

### 2. Antigravity 各サーフェスでの確認

- **Antigravity CLI (`agy`)**:
  ターミナルで `agy` を起動し、`/` を入力するとインストールされたスキル（`/ask-matt`, `/grill-with-docs` 等）を呼び出せます。
- **Antigravity 2.0 (Desktop / IDE)**:
  左サイドバーの「Skills & Customizations」パネル、またはチャットキャンバスで `/`（スラッシュコマンド）を入力するとスキル一覧が表示されます。

---

## 初期設定と使い方

### 1. リポジトリごとの初期セットアップ（`/setup-matt-pocock-skills`）

新しい開発リポジトリで最初に1回、Antigravity 上で `/setup-matt-pocock-skills` を実行してください。対話形式（`ask_question` ツール）で以下を設定し、`AGENTS.md`（または `GEMINI.md`）、`docs/agents/`、および `.agents/scripts/call_argon.py` を自動生成します。

- **Issue トラッカー**: GitHub Issues、GitLab Issues、ローカル Markdown（`.scratch/`）など
- **トリアージラベル**: `/triage` で使用する5つの状態ラベル名
- **ドメインドキュメント構成**: `GLOSSARY.md`（用語集）および `docs/adr/` の配置ルール
- **Antigravity 3大必須ルール**: 完全日本語対応、`ask_question` ツールの強制使用、複雑タスク時の `call_argon.py` 呼び出しルール

### 2. `GEMINI_API_KEY` の設定（オプション: `gemini-4-argon` 外部推論用）

アーキテクチャの深い設計や難解なバグの診断など高負荷な局面で、エージェントは `.agents/scripts/call_argon.py` を経由して `gemini-4-argon` を呼び出します。
（※未設定の場合でも、エージェントは現在選択されているモデルのまま作業を継続します。）

以下のいずれか1つに `GEMINI_API_KEY` を設定してください（上から優先して探索されます）。

1. **プロジェクトルートの `.env` ファイル**: `./.env` 内に `GEMINI_API_KEY=AIza...` を記述
2. **OSの環境変数**: `export GEMINI_API_KEY=AIza...`（Linux/macOS）またはユーザー環境変数（Windows）
3. **ユーザーホーム配下のグローバル設定**: `~/.gemini/.env`（Windows: `C:\Users\<User>\.gemini\.env`、Linux: `/home/<user>/.gemini/.env`）

設定確認コマンド:

```bash
# Linux / macOS
python3 .agents/scripts/call_argon.py --check-key

# Windows
python .agents/scripts/call_argon.py --check-key
```

### 3. 基本的な開発ワークフロー

どのスキルを使うか迷ったときは、**`/ask-matt`** を実行すると現在の状況に最適なスキルやワークフローを日本語で案内してくれます。代表的な流れは以下の通りです。

```
[要件の明確化]
  /grill-with-docs  (1問ずつのインタビューで設計ツリーを詰め、GLOSSARY.md / ADR を更新)
        │
        ▼
[仕様化 & チケット分割]
  /to-spec          (対話内容から仕様書 Spec を作成し Issue に公開)
        │
  /to-tickets       (依存関係グラフを持つ Tracer Bullet チケット群に分割)
        │
        ▼
[実装 & レビュー]
  /implement        (チケット単位の実装: 内部で /tdd と /code-review を自動実行)
    または
  /implement-spec   (並列サブエージェントで仕様全体を一気に実装・統合)
        │
        ▼
[振り返り & 環境改善]
  /retro            (セッションの振り返りを行い、Linter・規約・ツールを改善)
```

---

## スキル一覧（リファレンス）

スキルは起動方法によって2種類に分かれます。
- **User-invoked**: ユーザーが `/skill-name` と入力したときのみ起動するオーケストレーション用スキルです。
- **Model-invoked**: ユーザーが直接呼び出すことも、タスクに応じてエージェントが自律的に参照・起動することもできるスキルです。

### Engineering（日々のコード開発用スキル）

**User-invoked**

- **[ask-matt](./skills/engineering/ask-matt/SKILL.md)**: 今の状況にどのスキルやワークフローが適しているかを相談できるルータースキル。
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: 計画や設計を徹底的にインタビュー（グリル）しながら、プロジェクトの `GLOSSARY.md`（用語集）や ADR をリアルタイムに構築・更新する。
- **[triage](./skills/engineering/triage/SKILL.md)**: Issue や外部 PR をトリアージの状態マシンに沿って分類・検証・グリルし、エージェントが実装可能なブリーフを作成する。
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: コードベースを走査してモジュールを深める（Deepening）機会を洗い出し、ビジュアルな HTML レポートとして提示した上で、選択した候補をグリルする。
- **[setup-matt-pocock-skills](./skills/engineering/setup-matt-pocock-skills/SKILL.md)**: リポジトリの Issue トラッカー、トリアージラベル、ドメインドキュメント構成、Antigravity 必須ルールを初期設定する（リポジトリごとに初回1回実行）。
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: これまでの対話内容とコード理解を統合して仕様書（Spec）を作成し、Issue トラッカーへ公開する。
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: 計画や仕様書を、ブロッキング依存関係を持つ Tracer Bullet（垂直スライス）チケット群に分割して公開する。
- **[implement](./skills/engineering/implement/SKILL.md)**: 仕様書やチケットに基づき、合意した Seam（境界）での `/tdd` と完了後の `/code-review` を回して機能を実装・コミットする。
- **[implement-spec](./skills/engineering/implement-spec/SKILL.md)**: 仕様書に紐づくチケット群をタスクグラフとして読み込み、並列サブエージェントで実装・マージして単一の統合ブランチ上で完結させる。
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: 1セッションに収まらない大規模・不確実な取り組みを、Issue トラッカー上の「意思決定チケットの共有マップ」として計画し、1つずつ解決して道筋を明確にする。
- **[retro](./skills/engineering/retro/SKILL.md)**: コーディングセッションを振り返り、ナビゲーション・自動チェック・コーディング規約・ツールなどエージェント環境の改善点を重要度順に提案する。

**Model-invoked**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: 設計上の疑問に答えるための使い捨てプロトタイプ（状態・ロジック検証用の単一 HTML ファイル、または複数 UI バリエーションの切り替え画面）を作成する。
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: 難解なバグやパフォーマンス劣化に対する規律ある診断ループ（確実に Red になるフィードバックループ構築 → 最小化 → 仮説立案 → 計測 → 修正と回帰テスト）。
- **[research](./skills/engineering/research/SKILL.md)**: 信頼性の高い一次情報源（公式ドキュメント・ソースコード・仕様）をバックグラウンドのサブエージェントで調査し、出典付きの Markdown ファイルとして保存する。
- **[tdd](./skills/engineering/tdd/SKILL.md)**: Red-Green ループによるテスト駆動開発。公開インターフェースの Seam（境界）に対して1スライスずつテストファーストで実装する。
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)**: 用語の曖昧さや矛盾を指摘し、エッジケースのシナリオで検証しながら `GLOSSARY.md` と ADR をインラインで構築・洗練させる。
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: Deep Module（小さなインターフェースの背後に多くの実装を隠蔽し、明確な Seam でテスト可能にする設計）のための共通語彙と原則。
- **[code-review](./skills/engineering/code-review/SKILL.md)**: 指定した基準点からの差分を **Standards**（コーディング規約 + Fowler のコードスメル）と **Spec**（仕様との整合性）の2軸の並列サブエージェントでレビューする。
- **[pr](./skills/engineering/pr/SKILL.md)**: 変更の要点を最小限の図やツリーで示す Summary、変更前後の Evidence、Merge Danger（One-way / Two-way door と影響範囲）を備えた PR 本文を作成する。
- **[wizard](./skills/engineering/wizard/SKILL.md)**: インフラ構築、認証情報や CI シークレットの設定、外部ダッシュボード操作など、人間にしか行えない手順を段階的に案内する対話型 Bash ウィザードを生成する。

### Productivity（汎用ワークフロー・思考整理スキル）

**User-invoked**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: 計画や設計について、設計ツリーのすべての分岐が解決するまで1問ずつ徹底的にインタビュー（グリル）を行う（ファイル保存を伴わないステートレス版）。
- **[handoff](./skills/productivity/handoff/SKILL.md)**: 現在のセッションの文脈を要約し、別のエージェントや次のセッションが作業を引き継げるハンドオフ用ドキュメントを一時ディレクトリに生成する。
- **[teach](./skills/productivity/teach/SKILL.md)**: カレントディレクトリをステートフルな学習ワークスペースとして使用し、複数セッションにわたって新しいスキルや概念を段階的にレクチャーする。
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)**: 自分だけでは判断できない事項について、知識を持つ相手（誰に送り、何を得る必要があるか）をヒアリングし、非同期または会議で回答してもらうための質問票 Markdown を作成する。
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**: エージェントの直前の説明が分かりにくかったときに実行し、`GLOSSARY.md` の用語を使って平易で明快な日本語で説明し直させる。

**Model-invoked**

- **[grilling](./skills/productivity/grilling/SKILL.md)**: 計画・意思決定・アイデアの設計ツリーを1問ずつ（`ask_question` ツールで推奨回答付きで）掘り下げて合意形成するインタビューの基本プリミティブ。
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**: `SKILL.md` や `AGENTS.md` / `GEMINI.md` など、エージェントが読み込むドキュメントを予測可能かつ高効率に記述するためのリファレンス。
