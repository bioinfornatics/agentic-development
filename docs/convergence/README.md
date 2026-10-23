# Convergence: phase core and historical harness

This branch combines the locally authored agentic-development 0.4.2 method core
with historical main eb9edb1. It is a reviewable source candidate, not a release.
Issue references w70/ecv belong to the original local Beads workspace; no Beads DB
was imported, reset or synchronized. These reports are not a tracker database.

## Keep / adapt / remove
inventory.json classifies all 670 historical tracked paths with reasons.
- Keep: active agents, skills, recipes, applications, tests, release tooling,
  locks, specifications and provenance. Retention does not mean revalidation.
- Adapt: harness inventories/builder, consistency inventory, recipe DB checks,
  entry documentation and project policy to integrate the separate phase core.
- Add: plugins/agentic-development source including evaluation designs, operational
  projection utility and regression tests. Source methods retain short names.
- Remove: .agents.old, .goose.old, evals.old, and broken install-git-hooks.sh.
  Every removed path remains recoverable at the historical base in Git.
- Do not copy: local Git/Beads/host configuration, VSCode or session databases.

## Two delivery layers
The core contains Research/Plan/Implement/Test/Judge/Iterate and cycle.
The optional historical harness provides isolated agents, recipes, budgets,
telemetry and packaging. Neither layer silently replaces the other's gates.
Core methods define reporting, candidate identity, permission provenance and
independence. Beads remains task/state truth; Git and artifacts retain proofs.
Distinct sessions and env:reviewed labels are insufficient acceptance by themselves.
The existing budget guard does not prove COMPLETE acceptance criteria.

## Installation boundary
scripts/project-phase-core.py creates 49 operational files in a new destination,
excluding evals/fixtures and repository state; it never installs or overwrites.
The harness builder applies the same operational boundary for the core plugin.
Do not copy the complete source repo into a Goose plugin directory.
Goose plugin import prefixes short Skill names; manual copying does not execute
that import transformation. Namespace/routing must be tested on actual import.

## Explicit pending work / limits
Legacy hook scripts/configuration are retained, not newly enabled or certified.
Known limitations from the investigation: developer__shell matcher versus current
shell; bd show JSON array; label-only closure gate; observation-only failure hooks;
ephemeral telemetry not a complete session handoff; source installers replacing
user catalogs; signature origin verification absent in release installer.
These require a bounded follow-up, full runtime evidence and independent acceptance.
The phase-method core is structurally validated, not behaviorally accepted.
No automatic commit/push/sync, session creation, hook installation or UI claim.
The integration branch may be pushed for review; main promotion and release gates
remain separate from candidate publication.

## Verified Goose references
https://goose-docs.ai/docs/guides/context-engineering/plugins
https://goose-docs.ai/docs/guides/context-engineering/hooks
https://goose-docs.ai/docs/guides/sessions/session-management
