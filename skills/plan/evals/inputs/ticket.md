# Task IAM-7: Configure technical identities and secrets
Why: Deployments need permissions.
How: Use cloud identities and inject secrets externally.
Owner: unassigned.
Dependencies: ARCH-2.
Acceptance: IAM-7-AC1 unauthorized reads denied; IAM-7-AC2 no secrets in state.
## Previous architecture update
Use self-hosted vault with secret values managed in IaC.
## New architecture update
Use provider-managed secret store; do not put values in IaC.
Native tracker snapshot: assignee alex, status open, prerequisite ARCH-2.
History note: old architecture was proposed, never executed.
New user decision: provider-managed store selected, credential bootstrap still open.
