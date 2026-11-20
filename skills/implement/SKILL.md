---
name: implement
description: Executes an authorized change test-first (observed red, minimal green, refactor) and keeps a change ledger of owned hunks and evidence. Use when executing a planned task, a feature task or a confirmed bug repair dispatched by Plan or Iterate.
---

# Implement

## Select the action from the intent

Select the implementation intent; verify inputs and gates through the workflow.

| Intent / condition | Execute | Required result |
|---|---|---|
| Execute an authorized feature task | Resolve criteria and ownership, select one public behavior, observe red, implement green, then refactor | Minimal coherent behavior change, test observations and preserved-work ledger |
| Repair a confirmed bug | Reuse or establish the symptom-specific failing reproduction before changing production behavior | Repair that passes the original reproduction and relevant regressions |
| Change instructions or other non-executable source | Apply the authorized source change and run applicable static checks | Source diff and explicitly static evidence; agent behavior remains unverified |
| Encounter conflicting hunks or a necessary scope expansion | Preserve the current diff and return the conflict or decision to the coordinator/user | Exact conflicting paths or scope decision; no overwrite or unauthorized expansion |

Execute the selected action through the workflow below and verify its result
before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

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

1. [ ] **Verify implementation inputs and authority**

   Verify repository root, local instructions, tools and task goal.

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

   If the repository uses Beads, apply [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Run `bd prime` only when Beads context is missing or stale;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Apply [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions; verify current
   permission for the intended action, not historical approval.

   Apply [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria, checks or verification, and before running checks.
   Resolve the approved task baseline; retain verified Goals/Non-goals, FR/GWT and relevant
   quantified NFRs without inventing targets; keep missing requirements explicit.

   Apply [the review policy](references/review-policy.md) before setting or reporting
   acceptance/review requirements, before implementation, and before proposing or agreeing
   acceptance, judging or closing a task/US. Independence and closure requirements are
   set at plan time, before implementation; a missing capability does not waive them.

   Apply [the communication contract](references/communication-contract.md) before
   the first mutation and before preparing the first checkpoint or a Git/session transition,
   for ownership, transition, evidence and conditional UI reporting safeguards, not an
   up-front load of response templates. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   When acting as a delegated worker, use the coordinator's verified slice state; do not fabricate execution or acceptance.

   Before implementation, verify that the ticket names its service/runtime mechanism,
   ordered approach, inspected inputs, proposed outputs, preserved assets and exact
   restart action. Missing delivery design is a readiness gap: repair it under
   authorized planning scope or request its specific decision, not guess paths or
   substitute generic safety prose. Compare native dependencies/owner with text and
   verify current user authority instead of treating stale planning-only text as law.

   Read the approved plan, acceptance criteria, local instructions and ownership
   ledger. Specification gate: production edits start only from an approved
   specification, or for a single small task ticket criteria approved by the user or
   designated owner; a missing,
   draft or since-changed specification returns to Plan before any edit. A gap or
   contradiction found in the specification during work is a Plan decision, not a
   silent code choice. Reinspect branch/status/diff and compare pre-existing hunks. Block
   conflicting ownership; do not overwrite another contributor's work. Recover missing context or return to Plan before edits.

2. [ ] **Prepare the owned slice and reproduction**

   Apply [candidate identity](references/candidate-identity.md) before planning checks,
   freezing or comparing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions.
   For exact-candidate proof, use the contained [capture/validate/compare CLI](scripts/candidate_identity.py) with the [scope example](references/candidate-scope.example.json); consult the [manifest schema](references/candidate-identity.schema.json) and [manifest example](references/candidate-identity.example.json) when preparing or validating its JSON. Follow the candidate procedure above; equality is not acceptance.

   Before committing or drafting a proposed, performed, failed or externally observed commit report, apply [the commit report](references/commit-report.md). Before drafting a planned session end, explicit wrap-up or recommended context transition report, apply [the session report](references/session-report.md).

   Confirm branch fit and announce impending branch action if needed. Check
   action-specific Git authorization before creation/switch. Non-Git work can
   proceed on authorized files with branch marked not applicable.

   Select one requirement-derived behavior test at an approved public seam; use
   independent expected values and establish an observed red before the production change.
   Confirm the red fails on the expected assertion for the missing behavior, not on a
   syntax, import, fixture or setup error; a test that passes before the change proves nothing.
   For a bug, require a symptom-specific red-capable reproduction, not an unrelated
   missing symbol. For instruction-only work, use source-contract/static checks and
   report their limits. Missing access to a seam for executable behavior is a capability
   finding: preserve its behavioral criterion as unverified, do not substitute static
   checks or proceed with a required reproduction gate unmet.

   Read relevant glossary/ADRs and preserve public contracts. Every assertion's expected
   result comes from the independent oracle the plan named for its criterion, or from
   another independent oracle recorded in the change ledger when the plan named none;
   production logic is never used to compute it.
   When the task owns a user story's outer acceptance check, write it first and observe
   it failing for the missing behavior. Until the story's last task, keep it visibly
   pending, not deleted or silently skipped: prefer an expected-failure mark; keep it
   outside the required suite only when the runner has no such mark, and then list the
   exclusion in the change ledger. Either way name the story and the task that will make
   it pass.
   The task that completes the story removes that mark and observes it pass; only then
   is the story complete. For an instruction-only story the outer check is a labeled
   static check. Inner slices then follow the loop below.
   Reuse suitable tests. Work through the planned test list one item at a time: red,
   green, refactor, then the next item. The first item is the tracer bullet, the
   thinnest check that crosses every layer the story needs, so later items extend a
   path already shown to work. Apply [test value](references/test-value.md)
   before adding a test: name its product guarantee, concrete incorrect behavior and
   marginal detection beyond existing checks; select the cheapest valid oracle, not a
   test-count or coverage-percentage target. A variant that changes only an input value
   needs a distinct branch in the code or a case the specification distinguishes.
   Testability means a minimal meaningful public seam with controlled external inputs
   and observable outputs/effects. Do not add speculative abstractions, exports of
   private helpers, injection layers or production-only switches solely to multiply
   tests. If the required seam is absent, report the specific gap and obtain scope for
   the smallest justified change; do not bypass the required reproduction gate.
   Within authorized rationalization, retain/merge/remove/replace tests with the
   guarantee and discrimination evidence recorded; preserving every legacy test is
   not required. Never delete a meaningful regression or weaken acceptance to get green.
   Mock only dependencies: assert the subject's contract, exact known outcomes and
   important errors, not the mock's setup or copied expected calculations.
   Name each new test after the rule (protected behavior) it protects and keep its
   criterion ID in a docstring or marker unless project conventions differ; arrange only
   the conditions that matter, perform one action and assert the outcome and its relevant
   effects, so the suite reads as living documentation.

   If code you must refactor or modify has no discriminating test at its public seam,
   first add a characterization test of its current behavior and observe it green before
   the change. Label it characterization, not specification: it pins today's behavior,
   including defects, until a criterion says otherwise.

3. [ ] **Implement minimal green and refactor**

   Make the smallest coherent production change to reach green; rerun the same checks,
   then refactor without changing behavior and rerun again. Refactoring stays inside the
   owned slice and its paths, starts only from green and must keep the same checks green
   without editing their assertions; a wider restructuring is a separate planned task.
   Preserve external contracts, avoid unrelated cleanup and secrets.

   For parallel writers the default is disjoint paths in the shared tree. Use an
   approved worktree per writer when writers would collide on files, build outputs,
   branch or generated artifacts; otherwise serialize. This default grants no Git
   authority: creating a worktree or branch still needs current permission. Return
   conflicting changes to the coordinator before writing.

   Remove temporary debug instrumentation or explain retained authorized diagnostics.

4. [ ] **Observe and integrate each coherent change set**

   After each coherent change set inspect the actual diff, maintain the implementation
   change ledger with owned paths/hunks and reasons, and emit the short checkpoint.
   For executable changes the ledger also records, per behavioral criterion ID, the red
   command and a failing-output excerpt observed before that criterion's production
   edit, and lists each deleted, skipped, renamed or loosened test, assertion,
   fixture or expected value with its approved criterion change, test-value decision
   or pending outer acceptance check naming its owner task; an unjustified entry
   blocks handoff. Run cheap
   focused tests/type checks near changes, then risk-relevant broader regressions
   before handoff; record commands and actual outputs. Run the full suite when the
   scope requires it and tooling allows.

   Before advancing a dependent node group, verify that the observed result satisfies
   the next affected consumer's input/precondition, including material format,
   interface, state, environment and authority. A passing producer check alone is
   not a verified transition or project-wide completion. If feasibility or
   compatibility fails, pause affected nodes and route the finding to Iterate with
   the preserved diff, evidence and budget; independent ready nodes may continue
   within current scope/authority. Do not stop the whole project by default.

   For UI/journey changes provide ASCII with CRUD and +/~/-/=, functional/visual
   differences and explicit observed/tested/inferred/not-run status. Record any
   capture independently of the drawing. Do not infer browser quality from code.

   When work was delegated, verify each worker's authorized scope, exclusive writable paths, invocation/completion status, source identity and result locator against the actual diff and checks. Resolve or expose conflicting results; incomplete or failed work remains provisional. Delegation is not required.

   After each coherent verified unit, evaluate its commit boundary before starting a distinct objective.
   Use the approved plan and verified task IDs, with epic/US context when available.
   Commit one reviewable outcome, not one commit per file or task: a task may need
   more than one commit, and closely related tasks may share a coherent commit.
   Keep unrelated outcomes separate; record scope and a proposed message while the
   reason is fresh. Evaluate incomplete work as WIP, not verified or accepted.
   If committing is appropriate and current scoped authority covers the action,
   apply step 5 now rather than accumulate unrelated changes until final handoff.
   Otherwise propose the message and retain the owned/preserved-hunk ledger; seek
   a decision before combining an objective that would obscure the existing scope.

5. [ ] **Check candidate provenance and any separate commit boundary**

   Match the change ledger to the authorized plan and criterion IDs; confirm
   that each scoped behavior and preserved-work entry has current evidence.

   Check recorded observations: requirement-derived observed red before executable production changes, the smallest green change and same-check refactor reruns; for instruction-only work, label checks static. Retain actual commands/results, relevant regressions and any UI journey/capture limits.

   Keep missing evidence, public-seam access, tools, permissions and required review/independence explicit; passing focused checks is not acceptance. Verify candidate/check provenance and identify what remains unverified. Freeze exact handoff candidate, after any commit below.

   Describe the actual outcome and scope using the project message convention,
   with verified task IDs when the tracker applies. Use Gitmoji only when the project convention approves it;
   the emoji never replaces meaningful text or proves task completion. Choose the
   type/emoji from the actual staged change, not from a parent epic or intended work.

   A commit is optional and separately authorized. Before an authorized commit,
   announce coverage, checks/limits, exact owned paths/hunks and message; inspect
   staged content to exclude initial user changes and unrelated files. Do not use
   indiscriminate staging. Report actual hash only after success. If not permitted,
   return a proposed message and preserve uncommitted state. Never auto-push.

   After each performed commit emit the mandatory contract commit report with
   verified committed files, problem/feature, actual metadata and remaining state.

   Verify identity, actual message and committed paths. Link results in Beads only when
   permitted and read back updates. After a performed commit, capture the handoff candidate again
   and freeze its new candidate_id; reuse pre-commit evidence only through the
   commit rebind in candidate identity, otherwise rerun. Never claim checks ran on the new commit.
   Failed mandatory checks leave a documented WIP candidate, not acceptance.

6. [ ] **Verify readiness and draft the phase response**

   Prepare the immediate next action and its exact prerequisites, owner when known and expected result; distinguish proposed from performed actions. Collect facts for the exact candidate, criterion IDs, reproduction/tests, change ledger and limits, and the inputs needed for a handoff; draft its state card and restart prompt only after reading the delivery guidance.

   After investigation and before drafting any user-facing phase response (including blocked or unchanged results), apply [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and selected delivery form (compact when eligible, otherwise five-section report). Combine overlapping reports without duplication. After reading delivery guidance, draft the response and, at an actual handoff, the fenced YAML state card and copy-ready restart prompt.

7. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   After the scoped change and focused checks, Load `agentic-development:test`
   with the exact candidate, criterion IDs, reproduction/tests, change ledger and limits.
   If evidence exposes a defect requiring a new correction decision, Load
   `agentic-development:iterate` with the finding, preserved diff and current
   budget. If the task lacks the context needed to edit, Load `agentic-development:plan`
   with the missing context before editing; return scope expansion, permission or
   ownership conflicts to the coordinator/user. Never call the implementation accepted
   because focused tests passed.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
