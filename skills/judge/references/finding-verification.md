# Verify findings before publishing

Read when judging code changes or assessing a specialist reviewer finding. It refines evidence quality; it does not replace the acceptance criteria, rubric or independence policy.

## Check the claim

1. Match location and source version to the frozen candidate. Read surrounding context, callers and relevant contracts before interpreting an isolated line. Check reachability and the preconditions under which the alleged failure can occur. Inspect protective validation or error propagation before claiming it is absent.
2. Identify the requirement or documented standard affected. State the concrete expected versus actual outcome and impact. Generic taste, arbitrary function-size thresholds and speculative refactors are not defects without a relevant source or demonstrated failure.
3. Prefer a minimal permitted reproduction at the public seam. Otherwise record a source-grounded argument, assumptions and what was not reproduced. Mark evidence observed, inferred or unknown; source inspection may establish a defect, but must not be mislabeled as executed behavior. Do not repair the candidate or execute unapproved side effects.
4. Check whether an automated result or another finding already covers the same root cause. Consolidate duplicate findings while preserving distinct impacts and criterion links; never inflate the count by restating the same issue.

## Qualify severity and uncertainty

Assign severity from demonstrated impact, exposure/reachability and affected scope using the agreed project policy. Do not invent confidence percentages or promote style preferences to security failures. Missing context/access means an explicit evidence gap, not a clean result. Suspicious but unconfirmed claims belong in uncertainties with the smallest verification prerequisite, not in a list of confirmed defects.

Do not discard a known mandatory acceptance failure because it is small, inconvenient, not reproduced dynamically, or below a generic review threshold. Conversely, an unsupported claim is not a known blocker. If mandatory evidence or required independence is missing, retain the existing indeterminate gate unless an established defect requires needs-correction.

## Publish an actionable finding

Record ID, requirement/standard source, exact location, preconditions, evidence type and locator, expected/actual result, impact, justified severity, blocking versus recommendation status and minimal corrective verification. Keep requirement and standards findings separate, and preserve the judgment evidence/verdict/score distinction. Return findings to Judge/coordinator; a specialist review is not an independent acceptance decision by itself.

## Review scenarios

- A launcher appears to suppress failure: inspect child status and wrapper propagation; reproduce at the public CLI when permitted before claiming observed success masking.
- A long function works and violates no project standard: omit a taste-only defect; record a recommendation only if its concrete maintenance benefit is justified.
- Missing access prevents checking a reported security path: retain the uncertainty and next probe without inventing a confirmed vulnerability or accepting a mandatory unverified criterion.
