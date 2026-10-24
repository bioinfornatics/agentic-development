# Connecting tasks, commits and sessions

These integrations are optional. Verify their tools and permissions in the
current project; their presence proves neither activation nor compatibility.

## Beads: recover the work

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
