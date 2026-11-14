# Pilot Skill evaluation

Apply only to an explicitly requested Skill evaluation in a source checkout.

## Official tool: default

1. Load agent-plugins:skill-creator. Read its evaluation workflow and artifact contracts.
2. Resolve its installed executable or scripts/skill-creator.mjs launcher. Read --help. Do not install or copy a runtime.
3. Confirm the source root, Skill, canonical evals/evals.json and writable workspace. Keep one workspace per Skill/iteration.
4. Freeze source, scenarios and assertions. Give both variants equivalent fixtures and tool access; hide expected answers and assertions from candidates. Explanation cases grade final-output properties only. Canonical execution_assertions and navigation requirements need actual tool-event/order evidence; normalization may omit custom metadata, so preserve the canonical inventory separately. Never regrade historical outputs under changed criteria.
5. Confirm executor/grader models, baseline, run profile and spending bounds. Reuse verified choices; ask only for missing decisions.
6. Use without_skill to measure instruction contribution. Use old_skill plus a frozen baseline to compare versions.
7. Use fast for one exploratory pair per case; standard for three; release for five. Verify aggregate_budget for standard/release. Do not infer spending authority from it.
8. Verify supported provider transport without printing secrets. Do not extract keyring data, copy credential files or request secrets in chat.
9. Run validate, audit and design-evals. Resolve errors before model execution. Treat --dry-run as planning only.
10. Before model execution, verify one fresh context per case/variant and actual ambient instruction exclusion. A fresh cwd, --no-session or --no-profile alone does not establish exclusion of installed Skills, hints or ancestor instructions. Keep normal authentication unchanged; do not fake HOME or extract credentials to manufacture isolation. If exclusion is unverified, stop the clean-baseline experiment and report the missing host capability. Only after this gate run full-eval --execute from the current session's shell and let the official runner launch paired candidates.
11. Use subprocess grading by default. Let each separate blinded grader assess one output against all frozen semantic criteria; never self-grade or expose sibling outputs/prior grades.
12. Inspect the actual exit code, JSON status, phase results and recovery commands. Distinguish transport/host failures, incomplete evidence and behavioral failures.
13. Preserve failed workspaces. Fix only the authorized prerequisite; resume with --resume and unchanged bound inputs/settings. Use a new iteration after source/scenario changes.
14. If awaiting-grading, read the creator's delegated-grading workflow before importing grades. Do not substitute invented receipts or local adapter records.
15. Verify every required variant/repetition has outputs, timing or explicit unavailability, and bound grading. Capture duration at each invocation, not around a batch; record provider token/cost data only when actually exposed. Unknown metrics remain null with unavailable_reason; use a verified creator version supporting that local contract. Keep missing grades separate from present inconclusive grades, and inspect missing telemetry regardless of the primary status. Never infer acceptance or zero usage from exit 0.
16. Run aggregate and review --static if those phases remain incomplete. Use the official HTML viewer, not a custom readiness report.
17. Resume remaining official phases; run evaluation-profile verification and analyze. Inspect receipt completeness separately from pass/fail and human review.
18. Report completed/required runs, grades, failures, comparison limits and the HTML path. Keep review-ready distinct from behavioral failure; complete is not pass or release acceptance.
19. Stop on an unresolved transport, exhausted budget or missing authority. Return the exact prerequisite and next command; never repeat a known global failure across all suites.

Run from the verified source root. Replace every placeholder before execution.
Set CREATOR to the verified installed source launcher; use its native executable instead when applicable.

~~~sh
CREATOR=/absolute/agent-plugins/skills/skill-creator/scripts/skill-creator.mjs
SKILL=skills/cycle
NAME=cycle
WORKSPACE="evidence/runs/<campaign>/iteration-1"
MODEL="<executor-model>"
GRADER="<grader-model>"
node "$CREATOR" full-eval --help
node "$CREATOR" validate "$SKILL"
node "$CREATOR" audit "$SKILL" --format json
node "$CREATOR" design-evals "$SKILL/evals/evals.json" --skill-path "$SKILL" --format json
node "$CREATOR" full-eval "$SKILL" --workspace "$WORKSPACE" --execute --baseline without_skill --model "$MODEL" --grader review-a="$GRADER" --grading-mode subprocess --run-profile fast --concurrency 2 --provider-max-attempts 1 --max-grader-calls <approved-call-cap> --format json
# Resume with the same execution arguments plus --resume; follow returned recovery commands.
node "$CREATOR" aggregate "$WORKSPACE" --skill-name "$NAME"
node "$CREATOR" review "$WORKSPACE" --skill-name "$NAME" --benchmark "$WORKSPACE/benchmark.json" --static "$WORKSPACE/review.html"
node "$CREATOR" verify "$SKILL" --profile evaluation --evaluation "$WORKSPACE" --format json
node "$CREATOR" analyze "$WORKSPACE" --skill-path "$SKILL" --format json
~~~

For a version comparison, replace --baseline without_skill with
--baseline old_skill --baseline-skill /absolute/frozen/skill.
Add approved provider cost/token/time caps supported by the installed help.
Do not widen retries, run counts or grading calls implicitly.

## Native session adapter: optional

1. Select this path only explicitly. Verify tools/session_eval.py in the source checkout; do not install it.
2. Use explain-level text cases and a new local workspace, never an official full-eval workspace.
3. Prepare requests. Delegate each request.json in a separate context with its supplied cwd, model and budget; hide criteria, sibling runs and parent conclusions.
4. Record only successful returned bytes with observed delegate IDs. Leave failed delegations pending.
5. Send each grading-request.json to a new independent grader. Import exactly one result per criterion with id, verdict, evidence_quote and rationale.
6. Run status; resume pending tasks without overwriting completed work. Generate HTML with the installed official viewer module.
7. Label results session-observed, not official full-eval receipts. Disclose ambient baseline exclusion, model/identity and telemetry limits; do not claim an OS sandbox or stable winner.

~~~sh
python3 -B tools/session_eval.py prepare skills/cycle <new-workspace> --eval-set skills/cycle/evals/evals.json --model <model> --ids 25
python3 -B tools/session_eval.py record <workspace> <run> <response.txt> --delegate-id <observed-id> --model <model>
python3 -B tools/session_eval.py grade <workspace> <run> <grader-response.json> --delegate-id <observed-grader-id> --model <model>
python3 -B tools/session_eval.py status <workspace>
python3 -B tools/session_eval.py report <workspace> --viewer <installed-skill-creator>/runtime/dist/eval-viewer/generate_review.js
~~~
