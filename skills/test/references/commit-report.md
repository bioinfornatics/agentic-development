## Mandatory commit report

Contract ID: agentic-development/commit-report
Contract version: 1.0.0

Before a permitted commit announce the problem/feature, intended outcome, exact
owned files/hunks, known checks, limitations and proposed message. Immediately
after each successful agent commit, before another task, emit the report below.
Verify actual commit metadata and its file list; working-tree changes are not
necessarily committed. Include renames/deletions and separate remaining dirty
work and pre-existing user hunks. A failed commit has no invented hash; report
its error and remaining state. Label a recommendation proposed/not performed.
Verify externally observed commits and label them external, without claiming
agent authorship. This contract is not a Git event hook.

Translate these required fields into the user's language:

Default report:
- Commit status: performed / failed / proposed / externally observed.
- Problem or feature; milestone / epic / US / slice / verified linked task IDs.
- Outcome covered and acceptance scope.
- Committed files: + added / ~ modified / - removed / renamed old -> new;
  each path with reason and owned hunks when relevant.
- Checks: evidence IDs, candidate, actual results, mock/real environment.
- Limitations and open criteria.
- Actual hash and message, or not performed / error.
- Remaining staged / unstaged / untracked state and preserved user work.
- Next action, expected result and prerequisites.

Unknown task IDs remain unknown or not-applicable. A commit does not by itself
accept a US or make checks pass. Session closure never grants commit permission.


## Git, Beads and optional Entire linkage

Beads owns task state; Git records source; Entire can capture session context but
cannot grant permissions or acceptance. Include verified task IDs in an authorized
commit message by project convention. After success, inspect the actual hash,
message and committed paths, then update the owning task with result, criteria,
commands/results, commit and remaining work; verify the update independently.
A failed commit has no commit receipt; a failed tracker update leaves durable linkage
incomplete and must be reported with a retry/restart action, not hidden as success.

If Entire is available, inspect its current repository/worktree status and supported
agent integration before relying on it. Record only observed session/checkpoint IDs
and their real commit association. Do not assume any host is supported, enable hooks,
install integration, create checkpoints or forge trailers merely to fill a report.
If disabled, unsupported or inaccessible, report Entire unavailable with the reason;
Git/Beads evidence still stands for its own scope. Never infer checkpoints from hashes.
