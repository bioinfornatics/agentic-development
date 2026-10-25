# Delegated investigation contract

Read before dispatching a selected Research mode. Workers explore in separate contexts; the coordinator keeps product context and integrates compact evidence-bound results. This internal worker contract is not the user-facing five-section report or a command to launch every mode.

## Dispatch and ownership

1. Give each worker the product objective, question, mode, scope/exclusions, source identity, useful pointers, allowed probes, permissions, capabilities and explicit agreed turn/time/output budget. Do not inject the full conversation or private builder reasoning. Resolve missing budget/capability rather than assume an override took effect.
2. Default to read-only source exploration. Do not mutate Beads, source, Git, installed plugins or host settings. The coordinator owns tracker updates. If persistence is authorized, assign one exclusive artifact path per worker; no overlapping writes, cleanup or secrets.
3. Usually locate files first, then delegate code/pattern analysis in parallel when inputs suffice. External research remains conditional. Unavailable delegation requires an explicit direct-investigation waiver or exact prerequisite, not silent fallback.
4. Observe actual completion and returned status. A failed invocation with a success-shaped summary is not a completed worker or accepted gate. Preserve partial findings as provisional and stop repeated no-progress retries.

## Compact common return

Return decision-relevant findings and verifiable pointers, not transcripts, exhaustive file lists or private chain-of-thought. Large extracts/logs stay in authorized artifacts. Without persistence, give a self-contained compact return and disclose that no artifact was saved. Use this shape or equivalent Markdown:

~~~yaml
mode: analyze_code
status: partial  # complete | partial | blocked: investigation status, not acceptance
question: <bounded question tied to product outcome>
scope:
  inspected: [<actually inspected paths/components/topics>]
  excluded: [<out-of-scope areas>]
source_identity:
  candidate: <verified identity, or unknown with provenance limit>
findings:
  - id: F1
    observation: <fact, or explicitly labeled inference>
    evidence: [E1]
    implication: <separate consequence for the decision>
evidence:
  - id: E1
    locator: <path:symbol:lines, URL:section, or local artifact>
    kind: source  # executed | source | external_claim
    source_version: <commit/version/date or unknown>
reading_references:
  - locator: <verified file/capture; URL if no local copy>
    section_or_symbol: <specific entrypoint or section>
    reason: <why this task needs this reading>
    read_order: 1
    priority: required  # supporting; only when relevant to the given task
    source_identity: <digest/commit/version/date or unknown>
unknowns:
  - question: <remaining uncertainty or contradiction>
    decision_impact: blocking  # nonblocking
    next_probe: <smallest discriminating verification>
execution:
  checks: [<actual command/result, or NOT RUN with reason>]
  changes: none
  artifact: <verified output path/digest, or not saved>
~~~

References are curated task inputs, not a bulk-reading mandate. Include inspected relevant sources with reasons and entrypoints; label proposed or inaccessible sources separately. Relative paths need a workspace root; line ranges need a symbol/section and source identity to survive drift.

## Mode-specific payload

| Mode | Retain | Do not claim |
|---|---|---|
| find_files | Paths, roles, boundaries, product docs, implementation/test entrypoints, searched areas with no result | Location proves behavior or exhaustive coverage |
| analyze_code | Relevant input/data/control flow, effects, invariants, public seams, errors, tests and source symbols | Source reading proves executed behavior or confirmed bug cause |
| find_patterns | Representative examples/tests, observed conventions, applicability, differences, reuse/extend/avoid rationale | Existing code is automatically best practice or a project rule |
| state_of_the_art | Date/version window, primary claims, maturity, conflicts, applicability, decision impact and authorized local captures | Snippets/access dates/benchmark claims establish recency or effectiveness |

## Coordinator integration gate

Deduplicate without losing evidence; expose contradictions and verify decision-critical conclusions against accessible sources or bounded probes. Separate source observations, executed behavior and external claims. A worker result is not an independent acceptance review. Synthesize product context, behavior/seams, patterns, alternatives, constraints, unknowns and next decision rather than concatenate worker reports.
Retain task-specific reading references and pass them to Plan; record in Beads only under applicable tracking/permission rules. If artifacts are inaccessible to the next worker/session, repair the locator or preserve essential findings inline; do not claim durable handoff.
