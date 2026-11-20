# MM-M1c — prequential residual envelope (synthetic, uncalibrated)

## What is being tested

[`residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py)
performs a **retrospective diagnostic** over fictional daily positive-invoice
lines and **caller-declared, unauthenticated** release dates. It reuses the
fixed seven-day seasonal-naive estimate from the existing baseline module,
then asks whether the observed target falls inside a *heuristic envelope*
based on the **maximum absolute error** of previously released, historically
eligible forecasts.

**This is not conformal prediction, a calibrated prediction interval, a
confidence interval or a nominal coverage guarantee.** No nominal level
is estimated or output. The immutable input projection is not declared
complete demand, and no calendar gap is filled with zeros.

## Exact temporal rules

For a target on day T, the forecast origin is T-1. The forecast requires
seven *consecutive* positive product-days recorded and declared available
no later than T-1. A retrospective outcome is eligible for scoring only
when declared released by the final evaluation cutoff.

Calibration examines up to 21 preceding candidate target dates by default
(bounded 5–60). A candidate residual enters the envelope only if:

1. Its event date precedes T, and its outcome was declared available by
   **T-1**, not merely by the final evaluation cutoff.
2. Its own seven historical feature dates were available before **its
   own forecast origin**, not retrospectively backfilled with future data.
3. It has a positive-line target present. Missing data, cancellations,
   returns and stockouts are never imputed as zeros.

At least five qualifying past residuals are required by default (minimum
configurable 3, never greater than the candidate window). The maximum
absolute eligible residual determines the envelope radius around the
seasonal-naive point estimate; the lower bound is clipped to zero.
Only an aggregate retrospective hit counter and an explicit denominator
are returned. No per-product, customer or invoice identifiers, residual
values, per-origin predictions or per-origin envelope bounds leave the
function. Origin audit rows contain only dates and abstention statuses.

The denominator is the number of **evaluated** origins, not every
requested day. An empty denominator is reported as zero with no percentage
or calibrated interval. Selection bias, dependence, source licensing,
producer provenance, later revisions and empirical future performance
remain unmeasured.

## Negative controls and invented example

The [unit regression suite](../../tests/unit/test_retail_residual_envelope.py)
generates entirely invented positive-line histories. A normal 70-day case
can evaluate seven last-day origins. A second version declares day 60
published only on day 70: its value cannot be used in forecast features
or calibration residuals at origins before day 70. Mutating that hidden
value from 4 to 999,999 leaves the full result unchanged. With an
unpublished final target, that fixture evaluates two origins, abstains on
four missing forecast histories and withholds one unpublished target.

A separate case forces **insufficient calibration** and checks that
zero origins are evaluated rather than making up an interval. Missing
positive-line targets remain missing, not zero; incomplete release
declarations and invalid date/window inputs fail closed.

Curated behavior claim **MM-RENV-001**:
`tests/unit/test_retail_residual_envelope.py::test_delayed_historical_value_is_unavailable_for_forecast_and_calibration`.

```bash
python -m pytest -q tests/unit/test_retail_residual_envelope.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## What remains blocked

Source-authenticated publisher vintages and lawful ingestion, complete
product/store observation and exposure calendars, independent untouched
holdouts, empirical interval calibration, distribution-shift analysis,
per-store dependency adjustment, and statistical coverage guarantees.
Do not compare this toy empirical coverage to an arbitrary claimed 80%
confidence level; no such level exists in this method. No real inference
endpoint, WorldKernel decision execution, or model deployment is enabled.

## Local prequential forecast reuse (experimental)

The residual evaluator now memoizes the seasonal-naive forecast for each
**target date** within one invocation. A target-date prediction always uses
its seven consecutive feature dates available no later than **that target's
own forecast origin**. The release/availability check, calibration outcome
release check at each *current* origin, missing-target refusal and maximum
residual calculation are unchanged. No later value is introduced as an
eligible earlier feature. The cache is **call-local**: a second evaluation,
even with the same cutoff, computes its own forecasts against that call's
projection and declared releases. No source values or identities are
persisted or returned through the receipt.

For the fully published invented seven-day holdout with 21 calibration days,
the repeated loop can request up to `7 × (1 + 21) = 154` predictions.
Call-local caching makes only **28 distinct target-date forecast calls**
for this fixture (21 calibration targets plus 7 holdout dates). This is
a **counted-work reduction** backed by an instrumented test, not a measured
wall-clock speedup or benchmark. The callable still refuses calibration
with insufficient as-of residuals and cannot claim interval calibration.

Evidence **MM-RENV-002**:
`tests/unit/test_retail_residual_envelope.py::test_each_distinct_prequential_target_prediction_runs_once`.
A second regression proves that separately evaluated calls do not share
cached forecasts, and parameterized tests cover missing or late source rows.

## Differential validation against uncached execution

The cache is now compared against the **same historical evaluator with its
memoization decorator disabled** for 18 deterministic combinations of
fictional release delays, missing positive-line days, two products, large
valid quantities, evaluation cutoffs and calibration windows. These tests
compare the entire returned report—including each origin's dated status,
eligibility, coverage counts and explicit uncalibrated flags—not just
aggregates. They assert that customer, product and invoice identifiers
remain absent from reports.

An instrumented **uncached** full-history run performs 154 actual baseline
prediction calls, versus 28 calls with call-local caching, while returning
the same report. A separate regression changes the *declared publication
schedule* between evaluations and confirms the later invocation does not
reuse a stale earlier forecast.

Evidence **MM-RENV-003**:
`tests/unit/test_retail_residual_envelope.py::test_cached_and_uncached_history_agree_under_adversarial_publication_schedules`.
A differential execution path is a **regression oracle for the caching
transformation**, not independent scientific confirmation of the baseline
method, publisher authenticity, true demand or uncertainty calibration.

## Incremental release-aware calibration window (experimental)

A bounded, call-local calendar sweep replaces the repeated nested scan of
all 5–60 calibration candidates for each of 2–30 holdout origins. Candidate
publication declarations schedule *when* an observed target may become
eligible; the candidate's positive-line units and own-origin seasonal-naive
forecast are consulted only after its declared release is no later than the
**current** holdout forecast origin. Candidates already outside the trailing
calendar window are discarded, including when their release arrives too late.
A heap tracks the maximum absolute eligible residual and a separate
chronological expiration heap tracks the exact number of active candidates.
Neither missing days nor late release dates are imputed as zeros.

For every holdout origin, only the dates inside the original trailing window
are eligible, regardless of how long a publication was delayed. Each
candidate's own seven history days must still have been available **at that
candidate's own forecast origin**. Date-filtered maxima and eligibility
counts feed the same abstention and heuristic-radius logic. This reduces
repeated candidate selection work; no wall-clock benchmark or new calibrated
uncertainty property is claimed.

The original evaluator made up to 154 calibration candidate checks on the
seven-origin / 21-day fictional fixture. The previous call-local forecast
memoization reduced distinct predictions to 28; the incremental scan now
also avoids repeated full calibration traversal. The corresponding no-cache
comparison in the regression suite must measure this **new** algorithm,
not assert the former 154 prediction invocations as current behavior.
The 154-vs-28 comparison remains historically documented in PR #34.

Test claim **MM-RENV-004**:
`tests/unit/test_retail_residual_envelope.py::test_incremental_calibration_exactly_matches_naive_reference`.
The test-only quadratic reference checks full origin statuses and aggregate
retrospective coverage under deterministic release schedules and missing
positive-line days. This software equivalence does **not** establish
publisher authenticity, statistical validity or predictive accuracy.
