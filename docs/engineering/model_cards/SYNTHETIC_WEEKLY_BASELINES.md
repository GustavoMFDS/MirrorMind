# Synthetic evaluation model card — weekly baselines v1

**Status:** experimental teaching comparison, not a trained
production forecast. No licensed empirical dataset,
statistical calibration or approval for real decisions.

## Models and targets

- **Target:** next day's synthetic unit count for the
  **same** series.
- **Input fixture:** [synthetic dataset card](../datasets/SYNTHETIC_WEEKLY_CARD.md).
- **Seasonal naive lag 7:** `prediction[t] = observed[t - 7]`.
- **Trailing mean lag 7:** average of `observed[t-7:t]`.
- **Model code:** [`examples/m1_temporal_backtest.py`](../../../examples/m1_temporal_backtest.py).
- **Horizon:** exactly one day, rolled forward after each
  observed target. This is **not** a simultaneous
  seven-day prediction from a single origin.
- **Parameter selection:** lag 7 and the two comparators
  fixed before fixture scoring; no hyperparameter search.
- **Training:** these are fixed heuristics rather than
  fitted statistical models.

## Retrospective evaluation protocol

- **Series:** 35 consecutive days, 2025-01-01..2025-02-04.
- **Historical prefix before first test origin:** 28 days,
  through 2025-01-28.
- **Holdout:** seven one-day rolling origins,
  2025-01-29..2025-02-04.
- **At origin `t`:** only values in prefix `[:t]`
  are provided to either heuristic. The previous
  day's actual observation may enter the **next**
  origin, once it is in that origin's past.
- **No gap policy:** abstain on any missing calendar
  day. No implicit zero imputation.
- **Availability weakness:** known observation dates
  do not certify real-world publication times. The
  dataset and test were intentionally constructed
  together; this is not an untouched empirical holdout.

## Held-out scores on the synthetic weekly pattern

| Metric | Seasonal naive lag 7 | Trailing mean lag 7 |
| --- | ---: | ---: |
| MAE (units/day) | 0 | 24/7 ≈ 3.4286 |
| RMSE (units/day) | 0 | 4 |
| Signed bias (forecast minus observed) | 0 | 0 |
| WAPE (ratio) | 0 | 3/7 ≈ 0.4286 |

**Why the baseline wins:** the synthetic observations
repeat the *same* weekly values. That is how the
fixture was created, not a discovery about demand
patterns. No significance interval, interval calibration,
backtesting across stores or distribution shift was
evaluated. A positive result here must not be
advertised as model performance on M5 or a retailer.

The WAPE denominator is `sum(observed)`;
when the holdout sum is zero, WAPE is **undefined
and emitted as JSON null**, rather than a misleading
0%. Error magnitudes are in synthetic units/day.

## Evidence and adverse cases

- `tests/unit/test_m1_temporal_backtest.py::test_seasonal_naive_is_exact_on_weekly_fixture_and_mean_is_not`
- `tests/unit/test_m1_temporal_backtest.py::test_each_one_step_prediction_receives_only_prior_observations`
- `tests/unit/test_m1_temporal_backtest.py::test_zero_denominator_wape_is_null_not_zero_percent`
- `tests/integration/test_m1_temporal_backtest_cli.py::test_synthetic_weekly_fixture_cli_reports_held_out_metrics`

**Still not established:** legal data use, temporal
availability, model drift, data leakage via hidden
feature engineering, model selection without holdout
contamination, stochastic uncertainty, real-world
forecast accuracy or business cost optimization.

## Release / decision boundary

Do **not** use this synthetic backtest to estimate
real inventory, recommend replenishment, compare
forecast risk or feed unverified distributions to
WorldKernel as though they were measured evidence.
Before changing forecasting from `planned` to
`experimental` as a real platform feature, supply
an authorized dataset card, separate untouched
temporal holdout, model version, leakage controls,
independent score review and appropriately scoped
API/runtime execution tests. See the
[forecast model card template](../FORECAST_MODEL_CARD_TEMPLATE.md)
and [M1 execution plan](../M1_EXECUTION_PLAN.md).
