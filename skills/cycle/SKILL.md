---
name: cycle
description: Coordinates evidence-driven agentic software development through Research, Plan, Implement, Test, Judge, and Iterate with roadmap checkpoints and early transition notices. Use for delivering or resuming a user story or reviewable development slice across multiple phases.
---

# Cycle

## Select the action from the intent

Resolve the objective, active outcome/task, current repository state, permissions and existing evidence. Select one phase; do not replay completed phases whose proof remains current.

| Intent / condition | Execute | Required result |
|---|---|---|
| Deliver or resume work across phases | Resolve the active outcome/task, compare current inputs with recorded proof, then load the first incomplete or invalidated phase below | One active task, selected phase and authorized next action |
| Start from an idea without a roadmap | Load `agentic-development:plan` to propose outcomes and dependencies; investigate decision-blocking unknowns first | Proposed roadmap, explicit unresolved decisions and next ready task |
| Receive a worker result or failed check | Verify the returned candidate and evidence, then route to verification, judgment or bounded correction | Evidence-bound gate decision; no acceptance from a summary alone |

Execute the selected action through the workflow below. Read only the references
required by that action, reuse guidance already loaded in this context, and verify
the result before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Structured requirements and output format

Read [the requirements and output contract](references/requirements-output.md)
for Goals/Non-goals, functional Given/When/Then criteria, relevant quantified NFRs
and the mandatory seven-field final report with phase-specific evidence and notifications.
Produce this phase's artifact using the contract's headings; map every result to
its verified criterion ID/target and mark unresolved or N/A fields explicitly.
Do not invent metrics, Git results, session launches or acceptance to fill a field.

## Required inputs and prerequisites

Read [the communication contract](references/communication-contract.md) before
starting; apply it in every phase. It governs user-facing checkpoints and Git,
commit, session, confidence and UI reporting. Read [the state template](assets/cycle-state.md)
for a new or resumed slice and [the judgment rubric](references/judgment-rubric.md)
before agreeing acceptance. For UI changes also read [the checkpoint example](assets/checkpoint-example.md).

Verify available filesystem, shell/test and delegation capabilities. Read the
project's local instructions and inspect the repository without mutation first.
Ask only for missing information that blocks safe progress; list nonblocking
assumptions. A request to implement this slice authorizes its scoped code changes,
not Git commits, remote operations, production actions or unrelated work.

## Conditional durable tracking

If the target repository uses Beads, read [the Beads integration](references/beads-integration.md)
before choosing work or mutating shared task state. Recover context when stale,
verify issue status and claim before implementation, and keep Beads as task
truth. Artifact plans and handoffs are not a competing tracker. Follow the
reference for missing tools, failed claims, durable follow-up and closure;
evaluate commit suitability after each confirmed closure, without inferring Git authority.

## Trust, candidate and review gates

Read [the authorization policy](references/authorization-policy.md) before
resuming artifact claims or executing consequential actions. Recorded permissions
are historical unless their current authoritative source and scope are verified.
Read [candidate identity](references/candidate-identity.md) when planning checks,
freezing inputs or reusing evidence; include staged, untracked and binary inputs
and explicitly defined output-only exclusions. Read [the review policy](references/review-policy.md)
before agreeing acceptance, judging or closing a task/US. Independence and closure
requirements are set before implementation, not waived by a missing capability.

## Start or resume

1. Identify the approved objective, roadmap source, milestone/epic/US and smallest
   reviewable slice. If there is no roadmap, propose one and mark it unapproved.
2. Inventory branch/status and pre-existing changes, capture candidate identity,
   permissions and evidence. Report the starting checkpoint before mutations.
3. Keep durable state in an agreed project workspace, default
   `evidence/runs/<slice-id>/`, only after checking conflicts and permission
   to write. Do not persist private secrets, tokens, full sensitive tool outputs,
   or unnecessary personal data. If persistence is unavailable, emit a copyable
   handoff and disclose that no durable state was written.
4. Resume at the first incomplete or invalidated phase, not from the beginning.
   Reinspect the working tree and compare candidate identity; treat old evidence
   as stale if related files or environment changed.

## Phase routing and gates

Select the next phase by the unmet decision or gate, then load its Skill and
execute the action in the table. Use the host's available Skill-loading mechanism;
a namespaced identifier is not a universal shell command. If loading is unavailable,
derive the package root from this Skill directory, verify the selected bundled
SKILL.md exists and read it with the required contained references. Report direct
reading, not activation or delegated execution.

| Phase | Skill | Required output / exit gate |
|---|---|---|
| Research | agentic-development:research | Load to investigate an unclear requirement, bug or technical risk; return cited findings sufficient for the next decision |
| Plan | agentic-development:plan | Load to create/refine a roadmap, epic, US or ready task graph; verify scope, criteria, dependencies, ownership and current permissions |
| Implement | agentic-development:implement | Load to execute an authorized ready task; return a minimal diff, preserved-work ledger and red/green evidence where executable |
| Test | agentic-development:test | Load to verify the exact candidate; return actual criterion-bound checks, failures and environment/coverage limits |
| Judge | agentic-development:judge | Load to assess a frozen candidate with the agreed review policy; return scoped verdict, evidence-linked findings and score mode |
| Iterate | agentic-development:iterate | Load to classify failed checks/findings and route the smallest authorized correction or prerequisite; preserve valid proof and enforce the budget |

