# Iterate output and handoff contract v1.3.0

Apply this contract only to iterate. Read after investigation and before drafting the
phase response, with common-output.md directly linked from SKILL.md. Check both
before delivery. Operational requirements are separate in requirements-baseline.md.
The common five-heading Markdown envelope remains mandatory; this reference adds this phase's
content, not another final report or permission to write artifacts.

### iterate

Artifact: iteration.md. Headings: Finding and task; Goals and Non-goals;
Unchanged criteria (FR/NFR IDs); Current candidate and retained proof;
Cause hypothesis and reproduction; Capability/budget decision; Authorized correction;
Observed result and invalidated evidence; Next phase and restart conditions.
Record counter before/after, selective proof invalidation and original GWT/NFR rerun.
Capability-only waiting consumes zero attempts; no weaker criteria to make tests pass.

## Phase delivery checklist

Complete the common delivery checklist, then verify these iterate obligations:

- [ ] Record counter before/after, retained/invalidated proof and unchanged criteria; waiting consumes zero attempts.
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
phase: iterate
roadmap_position: "Roadmap unavailable; resolve the named prerequisite before later phases"
current_goal: "Establish a reviewable cancellation slice"
success_criteria:
  - id: "AC-1 (illustrative)"
    expected: "Stopping a stream cancels the pending request"
    status: "unverified"
    evidence: "None: required prerequisite missing"
phase_output:
  attempt_counter: {before: 0, after: 0}
  retained_proof: ["None supplied"]
  invalidated_proof: ["None: candidate unchanged"]
change_explanation: "No unsupported success is claimed; the prerequisite remains visible."
files_modified: []
preserved_files: ["<verified initial user hunks, or none>"]
review_order:
  - path: "<requirement source>"
    reason: "Check requested behavior and authority first"
  - path: "<iterate artifact or inline report>"
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
  phase: test
  status: blocked
  reason: "Continue only after the missing prerequisite is resolved"
  prerequisite: "<specific missing input, capability or decision>"
restart:
  session_action: not_performed
  prompt: "Resume the verified task; read its current criteria, this phase result and candidate. Recheck ownership and permissions. Resolve the named prerequisite before execution; no Git or installation authority is granted by this example."
~~~
