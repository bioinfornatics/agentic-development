---
name: cycle
description: Coordinates evidence-driven software development. Use for every new or resumed development task, including single-phase investigation, planning, implementation, fixing bugs, testing or reviewing.
---

# Cycle

## Select the action from the intent

Load cycle when entering software-development work, including a single-phase
request. Reuse it while its guidance remains available; do not reload per tool.
For a single-phase request, coordinate only the requested phase and its necessary
prerequisites; return its proposed handoff and stop rather than expand scope.

| Order | Intent / condition | Skill | Required output / exit gate |
|---|---|---|---|
| 1 | Every new development objective: establish product context, including clear/familiar requests; on resume verify existing context | agentic-development:research | Cited purpose, users/outcome, current behavior, constraints, affected seams and assumptions sufficient for the next decision, or targeted missing-context probe |
| 2 | Research context established or verified; define roadmap, scope, criteria or dependencies | agentic-development:plan | Proposed or approved scope, criteria, ownership, task graph and verification/review policy; investigate decision-blocking unknowns first |
| 3 | Ready authorized implementation, feature, refactor or repair | agentic-development:implement | Minimal diff, preserved-work ledger and symptom-specific/static evidence as applicable |
| 4 | Worker result or exact candidate needing checks | agentic-development:test | Criterion-bound results, failures and environment/coverage limits |
| 5 | Frozen candidate and evidence ready for acceptance assessment | agentic-development:judge | Scoped verdict, verified findings, agreed score mode and independence limits |
| Loop | Failed check, rejected candidate or missing proof | agentic-development:iterate | Classified gap and smallest authorized correction/prerequisite; retain valid proof and correction budget |

Research precedes Plan for a new development objective, even when the request
appears clear. Establish product context or verify a cited current baseline first.
Do not treat familiarity or a detailed prompt as research evidence. Existing
research can be reused only after coverage and freshness verification.
This is the usual dependency order, not a mandatory replay. Resume at the first incomplete or invalidated phase.
Reuse current research/plans and do not skip relevant verification or judgment. Before a nonstandard transition, announce
its reason, reused evidence and required gates. A missing mandatory prerequisite
blocks the action, not permission to pretend the phase passed. A result summary
alone is not acceptance. Repeated failures or an exhausted budget require a stop.

## Workflow

Read each reference before its governed action when its local condition first applies,
even if that occurs earlier than the step containing its link. Reuse unchanged guidance
already loaded; these internal steps are not additional development-cycle phases.

