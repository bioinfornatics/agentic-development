# Common requirements and output contract v1.2.0

Mandatory for all seven phases, including standalone use. These are Markdown formats,
not a runtime schema or automatic notification hook. Keep candidate/permission/review
gates. Respond in the user's language; retain the exact final labels and order
and translate their values. Reuse verified task records, not a second task database.

## Requirements baseline

Before implementation, state Goals and Non-goals explicitly with stable IDs and the
requirement/task source. Goals describe observable outcomes; Non-goals name excluded
behavior, environments and operations. Distinguish approved goals from proposals.
Each phase carries the same baseline or a verified locator and a short summary.
Research records a research question and deliverable, not invented product acceptance.

### Functional requirements (FR)

Use Given/When/Then systematically for every functional acceptance criterion,
including relevant error, cancellation and boundary paths. One observable behavior
per scenario; And adds related conditions/outcomes only. Assign an ID, source and
public verification seam. Then must be independently observable, not a private
implementation detail or copied algorithm logic. Do not force a research question,
source-hash check or pure documentation criterion into fake user behavior; mark FR
N/A with a reason and use a verifiable deliverable criterion instead.

| ID / source | Given (state/data/preconditions) | When (action/event) | Then (observable result) | Check / seam | Status / evidence |
|---|---|---|---|---|---|
| FR-<id> / <verified source> | <precondition> | <single action> | <expected value/invariant> | <test/observation> | <approval and check status> |

### Non-functional requirements (NFR)

NFR means non-functional requirements. For each relevant quality constraint, record
Metric, Target (comparator included), Unit, Workload/data size and duration,
Environment, Measurement method/sample window, and Approval/source. Quantify latency,
throughput, resource use, reliability and other measurable constraints when relevant.
Record a known baseline separately from an approved target. For security/accessibility
also identify standard/version and an observable pass/fail check; quantify meaningful
limits, not fake numbers.

| ID / source | Metric | Target | Unit | Workload / window | Environment | Measurement / check | Approval | Status / evidence |
|---|---|---|---|---|---|---|---|---|
| NFR-<id> | <metric or standard/version> | <approved bound or unresolved> | <unit or N/A reason> | <load/data/duration/sample> | <scope/config> | <method/tool/pass rule> | <source or pending> | <not-run/PASS/FAIL/BLOCKED/UNKNOWN> |

Do not invent targets, approval, sample sizes or measured results. Label suggestions
proposed and obtain the responsible decision before using them as acceptance limits.
Missing mandatory bounds or measurement capability leave the criterion unresolved/
blocked, not passed. If none applies, write NFR: N/A — <scope-based reason>, retaining
existing project-wide constraints. Avoid vague "fast" or "secure" requirements.
A measurement proves only its workload/environment/window. GWT may reference an NFR
ID; retain its numerical measurement definition in the NFR matrix.

## Mandatory seven-field final report

End every phase delivery with this report, including standalone use, blocked work,
no-change results and explicit wrap-up. Keep these exact English labels and order;
write values and the explanation in the user's language. Use Markdown headings,
not JSON. This is the sole final envelope, not an additional summary after another
report. In-progress updates may remain concise. The current phase may vary; fields
must not be omitted. No blank values or fabricated execution.

~~~markdown
## step
<cycle|research|plan|implement|test|judge|iterate>

## modified files
N/A — <no files changed in this delivery, with reason>
OR
- <+ added / ~ modified / - removed / renamed old -> new path — purpose>

## next step
<cycle|research|plan|implement|test|judge|iterate|loop again|blocked|done>

## current goal
<short description of the objective addressed, with verified task ID if available>

## next goal
<short description of the next objective or missing prerequisite; N/A if done>

## closed tasks
N/A — <no confirmed closures in this delivery, or tracker unavailable>
OR
- <verified ID — title and confirmed closed status; performed or externally observed>

## explanation
<Pedagogical explanation: what was done, why, what the evidence establishes and
what remains. Include the applicable details below and the commit evaluation for
each confirmed closed task. Distinguish proposed, performed, failed and observed.>
~~~

Report only files actually changed by this delivery; separate preserved user hunks
in the explanation, never attribute the entire initial dirty tree to the agent.
List repository-relative paths, including removed paths and both sides of renames.
A modified file is not necessarily committed. Read back tracker status before
listing confirmed closed tasks; failed/proposed closures stay out of that list and
are explained as failed/proposed. Do not invent tasks on non-Beads work.

For cycle, step is the last substantive phase actually performed when identifiable,
otherwise cycle for coordination-only work. next step is a recommendation unless
explicitly reported as already performed. loop again means repeat the current phase;
name the correction and retained criteria. blocked names the missing prerequisite,
not an executable phase. done means the requested scope is complete, not that its
parent, release or deployment is accepted. Do not launch a new phase by reporting it.

Retain phase-specific artifacts and the existing evidence/permission/acceptance
requirements. Put their essential facts or verified locators under explanation.
Use the boundary facts below inside explanation when relevant to a full boundary;
they are supporting content, not a competing final envelope. For a small
phase delivery, concise prose or bullets can cover the same applicable facts.

## Boundary facts and preservation

At commit, judgment or session boundaries include the applicable facts once inside
explanation: verified task and requirement source, candidate/environment/checks and
coverage, owned versus preserved files, actual branch/commit/push/merge state,
tracker readback, reviewer independence and verdict/score, session recommendation
versus actual action, and copy-ready restart instructions. Use the directly linked
commit/session references when their conditions apply; never infer Entire identifiers.
No blank required values: use unknown, not-run, blocked or N/A with a reason.
Unchanged criteria keep their IDs and approval; do not silently lower targets, omit
negative paths or redefine Non-goals. Scope changes need current authority.
A new artifact format is not permission to create files or a competing task database.

## Common delivery checklist

Read this contract before work; before delivery verify it together with the current
phase contract. Reuse already loaded unchanged guidance rather than reload blindly.

- [ ] Keep the seven exact final headings in order, including blocked/no-change work.
- [ ] Identify the actual phase, verified task/status, goal and success criteria.
- [ ] Separate observations from proposals, unknowns and hypothetical examples.
- [ ] Report owned files separately from preserved user work; give review order and reasons.
- [ ] Verify session, candidate, tracker and Git claims; mark unavailable identifiers explicitly.
- [ ] Report commit, push and merge separately with status and observed identifiers.
- [ ] Explain the next action, prerequisite and current permission boundary pedagogically.
- [ ] At a handoff boundary give a copy-ready restart prompt; do not auto-launch a session.

## State card inside explanation

For a phase handoff, use the current phase's worked YAML example as a compact state
card inside explanation. For small in-progress checkpoints, concise prose may express
the same applicable facts. This is not a second final envelope, runtime schema, task
database or automatic file write. Beads remains task truth. Use verified locators
for long unchanged detail; retain the essential next action and its prerequisite.
Example keys stay English; translate human-readable values into the user's language.
Examples are hypothetical, not evidence or permission. Replace placeholders with
verified values or unknown, not-run, blocked or N/A with a reason.

Required state: session identifier/status, current tasks/statuses, goal, success
criteria/status/evidence, phase, pedagogical explanation, modified/preserved files,
review order/reasons, separate commit/push/merge statuses, next action/prerequisite
and restart context. Git statuses: not_performed, proposed, performed, failed,
blocked, externally_observed. Pending requires a concrete waiting condition.
A merged branch is not a commit status; a saved state card grants no authority.
