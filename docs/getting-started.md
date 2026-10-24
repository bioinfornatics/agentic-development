# Getting started

## 1. Describe the outcome, not a list of files

Identify the affected user, expected behavior and current problem.
Specify what is excluded and what the agent may actually execute.

> Fix stopping a stream: when the user clicks Stop, the active transport
> must be cancelled exactly once. Do not change the interface or storage.
> You may modify code and local tests; do not push or deploy anything.

Load **agentic-development:cycle** to guide the workflow. For a single phase,
load the corresponding skill through your tool's mechanism:

| Intent | Skill to load | Expected result |
|---|---|---|
| Explore a need or risk | agentic-development:research | Source-grounded findings and a decision to prepare |
| Structure a roadmap, US or tickets | agentic-development:plan | Ready plan and tasks; authorized and verified tracker writes |
| Implement an authorized plan | agentic-development:implement | Bounded change and local checks |
| Verify a candidate | agentic-development:test | Reproducible results and limits |
| Judge evidence and the candidate | agentic-development:judge | Verdict on the exact scope |
| Correct findings | agentic-development:iterate | Bounded corrective action or precise prerequisite |

Example: “Load agentic-development:plan to create a roadmap and priority tasks
from this need. You may create tickets in the project's tracker,
but not modify code.” These identifiers are not shell commands.

## 2. Have criteria clarified before coding

Require explicit **Goals / Non-goals** and observable criteria:

- **Given**: a stream is active.
- **When**: the user requests that it stop.
- **Then**: the transport is cancelled once, without a new message.

Add relevant errors and boundaries: repeated stop, no stream, network failure.
For a performance constraint, specify the metric, approved threshold, unit,
workload, duration, environment and measurement method. Without an approved threshold,
the criterion remains unresolved; the agent does not invent a number to manufacture success.

Research or a documentation change instead uses a verifiable deliverable:
do not force an artificial user scenario.

## 3. Check the proposed plan

Review scope, owned or preserved files, proposed tests,
dependencies and permissions. Resolve blocking decisions.
A plan already covered by your request does not require ritual approval.

## 4. Request an actionable report

The report must separate outcome, changes, evidence and judgment. It identifies
the commands actually executed, modified files, Git actions performed
or merely proposed, and the next step.

If the agent is blocked, ask for the prerequisite and a precise restart point,
not simulated acceptance. A local test does not prove production behavior.

Next: [steer the cycle](cycle.md) or [prepare integrations](integrations.md).
