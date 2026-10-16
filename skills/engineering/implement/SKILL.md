---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets. Communicate with the user in **Japanese**.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask via `ask_question`.

Use `view_file` to read `.agents/skills/tdd/SKILL.md` and follow its TDD loop where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end via `run_command`.

Once done, use `view_file` to read `.agents/skills/code-review/SKILL.md` and run a two-axis review of the work.

Commit your work to the current branch.
