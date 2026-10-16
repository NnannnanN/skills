Skills are organized into bucket folders under `skills/`:

- `engineering/`: daily code work
- `productivity/`: daily non-code workflow tools
- `misc/`: kept around but rarely used, not promoted
- `in-progress/`: beta: public on purpose, feedback wanted, not shipped in the plugin
- `deprecated/`: no longer used

Every skill in `engineering/` or `productivity/` (the **promoted** buckets) must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`'s `skills` array (the Claude Code plugin ships exactly the promoted set). Skills in `misc/`, `in-progress/`, and `deprecated/` must not appear in either.

Install commands are copied verbatim from [.agents/install-block.md](./.agents/install-block.md). `.claude-plugin/marketplace.json` is the repo's own marketplace. Every agent except Claude Code installs from it to get automatic updates, and Claude Code uses `claude-plugins-official`. Run `claude plugin validate . --strict` after touching either manifest. [ADR 0002](./.agents/adr/0002-ship-as-a-claude-code-plugin.md) records why.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`. The promoted buckets' `README.md`s and the top-level `README.md` group entries into **User-invoked** and **Model-invoked**; non-promoted bucket `README.md`s (`misc/`, `in-progress/`) use a flat list.

Skills in `engineering/` and `productivity/` also have a human-facing docs page at `docs/<bucket>/<skill-name>.md` (the docs tree mirrors those two bucket folders under `skills/`). The published URL is `https://aihero.dev/skills-<skill-name>` regardless of bucket: the docs path is repo organisation only. When you add, rename, or change the behaviour of a skill in `engineering/` or `productivity/`, create or re-sync its docs page following [.agents/writing-docs.md](./.agents/writing-docs.md). A finished page carries four sections: **What it does**, **When to reach for it**, **Common questions**, and **It's working if**. `writing-docs.md` holds the template, the section order, and where to hunt for the questions. Skills in the non-promoted buckets (`misc/`, `in-progress/`, `deprecated/`) get **no** docs page. The one exception is a promoted skill removed outright: its page stays, marked archived (see `writing-docs.md`).

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

[`ask-matt`](./skills/engineering/ask-matt/SKILL.md) is the router that maps every user-reachable skill and how they relate. The same trigger that re-syncs a docs page applies to it: whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read `ask-matt`'s `SKILL.md` and update it so the map stays accurate: a new skill it never mentions, or a stale one it still routes to, is a router that lies.

To (re)link every skill outside `deprecated/` and `misc/` into the workspace skill directory (`.agents/skills`) and the local harness skill directories (`~/.claude/skills`, `~/.agents/skills`), run `python3 scripts/link-skills.py` on Linux/macOS or `python scripts/link-skills.py` on Windows (or `scripts/link-skills.sh` on POSIX). Each entry is a symlink (or junction/copy on Windows) into this repo, so a `git pull` keeps installed skills current; re-run the script after adding, removing, or renaming a skill.

No em-dashes anywhere in this repo's prose (`SKILL.md` files, docs, `README.md`, `CHANGELOG.md`, ADRs, changesets, code comments). Where a sentence reaches for one, rewrite it instead with a comma, colon, period, parentheses, or a conjunction, whichever the sentence actually wants; never do a blind character substitution.

## Agent skills

### Triage labels

Canonical names, unchanged. See `docs/agents/triage-labels.md`. Issues are judged against [`SCOPE.md`](./SCOPE.md).

### Antigravity & AI Studio (`gemini-4-argon`) 必須ルール

1. **完全日本語対応**: ユーザーへの質問、選択肢の提示、解説、回答、および生成するドキュメント（仕様書・チケット・ADR・用語集など）はすべて日本語で記述すること。
2. **質問ツールの強制使用**: ユーザーに確認や質問を行う際は、通常のテキスト出力で済ませず、必ず1問ずつ Antigravity 組み込みの `ask_question` ツールを使用すること。
3. **複雑な問題における `gemini-4-argon` 外部スクリプト呼び出し**: アーキテクチャの深い設計、難解なバグの原因特定、複数モジュールに跨る仕様策定など「複雑な問題」だと判断した場合、`GEMINI_API_KEY`（1: `./.env`、2: OS環境変数 `GEMINI_API_KEY`、3: `~/.gemini/.env`）を確認した上で、`.agents/scripts/call_argon.py` を `run_command` ツール経由で実行し、その推論結果を取得して活用すること。詳細は [`docs/agents/antigravity.md`](./docs/agents/antigravity.md) を参照。
