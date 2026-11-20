# Conditional Beads integration v1.5.0

Contract ID: agentic-development/beads-integration
Contract version: 1.5.0
Apply only when the repository uses Beads; this is a bridge, not a CLI manual.

## Obtain current operating instructions

- Verify the intended repository/workspace and installed `bd` capability. Use local Beads guidance and fresh injected context; run `bd prime` only when missing or stale. Read the complete output; use `bd <command> --help` as needed. Empty prime output does not prove an empty database: see `bd where`.
- Current user/project permissions override suggested prime close/Git/sync steps. Loading this bridge never authorizes installation, initialization or hooks.

## Connect the phase to task truth

- Read the actual task and blockers before choosing work; verify ownership/claim before implementation. Missing access or a failed claim is a blocker: never work untracked or invent IDs; return the exact prerequisite.
- Beads owns status, dependencies and durable follow-up; phase artifacts and restart prompts supply evidence, not a competing task database. One coordinator owns updates per issue; workers return findings and evidence. A claim grants neither file ownership nor Git authority.
- Keep description structured, criteria in the acceptance field, results in notes; apply ticket authoring before repairs. When authorized, record progress, proof locators, blockers and restart action; verify updates/closure by readback. Preserve incomplete work.
- Close a task only with Test evidence, a Judge `accepted` verdict for that exact candidate and current closure authority; otherwise it stays open and its notes get the named blocker and restart action. Passing tests, session end or a commit does not approve a parent/US/release.
- List batch WIP with `bd list --status in_progress --parent <epic>` and ready work with `bd ready --parent <epic>`. Record discovered work as an open follow-up with `bd create ... --deps discovered-from:<id>`; never claim it or add it to the active batch.
- Release a blocked batch task with `bd update <id> --status open --assignee ""`; record its named blocker (native dependency edge when one exists) and restart action; other batch tasks continue.

## Post-closure commit evaluation

- After each confirmed closure, report perform / propose / skip / blocked, accounting for already committed work. Evaluation is not permission: perform only under a verified standing Git autonomy grant (Level 1 commit, Level 2 fast-forward push of a covered branch) with exact owned/staged paths and verified receipts. Never auto-push otherwise; publication needs separate scoped authority. Snapshot and Dolt push follow Persistence checkpoints below. Report local-only or failed persistence honestly.

## Persistence checkpoints

- Checkpoints: after each confirmed task or epic closure, and before a handoff or session end. Report each action below as perform / propose / skip / blocked. Perform only under a verified Beads sync grant (see the authorization policy) or current per-action authority for that command; otherwise propose the exact command.
- JSONL snapshot: only when `git ls-files .beads/issues.jsonl` shows the file tracked; if it is not tracked, skip and propose no snapshot commit. Run `bd export -o .beads/issues.jsonl` (memories stay excluded: no `--include-memories` or `--all`), review the diff for secrets or private data, then stage that path alone and commit it as `chore(beads): snapshot (<IDs>)` after any task commit, on the current working branch, never directly on `develop`, `main`, the default or a release branch; on such a branch report blocked and propose the commit on a working branch. If export, staging or commit fails (including a hook failure or unexpected staged paths), stop and report blocked; never retry with `--no-verify` or force. JSONL is an export, not task truth or a Dolt backup: never edit or import it to sync status. Pushing the snapshot commit follows the Git grant (Level 2), not this checkpoint.
- Dolt push: only when `bd dolt remote list` shows a remote; with none, report local-only. At epic closure, handoff or session end, commit pending Dolt changes with `bd dolt commit` if bd reports any, then run `bd dolt push` to the existing remote. Never `--force`, add or change remotes, or `bd dolt pull` to resolve a conflict; on rejection, divergence or authentication failure, stop and report the remote state and the decision needed.
