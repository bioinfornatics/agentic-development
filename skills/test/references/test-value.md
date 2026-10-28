# Product guarantees and test value

Apply when selecting or reviewing application tests, or analyzing a suite for
rationalization. This is not permission to edit tests or the frozen candidate.
Test diagnoses and proposes changes; authorized corrections go through Iterate
and Implement, then Test checks the changed candidate.

## Contents

- [Select evidence, not volume](#select-evidence-not-volume)
- [Challenge the oracle before counting a pass](#challenge-the-oracle-before-counting-a-pass)
- [Rationalize within authority](#rationalize-within-authority)
- [Measure the mandatory path honestly](#measure-the-mandatory-path-honestly)
- [Source and applicability](#source-and-applicability)

## Select evidence, not volume

1. Start from the approved product guarantees and important user journeys, not
   existing test files or implementation structure. Include relevant errors,
   cancellation, boundaries, security and observed incidents. Do not invent every
   imaginable input combination. Missing expected behavior is a requirements gap.
2. For each selected test or coherent test family answer:
   **Which incorrect observable product behavior does this detect that the other
   selected checks do not already detect?** Record the guarantee/criterion ID,
   concrete fault, independent oracle, public seam and evidence level. A distinct
   environment or boundary can justify overlap; assertion/file count cannot.
3. Choose the cheapest valid check at that seam. Use direct deterministic cases
   for business-rule variations; keep a representative integration for actual
   wiring and a small set of operational journeys for required system guarantees.
   Do not replace a required integration, installed-package, real-provider or UI
   observation with a cheaper mock that cannot expose the same fault.
4. Add a case only for a distinct risk, boundary, incident or confidence question.
   Existing tests are not a preservation obligation. There is not a fixed test-count ceiling
   or minimum: a large suite can be justified, a small green suite can be worthless.
   Do not target an arbitrary reduction percentage, coverage percentage or number.

A compact selection matrix is enough; group genuinely equivalent cases rather
than produce an audit document per test. For a requested whole-suite audit,
account for every test/family; an uninspected subset stays unknown, not useless.

| Guarantee / source | Incorrect behavior | Oracle / seam / level | Marginal detection value | Cost / required lane |
|---|---|---|---|---|
| Approved criterion ID | Concrete externally wrong result | Independent expected result, actual subject | Distinct fault or justified overlap | Measured or unknown; local/required CI/optional |

## Challenge the oracle before counting a pass

- Exercise the actual subject. A test that only calculates or asserts its own
  setup is a tautology; copied production logic is not an independent oracle.
  Use specification examples, known exact values or independently justified
  properties. A test-only reimplementation of the subject proves nothing about it.
- A mock controls an external dependency, not the behavior being verified.
  Returning the mock's value and asserting that same value is insufficient unless
  a distinct product contract is discriminated (for example selecting the correct
  customer's ID, forwarding a mandated parameter, or translating a dependency error).
  Do not ban mocks or contractually meaningful interaction assertions wholesale.
- When the contract determines an exact outcome, assert it, including important
  persisted effects or absence of forbidden effects. Non-null, truthy, nonnegative
  or shape-only checks cannot substitute for the known result. Tolerances or
  property assertions need a contract-based justification, not vague correctness.
- Specify one expected outcome per input/state. Do not accept success or error
  interchangeably, catch failures to pass, silently skip missing prerequisites,
  or branch on the observed result to choose whichever assertion passes. Assert
  the success and important error paths separately with deterministic conditions.
- Check discrimination with a symptom-specific failing reproduction or a bounded
  counterexample/mutation at the real seam when authorized: wrong exact value,
  inverted decision, missing effect or swallowed error must make the relevant
  test fail. Keep probes isolated, restore the candidate, and never mutate the
  frozen candidate during Test. An existing pre-fix red can provide this evidence;
  do not mandate an exhaustive mutation campaign for every test. Without execution,
  label the fault hypothetical and discrimination unverified. Static red/green
  establishes source conformance, not application or agent behavior.

## Rationalize within authority

For an authorized suite rationalization, inspect assertions, setup and observed
cost hotspots before optimizing scheduling. Profile slow families and repeated
campaign setup first, not just cheap individual assertions. If no timings exist,
record unknown cost and propose the smallest useful measurement.

| Decision | Use when | Evidence needed |
|---|---|---|
| retain | Distinct product fault, security boundary, incident regression or required environment | Criterion, discriminating oracle and unique risk or justified overlap |
| merge | Checks duplicate the same guarantee or expensive setup | Representative integration plus cheap direct cases; preserve distinct faults |
| remove | Test validates only setup/internal detail or duplicates another check without distinct value | No unique product guarantee lost; identify retained coverage or explain irrelevance |
| replace | Guarantee matters but current test cannot expose its fault or is unnecessarily expensive | Better observable seam/oracle and relevant red-capable regression |

Record test/family, decision, rationale, guarantee lost or preserved, replacement
or retained check, discrimination evidence, cost before/after (or UNKNOWN), and
actual or proposed status. Removal/fusion is allowed within approved scope; do not
weaken product acceptance or discard meaningful incidents to obtain green or faster
results. Missing required coverage remains open until a valid replacement passes.
Preserve unrelated work and keep the old evidence's candidate identity intact.

Repeated costly end-to-end/provider/evaluation campaigns need a distinct risk or
confidence question, workload/sample justification, budget and stop rule. Prefer
one representative wiring journey and inexpensive rule cases when they expose
the same faults. Nondeterministic confidence requirements can justify repetition;
name the uncertainty being measured. Stop adding/running checks when selected
mandatory guarantees and scoped risk questions have adequate evidence, or stop
with explicit gaps when prerequisites/budget fail. Green count is not a stop rule.

## Measure the mandatory path honestly

Distinguish:
- individual and summed test durations: hotspots, often not end-to-end elapsed time;
- aggregate runner/compute time and costly service calls: total execution cost;
- required CI wall time: end-to-end mandatory workflow path, including checkout,
  dependency setup, build, tests, artifacts and required job dependencies/joins.

For CI claims identify the candidate, workflow/required jobs, runner environment,
parallelism/cache state, measurement start/end and observation window/runs. State
whether queue time is included. Compare only to an approved target and like-for-like
baseline; a local grouped run or summed timings do not prove the complete CI path.
Parallelism can reduce waiting without reducing aggregate work or improving test
value. Classify optional lanes explicitly; moving a required guarantee off the
mandatory path needs scoped approval, not an unreported speed optimization.
Unavailable CI measurement is UNKNOWN/NOT RUN, never an extrapolated pass. Targets
for downstream applications stay unresolved until their workload and approval are known.

At delivery carry the selection/decision matrix, defects actually detected with
reproduction evidence versus hypothetical faults, retained guarantees, open gaps,
and mandatory-path wall time versus aggregate cost. Test count is secondary context,
not evidence of confidence, rationalization or acceptance.

## Source and applicability

Michael Bromley, [The Problem With Your AI Tests](https://www.michaelbromley.co.uk/blog/the-problem-with-your-ai-tests/),
7 September 2026 (consulted 28 October 2026), describes tautologies, weak assertions,
missing edge cases, conditional pass logic and implementation-mirroring setup.
Its large suite and reported review findings are the author's observations, not
benchmarks or efficacy evidence for this Skill. The selection, rationalization
and CI-cost procedure above also incorporates the user's disproportionate-suite
feedback; historical counts and timings are not portable acceptance targets.
