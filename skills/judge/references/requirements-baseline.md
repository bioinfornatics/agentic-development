# Requirements baseline v1.3.0

Read before defining or changing scope, criteria or verification, and before implementation.
Reuse a verified baseline; investigation needs a bounded question, not a completed plan.
These requirements govern actions, not final-response formatting.

## Goals and Non-goals

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

