---
name: judge
description: Reviews a frozen software candidate for acceptance. Use when testing is complete or an independent judgment of requirement fidelity and repository standards is requested.
---

# Judge

## Select the action from the intent

Resolve approved scope, frozen candidate, evidence index, review mode and independence policy. Identify the reviewer and validate provenance before deriving a verdict.

| Intent / condition | Execute | Required result |
|---|---|---|
| Review a tested candidate for acceptance | Verify scope, candidate, evidence and required independence; review every mandatory criterion | Scoped verdict, actionable findings and uncertainties |
| Review requirement fidelity and repository standards | Assess requested behavior separately from documented quality standards | Separate requirement and standards findings with sources and corrective checks |
| Score a candidate | Apply the review mode and rubric agreed before implementation | Evidence-derived weighted score/coverage, or N/A in predefined small-task mode |
| Evidence or required independence is missing | Record the exact gap; use indeterminate unless a known defect already requires correction | Specific prerequisite, not self-approval or an invented pass |

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

1. [ ] **Verify scope, authority and reviewer prerequisites**

   Apply [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or checks. Resolve the approved task baseline;
   retain Goals/Non-goals, FR/GWT and relevant NFRs; keep missing requirements explicit.

   Apply [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions; verify current
   permission for the intended action, not historical approval.

   Before creating or repairing task descriptions or acceptance criteria, apply
   [ticket authoring](references/ticket-authoring.md); verify readable purpose,
   criteria, ordered inputs and restart context without duplicating execution history.

   If the repository uses Beads, apply [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Use fresh `bd prime` guidance;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Apply [the communication contract](references/communication-contract.md) before preparing
   the first checkpoint or a Git/session transition, for ownership, transition, evidence
   and conditional UI reporting safeguards. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   Use the coordinator's verified slice state when available; do not fabricate execution or acceptance.

   Before deriving a judgment, apply [the judgment rubric](references/judgment-rubric.md) unless
   an explicitly approved replacement rubric is supplied. Record its version.

   Require approved acceptance scope, frozen candidate identity, diff/ownership
   ledger, evidence index and known limitations. Recommend an independent context
   before judgment; announce the transition and prepare a handoff without an
   automatic commit. Identify reviewer/context and all required independence dimensions from the review policy.
   Require the plan-time independence decision; default US acceptance requires
   independent review. A new session alone is insufficient. If reviewing your own work in the
   same context, disclose limited self-review; never claim independence. If required
   independence is unavailable, the verdict is indeterminate unless a known blocker
   already justifies needs-correction.

2. [ ] **Bind the frozen candidate and review basis**

   Apply [candidate identity](references/candidate-identity.md) before planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions. Apply [the review policy](references/review-policy.md)
   before agreeing acceptance, judging or closing a task/US. Independence and closure
   requirements are set before implementation, not waived by a missing capability.
   For exact-candidate proof, use the contained [capture/validate/compare CLI](scripts/candidate_identity.py) with the [scope example](references/candidate-scope.example.json); consult the [manifest schema](references/candidate-identity.schema.json) and [manifest example](references/candidate-identity.example.json) when preparing or validating its JSON. Follow the candidate procedure above; equality is not acceptance.

   Match proofs to candidate/environment and scope. Inspect relevant code and
   actual test artifacts; do not accept builder summaries as sole proof.

3. [ ] **Review requirements and standards separately**

   Identify the requirement/specification and documented standards for the exact
   candidate. Report requirement fidelity (missing, incorrect or unauthorized behavior)
   separately from repository standards/maintainability. A passing standards review
   cannot compensate for implementing the wrong behavior. Missing specification or
   standard sources are disclosed, not invented. A pinned Git comparison is useful
   but must include relevant staged, dirty and untracked inputs in candidate identity.

   Treat code smells as labeled heuristics, not hard violations; project standards
   take precedence over generic taste. Do not repeat automated checks as unsupported
   manual findings. Use parallel read-only reviewers only when capabilities and
   independence requirements are satisfied; different sessions/models alone are not proof.

   Collect Requirement findings and Standards findings separately for the judgment
   report evidence section. Each finding needs criterion/source, location, observation,
   impact and minimal corrective check. Preserve the existing evidence/verdict/score/
   insights separation; no invented numeric score or acceptance from builder assertions.

   Review each mandatory acceptance criterion, risk-based security/regression,
   maintainability and operability. Missing evidence is unknown, not zero defects.
   For application-test evidence, challenge marginal detection value and independent
   oracles: mock self-validation, copied expected calculations, vague assertions for
   exact outcomes, success/error ambiguity and missing important error paths cannot
   support the claimed guarantee. Review rationalization decisions against preserved
   product coverage, not legacy volume; a green test count is not quality or acceptance.
   Check observed failing counterexamples versus hypothetical faults and required
   end-to-end CI wall time versus aggregate/local durations. Missing measurements or
   discrimination stay explicit; do not infer CI acceptance from parallel local runs.
   Keep this review risk-scoped; no exhaustive new test/mutation campaign or candidate
   edits during Judge.
   Reproduce checks only when capabilities and permissions allow; do not mutate
   the candidate or repair code while judging.

   If specialist or parallel reviewers are used, verify actual invocation/completion status, source/candidate identity, result locators and required independence. Incomplete results remain provisional.

4. [ ] **Verify findings and derive the scoped verdict**

   For code review or specialist findings, read [finding verification](references/finding-verification.md)
   before publishing claims. Check surrounding context and reachable failure paths,
   separate observed from inferred evidence, justify severity by impact and consolidate
   duplicates. Keep mandatory defects and missing-evidence gates; a filter against
   unsupported findings is not permission to suppress a required acceptance failure.

   Record findings with severity, location, criterion, evidence, impact and
   corrective verification. Distinguish blocking defects from recommendations.

   Apply the plan-time review mode in the versioned rubric. In weighted mode,
   calculate criterion values, coverage and score from evidence, keeping unknowns
   null. In small-task mode report score not-applicable, without numeric grading.
   Neither mode can override a failed mandatory gate or waive independence.

   Unknown criteria and incomplete overall score remain null; never normalize partial assessment into a complete score.

   Accept only an exact candidate with every mandatory criterion evidenced and no
   blocking findings. Candidate changes invalidate affected judgment. Never silently
   relax criteria, retroactively redefine the rubric or approve your own human gate.

   **Result contract**

   Return one scoped verdict and a separate score state; PASS/FAIL labels belong to
   executed checks, not the acceptance verdict. Use these exact verdict values:

   | Verdict | Choose when |
   |---|---|
   | `accepted` | Every mandatory criterion is evidenced, no blocker remains and required independence is satisfied |
   | `needs-correction` | A confirmed defect or unmet mandatory criterion requires correction; known blockers take precedence over gaps |
   | `indeterminate` | Required evidence, capability, provenance or independence is missing, with no known blocker establishing correction |
   | `not-run` | No Judge review was executed; do not assign a score |

   Use the plan-time mode: `weighted` yields a 0–100 score only when every rubric
   criterion is assessed; unknowns leave the overall score null. `small-task` yields
   score N/A. A high score never overrides mandatory gates; 75/100 can mean conformity,
   not failure. At step 6 emit the delivery contract's result block inside explanation,
   with reasons and evidence; do not create another outer report or runtime JSON.


5. [ ] **Collect judgment facts and the immediate prerequisite**

   Collect judgment report facts for inline delivery or an explicitly authorized
   saved report. Keep evidence, scoped verdict, rubric mode/score,
   insights (observed/inferred/to-verify), risks and unknowns separate; format the
   delivery only at the output gate below.
   Use accepted, needs-correction or indeterminate with reasons. If no review ran,
   report not-run and no score. Local acceptance is not real-provider approval.
   Collect verdict, review mode, rubric identity/version, score state/coverage,
   blockers and limitations for the result block; do not invent missing values.

   Collect checkpoint inputs: candidate, exact acceptance scope, open findings,
   immediate action and its prerequisite. Publish them only at the delivery gate;
   a proposed transition never authorizes closure or Iterate.

6. [ ] **Read delivery guidance and draft the phase response**

   After investigation and immediately before drafting any user-facing phase response (including blocked or unchanged results), apply [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and selected delivery form (compact when eligible, otherwise five-section report). Keep the canonical phase artifact within that report. Before drafting a proposed, performed, failed or externally observed commit report, apply [the commit report](references/commit-report.md). Before drafting a planned session end, explicit wrap-up or recommended context transition report, apply [the session report](references/session-report.md). Combine overlapping reports without duplication.

   After reading delivery guidance, draft the actual handoff fenced YAML state card and copy-ready restart prompt; distinguish proposed from performed actions.

7. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   Select exactly one route from the verdict; record its owner, prerequisite and expected result.

   | Verdict | Immediate action | Required inputs / result |
   |---|---|---|
   | `accepted` | Return the exact accepted scope to the coordinator/user; no implicit closure, commit, push, merge or release | Candidate ID, criterion evidence, score state and limits; any publication/closure needs separate authority |
   | `needs-correction` | If continuation is authorized, Load `agentic-development:iterate`; otherwise return the proposed correction handoff and stop | Confirmed finding IDs, scoped verdict, candidate, evidence, minimal corrective checks and current correction budget; repair then Test and Judge the changed candidate |
   | `indeterminate` | Resolve the named proof/capability/provenance/independence gap; no speculative code repair | Name missing input and supplier; route missing checks to Test only when authorized, or request the required reviewer/access. Re-run Judge when prerequisites are satisfied; a newly confirmed defect changes the route to needs-correction |
   | `not-run` | Execute Judge only if requested and its prerequisites are available; otherwise return its prerequisite checklist and stop | Approved scope, frozen candidate, evidence index, plan-time mode and reviewer/independence; first review produces a verdict, not an assumed failure or acceptance |

   needs-correction means change a confirmed defective candidate; indeterminate means
   establish whether it can be judged. Keep them distinct because their actions differ.
   Missing permission blocks the selected action, not permission to substitute another route.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
