---
name: claude-handoff
description: Hand the current conversation off to a fresh background agent that picks up the work immediately.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff summary in **Japanese** of the current conversation so a fresh agent can continue the work. Save it to the temporary directory of the user's OS, then launch a background subagent via `invoke_subagent` (in Antigravity) or `claude --bg --name "<descriptive name>" -- "$(cat <summary file>)"` (in Claude Code) seeded with the summary as its prompt. Passing the file keeps the shell from running backticks or expanding `$` in the summary.

Always provide a descriptive role/name (e.g. `Role: "Fix login bug"` in `invoke_subagent`, or `--name "Fix login bug"`).

Include a "suggested skills" section in the summary, naming which skills the next agent should read via `view_file` (`.agents/skills/<name>/SKILL.md`).

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information, since the summary becomes the agent's prompt.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the summary accordingly. (If clarification is needed, ask via `ask_question`.)
