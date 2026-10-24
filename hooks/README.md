# Plugin Goose hooks

Skills and hooks belong to the same plugin: rules are in
hooks/hooks.json and the handler in scripts/observe.py. No second manifest.

## Understand what is observed

| Event | Information |
|---|---|
| SessionStart / SessionEnd | Start/end and hashed session reference |
| Stop | Presence of legacy six numbered checkpoint headings, not their quality |
| AfterFileEdit | Successful edit, without path or content |
| AfterShellExecution | Successful command, without the command or raw result |
| PostToolUseFailure | Failure of a shell, write or edit tool |
| PreToolUseResult | The host's decision for these tools, without modifying it |

The filter for PreToolUseResult and PostToolUseFailure events is exact:
`^(developer__)?(shell|write|edit)$`. It accepts the short names documented by current
Goose and only their three explicit `developer__` aliases, found in the creator's
older documentation. The handler normalizes these aliases to shell,
write and edit. Other namespaces and suffixes remain excluded; stripping any
arbitrary prefix would improperly expand scope. Local tests cover the aliases,
without claiming that the current binary emits them.

These hooks block nothing: they create no commit,
branch, task, session or Entire checkpoint. They do not validate acceptance.

The Stop diagnostic still checks legacy six numbered checkpoint headings. It does
not recognize or validate the Skills' mandatory seven-field final report. A missing
legacy shape is not a failed Skill delivery, a blocking decision or an acceptance
verdict. Updating this diagnostic is separate runtime work.

## Verify before activation

1. Use a Goose version whose events and format have been verified.
2. Check that python3 is available on the hook's PATH; no other dependency is needed.
3. Review scripts/observe.py and existing hooks to avoid duplicates.
4. Obtain authorization to install the package in the target environment.
5. Verify events: source alone does not activate the plugin.

An earlier isolated probe targeted Goose CLI 1.55.0 with a temporary project and
HOME and a local mock provider. That historical observation is not verification
of this current candidate. No installed-hook or Goose runtime probe was rerun for
these alias changes. Another version or candidate requires its own verification.

## Validator compatibility

The target is the documented Goose loader: retain `hooks/hooks.json` and
`PreToolUseResult`. Do not migrate to
`extensions/io.github.bioinfornatics.agent-plugins.goose/hooks.json` to satisfy
a creator that does not match this target. The installed creator rejects
`PreToolUseResult` and warns about the root location: its check remains a
known failure, not validated or corrected by this plugin. Configuration and handler
tests provide separate, narrower evidence; they do not turn that failed validator
into a pass or establish current installed-runtime acceptance.
This choice is not universal Agent Plugins validation.

## Privacy and limits

The handler writes a bounded diagnostic to stderr, never a decision to stdout.
It retains no log and does not read Git/Beads/Entire state. Prompts, commands,
contents, paths and reasons are not returned. IDs are hashed for correlation:
they remain correlatable, without guaranteed anonymization. Goose logs are outside its control.

Input is limited to 1 MiB and each action to 3 seconds. A hook error does not block
the tool; there is no notification or persistence guarantee. The Stop check is
structural, not a security safeguard or independent judgment.

Reference: [Goose hook documentation](https://goose-docs.ai/docs/guides/context-engineering/hooks).
