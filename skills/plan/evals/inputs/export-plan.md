# Export plan draft

Fictional planning data; node states below are supplied records, not live tracker observations.

## Requirement R1
An accountant selects a month in the existing app and downloads a CSV of that month's invoices. Each row must contain invoice ID, issue date and amount in cents; a month with no invoices yields a header-only CSV. The approved non-goals are scheduling, email delivery and new storage. Existing primary research confirms this need and the current month selector.

## Current complete plan P1
- A, owner Alex: produce a monthly invoice summary as UTF-8 CSV with columns invoice_id, issue_date, amount_cents. Its local check compares a fixed two-row sample and a header-only sample against independently specified CSV bytes. A has no prerequisites.
- B, owner Bea: render a preview table from a JSON array whose keys are invoiceId, issuedAt and amountCents. B depends on A. Its check asserts the preview rows from an independent JSON fixture. There is no CSV parser, JSON producer or adapter in P1.
- C, owner Chen: explain invoice export terminology in the help panel. C has no dependencies and distinct writer paths from A and B.
These are all current nodes, including future work. No node connects the month selection to a downloadable CSV response, and none checks a user download. The A and B checks are individually well-defined. The graph has no cycle. No separate complete-plan reviewer has returned findings yet.

## Available scope
This request permits an inline plan review and dependency/bridge proposals, not implementation or tracker writes. Owners and output contracts are planning inputs. Runtime paths have not been supplied.
