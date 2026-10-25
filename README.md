# Agentic Development

AI coding agents can lose context, drift beyond scope, and mistake passing tests for completed work.
**Agentic Development gives them a repeatable workflow: clear goals, bounded changes, verifiable evidence, and explicit handoffs.**

## Start with one change
Read the [getting started guide](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/getting-started.md), then give your agent a concrete outcome:

> Use Agentic Development to deliver this change: [desired behavior].
> Clarify scope and acceptance criteria before editing. Verify the result,
> report remaining risks, and ask before actions that need my approval.

## What you get
Seven reusable Skills guide the work: six phases and one coordinator.

```text
Goal / need → Research → Plan → Implement → Test → Judge → Scoped acceptance
                                  ↑                 │
                                  └── Iterate ←─────┘
                                      if correction is needed
```

| Phase | Question to resolve | Expected output |
| --- | --- | --- |
| **Research** | What must we understand before deciding? | Cited findings, risks, unknowns, and constraints. |
| **Plan** | What will we deliver, and how will we recognize success? | Scope, acceptance criteria, dependencies, tasks, and review policy. |
| **Implement** | How do we execute the authorized task without scope drift? | A focused diff, preserved existing work, and initial verification evidence. |
| **Test** | What does this exact candidate actually demonstrate? | Criterion-linked checks, observed results, and coverage/environment limits. |
| **Judge** | Is the evidence sufficient to accept this scope? | A verdict on a frozen candidate, evidence-linked findings, and the agreed evaluation mode. |
| **Iterate** | What is the smallest correction that addresses the failures? | Bounded correction, followed by renewed verification and judgment. |

**`cycle` coordinates these transitions:** it selects the needed phase, verifies prerequisites, and prepares resumable handoffs.
Keep requirements, decisions, and restart context explicit; make small, reviewable changes; separate test results from acceptance and report missing evidence. Use the whole cycle or the phase your task needs. These are agent instructions, not an enforcement engine or a guarantee of correct software.

Install: `goose plugin install https://github.com/bioinfornatics/agentic-development.git`.
Check: `goose skills list` — only this plugin’s seven Skills, no evaluation fixtures.
Update: `goose plugin update agentic-development`. See [Goose Plugins](https://goose-docs.ai/docs/guides/context-engineering/plugins) and [Agent Skills](https://goose-docs.ai/docs/guides/context-engineering/using-skills).

## Dependencies and workflow tools
The Skills are Markdown instructions: use an agent that can load them and your project's own development tools. No package installation or build is required for the Skills.

| Tool | Why use it? | How it fits into the workflow |
| --- | --- | --- |
| Git | Preserve reviewable source history. | Inspect the diff, then commit verified changes when authorized. |
| GitHub CLI (`gh`), optional | Manage GitHub reviews from the terminal. | Verify the account and repository; create or inspect PRs and check CI results. |
| Beads (`bd`), required when the project uses it | Recover task scope, ownership, dependencies, and progress across sessions. | Read and claim the task before editing; record results and the next action in the existing tracker. |
| Entire, optional | Capture session context and connect it to checkpoints. | Verify support for your agent and worktree; link only observed session/checkpoint IDs to the task. |

**Handoff:** user prompt → task with scope and acceptance criteria → execution → evidence, status, and next action recorded in Beads → restart prompt with task ID.
The next session rereads the task: Beads is task truth, not the prompt or a notebook.
Beads adoption is conditional; once chosen, missing access or a failed claim blocks implementation, not permission to continue untracked. Without Beads, agree another tracking approach.
Entire captures context, not task truth or acceptance; no tool grants permission to commit, push, or close tasks.
See the [integration guide](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/integrations.md) for setup checks and boundaries.

## Learn more
- [Development cycle](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/cycle.md): how the phases fit together.
- [Integrations](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/integrations.md): Beads, Git, Entire, and optional Goose observation hooks.
- [Contributing](https://github.com/bioinfornatics/agentic-development/blob/develop/docs/contributing.md): improve the method on develop.

The main branch contains the generated installation package; develop contains its source and documentation. Both use this same README. Skills need no build; optional observation hooks require Python 3.10+ and use only the standard library.
