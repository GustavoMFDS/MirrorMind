# MM-M1c — synthetic rolling-origin baseline comparison

**Scope:** local experimental teaching example, **not** a deployed
forecasting service, a trained model, a licensed dataset, a forecast
for a real retailer, or a WorldKernel simulation.

Implementation:
[`examples/m1_temporal_backtest.py`](../../examples/m1_temporal_backtest.py).
Input fixture:
[`examples/synthetic-weekly-sales.json`](../../examples/synthetic-weekly-sales.json).
Use the [synthetic dataset card](datasets/SYNTHETIC_WEEKLY_CARD.md)
and [synthetic forecast evaluation card](model_cards/SYNTHETIC_WEEKLY_BASELINES.md)
to interpret this output. See also
[the M1 execution plan](M1_EXECUTION_PLAN.md).

## 1. The narrow experiment

The generated fixture contains **35 consecutive** synthetic dates from
2025-01-01 through 2025-02-04, with a deliberately repeated seven-day
pattern `[2, 4, 6, 8, 10, 12, 14]`. Its date labels are not source
publication-time evidence, and its numbers are not real sales.

We use the first 28 observations before the first origin and evaluate
the final seven **one-day-ahead rolling origins**. Each subsequent
origin is allowed to use the *already observed* previous day's
synthetic outcome. **This is not one seven-day-ahead forecast issued
on January 28.**

Compare two fixed, predeclared toy baselines:

- **Seasonal naive lag 7:** forecast next daily count as the count
  observed on the same weekday one week earlier.
- **Trailing mean lag 7:** forecast as the arithmetic mean of the
  most recent seven **previous** daily counts.

Neither estimator has learnable parameters, a fitted distribution,
uncertainty intervals, source authorization or a production model
registry. On this deliberately perfect weekly pattern the first
baseline makes no errors, which **does not** imply generalization.

## 2. Method contracts and leakage boundaries

| Symbol | Inputs / output | Rejection / interpretation |
| --- | --- | --- |
| `_predict(past)` | Tuple of **past** integer observations, two one-step estimates | Refuses fewer than seven; does not consume the target or any future row |
| `_score(predictions, actual)` | Aligned held-out arrays; MAE, RMSE, bias and WAPE | Refuses empty/misaligned vectors; WAPE is `null` if all observed units sum to zero |
| `backtest_batch(payload, holdout_days=7, min_train_days=14)` | Validates source teaching labels, preflight, complete contiguous dates, exact caps; creates rolling-origin report | Refuses gaps instead of treating missing as zero, old/late cutoff, unsupported labels and insufficient history |
| `main()` | Local fixture path, optional holdout size; JSON summary | 1 MiB input cap, duplicate JSON key rejection, generic error code 2 without echoing input |

For each held-out index `i`, the implementation passes
only `values[:i]` to `_predict` and compares the resulting
forecast with `values[i]`. A regression intercepts the prediction
helper and verifies it received precisely these historical prefixes.

**Temporal caveat:** this protects against direct future-target
lookup in the *toy algorithm*, not against late publication,
revisions, hidden future-derived features, tuning on the evaluation
set or wrong real-world timestamp/rights metadata.

## 3. Defined metrics and hand-worked result

Given held-out values `[2, 4, 6, 8, 10, 12, 14]`,
the seasonal naive repeats exactly the same series, so its MAE,
RMSE and bias are zero. The trailing mean is always 8:

- MAE = `(6+4+2+0+2+4+6)/7 = 24/7 ≈ 3.4286 units`.
- RMSE = `sqrt(112/7) = 4 units`.
- Signed bias = average `predicted - observed = 0 units`.
- WAPE = `24/56 = 3/7 ≈ 0.4286`, a ratio (≈42.86%).

WAPE is `null`, not zero, when the sum of observed
values is zero. The comparison field `lower_mae_on_this_fixture`
does **not** make a recommendation outside this synthetic fixture.

```bash
python -m examples.m1_temporal_backtest examples/synthetic-weekly-sales.json
python -m pytest -q tests/unit/test_m1_temporal_backtest.py
python -m pytest -q tests/integration/test_m1_temporal_backtest_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

The commands are reproduction instructions; actual CI results
are checked before merge. This script emits aggregate synthetic
scores only, not source records or an automated action.

## 4. Curated tests and what they do *not* establish

| Claim | Real regression | Limitation |
| --- | --- | --- |
| **MM-FCST-001** | `tests/unit/test_m1_temporal_backtest.py::test_seasonal_naive_is_exact_on_weekly_fixture_and_mean_is_not` | A deliberately repeated synthetic pattern is not an independent performance estimate |
| **MM-FCST-002** | `tests/unit/test_m1_temporal_backtest.py::test_each_one_step_prediction_receives_only_prior_observations` | Source availability, late revisions and test-set tuning are not covered |
| **MM-FCST-003** | `tests/unit/test_m1_temporal_backtest.py::test_missing_day_abstains_instead_of_zero_imputation` | A contiguous series is not evidence that missing sales were absent at source |
| **MM-FCST-004** | `tests/unit/test_m1_temporal_backtest.py::test_zero_denominator_wape_is_null_not_zero_percent` | Correct WAPE handling does not establish statistical calibration or reliable forecasts |

Other negative cases test invalid cutoffs, forged source labels,
unsupported holdout sizes, insufficient history and a safe CLI.
The fixture is explicitly **synthetic_unverified**.

## 5. Independent exercise and next real-data gate

Change only the final day's demand from 14 to 0 and
predict which previously-issued one-step estimates can
change. Why must the last outcome not be supplied when
constructing the prediction for that same day? Run the
backtest, compare metrics, and explain why choosing a model
using this same holdout makes it no longer untouched.

Then introduce a gap on January 8. Explain why the code
refuses to evaluate rather than silently calling the missing
day zero demand. State what publication timestamps,
verified permitted use, revision histories and privacy
controls would be required before replacing the synthetic
fixture with an authorized dataset.

**Remain planned:** licensed/authorized source ingestion,
genuine forecasting with temporal holdouts, uncertainty
evaluation, API forecast serving, agent orchestration,
WorldKernel adapter and decision evaluation. The current
experimental result does not satisfy the full M1 milestone.
