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

The report follows six sections, in this order:
1. **Objective and roadmap position**: milestone, epic, US, slice, phase, scope and task.
2. **Result**: what is complete, incomplete or unchanged.
3. **Changes and evidence**: files, branches, commits, commands and limits.
4. **Verdict and uncertainties**: facts, risks, independence and applicable score.
5. **Transition**: next phase and session recommendation, distinct from the action.
6. **Next action and restart**: prerequisites and a concrete first step.

A proposed commit has no hash. A recommended session has not been launched.
The report distinguishes modified files from files actually committed.

## Judge and correct without changing the rules

Freeze the candidate and criteria before judgment. Tests are evidence,
not acceptance. Required but unavailable independence remains a limit.
Freeze judgment rubric v1.0.1 or an explicitly approved replacement before
implementation. The bundled method uses weighted scoring and preserves unknown
criteria; this documentation does not introduce a small-task scoring mode.

Correct the most precise defect, then rerun its checks and regressions.
Keep evidence that remains valid; invalidate evidence whose inputs have changed.
Do not lower a threshold or remove a test to obtain success.
The coordinator's default budget is three correction rounds. Iterate records
the round counter and stops when a required capability is unavailable. Follow the
bundled round policy; this documentation does not add a diagnosis/waiting exemption.
When blocked or out of rounds, stop and prepare the handoff. Close only the scope
actually verified and authorized.

Next: [manage tasks, commits and sessions](integrations.md).
