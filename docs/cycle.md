# Steering the development cycle

Choose a coherent slice: an outcome you can verify and resume independently.
Do not create one task per file or per phase.

## Stages and their outputs

| Stage | Action | Expected output |
|---|---|---|
| Research | Establish product context before planning, then explore relevant sources | Purpose, users/outcome, current behavior, constraints, facts and unknowns |
| Plan | Define scope, criteria, ownership and verification | Executable plan, dependencies and permissions |
| Implement | Make the smallest coherent change | Explained diff, preserved work and targeted tests |
| Test | Run checks on the identified candidate | Commands, results, environment and limits |
| Judge | Compare evidence, requirements and standards | Verdict, findings, applicable score and independence |
| Iterate | Correct a defect or resolve a prerequisite | Bounded correction and evidence to rerun |

Begin every new development objective with Research, even for a clear request or familiar code.
Research → Plan → Implement (RPI) prevents plans from relying on unchecked product assumptions.
The coordinator chooses the next step and finalizes traceability.
Reuse research only after checking its context coverage and freshness; reuse a plan that is still valid. Do not restart the whole cycle
on every resumption, but do not skip a necessary check.

## Work one epic in batches

1. Keep one active epic across sessions; only you decide to switch it.
2. Pull ready work from that epic only, for example `bd ready --parent <epic>`.
3. Form the batch from all ready, independent tasks; the host's subagent limit sets its size.
4. Give each worker one task and its own files; the coordinator owns the batch.
5. Close or release every batch task before pulling the next batch.
6. When no ready task remains, refine the next batch through Research → Plan (a proposal; tracker writes need your authority).

## Develop with rapid feedback

For executable behavior:
1. Write or reuse a test at a public interface.
2. Observe a failure that actually reproduces the defect (**red**).
3. Make the minimal correction and observe success (**green**).
4. Refactor without changing behavior, then rerun tests.
5. Move to the next behavior and relevant regressions.

Expected results come from the requirement or an independent oracle, not the tested code.
A documentation-format check does not prove agent behavior.

Write tests as living documentation: a reader who never opens the implementation should
learn the rule from them. The name states the rule, the setup holds only the conditions
that decide the outcome, one action runs, and the assertions show the result and its
effects. For example, `test_site_without_approval_cannot_be_published` uses an authorized
publisher, so the refusal can only come from the missing approval, and checks that the
site stays ready.

Same branch is not a new test. Before adding a case that differs from another only in an
input value, check that the code or the specification treats that value differently. A
case the specification names but the code ignores is worth writing: its failure reveals
a gap. See [test value](../skills/test/references/test-value.md) for the full rules.

## Read each stage's report

The final report uses five sections, in order:
1. **current goal {step: …}**: the outcome addressed and actual phase, with the verified task ID.
2. **roadmap position**: verified roadmap/epic/US references, a compact cycle visual, next action and blocker/status.
3. **modified files**: changed paths, or N/A when none changed.
4. **closed tasks**: confirmed closed task IDs, or N/A.
5. **explanation**: what was done and why, evidence, limits and next gate.

States such as blocked, done and loop again are not phases; keep them in roadmap position.
Do not invent roadmap progress. If it is unavailable, say so and show known cycle progress only.
For example: `Research [reused] → Plan [active] → Implement [pending] → Test [pending] → Judge [pending]`.
The roadmap describes outcomes; the cycle describes phases. Explain nonstandard transitions with current proof or missing prerequisites.
Labels remain fixed; values use the user's language. Preserve relevant Goals/Non-goals, criteria, checks and verdict in explanation.
Blocked and unchanged results still use all five sections.

Read requirements before the actions they govern. Read the common output and phase delivery contracts after investigation, before drafting the response.

A proposed commit has no hash. A recommended session has not been launched.
The report distinguishes modified files from files actually committed.

## Judge and correct without changing the rules

Freeze the candidate and criteria before judgment. Tests are evidence,
not acceptance. Required but unavailable independence remains a limit.
Choose the scoring mode before implementation; a requested numerical score
does not disappear because the task is small.

Correct the most precise defect, then rerun its checks and regressions.
Keep evidence that remains valid; invalidate evidence whose inputs have changed.
Do not lower a threshold or remove a test to obtain success.
The default budget is three authorized attempts; waiting and diagnosis
do not consume an attempt. When blocked or out of attempts, stop and prepare
the handoff. Close only the scope actually verified and authorized.

See [how the Skills chain together](skill-flow.md) for the routing map.

Next: [manage tasks, commits and sessions](integrations.md).
