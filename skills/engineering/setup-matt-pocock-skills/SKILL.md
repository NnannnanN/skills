---
name: setup-matt-pocock-skills
description: "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills."
disable-model-invocation: true
---

# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them
- **Antigravity & AI Studio (`gemini-4-argon`) rules**: the 3 mandatory rules (full Japanese output, mandatory `ask_question` tool usage, and `.agents/scripts/call_argon.py` invocation for complex reasoning)

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user using the `ask_question` tool (in Japanese), then write.

## Antigravity Conventions

- **Output language**: Communicate with the user, present choices, and generate all documentation in **Japanese**.
- **Questions**: Always use the `ask_question` tool (one question at a time) instead of asking questions in plain chat text.
- **Built-in tools**: Use `view_file` to read files, `write_to_file` to create files, `replace_file_content` to edit existing files, and `run_command` to execute shell commands.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` at the repo root: does any exist? Is there already an `## Agent skills` section in it?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.agents/scripts/call_argon.py`: does the `gemini-4-argon` helper script already exist?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing in Japanese. Then take the sections in order. One section, one answer via `ask_question`, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer via `ask_question`:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question via `ask_question`:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want via `ask_question`.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `AGENTS.md` / `GEMINI.md` is being edited (see step 4 for selection rules), including the 3 mandatory Antigravity rules
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, `docs/agents/antigravity.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)
- Creating/updating `.agents/scripts/call_argon.py` for cross-platform `gemini-4-argon` API invocation

Confirm with `ask_question` and let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `AGENTS.md` exists, edit it.
- Else if `GEMINI.md` exists, edit it.
- Else if `CLAUDE.md` exists, edit it (or migrate to `AGENTS.md` if requested).
- If none exists, ask the user via `ask_question` whether to create `AGENTS.md` (recommended) or `GEMINI.md`.

Never create a duplicate rules file when `AGENTS.md` or `GEMINI.md` already exists; always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place using `replace_file_content` rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Antigravity & AI Studio (`gemini-4-argon`) 必須ルール

1. **完全日本語対応**: ユーザーへの質問、選択肢の提示、解説、回答、および生成するドキュメント（仕様書・チケット・ADR・用語集など）はすべて日本語で記述すること。
2. **質問ツールの強制使用**: ユーザーに確認や質問を行う際は、通常のテキスト出力で済ませず、必ず1問ずつ Antigravity 組み込みの `ask_question` ツールを使用すること。
3. **複雑な問題における `gemini-4-argon` 外部スクリプト呼び出し**: アーキテクチャの深い設計、難解なバグの原因特定、複数モジュールに跨る仕様策定など「複雑な問題」だと判断した場合、`GEMINI_API_KEY`（1: `./.env`、2: OS環境変数 `GEMINI_API_KEY`、3: `~/.gemini/.env`）を確認した上で、`.agents/scripts/call_argon.py` を `run_command` ツール経由で実行し、その推論結果を取得して活用すること。詳細は `docs/agents/antigravity.md` を参照。
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

When Section B ran on GitHub or GitLab, create each configured label the tracker lacks (`gh label create` / `glab label create`) via `run_command`.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout
- [antigravity.md](./antigravity.md): Antigravity 3 mandatory rules, `GEMINI_API_KEY` resolution priority, and cross-platform `call_argon.py` usage (`docs/agents/antigravity.md`)

Also ensure `.agents/scripts/call_argon.py` is present in the target repository by copying [scripts/call_argon.py](./scripts/call_argon.py) from this skill folder to `.agents/scripts/call_argon.py` (with LF line endings, and running `chmod +x .agents/scripts/call_argon.py` on Linux/macOS).

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user (in Japanese) that the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
