---
name: test
description: Verifies software candidates against acceptance criteria. Use for testing implementations or regression repairs, or rechecking evidence after candidate changes.
---

# Test

## Select the action from the intent

Select the verification intent; bind criteria, candidate and environment through the workflow.

| Intent / condition | Execute | Required result |
|---|---|---|
| Verify an implementation or regression repair | Bind criteria to the candidate, run available checks and record actual results | Reproducible criterion-to-check evidence, failures and coverage limits |
| Reuse previous proof after a change | Compare the proof's inputs/environment with current ones; rerun affected checks | Justified retained proof and new evidence for changed inputs |
| Verify an installed package, real provider or rendered UI | Use the exact required artifact/environment and inspect actual behavior | Environment-specific observations, or explicit missing capability; mock proof is not substituted |

Execute the selected action through the workflow below. Read only the references
required by that action, reuse unchanged guidance already loaded in this context, and verify
the result before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Workflow

Read references when their local conditions apply, before governed actions even if
earlier than the nominal step. Reuse unchanged guidance already loaded.

1. [ ] **Verify test inputs and authority**

   Verify repository root, local instructions, tools and task goal.

   If the repository uses Beads, read [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Use fresh `bd prime` guidance;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Read [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions. Recorded permissions
   are historical unless their current authoritative source and scope are verified.

   Read [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or verification, and before running checks.
   Reuse verified Goals/Non-goals, FR/GWT and applicable quantified NFRs; do not
   invent targets. Investigation needs a bounded question, not a completed plan.

   Read [the review policy](references/review-policy.md)
   before implementation or setting review requirements, and before agreeing acceptance,
   judging or closing a task/US. Independence and closure
   requirements are set before implementation, not waived by a missing capability.

   Read [the communication contract](references/communication-contract.md) before
   the first mutation, checkpoint or Git/session transition, for ownership, transition, evidence
   and conditional UI reporting safeguards. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   Use the coordinator's verified slice state when available; do not fabricate execution or acceptance.

   Before committing or drafting a proposed, performed, failed or externally observed commit report, read [the commit report](references/commit-report.md). Before drafting a planned session end, explicit wrap-up or recommended context transition report, read [the session report](references/session-report.md).  These conditions govern earlier boundaries too.

2. [ ] **Freeze the candidate and map checks**

   Read [candidate identity](references/candidate-identity.md) before planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions. 

   Freeze candidate identity and the acceptance/check matrix before running
   acceptance-bound checks. Preliminary near-change checks may use the limited-
   provenance path in candidate-identity.md; they must be rerun against a frozen
   candidate before acceptance or reuse, not retroactively promoted.
   Read the project test instructions and verify commands, environment, tooling
   and side effects. Isolate data; production tests need explicit authorization.

   Map mandatory criteria to checks: unit, integration, negative paths,
   regression, build/install and real-provider behavior as required by scope.
   Do not invent a command or assume a tool exists; inspect project scripts.

   Deterministic checks must discriminate the requested symptom, not just show a command
   ran. Prefer public seams and independent expected values. For nondeterminism record
   seed, repetition budget and observed failure rate; never call flaky runs deterministic
   or synthetic fixtures real usage.

3. [ ] **Run available verification without repairing**

   Execute available relevant checks. Capture command, exit result, timestamp,
   environment, candidate, mock/real mode and sanitized output artifact in
   evidence.md. Record PASS, FAIL, NOT RUN, BLOCKED or UNKNOWN distinctly.

   For UI changes test the functional journey and, when possible, capture and
   inspect actual rendering with viewport/state and evidence path. ASCII and
   source review alone are inferred, not visual observation. Missing browser
   leaves visual acceptance open. A passing automation test need not prove
   full visual correctness.

   For installed-package or real-provider criteria use the exact candidate
   artifact/environment. Mock tests cannot substitute. Explicitly distinguish
   missing credentials/capability from a failing executed test.

   Run cheap near-change checks and risk-relevant regressions. Record exact cwd, relevant
   versions/fixtures, exit codes and timestamps; unknown data stays unknown. Formatting
   checks do not establish functional quality. Do not repair the frozen candidate or
   weaken criteria. If checks mutate inputs, record before/after identities and rerun on
   a stable candidate or disclose that proof does not match the final candidate.

4. [ ] **Integrate observations and coverage limits**

   Bind the observations collected in step 3 to the criterion/check matrix.
   Confirm candidate/environment identity remained stable, or mark affected proof
   invalid and rerun. Preliminary near-change checks retain limited provenance
   until replayed against the frozen candidate. Separate current results from
   justified retained evidence and expose uncovered criteria.

   When checks were delegated, verify each worker's scope, invocation/completion status, candidate/environment identity, replay commands and result locators. Integrate coverage and expose contradictions; incomplete or failed workers do not establish passing gates. Delegation is not required.

   Keep mandatory missing evidence, credentials, capabilities, permissions and required review/independence open; distinguish an executed failure from a blocked or not-run check. Test reports evidence, not acceptance, and does not repair the candidate.

   Preserve the possibly uncommitted candidate, artifacts and replay commands for Judge;
   missing mandatory evidence cannot become an implicit pass.

5. [ ] **Verify readiness and draft the phase response**

   Prepare the immediate next action and exact prerequisites, owner when known and expected result. Preserve the candidate and artifacts; supply the criterion/check matrix, actual results, failures/repro steps, replay commands and limits, and the inputs needed for a handoff; draft its state card and restart prompt only after reading the delivery guidance.

   After investigation and before drafting any user-facing phase response (including blocked or unchanged results), read [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and five-section report. Reuse unchanged guidance already loaded; combine overlapping reports without duplication. After reading delivery guidance, draft the response and, at an actual handoff, the fenced YAML state card and copy-ready restart prompt.

   Announce the Judge context transition when applicable; Test reports evidence, not acceptance.

6. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   After recording available verification, Load `agentic-development:judge`
   with candidate identity, criteria/check matrix, actual results and missing evidence.
   For a confirmed repair need, Load `agentic-development:iterate` with the
   failing criterion and replay command; do not silently edit the tested candidate.
   An unavailable mandatory check stays open and is handed off as a prerequisite.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
