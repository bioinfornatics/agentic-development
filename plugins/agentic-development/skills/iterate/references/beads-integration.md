# Conditional Beads integration v1.0.1

## Scope and source

Derived from the project's .agents/skills/beads/SKILL.md: recovery, shared task
truth, inspect/claim lifecycle, durable follow-up, honest completion, JSON and
noninteractive updates. Memory, dependency and sync details below are additional
local AGENTS.md / bd prime guidance, not claims about that Skill's contents.
Apply only when the target repository uses Beads. Do not initialize Beads,
install bd or alter the project's Beads Skill merely because this plugin is loaded.

## Operational source precedence

When a local Beads Skill exists, read it for CLI workflow and recovery procedures,
then use the current bd prime/help for installed-version details. This reference
is the integration contract and contained fallback, not a replacement full CLI
manual. Keep project policy and plugin phase/acceptance rules distinct. Do not
copy procedure blocks into AGENTS.md or CLAUDE.md merely to enable this plugin.
If explicit first-time setup is needed, ask the coordinator to use cycle's
controlled initialization branch; phase workers must not run init themselves.

## Recover before choosing work

Read local instructions and, when available, the local Beads Skill. Check that bd
is available and runs in the intended repository. Run bd prime when its context
is missing or stale, including after a session change or compaction. Hooks may
already inject fresh context; do not repeatedly prime after every tool call.
If prime prints nothing, run bd where to determine whether an active workspace
exists. Empty prime output is not evidence of an empty issue database.

Inspect ready and active work using bd ready and bd list --status=in_progress;
use bd list --status=open for an inventory. An empty ready list does not prove
that no open work exists: inspect blockers and current assignments. Read the
relevant issue with bd show <id> before edits. Do not treat handoff task status
as current without verification against the tracker.

## Shared truth vs artifacts

Beads owns shared tasks, blockers, status, dependencies, durable follow-up and
work another session/agent must resume. Research, plans, evidence indexes, ASCII
sketches and restart prompts are supporting artifacts, not a second task DB.
Link them to verified issue IDs and store actionable remaining work in Beads.
Do not create Markdown TODO lists, TodoWrite or TaskCreate entries as a parallel
source of truth. Local reasoning is not shared project state. Reconcile stale
artifact task status with Beads without silently changing approved acceptance.
If local instructions require all task tracking in Beads, do not use competing
local trackers even temporarily.

## Inspect, claim and coordinate

Reuse an existing matching issue after inspection rather than create duplicates.
Before implementation, create a missing task with bd create (title, description,
type and numeric priority) when authorized, then claim with bd update <id> --claim.
Verify the claim result before writing. A failed/conflicting claim is a blocker;
inspect current ownership and coordinate, do not steal work or force an assignee.
An issue claim does not grant overlapping file ownership or Git authority.

Give delegates the verified issue context and exclusive writable paths. Designate
one owner for tracker updates per issue; avoid competing claims or closure.
Workers return evidence and findings to that owner rather than silently close a
shared US. If the issue already belongs to the authorized coordinating agent,
verify that ownership and avoid an unnecessary second claim.
If no matching issue exists and creation is not authorized, report that blocker
and request permission; do not claim an invented issue or proceed untracked.

## Follow-up and completion

Create/reuse durable follow-up tasks for missing proofs, discovered work and
blockers. Use actual IDs in roadmap checkpoints and restart prompts. Where the
local bd workflow supports it, bd dep add <issue> <depends-on> means the first
issue depends on the second; verify both IDs and that direction. Use bd blocked
and bd show to inspect dependencies rather than equate open with ready.

Update issue notes/status with actual progress and artifact references. Close
with bd close <id> --reason=<evidenced outcome> only when that issue's own scope
and agreed criteria are complete. A code-change task can finish while a parent
US or real-provider validation stays open. A session end, commit, passing mock
test or high score alone is not a closure criterion. Preserve incomplete active
work and blockers before handoff. Verify successful updates/closure; never
claim a task change that failed. Do not auto-close another contributor's work.

## Safe CLI, capabilities and local additions

Prefer --json for parsed issue operations and inspect actual errors/exit results.
Do not assume every installed command supports identical flags: consult local
help if needed. Never run bd edit: it opens an interactive editor. Use bd update
flags for field changes. Missing bd/database access in a Beads-required project
means durable tracking is blocked, not permission to fabricate IDs or replace it
with a Markdown task DB. Return a clearly labeled inline fallback handoff and
seek a capability fix; do not continue unclaimed implementation when claim is
required. On a non-Beads repository, use its agreed tracker without inventing bd.

When local instructions require persistent memory in Beads, use bd remember and
bd memories for reusable knowledge; do not create MEMORY.md. Keep secrets and
unnecessary personal information out of notes and artifacts.

When local instructions describe Dolt storage, use that architecture: JSONL is
an export, not the source of truth or normal sync protocol. Do not edit/import
it to synchronize work. Git code commits and Dolt data sync are separate actions;
bd prime or a close protocol does not authorize either. No automatic Git commit,
push, Dolt push/pull or third-party hosting setup. Follow explicit permissions.
If authorized synchronization fails, report the exact command/error and local
state rather than claim shared/remote persistence. Local-only DB persistence
must be labeled local-only in the handoff.

## Required checkpoint additions when Beads applies

- Workspace/tracker identity and context freshness.
- Verified issue IDs/titles, ownership/claim result and current status.
- Dependencies, blockers and durable follow-up IDs.
- Supporting artifact paths, not competing task statuses.
- Actual updates/closures and reasons, incomplete work preserved.
- Local-only persistence or sync result, and any unavailable capability.
Include these facts in the next-session prompt so recovery starts from the
tracker rather than stale conversation memory.
