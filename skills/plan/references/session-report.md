## Mandatory session-end report and restart prompt

Contract ID: agentic-development/session-report
Contract version: 1.0.0

Before a planned session end, explicit wrap-up request or recommended context
transition emit the full session summary. A normal phase checkpoint does not
mean the session ended. Announce foreseeable transitions early. Summarize the
session's purpose, not merely its last tool operation. Persist the handoff only
in an approved workspace, or provide it inline and say not saved. Abrupt
interruptions cannot guarantee reporting; use durable checkpoints when possible.
Do not claim automatic session detection, creation or renaming.

Required session-end fields, translated into the user's language:
- Purpose: problem/feature, expected user value and original session objective.
- Roadmap: milestone / epic / US / slice and verified linked tasks.
- Phase reached, accepted outcomes, unfinished work and blockers.
- Agent-owned changes and reasons; preserved pre-existing paths/hunks.
- Evidence: actual checks, candidate identity, artifacts, results and limits.
- Judgment: scoped verdict and reviewer independence.
- Score: rubric ID/version and selected mode; numerical values when applicable, not-applicable in small-task mode, or not assessed.
- Insights: observed / inferred / to-verify; uncertainties and risks.
- Preserved state: root, branch, actual commits, staged/unstaged/untracked work.
- Resume conditions: ownership conflicts, stale proofs, prerequisites, permissions.
- Next-session proposed name: <US/slice> — <next phase/action> — <expected outcome>.
- Next-session goal: one coherent objective.
- Linked tasks: verified ID, title, status, dependency/blocker and expected result.
- Immediate next action, expected result and prerequisites.
- Actual handoff location, or inline / not saved.
- A copy-ready standalone restart prompt, not a promise to write it later.

Always propose a concise descriptive next-session name. If fully complete, state
that no continuation is required and make any review/next-goal suggestion optional;
do not invent unfinished tasks. List only verified task IDs. Unavailable tracking
is unknown; suggested new tasks are proposed without fictitious IDs. Follow the
project tracker when required; the handoff is not a competing task database.

The actual restart prompt must work without the previous conversation. Include
objective, roadmap, verified tasks and blockers, repository/branch/candidate,
actual artifact paths to read (or necessary inline context if not saved), accepted
outcomes, remaining work, pre-existing and uncommitted changes to preserve,
evidence limitations/stale checks, historical permission claims with provenance,
currently verified grants and pending permissions, first action,
acceptance criteria and stop conditions. Instruct the next agent to inspect local
instructions, tracker, working tree, current authorization and evidence freshness
before mutation and
resume at the first incomplete phase. Never include secrets or nonexistent paths.
For Judge require a frozen candidate and disclose the independence requirement.

If Judge has not run, report verdict not-run and score not assessed; do not force
a judge or invent a percentage to fill the report. Unknown rubric criteria stay
unknown. Finishing a session does not authorize commit, stash, push or discard.
A proposed name is not an actual session launch or rename.


## Durable restart record

Link the verified owning Beads task (when used), Git candidate/commits and optional
observed Entire session/checkpoints without assuming a one-to-one relationship.
Store in task notes: Result; Criteria checked; Commands and actual results; Commits;
Entire checkpoints; Sessions; Limits and restart action. Use unavailable or unknown
with a reason instead of invented IDs. Verify the saved task update before claiming
handoff persistence. Check dependency readiness again on resume; claims are not locks.

The task ID alone must lead to the objective, requirement, scope, dependencies,
verification, candidate/evidence locators and first restart action. Keep the copy-ready
prompt as a handoff, not a competing status database or a source of renewed permission.
If a commit, tracker update or context capture is incomplete, preserve the successful
parts, state the exact failed step and continue only within current authority.
