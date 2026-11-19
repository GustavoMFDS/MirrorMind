# MM-M1c experimental retail backtest over declared releases

## Scope and scientific boundary

[`release_backtest.py`](../../src/mirrormind/domains/retail/release_backtest.py)
reuses the existing **fixed** lag-seven seasonal-naive and trailing-mean
baselines on strictly positive UCI-shaped fictional invoice-line counts.
It composes the previous [declared-release audit](DECLARED_RETAIL_RELEASES.md)
rather than silently deriving historical publication dates from transaction
dates. All release assertions remain **caller-declared and unauthenticated**.
No full-calendar demand, store opening, inventory, stockout or collection
completeness is proven.

The evaluator accepts one selected product, a date cutoff, and 2–30
one-day holdout origins. For each target date it first abstains if the target
positive line is absent (NOT zero) or declared unpublished by the evaluation
cutoff. It then requires exactly seven preceding **consecutive calendar**
dates with positive product/day records declared available by the immediately
preceding origin. Only matched eligible origins contribute to either model's
MAE/RMSE/bias/WAPE. Fewer than two scored origins produce null metrics,
not a spurious winner.

All supplied releases must cover all projected product-day keys exactly
once. This rejects missing/duplicated/unmatched/impossible releases even
when they concern a different product. No identifier or raw value is copied
into the output: only audit statuses, dates, aggregate scores and a proxy
description. This does not perform operational inference or store results.

## Synthetic demonstration and negative controls

[Unit tests](../../tests/unit/test_retail_release_backtest.py) create a
35-day invented positive-line history, with day 33 absent, day 27 declared
available on day 30, and the final day declared unpublished at the cutoff.
Over holdout days 29–35, **two origins are scored, three lack valid history,
one has no target and one has an unpublished target**. Both fixed models
use the same two targets. Mutating the withheld final target cannot change
the scored metrics; moving a critical historical release beyond the
evaluation cutoff forces full abstention.

Curated claim **MM-RBT-001** maps to
`tests/unit/test_retail_release_backtest.py::test_missing_late_and_unpublished_days_abstain_and_models_share_origins`.
This is evidence of code behavior on invented values, **not** real
predictive performance, source rights, opening-day completeness,
historical vintages or statistical validity of an inventory policy.

```bash
python -m pytest -q tests/unit/test_retail_release_backtest.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Independent learning exercise

Change the withheld target's units and show that metrics remain unchanged.
Then declare day 27 released only after the cutoff; demonstrate that neither
baseline forecasts from unavailable history. Finally, explain why
a calendar without positive sales cannot legitimately be padded with zeros
unless an independent, authorized complete-observation claim exists.

Before progressing to MM-M1c empirical evaluation: verify original data
reuse rights, privacy and attribution; independently authenticate publisher
snapshots and availability versions; define actual complete operating
calendars; preserve an untouched holdout and compare baselines with matched
statistical evidence. The `forecasting` API capability remains planned,
and no WorldKernel or action endpoint is involved.
