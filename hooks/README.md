# Plugin Goose hooks

Skills and hooks belong to the same plugin: rules are in
hooks/hooks.json and the handler in scripts/observe.py. No second manifest.

## Understand what is observed

| Event | Information |
|---|---|
| SessionStart / SessionEnd | Start/end and hashed session reference |
| Stop | Canonical five-heading or legacy numbered report shape, not content quality |
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

The Stop diagnostic recognizes the Skills' mandatory five-section final report
at full-delivery boundaries: `## current goal {step: <phase>}`, then
`## roadmap position`, `## modified files`, `## closed tasks`, `## explanation`.
The phase must be one of cycle, research, plan, implement, test, judge or iterate.
Headings must be unique, ordered and outside backtick or tilde fenced blocks.
Legacy six numbered headings remain supported; `checkpoint_sections` retains the
sorted unique numbers observed outside fences, including for incomplete shapes.

`report_format` is canonical, legacy, mixed or undetermined. `report_shape` is
complete, partial, duplicate, out-of-order, malformed, mixed or undetermined.
Mixed formats take precedence, then malformed current-goal phase/heading,
duplicate headings, ordering and completeness. These are structural diagnostics,
not valid/invalid delivery judgments. Arbitrary headings and raw phase values are
never emitted. Ordinary prose (including eligible compact delivery), empty text
and fenced examples alone are undetermined, not failures. A missing or nonstring
message yields `handoff_check: unavailable`; strings yield structure-only.
The observer does not check section contents, compact-delivery eligibility, YAML,
authorization, acceptance or efficacy; even an empty complete skeleton proves none
of those. It makes no blocking decision.

## Verify before activation

1. Use a Goose version whose events and format have been verified.
2. Check that python3 is available on the hook's PATH; no other dependency is needed.
3. Review scripts/observe.py and existing hooks to avoid duplicates.
4. Obtain authorization to install the package in the target environment.
5. Verify events: source alone does not activate the plugin.

An earlier isolated probe targeted Goose CLI 1.55.0 with a temporary project and
HOME and a local mock provider. That historical observation is not verification
of this current candidate. No installed-hook or Goose runtime probe was rerun for
these alias or Stop parser changes. The scripted probe now uses a canonical
fixture but has not been executed for this candidate. Direct subprocess tests
exercise the handler only, including legacy compatibility; they do not establish
installed event wiring. Another version or candidate requires its own verification.

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

The handler writes a diagnostic of at most 2048 bytes to stderr, never a decision
to stdout. It performs no filesystem, network or child-process actions.
It retains no log and does not read Git/Beads/Entire state. Prompts, commands,
contents, paths and reasons are not returned. IDs are hashed for correlation:
they remain correlatable, without guaranteed anonymization. Goose logs are outside its control.

Input is limited to 1 MiB and each action to 3 seconds. A hook error does not block
the tool; there is no notification or persistence guarantee. The Stop check is
structural, not a security safeguard or independent judgment.

Reference: [Goose hook documentation](https://goose-docs.ai/docs/guides/context-engineering/hooks).
