# Label correction task

Fictional task and source records for a planning consultation.

## Requirement L1 and product context
The maintainer requests changing the existing export button label from "Export report" to "Download CSV" so accountants see the file type before selecting it. No behavior, interface, styling, translation or dependency changes are requested. Existing product research establishes the monthly invoice download journey.

## Current evidence S1
The source record for app/export-label.ts at candidate label-base-7 contains the English literal "Export report", consumed by the existing export button with no transformation. The existing download handler and CSV contract are untouched. The source record for tests/export-label.test.ts at the same candidate checks the rendered label against an independently specified literal; baseline check record T1 passes with "Export report". Source/environment identity has been compared and is unchanged for this consultation. These records apply to the same English-only label path and candidate, not a different package or deployment.

## Proposed task L2
Owner Lina reads those two source records, modifies only the label literal and its independent expected test value, and preserves the handler and CSV contract. Success is the rendered label "Download CSV" with the existing download behavior unchanged. The first action is to read app/export-label.ts and tests/export-label.test.ts in the verified workspace before the scoped edit. No paths need to be guessed. Local edit and focused verification scope was approved; this consultation itself requests a readiness assessment only.

## Review limits
No separately completed whole-plan review is supplied. There is no known composition risk or decision-critical unknown about the literal's consumer. These excerpts are evidence inputs, not executable source files in this consultation.
