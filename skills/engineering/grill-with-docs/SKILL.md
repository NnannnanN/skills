---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Use `view_file` to read both `.agents/skills/grilling/SKILL.md` and `.agents/skills/domain-modeling/SKILL.md`, and follow their instructions together.

## Antigravity & AI Studio (`gemini-4-argon`) Conventions

- **Output language**: Conduct all interviews, explanations, and document updates (`GLOSSARY.md` and ADRs) in **Japanese**.
- **Questions**: Ask every question one at a time using the built-in `ask_question` tool (never plain chat text).
- **Deep architectural reasoning (`gemini-4-argon`)**: When evaluating complex multi-module design trade-offs or thorny domain boundaries during the interview, invoke `.agents/scripts/call_argon.py` via `run_command` (after verifying `GEMINI_API_KEY` in `./.env`, the `GEMINI_API_KEY` environment variable, or `~/.gemini/.env`):
  - `uv run .agents/scripts/call_argon.py "<design question>" -f GLOSSARY.md` (or `python3 .agents/scripts/call_argon.py ...` on Linux/macOS, `python .agents/scripts/call_argon.py ...` on Windows).
