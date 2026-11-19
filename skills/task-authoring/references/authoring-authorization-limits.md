# Task-authoring authorization limits

Loading guidance grants no permission. Verify current authority for the specific
tracker and create/repair action; historical task notes or approval are context,
not a renewed grant. Preserve existing native fields, owner, status, relationships,
criterion IDs and history unless the requested repair explicitly authorizes changes.
An assigned owner is not a file lock or permission to claim work. Do not steal a
claim, change scope silently, close/reopen tasks or treat closed-task approval as
current authority. Unknown scope/authority blocks only the affected write; return
an explicit proposal or prerequisite instead of simulating execution.

Ticket authoring does not authorize Git, installation, publication, deployment,
model calls, task closure, export or synchronization. Do not initialize a tracker,
import a snapshot or create a second task database to bypass missing access.
