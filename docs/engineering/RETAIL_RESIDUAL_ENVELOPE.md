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
