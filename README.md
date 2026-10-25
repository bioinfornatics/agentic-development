# Agentic Development

AI coding agents can lose context, drift beyond scope, and mistake passing tests for completed work.
**Agentic Development gives them a repeatable workflow: clear goals, bounded changes, verifiable evidence, and explicit handoffs.**

## Start with one change

Read the [getting started guide](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/getting-started.md), then give your agent a concrete outcome:

> Use Agentic Development to deliver this change: [desired behavior].
> Clarify scope and acceptance criteria before editing. Verify the result,
> report remaining risks, and ask before actions that need my approval.

## What you get

Seven reusable Skills guide the work:

**Cycle → Research → Plan → Implement → Test → Judge → Iterate**

- Keep requirements, decisions, and restart context explicit.
- Make small, reviewable changes with checks tied to the requested behavior.
- Separate test results from acceptance; report missing evidence instead of claiming completion.

Use the whole cycle or the phase your task needs. These are agent instructions,
not an enforcement engine or a guarantee of correct software.

## Dependencies and optional tools

The Skills are Markdown instructions: use an agent that can load them and your
project's own development tools. No package installation or build is required for the Skills.

| Tool | Why use it? | How it fits into the workflow |
| --- | --- | --- |
| Git | Preserve reviewable source history. | Inspect the diff, then commit verified changes when authorized. |
| GitHub CLI (`gh`), optional | Manage GitHub reviews from the terminal. | Verify the account and repository; create or inspect PRs and check CI results. |
| Beads (`bd`), optional | Recover task scope, ownership, dependencies, and progress across sessions. | Read and claim the task before editing; record results and the next action in the existing tracker. |
| Entire, optional | Capture session context and connect it to checkpoints. | Verify support for your agent and worktree; link only observed session/checkpoint IDs to the task. |

Without these integrations, keep an explicit task brief and handoff. Entire does
not replace task tracking or acceptance, and no tool grants permission to commit,
push, or close tasks. Optional observation hooks require Python 3.10+ only.
See the [integration guide](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/integrations.md) for setup checks and boundaries.

## Learn more

- [Development cycle](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/cycle.md): how the phases fit together.
- [Integrations](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/integrations.md): Beads, Git, Entire, and optional Goose observation hooks.
- [Contributing](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/contributing.md): improve the method on develop.

The main branch contains the generated installation package; develop contains
its source and documentation. Both use this same README. Skills need no build;
optional observation hooks require Python 3.10+ and use only the standard library.
