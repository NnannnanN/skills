---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Use `view_file` to read both `.agents/skills/grilling/SKILL.md` and `.agents/skills/domain-modeling/SKILL.md`, and follow their instructions together.

## Session Conclusion & Next Step

The session is done when the interview frontier is empty: every branch of the design tree visited, terms recorded in `GLOSSARY.md`, ADRs created if qualified, and a shared understanding is reached.

When confirming completion with the user via `ask_question`:
- Do NOT ask open-ended questions like whether to proceed to implementation or continue grilling.
- The standard next step in the main build chain (`grill-with-docs → to-spec → to-tickets → implement`) is `/to-spec`. Always ask via `ask_question` whether the user wants to proceed to `/to-spec` in the same conversation.
- Format the options with the primary choice recommended:
  1. `(Recommended) /to-spec を実行して仕様書を作成する`
  2. `まだ確認したい点があるのでグリルを続ける`
  3. `仕様書を作らずに直接実装（/implement）に進む`

## Antigravity & AI Studio (`gemini-4-argon`) Conventions

- **Output language**: Conduct all interviews, explanations, and document updates (`GLOSSARY.md` and ADRs) in **Japanese**.
- **Questions**: Ask every question one at a time using the built-in `ask_question` tool (never plain chat text).
- **Deep architectural reasoning (`gemini-4-argon`)**: When evaluating complex multi-module design trade-offs or thorny domain boundaries during the interview, invoke `.agents/scripts/call_argon.py` via `run_command` (after verifying `GEMINI_API_KEY` in `./.env`, the `GEMINI_API_KEY` environment variable, or `~/.gemini/.env`):
  - `uv run .agents/scripts/call_argon.py "<design question>" -f GLOSSARY.md` (or `python3 .agents/scripts/call_argon.py ...` on Linux/macOS, `python .agents/scripts/call_argon.py ...` on Windows).

