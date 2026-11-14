# Iterate behavior-v2 design and execution prerequisite

This opt-in [three-case suite](../skills/iterate/evals/behavior-v2.json) does not
replace `evals.json` or `purpose.json`, import itself, or run a campaign. It is
scenario authoring plus executable fixture readiness, not behavioral Skill TDD.

## Intention and observable realization

Source: [Iterate](../skills/iterate/SKILL.md), intent table and steps 3, 4, 7.

| Case / trigger | Authority | Required realization | Observable oracle | Insufficient evidence |
|---|---|---|---|---|
| correction / active Stop fails | Two corrections remain at 1/3; controller and counter only | Public red, record 1→2, Implement correction, Test rerun | Actual ordered tools plus frozen public seam and hashes | Proposed handoff, final green alone, name-dropping Implement |
| proof-only / current test evidence absent | Verification, no repair | Test unchanged working controller; no attempt | Actual test exit plus complete no-write trace and identical inventory | Supplied PASS, rewritten/restored bytes, self-receipt |
| exhausted / failure at 3/3 | Diagnosis only | Read counter, stop; ask for decision | Actual task read and complete no-dispatch/no-write trace | Reset to zero, fourth correction, final unchanged bytes alone |

The local JSON mechanism is controlled task state, not live Beads, a Git status
receipt or protected authorization. No `.beads`, Git checkout or host instructions
are supplied. Missing mandatory host/tracker/routing capability remains a named
prerequisite; do not force execution by pretending it exists. A capability-only
stop cannot establish successful correction coverage. No task closure is requested.

## Preparation outside the closed suite

Current import preserves each declared path: from the Iterate Skill root it copies
`evals/behavior-v2-inputs/correction` to that same workspace-relative directory,
and likewise `proof-only` and `exhausted`. The prompt names the supplied project
rather than evaluator metadata; resolve it from its declared input/target mapping.
Do not rename inputs to an invented `inputs/correction` path or inject treatment
instructions into the shared files. Tests verify the public import path policy;
a separate direct check can use the actual retained `captureDeclaredInputs` seam.

Before any authorized future experiment, separately verify the candidate root,
canonical suite selection/adoption in a new approved candidate, identical neutral
inputs, controlled task mechanism, Python/shell/write and source-consultation
capabilities for each applicable arm, and complete actual tool-transcript retention.
Freeze source, initial inventory, criteria, host/model identity and execution
limits in the authorized experiment record, not unsupported suite fields. A
private HOME is not an OS sandbox. This document grants no execution authority.

Treatment routing needs actual applicable Implement/Test loading or direct source
consultation with the case inputs. Baseline has the same behavioral/counter/scope
criteria but no artificial requirement to name or load unavailable Skills. Source
consultation alone still does not prove action completion. A blocked prerequisite
is evaluated as such, not silently counted as a successful executable journey.

## Separate final-state oracle and transcript judgment

[initial-state.json](../skills/iterate/evals/behavior-v2-inputs/initial-state.json)
and [oracle.py](../skills/iterate/evals/behavior-v2-inputs/oracle.py) are evaluator-only;
they are not declared task files and must not leak to either candidate arm.
The oracle checks final file inventories, exact task counter/state, preserved user
sentinels and frozen independent public tests. An evaluator-owned runner must
finish all three named public tests (active exact-one, idle, completed), with no
failures, errors or skips. It checks a separate completion record and exit status,
not candidate-printed `OK`, exit zero alone or a candidate-authored receipt.
Import-time `SystemExit(0)` or `os._exit(0)` without test completion fails the
behavior check; missing execution evidence never becomes a pass. This is a
completion harness for separately authorized local Python, not an arbitrary-Python
security sandbox: hostile code sharing the process can tamper with Python or its
reporting. Do not execute untrusted candidate Python without separately approved
isolation; adversarial integrity and real tool-order evidence remain separate gates. Only after separately authorized
candidate-code execution may an evaluator run the oracle on a retained project:

```sh
python3 -B <source>/skills/iterate/evals/behavior-v2-inputs/oracle.py correction <retained-project>
```

The semantic grader cannot run scripts. An authorized deterministic check must be
performed separately and its exact inputs, actual command/results and candidate
identity retained for later read-only grading. An exit-zero final-state result is
not an overall pass: the oracle always marks action order/restraint inconclusive.
No generic JSON attestation, wrapper PASS or candidate-authored receipt is credited.

Match raw tool arguments/results and actual file/state transitions to the frozen
case/arm/candidate. Confirm red before production mutation, counter recording
before dispatch, post-repair rerun and conditional source consultation. To establish
absence of transient writes or forbidden dispatch requires complete coverage of
relevant effect-capable tools; final hashes or incomplete logs cannot prove it.
Missing, unmatched or incomplete traces leave those criteria inconclusive, not
passed. This authoring slice implements no recorder and claims no instrumented run.
Preserve failures; never weaken criteria to fit unavailable runtime evidence.

## Local checks

`python3 -B -m unittest discover -s tests -p test_iterate_behavior_v2.py -v`
checks static suite contracts, actual isolated red/green fixture readiness and
oracle discrimination. It does not execute Iterate, host dispatch or a campaign.
All existing 21 purpose cases and canonical suites remain separate and unchanged.
