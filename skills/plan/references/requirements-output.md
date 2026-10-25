# Plan output and handoff contract v1.2.0

Apply this contract only to plan. Before work read it with the common-output.md
contract directly linked from SKILL.md. Before delivery check both. The common
seven-heading Markdown envelope remains mandatory; this reference adds this phase's
content, not another final report or permission to write artifacts.

### plan

Artifact: plan.md. Headings: Outcome and task graph; Goals and Non-goals;
Scope and exclusions; Functional requirements (Given/When/Then);
Non-functional requirements (measurement matrix); Acceptance and verification matrix;
Public seams; Ownership and permissions; Review/closure policy; Commit boundaries;
Risks and stop budget; Next ready task and restart context. Map approved FR/NFR IDs
to checks and capabilities before declaring ready.

## Phase delivery checklist

Complete the common delivery checklist, then verify these plan obligations:

- [ ] Map approved scope and FR/NFR to checks, dependencies and ownership; name unresolved readiness decisions.
- [ ] Include the phase artifact or verified locator, remaining criteria and handoff inputs.

## Worked handoff example

Hypothetical missing-prerequisite example, not an executed run. Place this card
inside the common report's explanation; retain all seven outer headings. Replace
placeholders with verified values; use locators for long unchanged details.

~~~yaml
session:
  id: null
  status: "Identifier not exposed; no session launched"
current_tasks:
  - id: "<verified Beads ID, or N/A if no tracker>"
    status: "<read-back status, or unknown>"
phase: plan
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
