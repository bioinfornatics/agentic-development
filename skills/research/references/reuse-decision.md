# Reuse, extend or build

Read when investigating a new utility, dependency, integration or capability that may already exist. This is a decision procedure, not a requirement to search every registry for every edit.

## Resolve the need and search scope

1. State required behavior, public interface, environment and constraints before looking for solutions. Check the repository implementation, tests, declared dependencies and existing project conventions first. Cite relevant paths and identify whether the existing capability meets the need.
2. If a meaningful gap remains, select accessible official documentation, package registries or maintained source projects relevant to that gap. Verify tool availability and permitted network/access effects first. A missing channel is unavailable, not evidence that no solution exists. Do not read credential files or run an installer to discover candidates.
3. Refine the search using observed API names, terminology and missing capabilities; retain only decision-relevant evidence. Stop when there is sufficient evidence to choose or state the exact unresolved prerequisite. Broad repeated searches and exhaustive catalogs are not the goal.

## Compare alternatives

For viable options record source/version, required behavior coverage, compatibility with the project/runtime, license suitability, maintenance evidence, security and data-access implications, dependencies and integration cost. Separate observations from assumptions; unresolved license or security suitability must not be reported as approved. Use official documentation and existing tests where accessible; popularity alone is not proof of fit.

- **reuse**: an existing project capability or suitable dependency already meets the need. Prefer its public interface; describe verification needed at the integration seam.
- **extend**: a small compatible adapter or targeted extension closes the gap. Name the gap, owned boundary, upgrade implications and checks of preserved behavior.
- **build**: viable existing options do not fit, or the demonstrated integration/maintenance burden outweighs their benefit. Record considered options and reasons, not an unsupported claim that nothing exists.

If access is unavailable, report the searches actually performed, remaining uncertainty and whether it blocks the decision. A provisional build proposal may be useful, but it is not evidence of exhaustive coverage or permission to implement.

## Verify and hand off

Include the decision, alternatives rejected with evidence, unresolved risks and proposed integration tests in the Research artifact using its canonical output contract. Hand off to Plan with scope and dependencies; reuse a current approved plan when applicable. This decision does not authorize installation, package changes, credential access or publication. Stop at a missing mandatory compatibility/license/security fact and name the next authorized probe.

## Review scenarios

- Existing repository helper satisfies the request: recommend reuse with cited behavior/tests, not a second implementation.
- Candidate library lacks one necessary runtime feature: compare an adapter against building and disclose license/upgrade constraints, not just package popularity.
- Registry access unavailable: report local evidence and the unavailable channel; do not claim no packages exist or install to bypass access.
