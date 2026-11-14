# Judge output and handoff contract v1.4.0

Apply this contract only to judge. Read after investigation and before drafting the
phase response, with common-output.md directly linked from SKILL.md. Check both
before delivery. Operational requirements are separate in requirements-baseline.md.
The common contract selects compact delivery or the full five-heading Markdown envelope; this reference adds this phase's
content, not another final report or permission to write artifacts.

### judge

Report content: judgment report. Topics: Task and candidate; Goals and Non-goals;
Evidence (Requirement findings, Standards findings); Scoped verdict;
Rubric mode and score/coverage; Insights, risks and unknowns; Next action.
Assess FR/GWT and approved NFR bounds separately from coding standards; missing
measurement/required independence stays explicit. No self-approval.

Optional filename: `judgment.md` — not a required input or automatic write.
Deliver inline by default; save only through the common output contract’s explicit-destination,
permission and conflict checks. These topics belong in the selected delivery form or its linked
report; the full report places them in explanation, not additional outer headings.

## Result block

Keep the five outer headings. Put this fenced YAML block in explanation (or retain
it in the linked judgment report and show its verdict/score summary). It is a report
contract, not a runtime schema or permission grant. Replace illustrative values.

~~~yaml
verdict: accepted
review_mode: weighted
rubric_id: slice-acceptance
rubric_version: "1.1.0"
score_status: complete
score: 75
score_max: 100
assessment_coverage_percent: 100
blocking_findings: []
limitations: []
~~~

Use exact field names and values:

| Field | Required value / rule |
|---|---|
| verdict | accepted / needs-correction / indeterminate / not-run, with reason and scope in adjacent prose |
| review_mode | weighted / small-task; null only if no mode was selected and no review ran |
| rubric_id, rubric_version | Actual approved rubric identifier/version; null if unavailable, disclose the gap |
| score_status | complete / partial / not-applicable / not-assessed |
| score | Number 0–100 only for complete weighted assessment; otherwise null |
| score_max | 100 in weighted mode; null in small-task or unselected mode |
| assessment_coverage_percent | Assessed weight / total weight * 100 in weighted mode; null for small-task or not-run |
| blocking_findings | List confirmed blocking finding IDs, linked to evidence; [] means none confirmed, not proof of completeness |
| limitations | List concrete gaps or review limits; [] only when none were identified |

No numerical acceptance threshold is defined. Derive verdict from mandatory gates,
not score. Document criterion values, weights and calculation in the judgment report.
Keep unknown criteria null; never normalize a partial assessment. N/A is represented
by score_status: not-applicable and null numeric fields, not a zero score.

Use these variants; retain all other fields and replace the illustrative reason:

~~~yaml
# Partial weighted review: first four criteria rated 3, operability unknown.
verdict: indeterminate
review_mode: weighted
score_status: partial
score: null
score_max: 100
assessment_coverage_percent: 95
blocking_findings: []
limitations: ["Mandatory operability proof missing; earned points 71.25, assessed weight 95"]
~~~

~~~yaml
# Preselected small-task mode, mandatory evidence and independence satisfied.
verdict: accepted
review_mode: small-task
score_status: not-applicable
score: null
score_max: null
assessment_coverage_percent: null
blocking_findings: []
limitations: []
~~~

~~~yaml
# No review executed; weighted mode was selected in the plan.
verdict: not-run
review_mode: weighted
score_status: not-assessed
score: null
score_max: 100
assessment_coverage_percent: null
blocking_findings: []
limitations: ["Judge not executed"]
~~~

For a confirmed blocker, use needs-correction and its finding ID even if evidence
is also missing. For missing required independence, use indeterminate unless a
known blocker already establishes correction; a complete score may still exist.
A failed check is FAIL evidence; it establishes correction only when linked to a
confirmed defect or unmet mandatory criterion, not merely a tool/capability failure.

## Phase delivery checklist

Complete the common delivery checklist, then verify these judge obligations:

- [ ] Review requirements separately from standards; verify independence, scoped verdict and score mode.
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
phase: judge
roadmap_position: "Roadmap unavailable; resolve the named prerequisite before later phases"
current_goal: "Establish a reviewable cancellation slice"
success_criteria:
  - id: "AC-1 (illustrative)"
    expected: "Stopping a stream cancels the pending request"
    status: "unverified"
    evidence: "None: required prerequisite missing"
phase_output:
  requirement_findings: ["Criterion lacks bound evidence"]
  standards_findings: ["Not assessed"]
  verdict: "indeterminate"
change_explanation: "No unsupported success is claimed; the prerequisite remains visible."
files_modified: []
preserved_files: ["<verified initial user hunks, or none>"]
review_order:
  - path: "<requirement source>"
    reason: "Check requested behavior and authority first"
  - path: "<judge artifact or inline report>"
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
