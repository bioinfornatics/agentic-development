# Test output and handoff contract v1.5.0

Apply this contract only to test. Read after investigation and before drafting the
phase response, with common-output.md directly linked from SKILL.md. Check both
before delivery. Operational requirements are separate in requirements-baseline.md.
The common contract selects compact delivery or the full five-heading Markdown envelope; this reference adds this phase's
content, not another final report or permission to write artifacts.

### test

Report content: verification report. Topics: Task and candidate; Goals and Non-goals;
Acceptance-to-check matrix (FR/GWT and NFR IDs); Commands and environment;
Results and artifact locators; Coverage and limitations; Failures/reproduction;
Judge handoff. For application-test selection/rationalization include guarantee,
incorrect behavior, independent oracle, marginal detection and retain/merge/remove/replace
decisions with actual/proposed status and lost/preserved coverage. Separate defects
actually detected (reproduction evidence) from hypothetical faults and unverified gaps.
Report required end-to-end CI wall time/environment/window separately from summed test
or aggregate compute durations; unavailable CI measurements stay UNKNOWN/NOT RUN.
Do not substitute test-count changes or parallel local timing for value or CI proof.
For NFR record metric values/context or not-run/blocker; never
replace an approved target with a convenient observation.

Optional filename: `evidence.md` — not a required input or automatic write.
Deliver inline by default; save only through the common output contract’s explicit-destination,
permission and conflict checks. These topics belong in the selected delivery form or its linked
report; the full report places them in explanation, not additional outer headings.

## Phase delivery checklist

Complete the common delivery checklist, then verify these test obligations:

- [ ] Bind commands/environment/results to candidate; distinguish PASS/FAIL/NOT RUN/BLOCKED and coverage limits.
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
phase: test
roadmap_position: "Roadmap unavailable; resolve the named prerequisite before later phases"
current_goal: "Establish a reviewable cancellation slice"
success_criteria:
  - id: "AC-1 (illustrative)"
    expected: "Stopping a stream cancels the pending request"
    status: "unverified"
    evidence: "None: required prerequisite missing"
phase_output:
  candidate: "Unknown: exact freeze required"
  results: ["NOT RUN: transport fixture unavailable"]
  coverage_limits: ["No real-provider proof"]
change_explanation: "No unsupported success is claimed; the prerequisite remains visible."
files_modified: []
preserved_files: ["<verified initial user hunks, or none>"]
review_order:
  - path: "<requirement source>"
    reason: "Check requested behavior and authority first"
  - path: "<test artifact or inline report>"
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
  phase: judge
  status: blocked
  reason: "Continue only after the missing prerequisite is resolved"
  prerequisite: "<specific missing input, capability or decision>"
restart:
  session_action: not_performed
  prompt: "Resume the verified task; read its current criteria, this phase result and candidate. Recheck ownership and permissions. Resolve the named prerequisite before execution; no Git or installation authority is granted by this example."
~~~
