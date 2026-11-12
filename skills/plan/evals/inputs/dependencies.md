# Dependency snapshot
ARCH-2 selects networking, service layout and repository paths.
IMPL-3 implements the selected architecture.
Native blockers: ARCH-2 waits on IMPL-3. IMPL-3 has no blocker.
New request: replace the old implementation directly, retaining shared state.
No cloud mutation authority. The existing edges require reassessment, not blind reversal.
