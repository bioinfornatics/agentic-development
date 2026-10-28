---
name: implement
description: Supports authorized software implementation. Use when executing an approved delivery plan, feature task or confirmed bug repair.
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

Apply contracts before their governed actions, even before the nominal step
containing the link when its condition arises earlier. Load a reference only when its
applicable content is absent, incomplete or outdated in the active context; reuse
identical available content from another Skill's contained copy. The same ID/version
with different content is a conflict, not proof of identity: resolve it before the
affected action. A previous read or loaded marker does not prove availability.
After compaction, a new session or worker, recover required unavailable instructions;
on workspace changes revalidate applicability. Reusing authorization guidance never renews
a previous permission. This is an agent instruction, not a runtime cache.

1. [ ] **Verify implementation inputs and authority**

   Verify repository root, local instructions, tools and task goal.

   Before creating or repairing task descriptions or acceptance criteria, apply
   [ticket authoring](references/ticket-authoring.md); verify readable purpose,
   criteria, ordered inputs and restart context without duplicating execution history.

   If the repository uses Beads, apply [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Use fresh `bd prime` guidance;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Apply [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions; verify current
   permission for the intended action, not historical approval.

   Apply [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or checks. Resolve the approved task baseline;
   retain Goals/Non-goals, FR/GWT and relevant NFRs; keep missing requirements explicit.

   Apply [the review policy](references/review-policy.md)
   before implementation or setting review requirements, and before agreeing acceptance,
   judging or closing a task/US. Independence and closure
   requirements are set before implementation, not waived by a missing capability.

   Apply [the communication contract](references/communication-contract.md) before
   the first mutation, checkpoint or Git/session transition, for ownership, transition, evidence
   and conditional UI reporting safeguards. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   Use the coordinator's verified slice state when available; do not fabricate execution or acceptance.

   Read the approved plan, acceptance criteria, local instructions and ownership
   ledger. Reinspect branch/status/diff and compare pre-existing hunks. Block
   conflicting ownership; do not overwrite another contributor's work. Recover missing context or return to Plan before edits.

2. [ ] **Prepare the owned slice and reproduction**

   Apply [candidate identity](references/candidate-identity.md) before planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions. 
   For exact-candidate proof, use the contained [capture/validate/compare CLI](scripts/candidate_identity.py) with the [scope example](references/candidate-scope.example.json); consult the [manifest schema](references/candidate-identity.schema.json) and [manifest example](references/candidate-identity.example.json) when preparing or validating its JSON. Follow the candidate procedure above; equality is not acceptance.

   Before committing or drafting a proposed, performed, failed or externally observed commit report, apply [the commit report](references/commit-report.md). Before drafting a planned session end, explicit wrap-up or recommended context transition report, apply [the session report](references/session-report.md).  These conditions govern earlier boundaries too.

   Confirm branch fit and announce impending branch action if needed. Check
   action-specific Git authorization before creation/switch. Non-Git work can
   proceed on authorized files with branch marked not applicable.

   Select one requirement-derived behavior test at an approved public seam; use
   independent expected values and establish an observed red before the production change.
   For a bug, require a symptom-specific red-capable reproduction, not an unrelated
   missing symbol. For instruction-only work, use source-contract/static checks and
   report their limits. Missing access to a seam for executable behavior is a capability
   finding: preserve its behavioral criterion as unverified, do not substitute static
   checks or proceed with a required reproduction gate unmet.

   Read relevant glossary/ADRs and preserve public contracts. Expected values come from
   specification, worked example or independent oracle, not copied production logic.
   Reuse suitable tests; finish one vertical behavior slice before the next rather than
   writing all speculative tests then all code. Before adding a test, name its product guarantee,
   concrete incorrect behavior and marginal detection beyond existing checks; select
   the cheapest valid oracle, not a test-count or coverage-percentage target.
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

3. [ ] **Implement minimal green and refactor**

   Make the smallest coherent production change to reach green; rerun the same checks,
   then refactor without changing behavior and rerun again. Preserve external contracts,
   avoid unrelated cleanup and secrets. Parallelize only disjoint writable files;
   return conflicting changes to the coordinator before writing.

   Remove temporary debug instrumentation or explain retained authorized diagnostics.

4. [ ] **Observe and integrate each coherent batch**

   After each coherent change batch inspect the actual diff, maintain the implementation
   change ledger with owned paths/hunks and reasons, and emit the short checkpoint. Run cheap
   focused tests/type checks near changes, then risk-relevant broader regressions
   before handoff; record commands and actual outputs. Full-suite execution depends
   on scope/capability, not a typo ritual.

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

   Keep missing evidence, public-seam access, tools, permissions and required review/independence explicit; passing focused checks is not acceptance. Verify candidate/check provenance and identify what remains unverified. Freeze exact handoff candidate.

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
   permitted and read back updates. After HEAD/index changes retain original provenance;
   rebind documented equality or rerun rather than invent proof on the new commit.
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
   budget. Never call the implementation accepted because focused tests passed.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
