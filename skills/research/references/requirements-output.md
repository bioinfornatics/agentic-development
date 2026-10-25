# Research output and handoff contract v1.3.0

Apply this contract only to research. Read after investigation and before drafting the
phase response, with common-output.md directly linked from SKILL.md. Check both
before delivery. Operational requirements are separate in requirements-baseline.md.
The common five-heading Markdown envelope remains mandatory; this reference adds this phase's
content, not another final report or permission to write artifacts.

### research

Report content: research report. Topics: Product context and requested outcome; Question and task;
Goals and Non-goals; Context coverage/freshness and reuse rationale; Sources and affected paths; Investigation modes and findings; Optional state of the art (dated sources or N/A); Observed findings; Hypotheses and discriminating probes;
Task reading references (locator, section/symbol, reason, order, identity and freshness); Delegated worker status and evidence limits; Options and risks; Requirement gaps (FR/NFR proposed or N/A); Recommendation and
unresolved questions; Handoff. Separate observations from hypotheses and targets.

Optional filename: `research.md` — not a required input or automatic write.
Deliver inline by default; save only through the common output contract’s explicit-destination,
permission and conflict checks. These topics belong inside explanation or its linked
report, not additional outer response headings.

## Phase delivery checklist

Complete the common delivery checklist, then verify these research obligations:

- [ ] Evidence product purpose, users/outcome, current behavior and relevant constraints, or mark unknowns and their decision impact.
- [ ] Verify context coverage/freshness before reuse; separate observations from hypotheses and identify affected paths and unresolved questions.
- [ ] Tie WHERE/HOW/pattern findings to sources; when web freshness matters, report publication/version/access dates or missing capability, without inventing recency.
- [ ] Verify worker completion separately from findings; retain curated reading references and authorized offline capture provenance/digests, or disclose unavailable persistence.
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
phase: research
roadmap_position: "Roadmap unavailable; resolve the named prerequisite before later phases"
current_goal: "Establish a reviewable cancellation slice"
success_criteria:
  - id: "AC-1 (illustrative)"
    expected: "Stopping a stream cancels the pending request"
    status: "unverified"
    evidence: "None: required prerequisite missing"
phase_output:
  product_context: "User cancellation outcome known; current journey requires source verification"
  context_gaps: ["Current behavior and boundary constraints need primary sources"]
  observations: ["Supplied trace lacks a cancellation signal"]
  hypotheses: ["Adapter may not propagate cancellation"]
  open_questions: ["Which public seam discriminates this hypothesis?"]
change_explanation: "No unsupported success is claimed; the prerequisite remains visible."
files_modified: []
preserved_files: ["<verified initial user hunks, or none>"]
review_order:
  - path: "<requirement source>"
    reason: "Check requested behavior and authority first"
  - path: "<research artifact or inline report>"
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
  phase: plan
  status: blocked
  reason: "Continue only after the missing prerequisite is resolved"
  prerequisite: "<specific missing input, capability or decision>"
restart:
  session_action: not_performed
  prompt: "Resume the verified task; read its current criteria, this phase result and candidate. Recheck ownership and permissions. Resolve the named prerequisite before execution; no Git or installation authority is granted by this example."
~~~
