# M1 synthetic as-of rolling evaluation — evaluate only knowable history

**Status:** standalone local experiment on invented records and publication
dates. It does not ingest an authorized source, produce a validated
forecast, call an agent or run WorldKernel.

Implementation:
[`examples/m1_asof_rolling_backtest.py`](../../examples/m1_asof_rolling_backtest.py).
Fixture:
[`examples/synthetic-asof-weekly-sales.json`](../../examples/synthetic-asof-weekly-sales.json).
See the [two-timestamp preflight](M1_AVAILABILITY_PRECHECK.md),
[plain rolling-origin baselines](M1_TEMPORAL_BACKTEST.md),
[synthetic data card](datasets/SYNTHETIC_ASOF_WEEKLY_CARD.md),
and [scoring card](model_cards/SYNTHETIC_ASOF_WEEKLY_BASELINES.md).

## 1. Why one final snapshot is insufficient

A retrospective dataset may contain a record **today** that a
forecaster could not have used at a **past** origin.
A final cutoff check on the full file is not enough.

This example uses 35 invented consecutive daily observations,
with the seven-day pattern `[2, 4, 6, 8, 10, 12, 14]`.
One synthetic record **observed on Jan 27** is declared
available **Jan 31**. The final evaluation cutoff is
Feb 4, so the full file includes this value, but rolling
origins before Jan 31 must not read it.

Both heuristics need the **seven previous consecutive days**:

- `seasonal_naive_lag7`: repeat the oldest value in the
  seven-day historical window.
- `trailing_mean_lag7`: average those same seven values.

For a target date `t`, the prediction origin is `t-1`.
The code requires **every** day in the lag-7 window
to have `available_on <= t-1`, otherwise both
models **abstain**. It never fills an unavailable
value with zero or with a later revision.

## 2. Source-reviewed method contracts

| Symbol | Observable behavior | Boundary |
| --- | --- | --- |
| `backtest_asof(payload, holdout_days=7, min_train_days=14)` | Validates declared as-of schema and synthetic labels; sorts and checks contiguous event dates, then scores a common subset of one-step origins | Rejects impossible metadata, released-after-evaluation targets, invalid cutoffs and missing event dates; it does not authenticate publication |
| `_predict(past)` from the earlier backtest | Uses the exact seven published observations before the target | No direct access to target or later values; history completeness is checked first |
| `_score(predictions, actual)` from the earlier backtest | MAE, RMSE, signed bias and WAPE on identical scored targets | Returns WAPE `null` for all-zero observed denominator; no uncertainty calibration |
| `main()` | 1 MiB input cap, duplicate-key rejection, synthetic JSON summary | Generic exit 2 on invalid input; no raw fixture or path echoed |

The [earlier as-of preflight](M1_AVAILABILITY_PRECHECK.md)
checks **all** input row types, impossible event/publication
order and duplicate dates. The rolling function separately
checks **availability at each past origin**, not just at the
final extraction cutoff. The full dataset can be
35 days long while some prior origins lack a
complete seven-day available history.

## 3. Hand-worked result

| Target in seven-day holdout | Historical lag-7 value | Decision |
| --- | --- | --- |
| Jan 29 | Jan 27 not yet published | Abstain |
| Jan 30 | Jan 27 not yet published | Abstain |
| Jan 31 | Jan 27 not yet published at origin Jan 30 | Abstain |
| Feb 1–4 | Lag-7 windows fully published by each origin | Score four days |

The scored synthetic targets are `[8, 10, 12, 14]`.
Seasonal naive matches this artificial repeating pattern
exactly. Trailing mean predicts 8 at each scored origin.

| Metric on **four scored days only** | Seasonal naive | Trailing mean |
| --- | ---: | ---: |
| MAE | 0 | 3 |
| RMSE | 0 | sqrt(14) ≈ 3.7417 |
| Bias (forecast minus observed) | 0 | -3 |
| WAPE | 0 | 3/11 ≈ 0.2727 |

**Coverage is 4/7, not 7/7.** Reporting MAE without
abstention count would hide the missing three cases.
Because the scored subset is selected by availability,
performance on these four dates may be biased relative
to a complete seven-day holdout; **a perfect synthetic
score is not a validated empirical forecast**.

If all evaluated origins have incomplete history,
the result explicitly reports zero scored origins,
all origins abstained, `metrics: null` and no winner.
Fewer than two scored origins also produces no
numeric comparison. The code never guesses a
missing forecast.

## 4. Tests and evidence limits

| Claim ID | Test selector | Not established |
| --- | --- | --- |
| **MM-ASOF-001** | `tests/unit/test_m1_asof_rolling_backtest.py::test_late_weekly_observation_causes_three_safe_abstentions` | Synthetic timing is not verified original-source availability |
| **MM-ASOF-002** | `tests/unit/test_m1_asof_rolling_backtest.py::test_origin_inputs_use_only_full_last_seven_available_dates` | No guarantee against hidden future-derived features or revised production data |
| **MM-ASOF-003** | `tests/unit/test_m1_asof_rolling_backtest.py::test_all_origins_can_abstain_without_fake_scores` | Correct abstention does not establish predictive quality or an automated decision policy |

The [CLI regression](../../tests/integration/test_m1_asof_rolling_backtest_cli.py)
also checks bounded input and sanitized failures.

```bash
python -m examples.m1_asof_rolling_backtest examples/synthetic-asof-weekly-sales.json
python -m pytest -q tests/unit/test_m1_asof_rolling_backtest.py
python -m pytest -q tests/integration/test_m1_asof_rolling_backtest_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These are reproduction instructions. Check actual CI
results before claiming tests passed.

## 5. Independent learning exercise

First, identify the exact reason Jan 29, 30 and 31
cannot use Jan 27. Change the fictional Jan 27
availability to Jan 27 and predict the coverage
change from 4 to 7 scored origins. Next, set Jan 27
availability **after Feb 4** and explain why
even the final dataset snapshot cannot restore
past availability and why the algorithms must
not silently substitute another day.

Finally, answer: if a published score uses only four
of seven holdout dates, should its MAE be compared
directly to a model scored on all seven? What would
be needed to make that a fair comparison?

**M1b/M1c remain incomplete** for real authorized
snapshots, genuine source availability timestamps,
locked empirical holdouts, model evaluation and
deployed forecasting. This exercise demonstrates
a code-level guard, not the completeness of a
forecasting platform.