1. [ ] **Verify prerequisites and current authority**

   Read [the communication contract](references/communication-contract.md) when preparing
   the first checkpoint or a Git/session transition; it governs reporting safeguards,
   not an up-front load of response templates. For a UI checkpoint read [the checkpoint example](assets/checkpoint-example.md).

   Verify available filesystem, shell/test and delegation capabilities. Read the
   project's local instructions and inspect the repository without mutation first.
   Ask only for missing information that blocks safe progress; list nonblocking
   assumptions. A request to implement this slice authorizes its scoped code changes,
   not Git commits, remote operations, production actions or unrelated work.

   If the target repository uses Beads, read [the Beads integration](references/beads-integration.md)
   before choosing work or mutating shared task state. Recover context when stale,
   verify issue status and claim before implementation, and keep Beads as task
   truth. Artifact plans and handoffs are not a competing tracker. Follow the
   reference for missing tools, failed claims, durable follow-up and closure;
   evaluate commit suitability after each confirmed closure, without inferring Git authority.

   If Beads is explicitly chosen but not yet initialized, read [controlled Beads initialization](references/beads-initialization.md)
   before any setup. It documents minimal agent integration with reviewed optional Git hooks and
   a storage-only skip profile, with root, capability, permission and effect checks. Never reinitialize
   an existing workspace or treat this Skill load as setup permission. Phase workers
   report missing setup to the coordinator instead of initializing independently.

   Read [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions. Recorded permissions
   are historical unless their current authoritative source and scope are verified.
   Read [the review policy](references/review-policy.md)
   before agreeing acceptance, judging or closing a task/US. Independence and closure
   requirements are set before implementation, not waived by a missing capability.

2. [ ] **Frame or recover the bounded slice**

   Read [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or verification, and before implementation.
   Reuse verified Goals/Non-goals, FR/GWT and applicable quantified NFRs; do not
   invent targets. Investigation needs a bounded question, not a completed plan.

   Read [the judgment rubric](references/judgment-rubric.md) before selecting
   acceptance criteria or review mode.

   Read [candidate identity](references/candidate-identity.md) when planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions.

   Read [the state template](assets/cycle-state.md)
   when persisting or recovering a slice artifact or preparing a handoff, not for ordinary
   investigation.

   - Identify the approved objective, roadmap source, milestone/epic/US and smallest
      reviewable slice. If there is no roadmap, propose one and mark it unapproved.
   - Inventory branch/status and pre-existing changes, capture candidate identity,
      permissions and evidence. Report the starting checkpoint before mutations.
   - Keep durable state in an agreed project workspace, default
      `evidence/runs/<slice-id>/`, only after checking conflicts and permission
      to write. Do not persist private secrets, tokens, full sensitive tool outputs,
      or unnecessary personal data. If persistence is unavailable, emit a copyable
      handoff and disclose that no durable state was written.
   - Resume at the first incomplete or invalidated phase, not from the beginning.
      Reinspect the working tree and compare candidate identity; treat old evidence
      as stale if related files or environment changed.

   Treat roadmap outcomes, epic capabilities, user-story behavior and executable tasks
   as different levels. Keep distant work coarse and detail the ready frontier only.
   One run stays within one active epic; an epic may need multiple runs/sessions.
   One agent/session has one main verifiable task, not necessarily one phase or commit.
   Before writes, verify that the task ID leads to goal, requirement, scope, dependencies,
   checks and restart context. In Beads, parents express hierarchy, blocking edges express
   prerequisites; claim is not a file lock. Repair missing task context, not a second tracker.

   Keep related build/test/corrections in one session. Recommend a fresh context for an
   independent US, repository/worktree change, major research handoff, stale assumptions
   or required review separation. Compaction/commit alone is not a transition trigger. Recommendations do not
   automatically launch sessions or execute Git actions.
   When Entire is available, verify current host/worktree integration and record observed
   session/checkpoint links only; do not assume host support or create hooks/trailers.

3. [ ] **Dispatch and steer the selected phase**

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

   Load the selected phase from the intent-routing table with the verified task, scope,
   criteria, candidate, evidence and permissions. Verify its returned gate before selecting
   the next phase; preserve the requested phase-only boundary.

4. [ ] **Integrate observations and bound corrections**

   Verify applicable worker completion status, exact changes, candidate/evidence identity
   and result locator before integration. Reconcile conflicts; failed or partial results
   remain provisional, not accepted gates. Preserve valid proof and expose invalidated
   evidence; source-only checks remain static.

   Default to at most three correction rounds for the same slice unless the user
   sets another budget. After repeated failures, changed scope, exhausted budget,
   or incompatible evidence, stop and present the blocker, options and decision.
   A failed check cannot be turned green by deleting or weakening acceptance.

   Close a US only when its agreed mandatory criteria are evidenced and the judge
   accepts that exact candidate and scope. Local/mock acceptance can close only a
   local/mock slice, never an unmet real-provider US. Preserve open validation work
   in the roadmap. Do not mark proposed acceptance as user approval.

5. [ ] **Record verified progress and permitted finalization**

   Collect source-linked cycle state and checkpoint facts during work; format them
   in the next step. Link verified issue
   IDs and current artifacts instead of duplicating all phase reports. Finalization is
   a coordinator action, not a seventh worker phase: persist criteria checked, command
   results, observed commits/checkpoints, session references and limits; close only the
   permitted completed scope, leaving parent/real/release gates open. A commit message
   may carry verified Beads IDs by project convention; neither commit nor checkpoint
   proves acceptance. Missing integration is unavailable, not a fabricated link.

   At session start, objective change, slice completion, commit, judgment, handoff
   and US closure emit the full common checkpoint and
   update durable state if permitted. After other meaningful steps emit the short
   checkpoint form; suppress repetitive unchanged reports. On handoff include dirty
   work and resume conditions. After each performed commit emit the mandatory
   commit report. At session end emit the mandatory session summary with proposed
   next-session name, verified linked tasks and a standalone copy-ready restart
   prompt. If Judge has not run, score remains not assessed.

6. [ ] **Verify readiness and draft the cycle response**

   - Verify the active objective/task, product-context coverage and freshness, current candidate, permissions and first incomplete or invalidated phase; retain the routing rationale and unmet prerequisites.
   - Prepare the immediate next action and blockers within current scope/permissions; collect handoff inputs, distinguishing recommendations from performed actions; format them after the output-contract read below.
   - After investigation and before drafting any user-facing phase response (including blocked or unchanged results), read [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and five-section report. Reuse unchanged guidance already loaded.

   Read [the commit report](references/commit-report.md) only for a proposed,
   performed, failed or externally observed commit. Read
   [the session report](references/session-report.md) only for planned session end,
   explicit wrap-up or recommended context transition. The common communication
   contract governs these checkpoints; combine overlapping reports without duplication.

   After reading delivery guidance, draft the response and, at an actual handoff,
   the fenced YAML state card and copy-ready restart prompt.

7. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   After accepted judgment, persist results and perform only currently
   authorized issue closure or Git actions; keep unmet parent/release gates open.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
