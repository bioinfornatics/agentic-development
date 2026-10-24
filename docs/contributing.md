# Contributing to the method

## Choose the right location

- **skills/**: English instructions and resources required by each skill.
- **docs/**: short user guides, without logs or history.
- **tests/**: reproducible checks and explicitly triggered probes.
- **hooks/**: the plugin's Goose event configuration.
- **scripts/**: handlers called by hooks; no second plugin is required.
- Execution evidence stays separate from documentation; the tracker retains
  the current work status.

Start with the [repository instructions](../AGENTS.md). Check branch, index,
permissions and pre-existing changes. Define an objective and its exclusions
before modifying source.

English is the default for all repository and distributed content. Only an explicit user request authorizes
a language exception; the conversation language does not. English documentation is canonical; explicitly requested translations remain separate
and linked to their English source. Multilingual documentation and GitHub Pages
setup/publication require separate scoped work and deployment authorization.

## Write a useful instruction

Keep skill descriptions focused on what they do and when to use them.
In the body, direct execution: **intention → prerequisites → action → verified
result → next action or stop**. Name the action to perform, its inputs and
the skill to load next; a phase description is not enough.
Put conditional details in a directly linked resource. Keep the method
host-neutral; hooks remain a host-specific integration.

Specify Goals/Non-goals, Given/When/Then criteria for behavior and measurable NFRs
where relevant. Do not invent arbitrary numbers, implicit permissions
or simulated evidence. The [output contract](../skills/cycle/references/requirements-output.md)
provides the full formats; the [cycle](cycle.md) explains their use.

## Verify before proposing

From the repository root, run:

    python3 -m unittest discover -s tests -v

These tests cover source contracts and the observation handler, not model quality
or a global installation. Also use available official validations
for the changed component. A conflict between a validator and Goose requires checking
the documentation and runtime, not automatically declaring compatibility.

Check local links and shared-resource consistency.
A runtime change requires its own tests: authorized case, failure, malformed data
and relevant boundaries. Run an isolated probe only with its scope
and effects known; no installation or campaign is implicit.

## Deliver and hand off

Report the files actually changed, preserved work, commands/results,
limits and available judgment. For an authorized commit, verify message, hash and
contents. The next step must be recoverable from the task and a self-contained prompt.
Do not close a US or release based only on passing tests.
