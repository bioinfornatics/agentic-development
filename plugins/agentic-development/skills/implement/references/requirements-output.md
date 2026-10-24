# Requirements and output contract v1.1.0

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
Use the six detail groups below inside explanation when relevant to a full boundary;
they are supporting content, not a competing six-section final envelope. For a small
phase delivery, concise prose or bullets can cover the same applicable facts.

## Supporting checkpoint details inside explanation

Full boundaries include all applicable fields below once inside explanation; combine
overlapping commit/session details rather than emit parallel final reports.
No blank required values: use none, N/A with reason, unknown, not-run or blocked.
A locator replaces unchanged detail only if accessible and candidate/version identified;
inline essential scope and next action. The sample is a format, not observed evidence.

~~~markdown
## 1. Objective and scope
- Task / phase / milestone, epic, US: <verified IDs or unknown/N/A>
- Goals: <approved outcomes or proposal; requirement locator>
- Non-goals: <excluded behavior/operations/environment>
- FR: <GWT IDs and locator, or N/A reason>
- NFR: <approved measured constraints and locator; unresolved/N/A reasons>

## 2. Result
- Outcome / completed scope: <facts>
- Incomplete / unchanged criteria: <IDs and status>
- Phase artifact: <actual locator or inline/not saved>

## 3. Changes and evidence
- Files: <+ added / ~ modified / - removed / renamed old -> new / none>
  <each affected path/reason/owned hunks; separate preserved user work>
- Branches: <none / proposed / created / switched / failed / externally observed>
  <current branch/base/actual new branch; command/result or not performed>
- Commits: <none / proposed / performed / failed / externally observed>
  <actual hash/message/committed paths or proposal/error; never invented>
- Remaining state: <staged / unstaged / untracked; inspected result or unknown>
- Evidence: <criterion ID, candidate, command/observation, cwd/environment,
  actual exit/result, mock/static/real mode, timestamp, artifact and limits>
- Tracker / Entire: <verified update/readback and IDs or unavailable reason>

## 4. Verdict and uncertainties
- Verdict / scope / reviewer independence: <result/not-run/indeterminate>
- Score / rubric / mode: <numeric when required; N/A in agreed small-task mode>
- Findings / risks: <observed/inferred/to-verify; unresolved criteria>

## 5. Transition
- Recommended next phase/action: <reason and authorization/decision needed>
- Session recommendation: <continue / fresh session recommended / none required>
- Reason / next-session proposed name and goal: <one objective or N/A reason>
- Session action: <not performed / performed / unavailable; verified ID if exposed>
- Handoff: <actual path or inline/not saved; preserved work/resume conditions>

## 6. Next action and restart
- First action / expected result / prerequisite or blocker: <concrete step>
- Task/dependency/ownership and permission rechecks: <restart checks>
- At a session boundary: <copy-ready standalone restart prompt or inline locator>
~~~

Notify affected files after meaningful change batches. Announce branch/commit/session
intent before acting, then report observed results immediately after. A proposed branch
is not created; a proposed commit has no hash; recommending a session does not launch
it or authorize Git. On failure retain successful steps and name the failed action/retry.
Never list working-tree files as committed without checking. No branch/session per file
or phase: recommend fresh context for an independent next task/US, repository switch,
stale assumptions or required Judge separation. Related build/test/refactor can stay
together; commit/compaction alone is no trigger.

## Phase artifact formats

Use these sections in the agreed artifact plus the common user-facing envelope.
Keep phase details; merge equivalent sections, not contradictory parallel reports.
Goals and Non-goals are explicit in each artifact; FR/NFR tables may use verified
baseline locators. Unchanged criteria keep IDs and approval; do not silently lower
targets, omit negative paths or redefine Non-goals during repair. Scope changes need
authority. An artifact filename describes a permitted output, not an automatic write.

### cycle

Artifact: cycle state. Headings: Active outcome and task; Goals and Non-goals;
FR/NFR baseline; Phase and gate; Evidence and blockers; Authorized next action;
Restart point. Finalization links verified task updates, observed Git/Entire context
and checked scope; parent/release gates remain separate.

### research

Artifact: research.md. Headings: Question and task; Goals and Non-goals;
Sources and affected paths; Observed findings; Hypotheses and discriminating probes;
Options and risks; Requirement gaps (FR/NFR proposed or N/A); Recommendation and
unresolved questions; Handoff. Separate observations from hypotheses and targets.

### plan

Artifact: plan.md. Headings: Outcome and task graph; Goals and Non-goals;
Scope and exclusions; Functional requirements (Given/When/Then);
Non-functional requirements (measurement matrix); Acceptance and verification matrix;
Public seams; Ownership and permissions; Review/closure policy; Commit boundaries;
Risks and stop budget; Next ready task and restart context. Map approved FR/NFR IDs
to checks and capabilities before declaring ready.

### implement

Artifact: changes.md. Headings: Task and behavior; Goals and Non-goals;
FR/NFR baseline; Owned changes and preserved hunks; Tests/reproduction and results
(red, green, refactor where applicable); Deviations and unresolved issues;
Branch/commit receipt or proposal; Next verification. One vertical behavior slice
per red/green loop; source-format checks do not prove agent behavior.

### test

Artifact: evidence.md. Headings: Task and candidate; Goals and Non-goals;
Acceptance-to-check matrix (FR/GWT and NFR IDs); Commands and environment;
Results and artifact locators; Coverage and limitations; Failures/reproduction;
Judge handoff. For NFR record metric values/context or not-run/blocker; never
replace an approved target with a convenient observation.

### judge

Artifact: judgment.md. Headings: Task and candidate; Goals and Non-goals;
Evidence (Requirement findings, Standards findings); Scoped verdict;
Rubric mode and score/coverage; Insights, risks and unknowns; Next action.
Assess FR/GWT and approved NFR bounds separately from coding standards; missing
measurement/required independence stays explicit. No self-approval.

### iterate

Artifact: iteration.md. Headings: Finding and task; Goals and Non-goals;
Unchanged criteria (FR/NFR IDs); Current candidate and retained proof;
Cause hypothesis and reproduction; Capability/budget decision; Authorized correction;
Observed result and invalidated evidence; Next phase and restart conditions.
Record counter before/after, selective proof invalidation and original GWT/NFR rerun.
Capability-only waiting consumes zero attempts; no weaker criteria to make tests pass.
