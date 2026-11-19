# Beads authoring bridge

Apply only when the chosen tracker is Beads, before its native authoring operations.
Read applicable local Beads guidance and current installed CLI help; verify workspace
and database identity with supported read-only commands before choosing or writing
work. Inspect the matching issue, owner, prerequisites and existing history.
Missing access or identity mismatch blocks the write: do not initialize/import or
infer database identity to repair it.

Use current help for the specific create/update/show operations and supported fields;
do not assume all CLI versions expose the same flags or issue types. Store current
specification in description, canonical criteria in the acceptance field when
supported, observations in notes/comments, and ownership/status/relationships in
native fields. Parent hierarchy is not a prerequisite edge; verify edge direction
and reject cycles. Preserve the assigned owner and claim; this capability does not
claim work, change status or close it. After permitted create/repair, read back the
actual ID, changed fields and relevant links/history. Report errors and proposed
writes honestly. Authoring grants no closure, export, import or Dolt sync authority.
