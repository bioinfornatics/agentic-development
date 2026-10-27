# Plan output and handoff contract v1.4.0

Apply this contract only to plan. Read after investigation and before drafting the
phase response, with common-output.md directly linked from SKILL.md. Check both
before delivery. Operational requirements are separate in requirements-baseline.md.
The common contract selects compact delivery or the full five-heading Markdown envelope; this reference adds this phase's
content, not another final report or permission to write artifacts.

### plan

Report content: planning report. Topics: Outcome and task graph; Goals and Non-goals;
Scope and exclusions; Functional requirements (Given/When/Then);
Non-functional requirements (measurement matrix); Acceptance and verification matrix;
Public seams; Ownership and permissions; Review/closure policy; Commit boundaries;
Risks and stop budget; Next ready task and restart context. Map approved FR/NFR IDs
to checks and capabilities before declaring ready.

Optional filename: `plan.md` — not a required input or automatic write.
Deliver inline by default; save only through the common output contract’s explicit-destination,
permission and conflict checks. These topics belong in the selected delivery form or its linked
report; the full report places them in explanation, not additional outer headings.

## Phase delivery checklist

Complete the common delivery checklist, then verify these plan obligations:

- [ ] Verify cited research product context and coverage/freshness; report decision-critical gaps before planning.
- [ ] Attach verified task-specific reading references with locator/root, section/symbol, reason, read order, source identity and freshness limits; read back authorized tracker updates. A local capture is knowledge, not task truth or proof of currency.
- [ ] Map approved scope and FR/NFR to checks, dependencies and ownership; name unresolved readiness decisions.
- [ ] Include the phase artifact or verified locator, remaining criteria and handoff inputs.

## Worked handoff example

Hypothetical missing-prerequisite example, not an executed run. Place this card
inside the common report's explanation; retain all five outer headings. Replace
placeholders with verified values; use locators for long unchanged details.

~~~yaml
session:
  id: null
  status: "Identifier not exposed; no session launched"
current_tasks:
  - id: "<verified Beads ID, or N/A if no tracker>"
    status: "<read-back status, or unknown>"
phase: plan
roadmap_position: "Roadmap unavailable; resolve the named prerequisite before later phases"
current_goal: "Establish a reviewable cancellation slice"
success_criteria:
  - id: "AC-1 (illustrative)"
    expected: "Stopping a stream cancels the pending request"
    status: "unverified"
    evidence: "None: required prerequisite missing"
phase_output:
  scope: "Cancellation propagation"
  dependencies: ["Agree the transport test seam"]
  next_ready_task: "Resolve the public seam"
change_explanation: "No unsupported success is claimed; the prerequisite remains visible."
files_modified: []
preserved_files: ["<verified initial user hunks, or none>"]
review_order:
  - path: "<requirement source>"
    reason: "Check requested behavior and authority first"
  - path: "<plan artifact or inline report>"
    reason: "Review this phase's result and unresolved criteria next"
git:
  branch: "<observed branch, or N/A>"
  commit: {status: not_performed, hash: null}
  push: {status: not_performed, remote_ref: null}
  merge: {status: not_performed, merge_hash: null}
immediate_action:
  owner: "<verified owner, or unknown>"
  action: "Resolve the named prerequisite in the current phase"
  prerequisite: "<specific missing input, capability or decision>"
conditional_next_phase:
  phase: implement
  status: blocked
  reason: "Continue only after the missing prerequisite is resolved"
  prerequisite: "<specific missing input, capability or decision>"
restart:
  session_action: not_performed
  prompt: "Resume the verified task; read its current criteria, this phase result and candidate. Recheck ownership and permissions. Resolve the named prerequisite before execution; no Git or installation authority is granted by this example."
~~~
