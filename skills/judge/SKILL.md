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

Execute the selected action through the workflow below. Read only the references
required by that action, reuse unchanged guidance already loaded in this context, and verify
the result before taking the next action. Loading this Skill is not authorization
for tracker writes, Git operations, installation or production effects.

## Workflow

Read each reference when its local condition applies, before the governed action
even if needed earlier than its numbered stage. Reuse unchanged loaded guidance.
These stages do not authorize additional phases or side effects.

1. [ ] **Verify scope, authority and reviewer prerequisites**

   Read [the requirements baseline](references/requirements-baseline.md) before
   defining or changing scope, criteria or verification, and before implementation.
   Reuse verified Goals/Non-goals, FR/GWT and applicable quantified NFRs; do not
   invent targets. Investigation needs a bounded question, not a completed plan.

   Read [the authorization policy](references/authorization-policy.md) before
   resuming artifact claims or executing consequential actions. Recorded permissions
   are historical unless their current authoritative source and scope are verified.

   If the repository uses Beads, read [the Beads integration](references/beads-integration.md)
   before choosing work or mutating task state. Use fresh `bd prime` guidance;
   retain task ownership, readback and phase gates;
   evaluate commit suitability after each confirmed closure without inferring Git authority.

   Read [the communication contract](references/communication-contract.md) before preparing
   the first checkpoint or a Git/session transition, for ownership, transition, evidence
   and conditional UI reporting safeguards. Apply these safeguards in standalone use too.
   Respond in the user's language. Verify tools and permissions; unavailable
   capabilities produce an explicit blocker, never simulated execution evidence.
   Use the coordinator's verified slice state when available; do not fabricate execution or acceptance.

   Before deriving a judgment, read [the judgment rubric](references/judgment-rubric.md) unless
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

   Read [candidate identity](references/candidate-identity.md) before planning checks,
   freezing inputs or reusing evidence; include staged, untracked and binary inputs
   and explicitly defined output-only exclusions. Read [the review policy](references/review-policy.md)
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

   Within judgment.md, include Requirement findings and Standards findings under the
   evidence section. Each finding needs criterion/source, location, observation,
   impact and minimal corrective check. Preserve the existing evidence/verdict/score/
   insights separation; no invented numeric score or acceptance from builder assertions.

   Review each mandatory acceptance criterion, risk-based security/regression,
   maintainability and operability. Missing evidence is unknown, not zero defects.
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

5. [ ] **Collect judgment facts and the immediate prerequisite**

   Collect judgment.md facts in the approved workspace, or return them inline
   when persistence is unavailable. Keep evidence, scoped verdict, rubric mode/score,
   insights (observed/inferred/to-verify), risks and unknowns separate; format the
   delivery only at the output gate below.
   Use accepted, needs-correction or indeterminate with reasons. If no review ran,
   report not-run and no score. Local acceptance is not real-provider approval.

   Collect checkpoint inputs: candidate, exact acceptance scope, open findings,
   immediate action and its prerequisite. Publish them only at the delivery gate;
   a proposed transition never authorizes closure or Iterate.

6. [ ] **Read delivery guidance and draft the phase response**

   After investigation and immediately before drafting any user-facing phase response (including blocked or unchanged results), read [the common output contract](references/common-output.md) and [this phase's delivery contract](references/requirements-output.md); apply their checklists and five-section report. Keep the canonical phase artifact within that report. Before drafting a proposed, performed, failed or externally observed commit report, read [the commit report](references/commit-report.md). Before drafting a planned session end, explicit wrap-up or recommended context transition report, read [the session report](references/session-report.md). Reuse unchanged guidance already loaded; combine overlapping reports without duplication.

   After reading delivery guidance, draft the actual handoff fenced YAML state card and copy-ready restart prompt; distinguish proposed from performed actions.

7. [ ] **Execute the handoff or stop**

   Execute the next phase only when it belongs to the user's requested workflow and
   current scope/permissions cover its actions. For a phase-only request, return the
   phase result and proposed handoff, then stop; do not expand the request by loading
   or executing a new phase. If continuing is authorized, apply the routes below.

   For needs-correction, Load `agentic-development:iterate` with the scoped
   verdict, evidence-linked findings and minimal corrective checks. For indeterminate,
   return the specific evidence/independence prerequisite, not a speculative correction.
   For accepted, return the exact accepted scope to the coordinator or user; perform no
   implicit issue closure, commit, merge or release.

   Use the host's available Skill-loading mechanism; these identifiers are not shell
   commands. If loading is unavailable, read the selected bundled SKILL.md and its
   required contained references, and report direct reading rather than activation.
   Pass a copy-ready handoff if execution cannot continue in this context. State the
   specific missing input, permission or capability, who can supply it when known,
   and the next executable action. Do not merely say "blocked" or "continue later".
