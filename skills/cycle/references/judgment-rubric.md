# slice-acceptance — rubric v1.1.0

Contract ID: agentic-development/judgment-rubric
Contract version: 1.1.0

Freeze this default rubric before implementation, or record the approved
replacement identifier/version. Score is a structured assessment, not a
probability of correctness. Assess only the explicitly agreed acceptance scope.

| Criterion | Weight | Required basis |
|---|---:|---|
| Functional acceptance | 40 | Each approved functional criterion mapped to evidence |
| Verification quality | 25 | Relevant tests, negative paths, environment and candidate identity |
| Safety and regression | 20 | Risk-based security, data integrity and regression checks |
| Maintainability | 10 | Diff, interfaces, local conventions and avoidable complexity |
| Operability and handoff | 5 | Run prerequisites, limitations and reproducible next steps |

Per criterion: 0 unmet, 1 materially incomplete, 2 partial, 3 meets the agreed
scope, 4 exceeds it with concrete evidence. Weighted score = sum(weight * value/4)
on a 0–100 scale. Report unknown criteria as null. For partial scoring report
only earned/assessed weight and assessment coverage; do not normalize it into
an apparently complete overall score. Overall score remains null if any
criterion is unknown. Omit an irrelevant criterion only through an explicitly
approved versioned rubric amendment, not silently during grading.

Accepted: every mandatory acceptance criterion has adequate evidence and no
blocking finding remains. Needs-correction: a known defect or unmet mandatory
criterion exists. Indeterminate: evidence, capability, provenance or required
independence is missing. Known blockers take precedence over missing evidence.
Not-run: no judge was executed. A high score never overrides these gates.

For each finding record ID, severity, criterion, file/location, evidence,
impact, remediation and verification needed. Distinguish blocking findings from
nonblocking recommendations. Report reviewer identity/context and whether
review was independent, limited self-review or not executed.

## Explicit small-task mode

Select the mode before implementation, in the plan or verified scope. For a narrow local
or authoring task whose decision does not benefit from numerical grading, use
small-task mode: mandatory criteria, observed checks, findings, limitations and
scoped verdict; score and numerical coverage are not-applicable. No rubric
amendment is needed for this predefined mode. Never switch modes after seeing a
failure to hide it. A numeric score already required by the user/approved plan
remains required unless that authority approves the change.

Small-task mode does not waive exact-candidate acceptance, any mandatory proof,
independence, closure authority or parent/release gates. Weighted mode remains
the default for feature/release slices and for explicit numerical requests.

## Interpreting conformity

Five criteria rated 3 earn 40*3/4 + 25*3/4 + 20*3/4 + 10*3/4 + 5*3/4 = 75/100.
This means meets the agreed scope, not a 75 percent chance of correctness or
a failed acceptance gate. A 4 requires concrete evidence of exceeding scope,
not unauthorized extra work. Do not expand scope just to chase 100.

If the first four criteria are 3 and operability (weight 5) is unknown, earned
points are 71.25 against assessed weight 95; coverage is 95 percent and overall
score is null. Never normalize this partial result to a complete overall score.
Mandatory missing proof or required independence still prevents acceptance.
Apply review-policy.md for independence/closure; rubric scoring grants no authority.
