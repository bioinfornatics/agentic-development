---
name: cycle
description: Coordinates evidence-driven software development across phases. Use when starting or resuming a development objective such as a feature, fixing bugs, testing or reviewing, when working an epic in batches, or when claiming, updating or closing tracker tasks. A single-phase request may load only that phase Skill.
---

# Cycle

## Select the action from the intent

Load cycle to start or resume an objective, work an epic in batches or claim, update or
close tracker tasks. A request limited to one phase may load only that phase Skill, which
returns its handoff without finalizing; if cycle is loaded for one, coordinate only that
phase and its prerequisites, return its proposed handoff and stop rather than expand scope.
Reuse cycle while its guidance remains available; do not reload it per tool.

| Order | Intent / condition | Skill | Required output / exit gate |
|---|---|---|---|
| 1 | Every new development objective: establish product context, including clear/familiar requests; on resume verify existing context | agentic-development:research | Cited purpose, users/outcome, current behavior, constraints, affected seams and assumptions sufficient for the next decision, or targeted missing-context probe |
| 2 | Research context established or verified; define roadmap, scope, criteria or dependencies | agentic-development:plan | Proposed or approved scope, criteria (an unapproved specification stops for approval by the user or designated owner), ownership, task graph and verification/review policy; investigate decision-blocking unknowns first |
| 3 | Ready authorized implementation, feature, refactor or repair whose specification or criteria are approved and whose failing checks are named | agentic-development:implement | Minimal diff, preserved-work ledger and symptom-specific/static evidence as applicable |
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

A phase report is the result of this Skill, not a file to find before execution.
Collect its facts during work; deliver them inline by default at the delivery step.
Save a report only with an explicit destination and permission to write, following
the common output contract loaded at that step. Required evidence inputs and tracker
updates retain their own gates; an inline response does not replace task truth.

Apply contracts before their governed actions, even before the step that links them.
Read a reference only when it is absent, incomplete or outdated in the active context.
Reuse identical copies from another Skill. The same ID/version with different content
is a conflict, not proof of identity; resolve it before the affected action.
A loaded marker or earlier read does not prove availability. After compaction, a new
session or worker, reload missing required instructions. After workspace changes,
recheck applicability. Reused authorization guidance never renews a permission.
This is an agent instruction, not a runtime cache.

