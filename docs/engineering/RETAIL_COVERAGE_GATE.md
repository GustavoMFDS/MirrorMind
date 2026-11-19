# MM-M1c — conservative retail holdout coverage gate (experimental)

## What this does

The source [coverage gate](../../src/mirrormind/domains/retail/coverage_gate.py)
wraps the existing [release-aware fictional backtest](RETAIL_RELEASE_BACKTEST.md)
and **withholds the model ranking** when the eligible matched origins do
not meet an explicitly set minimum fraction. Default minimum is **80%**,
with an independent minimum of two scored origins. Arithmetic is exact:
`scored_origins * 100 >= holdout_days * minimum_coverage_percent`.
The threshold is a user-selected review criterion, not a validated
statistical power calculation or guarantee of accuracy.

The function retains aggregate abstention counts for missing targets,
unpublished targets and incomplete seven-day history; the counters must
sum exactly to the requested holdout days. Receipt outputs include exact
coverage numerator and denominator. Product, customer, invoice, prices
and source rows are never emitted. All release dates remain
**caller-declared and unauthenticated**.

A conditional rank, even when allowed, **does not prove model
generalization**: it describes lower MAE on the matched fictional
positive-invoice-line targets alone. The result explicitly returns
`uncertainty_status=not_estimated_or_calibrated` and
`prediction_interval=None`, never a fabricated confidence or prediction
interval. Source approval, true store calendar, real stock and
latent demand remain unknown.

## Fictional illustration

The 35-day fixture in
[unit regressions](../../tests/unit/test_retail_coverage_gate.py)
has seven target origins, including delayed input availability,
one missing positive-line target and one unpublished target. Only two
of seven origins are scored. Its exact coverage is **2/7** (about 28.6%),
so the default 80% gate rejects a model ranking even though the
underlying evaluator can calculate conditional toy scores on two origins.

A second fully declared fictional 35-day history scores all seven
origins and passes the gate, **without** establishing genuine forecast
skill. Integer threshold boundary tests check 28% versus 29% on the
2/7 case. No non-observed product-day is set to zero.

Curated claim **MM-RGATE-001** maps to
`tests/unit/test_retail_coverage_gate.py::test_incomplete_declared_releases_suppress_model_ranking_and_report_exact_coverage`.
This checks software behavior, not source authenticity, confidence
interval coverage or empirical external validity.

```bash
python -m pytest -q tests/unit/test_retail_coverage_gate.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Independent review and next evidence gate

Re-run the toy fixture with a 29% threshold (ranking suppressed), then
28% (conditional ranking permitted). Explain why that threshold change
does not improve the two model forecasts, fix publication metadata or
validate uncertainty. Any future interval method must be predeclared,
trained only on earlier eligible residuals, evaluated on untouched later
origins with empirical coverage diagnostics and with abstention whenever
insufficient observations exist. This module implements **no intervals**.

M1b authorized source ingestion, M1c empirical validation, WorldKernel
integration and operational decision automation are still pending.