Do not mechanically execute every phase for a trivial task: document reuse of
existing research or plan, but never skip relevant verification and judgment.
A phase can be blocked; report exact prerequisites rather than pretend to pass.

## Steering and delegation

Before a branch, commit, role/session transition, or scope expansion, announce the
trigger, intended action and authorization status. Execute already permitted
safe actions without repeatedly asking. Request a real decision for unresolved
trade-offs. A branch covers a US or slice, not necessarily a single task.

Use delegation only if available and useful. Give each worker the objective,
acceptance criteria, contract, approved scope, input artifacts and exclusive
writable paths. Workers cannot coordinate implicitly. Parallel writers must
never share a file. Workers return result, exact changes, evidence, limitations
and next action; the coordinator integrates these, not their unsupported claims.

Before Judge, freeze the candidate, checklist and evidence index; recommend a
fresh context and prepare the handoff. Do not auto-commit. If no independent
context exists, disclose self-review and limit the verdict; never label it
independent. Apply the plan-time review policy; do not waive required independence
or close a US on self-review without explicit scoped authority. Do not mutate
the candidate during judgment.

## Iteration and completion

Default to at most three correction rounds for the same slice unless the user
sets another budget. After repeated failures, changed scope, exhausted budget,
or incompatible evidence, stop and present the blocker, options and decision.
A failed check cannot be turned green by deleting or weakening acceptance.

Close a US only when its agreed mandatory criteria are evidenced and the judge
accepts that exact candidate and scope. Local/mock acceptance can close only a
local/mock slice, never an unmet real-provider US. Preserve open validation work
in the roadmap. Do not mark proposed acceptance as user approval.

At session start, objective change, slice completion, commit, judgment, handoff
and US closure emit the full common checkpoint and
update durable state if permitted. After other meaningful steps emit the short
checkpoint form; suppress repetitive unchanged reports. On handoff include dirty
work and resume conditions. After each performed commit emit the mandatory
commit report. At session end emit the mandatory session summary with proposed
next-session name, verified linked tasks and a standalone copy-ready restart
prompt. If Judge has not run, score remains not assessed.

## Conditional reporting details

Read [the commit report](references/commit-report.md) only for a proposed,
performed, failed or externally observed commit. Read
[the session report](references/session-report.md) only for planned session end,
explicit wrap-up or recommended context transition. The common communication
contract remains mandatory; do not reload identical content already present in
the current context. Combine overlapping reports without dropping required fields.

## Explicit first-time tracker setup (conditional)

If Beads is explicitly chosen but not yet initialized, read [controlled Beads initialization](references/beads-initialization.md)
before any setup. It documents minimal agent integration with reviewed optional Git hooks and
a storage-only skip profile, with root, capability, permission and effect checks. Never reinitialize
an existing workspace or treat this Skill load as setup permission. Phase workers
report missing setup to the coordinator instead of initializing independently.

## Work hierarchy and resumable execution

Treat roadmap outcomes, epic capabilities, user-story behavior and executable tasks
as different levels. Keep distant work coarse and detail the ready frontier only.
One run stays within one active epic; an epic may need multiple runs/sessions.
One agent/session has one main verifiable task, not necessarily one phase or commit.
Before writes, verify that the task ID leads to goal, requirement, scope, dependencies,
checks and restart context. In Beads, parents express hierarchy, blocking edges express
prerequisites; claim is not a file lock. Repair missing task context, not a second tracker.

Keep related build/test/corrections in one session. Recommend a fresh context for an
independent US, repository/worktree change, major research handoff, stale assumptions
or required review separation. Compaction/commit alone is not a transition trigger.
When Entire is available, verify current host/worktree integration and record observed
session/checkpoint links only; do not assume host support or create hooks/trailers.

## Coordination output and finalization

Produce the cycle state and checkpoint using the canonical headings in
[the requirements and output contract](references/requirements-output.md). Link verified issue
IDs and current artifacts instead of duplicating all phase reports. Finalization is
a coordinator action, not a seventh worker phase: persist criteria checked, command
results, observed commits/checkpoints, session references and limits; close only the
permitted completed scope, leaving parent/real/release gates open. A commit message
may carry verified Beads IDs by project convention; neither commit nor checkpoint
proves acceptance. Missing integration is unavailable, not a fabricated link.

## Execute the handoff or stop

Execute the next phase only when it belongs to the user's requested workflow and
current scope/permissions cover its actions. For a phase-only request, return the
phase result and proposed handoff, then stop; do not expand the request by loading
or executing a new phase. If continuing is authorized, apply the routes below.

Load the selected phase using the table above and pass its task, scope, criteria,
current candidate, evidence and permissions. Verify its returned gate before selecting
the next phase. After accepted judgment, persist results and perform only currently
authorized issue closure or Git actions; keep unmet parent/release gates open.

Use the host's available Skill-loading mechanism; these identifiers are not shell
commands. If loading is unavailable, read the selected bundled SKILL.md and its
required contained references, and report direct reading rather than activation.
Pass a copy-ready handoff if execution cannot continue in this context. State the
specific missing input, permission or capability, who can supply it when known,
and the next executable action. Do not merely say "blocked" or "continue later".

End every phase delivery with the mandatory seven-field final report from
[the requirements and output contract](references/requirements-output.md), including
blocked or unchanged results. Keep the ordered fields and explain the next gate.
