# Agentic Development

A method for guiding a software change from need to verification,
without losing context across tasks, commits and sessions.

**Start with an observable outcome.** The agent clarifies scope, prepares
checks, makes a bounded change and then submits it for judgment.

## Choose your guide

| Your need | Read |
|---|---|
| Assign a first task to the agent | [Getting started](docs/getting-started.md) |
| Understand and steer the stages | [Development cycle](docs/cycle.md) |
| Connect Beads, Git, Entire and hooks | [Integrations](docs/integrations.md) |
| Modify or verify the method | [Contributing](docs/contributing.md) |

## What the method provides

Seven skills: a coordinator and six phases — Research, Plan, Implement, Test,
Judge, Iterate. Load **agentic-development:cycle** to guide the workflow,
or **agentic-development:plan** to structure a roadmap, US and tasks.
Each skill routes an intent to an action, its verifiable result and
the next step. Criteria remain visible throughout corrections.

The method provides instructions; it is not an execution engine,
an authorization system or automatic acceptance. A passing test does not
replace judgment. A development request alone does not authorize
a push, installation or deployment.

Skills are host-neutral and written in English; the agent responds in
your language. Use your tool's skill-loading mechanism.
Goose hooks are in **hooks/** and their handler in **scripts/**, within the
same plugin, but are not required to apply the portable method.
Integrations must be verified before activation.

## Documentation language

English is the default for all repository and distributed content. Only an explicit user request authorizes
a language exception; the conversation language does not. English documentation is canonical; explicitly requested translations remain separate
and linked to their English source. Multilingual documentation and GitHub Pages
setup/publication require separate scoped work and deployment authorization.

The [Zensical website](website/README.md) builds the canonical English guides
and their complete French mirror. Its guarded Pages workflow is prepared locally;
publication and installation remain separate authorized actions.
