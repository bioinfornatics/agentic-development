# Steering the development cycle

Choose a coherent slice: an outcome you can verify and resume independently.
Do not create one task per file or per phase.

## Stages and their outputs

| Stage | Action | Expected output |
|---|---|---|
| Research | Explore sources and test hypotheses | Question, facts, options and unknowns |
| Plan | Define scope, criteria, ownership and verification | Executable plan, dependencies and permissions |
| Implement | Make the smallest coherent change | Explained diff, preserved work and targeted tests |
| Test | Run checks on the identified candidate | Commands, results, environment and limits |
| Judge | Compare evidence, requirements and standards | Verdict, findings, applicable score and independence |
| Iterate | Correct a defect or resolve a prerequisite | Bounded correction and evidence to rerun |

The coordinator chooses the next step and finalizes traceability.
Reuse research or a plan that is still valid. Do not restart the whole cycle
on every resumption, but do not skip a necessary check.

## Develop with rapid feedback

For executable behavior:
1. Write or reuse a test at a public interface.
2. Observe a failure that actually reproduces the defect (**red**).
3. Make the minimal correction and observe success (**green**).
4. Refactor without changing behavior, then rerun tests.
5. Move to the next behavior and relevant regressions.

Expected results come from the requirement or an independent oracle, not the tested code.
A documentation-format check does not prove agent behavior.

## Read each stage's report

The final report always uses these seven fields, in order:
1. **step**: the phase actually performed.
2. **modified files**: changed paths, or N/A when none changed.
3. **next step**: the recommended phase, loop again, blocked or done.
4. **current goal**: the short objective addressed.
5. **next goal**: the next objective or missing prerequisite.
6. **closed tasks**: confirmed closed task IDs, or N/A.
7. **explanation**: what was done and why, evidence, limits and next gate.

Labels remain fixed; values are written in the user's language. The explanation
retains relevant Goals/Non-goals, criteria, checks, verdict and session details.
A blocked result or unchanged phase still uses all seven fields.

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

Next: [manage tasks, commits and sessions](integrations.md).