1. [ ] **Verify prerequisites and current authority**

   Apply [the communication contract](references/communication-contract.md) before
   the first mutation and before preparing the first checkpoint or a Git/session transition,
   for ownership, transition, evidence and conditional UI reporting safeguards, not an
   up-front load of response templates. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   When acting as a delegated worker, use the coordinator's verified slice state; do not fabricate execution or acceptance.

   For a UI checkpoint apply [the checkpoint example](assets/checkpoint-example.md).

   For an explicitly requested Skill evaluation in a source checkout, read
   [evaluation piloting](references/session-evaluation.md) before launching runs.
   Pilot the official Skill Creator CLI from the session; use its Goose runner
   by default. Keep native delegation optional and evaluation separate from product acceptance.

   Verify available filesystem, shell/test and delegation capabilities. Read the
   project's local instructions and inspect the repository without mutation first.
   Ask only for missing information that blocks safe progress; list nonblocking
   assumptions. A request to implement this slice authorizes its scoped code changes,
   not Git commits, remote operations, production actions or unrelated work.

   Before creating or repairing task descriptions or acceptance criteria, verify
   current scope and write authority. Conditionally Load `agentic-development:task-authoring`
   using the host's available Skill-loading mechanism (not a shell command), with
   established goal, scope, criteria, native tracker context and current authority.
   Reuse its guidance when already available and current; do not load both routes
   normally. If the optional capability is unavailable, apply contained
   [ticket authoring](references/ticket-authoring.md) directly and report direct
   reading, not activation; do not retry loading or block routine work on its absence.
   For routine reads, claims, progress updates or closure, do not load task-authoring.
   Resume this caller after verified ticket readback or an explicit proposal/error;
   retain this phase's scope, ownership, review and evidence gates.

   Require explicit delivery mechanisms and asset maps for ready implementation work.
   Route changed scope through consolidated ticket sections and reconciled dependency
   edges; a populated tracker record alone does not prove execution readiness.

   If the repository uses Beads, apply [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Run `bd prime` only when Beads context is missing or stale;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   If Beads is explicitly chosen but not yet initialized, read [controlled Beads initialization](references/beads-initialization.md)
   before any setup. It documents minimal agent integration with reviewed optional Git hooks and
   a storage-only skip profile, with root, capability, permission and effect checks. Never reinitialize
   an existing workspace or treat this Skill load as setup permission. Phase workers
   report missing setup to the coordinator instead of initializing independently.

   Apply [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions; verify current
   permission for the intended action, not historical approval.

   Apply [the review policy](references/review-policy.md) before setting or reporting
   acceptance/review requirements, before implementation, and before proposing or agreeing
   acceptance, judging or closing a task/US. Independence and closure requirements are
   set at plan time, before implementation; a missing capability does not waive them.

2. [ ] **Frame or recover the bounded slice**

   Apply [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria, checks or verification, and before running checks.
   Resolve the approved task baseline; retain verified Goals/Non-goals, FR/GWT and relevant
   quantified NFRs without inventing targets; keep missing requirements explicit.

   Apply [the judgment rubric](references/judgment-rubric.md) before selecting
   acceptance criteria or review mode.

   Apply [candidate identity](references/candidate-identity.md) before planning checks,
   freezing or comparing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions.
   For exact-candidate proof, use the contained [capture/validate/compare CLI](scripts/candidate_identity.py) with the [scope example](references/candidate-scope.example.json); consult the [manifest schema](references/candidate-identity.schema.json) and [manifest example](references/candidate-identity.example.json) when preparing or validating its JSON. Follow the candidate procedure above; equality is not acceptance.

   Read [the state template](assets/cycle-state.md)
   when persisting or recovering a slice artifact or preparing a handoff, not for ordinary
   investigation.

   - Identify the approved objective, available roadmap/parent context and smallest
      reviewable slice. Propose a missing roadmap only for requested planning or a
      decision-blocking need; mark it unapproved. Otherwise report unavailable context;
      do not expand a bounded investigation merely to fill hierarchy labels.
   - Inventory branch/status, pre-existing changes, permissions and evidence. For
      source-only observations record inspected revision/paths, dirty state and limits;
      use preliminary or exact-candidate provenance only when the check's purpose
      requires it. Report the starting checkpoint before mutations.
   - Keep required durable state in the agreed tracker or explicitly authorized
      workspace. Do not invent a default directory; verify the destination, conflicts
      and permission before writes. Do not persist private secrets, tokens, full sensitive tool outputs,
      or unnecessary personal data. If persistence is unavailable, emit a copyable
      handoff and disclose that no durable state was written.
   - Resume at the first incomplete or invalidated phase, not from the beginning.
      Reinspect the working tree and select source-only observation, preliminary
      check or exact-candidate proof under candidate identity; compare exact inputs
      before proof reuse. Treat old evidence as stale if related files or environment changed.

   Treat roadmap outcomes, epic capabilities, user-story behavior and executable tasks
   as different levels. Keep distant work coarse and detail the ready frontier only.
   Keep exactly one active epic across runs and sessions; an epic may need several runs.
   Pull work only from its descendants (`bd ready --parent <epic>`). Switch the active
   epic only on an explicit user decision, never because another epic has ready work.
   Work in progress is the active batch: only its tasks are claimed or in_progress.
   The coordinator owns the batch and each worker owns one task, not one phase or commit.
   Give each task one primary deliverable and its exit criteria; each action or contribution
   must serve it or follow an explicit authorized objective switch. Do not start
   several tasks sequentially and leave them in progress: multiple active tasks
   require actual active workers with distinct assignments, not intended delegation.
   Distinguish planned/selected work, verified claims and observed execution in the
   existing tracker/checkpoint; a claim alone proves neither a running delegate nor
   permission. Keep contributions under their batch task unless independently resumable
   outcomes require separate authorized tickets; no ticket per file or phase.
   Before writes, verify that the task ID leads to goal, requirement, scope, dependencies,
   checks and restart context. In Beads, parents express hierarchy, blocking edges express
   prerequisites; claim is not a file lock. Repair missing task context, not a second tracker.

   When the active epic has no ready tasks for the next batch, propose Research → Plan
   refinement for it, or for the next epic in line once it is complete; switching the active epic still needs
   the user's decision. Refine one batch ahead, not the whole backlog; tracker writes need current authority.

   Before switching an unfinished primary deliverable, record its result, blocked or
   suspended disposition, candidate/diff, evidence, owner, worker dispositions and
   exact resume prerequisite. Verify replacement scope and authority before starting
   it. A switch grants no implicit closure, cancellation, reset or discard of work;
   use only authorized supported tracker/worker operations and read back their results.
   If required persistence fails, stop the affected transition, not unrelated work.

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

   Use delegation only if available and useful, subject to required isolation or
   independence. Coordinator baseline verification and bounded questions from
   sufficient available sources need no worker; deeper Research investigations
   follow that phase's dispatch policy. Form the batch from all ready, unblocked,
   mutually independent tasks of the active epic. Bound it only by the host's subagent
   concurrency limit, never by a plugin cap. Dispatch one subagent per task with disjoint
   writable paths; use an approved worktree only when tasks would collide, with current authority. For useful independent contributions with
   ready inputs, available capability and exclusive writable paths, launch the ready
   workers before awaiting their results. Record the dependency, capability, isolation
   or proportionality reason when serialization is necessary; do not manufacture
   parallelism by adding trivial work or splitting one coherent outcome.
   Record actual invocation handles/worker identifiers and observed status separately
   from proposed assignments; unavailable lifecycle evidence remains unknown, never
   simulated. One coordinator updates each issue; workers return evidence unless a
   distinct, currently authorized tracker responsibility was explicitly assigned.
   Give each worker the objective,
   acceptance criteria, contract, approved scope, input artifacts and exclusive
   writable paths, as pointers to where they are saved; copy an item only when it
   has no saved locator. Workers cannot coordinate implicitly. Parallel writers must
   never share a file. Workers return result, exact changes, evidence, limitations
   and next action; the coordinator integrates these, not their unsupported claims.
   Name each contribution's required output and integration/join responsibility;
   do not write a live worker's owned paths or begin work depending on its return.
   Typical pointers, not copies: the task ID and, when saved, the research report,
   specification and relevant commits; start each worker in a fresh context.

   Integration-branch batch mode is optional and used only when the user requests
   it or approves it for this epic; the default above stays non-mutating. It needs
   current scoped authority for each Git action: creating the integration branch,
   one worktree and branch per worker based on it, each worker commit, each merge
   or rebase that brings the integration tip into a worker branch, merging each
   finished worker into the integration branch, and removing each worktree. Each
   worker confirms its base, implements its one task test-first and, when authorized,
   brings in the current integration tip before returning. Merge finished work one
   worker at a time, then dispatch any tasks that the merge made ready. The
   integration branch is the candidate for Test and Judge. Never merge it into
   the target branch or any protected branch, push it, or remove a worktree without
   that action's own authority. A missing grant stops only the affected action and
   falls back to the default.

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
   Before dependent edits, checks or dispatch, join and verify the required worker
   contributions, candidate identity and integration compatibility. A required live,
   failed or incomplete worker leaves that dependent action pending; independent
   authorized batch tasks may continue. Partial returns are not accepted inputs. Record
   remaining worker dispositions rather than assuming completion or cancellation.
   Do not pull or claim tasks outside the active batch until every batch task is
   closed or released with a named blocker.

   Default to at most three correction attempts for the same slice unless the user
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
   - Prepare the immediate next action and blockers within current scope/permissions; collect handoff inputs, distinguishing recommendations from performed actions; format them after the output-contract application below.
   - After investigation and before drafting any user-facing phase response (including blocked or unchanged results), apply [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and selected delivery form (compact when eligible, otherwise five-section report).

   Apply [the commit report](references/commit-report.md) only for a proposed,
   performed, failed or externally observed commit. Apply
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
