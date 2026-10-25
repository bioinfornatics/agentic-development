# Connecting tasks, commits and sessions

Adopting these integrations is conditional. In a project using Beads, its task
tracking contract is mandatory; missing access or a failed claim blocks implementation.
Verify tools and permissions; presence proves neither activation nor compatibility.

## Beads: recover the work

Turn the user prompt into a task with objective, scope, criteria and restart context
(or reuse an existing matching task), with authorized tracker writes. After execution,
record evidence, status, blockers and next action in Beads. Give the next session a
restart prompt containing the verified task ID; it must reread the task before work.
The prompt transfers intent and references, not authoritative task status.

In a project using Beads, consult local guidance, the task, its owner
and dependencies before writing. Verify the result of claiming it;
an assigned task is not a file lock.

The task must be sufficient to recover objective, scope, criteria, inputs, verification
and restart context. Keep results and useful links in the tracker. A parent expresses
hierarchy; a dependency expresses a prerequisite. Do not duplicate status in
another Markdown notebook. Do not reinitialize an existing workspace.

## Git: record an explainable change

Before an action, check repository, branch, index and pre-existing work.
Announce the proposed branch or commit and its permissions. A branch may
cover several related tasks; a task may produce several commits.

Before an authorized commit, inspect the exact staged files and hunks.
After success, record the hash, message and paths actually committed, then link
the result to the task. If the tracker cannot be updated, say so and
retain the commit with a restart action. Do not claim that the handoff
has been recorded. Do not push automatically.

## GitHub CLI: review and check CI

Use GitHub CLI (`gh`) when the project is hosted on GitHub and terminal-based
PR management is useful. It is optional, not a dependency of the Skills.
Check the authenticated account with `gh auth status` and confirm the intended
repository before remote actions. Use `gh pr view` to inspect a PR and
`gh pr checks` to inspect its CI results; a green CI result is evidence,
not acceptance. Create a PR with `gh pr create` only with scoped authority,
a reviewed diff, and the correct base branch. Do not automatically authenticate,
push, merge, or change repository settings.

## Sessions and Entire: transfer context

Keep implementation, tests and related corrections in the same session while
the objective remains clear. Recommend a fresh session for an independent objective,
a different repository, stale hypotheses or judgment requiring a separate context.
A commit or compaction alone does not require a new session.

At a session boundary, provide: objective, task, candidate, files to preserve,
evidence and limits, permissions to revalidate, next action and a self-contained prompt.
Give the next session a proposed name and goal; state whether it has
actually been launched. A handoff grants no new permission.

Entire is optional context capture, not the tracker or judge.
Verify its configuration and agent integration. Report only sessions
and checkpoints actually observed; if it is unavailable, explain why.
Do not invent a link to a commit or add a fake trailer.

## Goose hooks: observe events

Hooks execute local scripts. Reread the Goose documentation and test
the version actually used, rather than assuming support from the standard.
The plugin groups its rules in **hooks/hooks.json** and their handler in
**scripts/observe.py**, alongside its skills. No adapter or second manifest.
The observer does not modify Git, Beads or Entire. It observes events and report
structure without judging content. Source presence is not an installation.
Before activation, review scripts, dependencies, privacy and configuration;
consult the [hook guide](../hooks/README.md).

Do not confuse an observation hook with a security safeguard, independent
acceptance or an automatic session launcher.

Reference: [official Goose hook documentation](https://goose-docs.ai/docs/guides/context-engineering/hooks).

## Evaluate a commit after task closure

After each newly confirmed Beads closure, evaluate the associated source changes.
Choose perform when a coherent verified diff and scoped commit authority exist;
propose when authority is missing; skip when already committed or no source diff
exists; blocked when ownership, checks or capability prevent a safe commit.
Record the reason in the final explanation and a real hash only after success.
Closure is not permission to commit, and no automatic push or Dolt sync follows.
