# Conditional Beads integration v1.3.0

Contract ID: agentic-development/beads-integration
Contract version: 1.3.0
Apply only when the repository uses Beads; this is a bridge, not a CLI manual.

## Obtain current operating instructions

- Verify the intended repository/workspace and installed `bd` capability. Use local Beads guidance and
  fresh injected context; run `bd prime` only when missing or stale. Read the complete output; use
  `bd <command> --help` as needed. Empty prime output does not prove an empty database: see `bd where`.
- Current user/project permissions override suggested prime close/Git/sync steps. Loading this bridge
  never authorizes installation, initialization or hooks.

## Connect the phase to task truth

- Read the actual task and blockers before choosing work; verify ownership/claim before implementation.
  Missing access or a failed claim is a blocker: never work untracked or invent IDs; return the exact prerequisite.
- Beads owns status, dependencies and durable follow-up; phase artifacts and restart prompts
  supply evidence, not a competing task database. One coordinator owns updates per issue;
  workers return findings and evidence. A claim grants neither file ownership nor Git authority.
- Keep description structured, criteria in the acceptance field, results in notes; apply ticket authoring
  before repairs. When authorized, record progress, proof locators, blockers and restart action;
  verify updates/closure by readback. Preserve incomplete work.
- Close a task only with Test evidence, a Judge `accepted` verdict for that exact candidate and
  current closure authority; otherwise it stays open and its notes get the named blocker and
  restart action. Passing tests, session end or a commit does not approve a parent/US/release.
- List batch WIP with `bd list --status in_progress --parent <epic>` and ready work with
  `bd ready --parent <epic>`. Record discovered work as an open follow-up with
  `bd create ... --deps discovered-from:<id>`; never claim it or add it to the active batch.
- Release a blocked batch task with `bd update <id> --status open --assignee ""`; record its named
  blocker (native dependency edge when one exists) and restart action; other batch tasks continue.

## Post-closure commit evaluation

- After each confirmed closure, evaluate and report perform / propose / skip / blocked, accounting for
  already committed work. Evaluation is not permission to commit; use the entrypoint-linked commit
  safeguards for exact owned/staged paths and verified receipts. Never auto-push. Git publication and
  Dolt synchronization need separate scoped authority. JSONL is an optional export, not live task truth
  or a Dolt backup; never import/edit it to sync status. Report local-only or failed persistence honestly.
