# Product guarantees and test value v1.0.0

Contract ID: agentic-development/test-value
Contract version: 1.0.0

Apply when writing, selecting or reviewing application tests, or analyzing a suite
for rationalization. This is not permission to edit tests or the frozen candidate.
Implement writes tests within an authorized task; Test diagnoses and proposes
changes; authorized corrections go through Iterate and Implement, then Test checks
the changed candidate.

## Contents

- [Select evidence, not volume](#select-evidence-not-volume)
- [Same branch is not a new test](#same-branch-is-not-a-new-test)
- [Write tests as living documentation](#write-tests-as-living-documentation)
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

## Same branch is not a new test

Before adding a test that differs from a neighbour only in an input value, confirm
that the production code or the specification distinguishes that value. A
passthrough field, or one guard rejecting every disallowed enum value, means the
existing test already covers it: add the value to that test's example data only
when it documents the rule, not as another test.

Add the case when the code branches on the value, when the specification names it
as a distinct boundary, error or incident, or when a distinct environment can
expose a different fault. If the specification distinguishes a value that the code
does not, write that test: its failure reveals a gap, not a duplicate.

Every redundant test costs CI time and the tokens an agent spends reading it later.
During an authorized rationalization, look for same-branch variants and
cross-file duplicates of the same guarantee, then apply the merge or remove
decision below with the retained check named.

## Write tests as living documentation

A reader who does not know the code should learn from the tests what the software
must do, by reading concrete examples that run.

| Part | What it must tell the reader |
|---|---|
| Name | The name states the rule: `test_site_without_approval_cannot_be_published`, not `test_publish_returns_409`. |
| Given | Only the conditions that matter. Name fixtures in domain terms; add those that rule out other causes, so the reader sees which condition decides the outcome. |
| When | Perform one action, by a user or the system. |
| Then | The expected outcome and, when the rule depends on them, its effects, including state left unchanged by a refusal. |
| Set of cases | The set of cases bounds the rule: at least one allowed and one refused example, plus each case the specification distinguishes. |

~~~python
def test_site_without_approval_cannot_be_published(
    ready_site_without_approval,
    authorized_publisher,
):
    site = ready_site_without_approval

    with pytest.raises(ApprovalRequired):
        site.publish(by=authorized_publisher)

    assert site.status == SiteStatus.READY
~~~

`authorized_publisher` establishes that permissions suffice, so the refusal can
only come from the missing approval. The last assertion states a second guarantee
of the same scenario: the refusal leaves the site unchanged.

- Choose the level by the guarantee. A domain rule is asserted on domain outcomes.
  A public API contract can assert the HTTP status and error code clients rely on,
  for example `409` with an approval-required code.
- Keep the criterion ID in a docstring or marker unless the project convention puts
  it elsewhere; the name stays readable as the rule.
- A green test confirms that the written scenario works. Review still checks that
  the scenario still expresses the intended rule; when a rule changes on purpose,
  review the behavior change and its examples together.
- Review question: **without opening the implementation, can I explain the rule
  this test protects and give a concrete example of what must happen?** A no is a
  readability finding.

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
- Replace only system boundaries: external services, the clock, randomness and,
  when a real or test instance is impractical, the database or file system. Do not
  mock modules the project owns or internal collaborators; exercise them through
  the public seam. At a boundary, pass the dependency in rather than constructing
  it inside the subject, and prefer one named operation per external call over a
  generic request function, so each replacement returns one specific shape. This
  is boundary design, not permission to add injection layers to multiply tests.
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

Ido Shamun, "Reducing redundant test bloat generated by AI coding agents", daily.dev
(text supplied by the user, consulted 19 November 2026), describes agents adding
repetitive coverage-driven tests and proposes the same-branch rule above; its
reported removals are the author's observations, not benchmarks. The living
documentation section incorporates the user's feedback of the same date.
