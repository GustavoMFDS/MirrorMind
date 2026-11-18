# M1c-local — rolling-origin baselines over structurally staged observations

**Status: experimental, offline and source-unverified.**
This is the first reusable baseline evaluator inside
[`src/mirrormind/modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py).
It consumes an immutable
[`StagedSnapshot`](M1_LOCAL_CSV_STAGING.md), not a real
approved dataset or a production forecast API.

See [synthetic weekly staged data](datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md),
[the evaluated model card](model_cards/STAGED_WEEKLY_BASELINES.md),
[M1 delivery plan](M1_EXECUTION_PLAN.md) and
[model evaluation requirements](FORECAST_MODEL_CARD_TEMPLATE.md).

## Source and dependency path

```text
Trusted local caller (not an HTTP endpoint)
  -> stage_csv_snapshot(bytes, expected_sha256) [structural preflight ONLY]
      -> immutable staged Observations, declared availability timestamps
  -> backtest_staged_snapshot(staged, series_id, evaluation_on)
      -> historical target day, prediction origin is the prior day
      -> available_as_of(staged, series_id, origin)
      -> require exactly seven preceding consecutive published days
      -> _predict(history): seasonal naive lag7 / trailing mean lag7
      -> _score on the exact same scored targets for both models
      -> one report with metrics or explicit null + abstention counts
```

**No source authorization happens anywhere in this path.**
A SHA-256 compared with the digest generated from the
same unverified data is not provenance authentication.
Future approved-source ingestion and secure permissions
must remain separate from statistical evaluation.

## Method-by-method reviewed contracts

| Symbol | Inputs / output | Critical failure and statistical boundary |
| --- | --- | --- |
| `_day(value)` | Canonical ISO calendar cutoff -> `date` | Reject invalid/ambiguous/non-string cutoffs; this is not a verified publication timestamp |
| `_predict(seven)` | Exactly seven nonnegative integer past observations -> two one-step estimates | Reject insufficient history; no fit, intervals or future-target access |
| `_score(forecasts, actuals)` | Aligned predictions and held-out actuals -> MAE, RMSE, signed bias, WAPE | Reject mismatched/empty arrays; WAPE `null` for zero observed sum |
| `backtest_staged_snapshot(staged, series_id, evaluation_on, holdout_days=7, min_history_days=14)` | Fixed last `holdout_days` calendar dates ending at the declared evaluation cutoff; returns counts, optional metrics and snapshot hash | Reject non-staged input, bad bounds, unknown series and insufficient event-span; abstain when a target was not published by final cutoff or the lag-7 input wasn't published by its own origin |

Each candidate target date is **fixed from the cutoff**,
not chosen because a convenient observation exists.
For day `t`, the forecast is formed at `t-1`
using only `t-7 ... t-1` **if every value was published
by that origin**. The code calls the shared staged
snapshot's `available_as_of`, never substitutes a
missing value with zero, and does not silently change
the comparison set for one model only.

The final evaluation may use target outcomes that were
published by the evaluation cutoff. It cannot claim a
true untouched or independently pre-registered holdout:
the fixture is explicitly generated to favor a seasonal
pattern. Real sources may have revisions, blackout
windows, backfilled labels and reporting timestamps
that this module cannot authenticate.

## Deterministic example: four of seven origins scored

The invented CSV has **35 consecutive January 1–February 4,
2025** dates repeating `[2,4,6,8,10,12,14]`, with
January 27 declared published only on January 31.

- Origins January 28, 29 and 30 cannot see January 27
  and abstain.
- The February 1–4 targets have complete seven-day
  published windows. Their synthetic actuals are
  `[8,10,12,14]`, and the last-seven mean is 8.
- Both models are evaluated on these **same four days**.

| Metric | Lag-7 seasonal naive | Trailing 7-day mean |
| --- | ---: | ---: |
| MAE (synthetic units/day) | 0 | 3 |
| RMSE | 0 | sqrt(14) ≈ 3.7417 |
| Signed bias (forecast minus observed) | 0 | -3 |
| WAPE ratio | 0 | 3/11 ≈ 0.2727 |
| Scored / requested origins | 4/7 | 4/7 |

The report separates `abstained_missing_history`
from `abstained_target_unavailable`. If fewer than two
origins are scored, it emits **null metrics and null winner**
instead of inventing a model ranking. A repeated-week
synthetic pattern yielding zero errors does not show
real predictive accuracy, improved retailer inventory
or causal benefit. Coverage selection itself can
bias the measured error.

## Reproduce using only invented local observations

```python
from hashlib import sha256
from pathlib import Path
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.forecasting.baselines import backtest_staged_snapshot

raw = Path("examples/staged-weekly-availability.csv").read_bytes()
staged = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
report = backtest_staged_snapshot(
    staged, series_id="item-A", evaluation_on="2025-02-04"
)
assert report["scored_origins"] == 4
assert report["abstained_missing_history"] == 3
assert report["source_status"] == "not_authorized_or_authenticated"
```

Again, this recipe hashes the same generated fixture:
**it demonstrates parser behavior, not actual source
or licensing proof**. The core functions do not open
files or issue network requests on their own.

## Curated regressions and explicit limitations

| Claim | Test selector | What this does not prove |
| --- | --- | --- |
| **MM-BL-001** | `tests/unit/test_staged_rolling_baselines.py::test_staged_rolling_baselines_score_four_of_seven_after_late_publication` | Scores are on invented seasonality and do not generalize to genuine demand |
| **MM-BL-002** | `tests/unit/test_staged_rolling_baselines.py::test_all_forecast_inputs_precede_origin_and_have_available_seven_day_window` | Explicit window selection does not authenticate actual publication dates or hidden features |
| **MM-BL-003** | `tests/unit/test_staged_rolling_baselines.py::test_all_origins_can_abstain_with_null_metrics_not_fake_winner` | Abstention prevents fabricated scores, but is not an uncertainty/calibration assessment |
| **MM-BL-004** | `tests/integration/test_staged_rolling_flow.py::test_staged_csv_to_matched_rolling_backtest_without_runtime_io` | Local fixture integration does not provide permission, production execution or versioned model serving |

Other tests cover observed zero versus missing target,
late publication, bad horizon/date, insufficient
prehistory and undefined WAPE at an all-zero denominator.

```bash
python -m pytest -q tests/unit/test_staged_rolling_baselines.py
python -m pytest -q tests/integration/test_staged_rolling_flow.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These are reproduction instructions, not claims that
real observations or authorized sources have been tested.

## Independent exercise and next acceptance gate

Change January 27's claimed `available_on` to
January 27 and predict why all **7/7** origins become
scorable. Then postpone January 28 publication until
March and identify why even the last origin must abstain.
Explain how a 4/7 result can conceal selection bias
against a model evaluated on all seven days, and why
a good WAPE on deliberately repeated invented data
cannot justify purchasing inventory.

Before calling a real forecasting feature
`implemented`, obtain a separately approved dataset,
first-availability and revision evidence, source rights,
locked temporal holdouts, a second measured baseline,
uncertainty evaluation, versioned inference output,
access controls, model-card review and actual replay.
**The existing `forecasting` capability remains planned.**
