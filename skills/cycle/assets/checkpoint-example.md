# Checkpoint example (fictional)

Translate the labels and content into the user's language when reporting.

```text
OBJECTIVE / ROADMAP
Milestone: Local playground. Epic: Usable playground.
US: Display streaming and allow stop.
Phase: Test. Mock checks PASS; acceptance pending Judge.
Remaining: installed package and real endpoint.

RESULT
Streaming and stop pass locally using mocked transport.

CHANGES / EVIDENCE
Branch: feature/playground-stream, suitable for this US.
~ src/view.ts: stream states, session-owned hunks.
~ src/controller.ts: cancellation; initial user hunk preserved.
+ tests/stop.test.ts: mocked scenario.
E1 PASS: mocked integration, snapshot abc (fictional identifier).
E2 NOT RUN: installed package. E3 UNKNOWN: real-provider cancellation.

VERDICT / INSIGHTS / UNCERTAINTIES
Judge: not-run. Score: not assessed, slice-acceptance v1.0.1.
Observed: mocked transport stops (E1).
Inferred: E1 provides no real-provider proof.
To-verify: real cancellation; server-side request continuation risk.

TRANSITION
Commit recommended after E2; not performed, no Git authorization granted.
Same session for E2; independent context recommended for Judge.
Preserve uncommitted work: the three paths above and initial user hunks.

NEXT ACTION
Verify stop in the installed candidate package.
Prerequisite: an available package installation environment.
```

## Session-end example (fictional)

Purpose: validate local stop. Mock checks pass; installed-package check is open.
Judgment: not-run. Score: not assessed, slice-acceptance v1.0.1.
Next-session proposed name: Streaming stop — Test package — Verify cancellation.
Linked tasks: IDs unknown; proposed next task: installed-package stop check.
Handoff location: inline / not saved.

### Copy-ready restart prompt

Continue the local streaming-stop slice. Confirm repository path and branch with
the user before mutation; no stored handoff artifact exists. Read local project
instructions and tracker, inspect working-tree ownership and candidate identity.
Previous mock checks need freshness verification; package and real-provider
checks remain unverified. Preserve dirty src/view.ts, src/controller.ts and
tests/stop.test.ts including the initial user controller hunk. The prior session recorded scoped file-edit permission; verify its authoritative
source and current scope before mutation. No commit/push/production operations
are authorized by this restart prompt. First confirm the
installation environment and test stop in the exact candidate package. Local
acceptance requires reproducible scoped evidence, not inferred real-provider
correctness. Stop if ownership or capability is unresolved. Prepare a frozen
candidate and handoff for independent Judge rather than silently self-approving.
