# Goose hook configuration

Use the current Goose-documented hooks/hooks.json layout and verify the exact runtime.
Rules belong to the main plugin and remain observation-only. Do not add policy blocking,
automatic task/Git/session mutations or raw payload logging implicitly. Check exact
matchers, timeout/failure behavior and handler paths in isolated runtime tests.
