# Cycle output and handoff contract v1.2.0

Apply this contract only to cycle. Before work read it with the common-output.md
contract directly linked from SKILL.md. Before delivery check both. The common
seven-heading Markdown envelope remains mandatory; this reference adds this phase's
content, not another final report or permission to write artifacts.

### cycle

Artifact: cycle state. Headings: Active outcome and task; Goals and Non-goals;
FR/NFR baseline; Phase and gate; Evidence and blockers; Authorized next action;
Restart point. Finalization links verified task updates, observed Git/Entire context
and checked scope; parent/release gates remain separate.

## Phase delivery checklist

Complete the common delivery checklist, then verify these cycle obligations:

- [ ] Verify actual phase/gate, active blockers, owner and one authorized next action.
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
phase: cycle
current_goal: "Establish a reviewable cancellation slice"
success_criteria:
  - id: "AC-1 (illustrative)"
    expected: "Stopping a stream cancels the pending request"
    status: "unverified"
    evidence: "None: required prerequisite missing"
phase_output:
  active_gate: "Missing Test evidence"
  blockers: ["Required fixture unavailable"]
change_explanation: "No unsupported success is claimed; the prerequisite remains visible."
files_modified: []
preserved_files: ["<verified initial user hunks, or none>"]
review_order:
  - path: "<requirement source>"
    reason: "Check requested behavior and authority first"
  - path: "<cycle artifact or inline report>"
    reason: "Review this phase's result and unresolved criteria next"
git:
  branch: "<observed branch, or N/A>"
  commit: {status: not_performed, hash: null}
  push: {status: not_performed, remote_ref: null}
  merge: {status: not_performed, merge_hash: null}
recommended_next_step:
  phase: test
  status: blocked
  reason: "Continue only after the missing prerequisite is resolved"
  prerequisite: "<specific missing input, capability or decision>"
restart:
  session_action: not_performed
  prompt: "Resume the verified task; read its current criteria, this phase result and candidate. Recheck ownership and permissions. Resolve the named prerequisite before execution; no Git or installation authority is granted by this example."
~~~
