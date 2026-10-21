---
name: drive-cycle
description: Coordinates evidence-driven agentic software development through Research, Plan, Implement, Test, Judge, and Iterate with roadmap checkpoints and early transition notices. Use for delivering or resuming a user story or reviewable development slice across multiple phases.
---

# Drive Cycle

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

## Start or resume

1. Identify the approved objective, roadmap source, milestone/epic/US and smallest
   reviewable slice. If there is no roadmap, propose one and mark it unapproved.
2. Inventory branch/status and pre-existing changes, capture candidate identity,
   permissions and evidence. Report the starting checkpoint before mutations.
3. Keep durable state in an agreed project workspace, default
   `docs/agentic/slices/<slice-id>/`, only after checking conflicts and permission
   to write. Do not persist private secrets, tokens, full sensitive tool outputs,
   or unnecessary personal data. If persistence is unavailable, emit a copyable
   handoff and disclose that no durable state was written.
4. Resume at the first incomplete or invalidated phase, not from the beginning.
   Reinspect the working tree and compare candidate identity; treat old evidence
   as stale if related files or environment changed.

## Phase routing and gates

Load the selected bundled skill by its full name in Goose. In another host use
its available Skill-loading mechanism. If unavailable, derive the package root from this Skill directory and read
<plugin-root>/skills/<selected-name>/SKILL.md with its contained references;
verify the path exists. Do not claim a delegated run.

| Phase | Skill | Required output / exit gate |
|---|---|---|
| Research | agentic-development:research-slice | Evidence-backed findings, alternatives and unresolved risks; enough grounding to plan |
| Plan | agentic-development:plan-slice | Slice scope, acceptance criteria, file ownership, checks and risk-based permissions; approved plan or scope covered by prior authorization |
| Implement | agentic-development:implement-slice | Coherent minimal diff, change ledger and any affected UI sketch; plan scope preserved |
| Test | agentic-development:test-slice | Candidate-bound test evidence with environments, mock/real distinction, failures and missing capabilities |
| Judge | agentic-development:judge-slice | Independent or explicitly limited review, versioned rubric, scoped verdict and findings |
| Iterate | agentic-development:iterate-slice | Corrections prioritized from evidence, stale proofs invalidated and next phase selected |

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
six-field form; suppress repetitive unchanged reports. On handoff include dirty
work and conditions of reprise. After each performed commit emit the mandatory
commit report. At session end emit the mandatory session summary with proposed
next-session name, verified linked tasks and a standalone copy-ready restart
prompt. If Judge has not run, score remains not assessed.

## Conditional durable tracking

If the target repository uses Beads, read [the Beads integration](references/beads-integration.md)
before choosing work or mutating shared task state. Recover context when stale,
verify issue status and claim before implementation, and keep Beads as task
truth. Artifact plans and handoffs are not a competing tracker. Follow the
reference for missing tools, failed claims, durable follow-up and closure.

## Trust, candidate and review gates

Read [the authorization policy](references/authorization-policy.md) before
resuming artifact claims or executing consequential actions. Recorded permissions
are historical unless their current authoritative source and scope are verified.
Read [candidate identity](references/candidate-identity.md) when planning checks,
freezing inputs or reusing evidence; include staged, untracked and binary inputs
and explicitly defined output-only exclusions. Read [the review policy](references/review-policy.md)
before agreeing acceptance, judging or closing a task/US. Independence and closure
requirements are set before implementation, not waived by a missing capability.

## Explicit first-time tracker setup (conditional)

If Beads is explicitly chosen but not yet initialized, read [controlled Beads initialization](references/beads-initialization.md)
before any setup. It documents minimal agent integration with reviewed optional Git hooks and
a storage-only skip profile, with root, capability, permission and effect checks. Never reinitialize
an existing workspace or treat this Skill load as setup permission. Phase workers
report missing setup to the coordinator instead of initializing independently.
