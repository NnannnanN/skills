---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly in **Japanese** until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask each frontier question **one at a time** using the Antigravity built-in `ask_question` tool (never ask questions as plain chat text). Provide selectable options in Japanese and put your recommended answer first, prefixed with `(Recommended)`. Wait for the user's answer via `ask_question` before asking the next question.

Each answer reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next question via `ask_question`. A question whose answer depends on another question still open belongs to a _later_ step, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), use `view_file` or `run_command`, or dispatch a subagent via `invoke_subagent` to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the subagent to report; ask the rest of the frontier now via `ask_question`. The _decisions_ are the user's: put each to them via `ask_question` and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Confirm with the user via `ask_question` that you have reached a shared understanding before acting on it.
