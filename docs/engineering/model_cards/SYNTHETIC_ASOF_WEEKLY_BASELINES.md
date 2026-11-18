# Synthetic as-of weekly baseline model card

**Status: experimental educational comparison only**.
Not a real source-trained model, production forecast,
uncertainty distribution or validated decision.

## Contract and evaluation

Implementation:
[`examples/m1_asof_rolling_backtest.py`](../../../examples/m1_asof_rolling_backtest.py).
Dataset:
[synthetic as-of weekly card](../datasets/SYNTHETIC_ASOF_WEEKLY_CARD.md).

- **Methods:** predeclared lag-7 seasonal naive and seven-day
  trailing mean, computed from exactly seven published
  synthetic past observations.
- **Horizon:** one day, advanced at each rolling origin,
  not one simultaneous seven-day-ahead scenario.
- **Fixture:** 35 invented dates, Jan 1 through Feb 4, 2025.
- **Holdout window:** Jan 29–Feb 4, seven one-step origins.
- **Availability rule:** both recorded event date and
  claimed publication date must be on/before each
  forecast origin. No interpolation or missing-as-zero.
- **Late record:** Jan 27 first declared available Jan 31.
- **Evaluability:** three dates abstained; four dates scored
  (Feb 1–4) on the **same** subset for both heuristics.
- **Review:** comparing different origin subsets is not
  automatically valid. Coverage is reported alongside
  metrics; an abstention can select easier periods.

## Results (only four scored synthetic dates)

| Metric | Seasonal naive lag 7 | Trailing mean lag 7 |
| --- | ---: | ---: |
| MAE (units/day) | 0 | 3 |
| RMSE (units/day) | 0 | sqrt(14) ≈ 3.7417 |
| Bias (forecast - actual) | 0 | -3 |
| WAPE ratio | 0 | 3/11 ≈ 0.2727 |
| Scored origins | 4 | 4 |
| Abstained origins | 3 | 3 |

**Synthetic perfect periodicity** gives the naive
model its zero score. It is not evidence of real-world
accuracy; the sample is small and deliberately
constructed. No variance estimate, interval
coverage, drift analysis, temporal availability
authentication or real licensing is demonstrated.

For fewer than two valid scored origins, the
implementation produces `metrics: null` rather
than a misleading statistical ranking. A complete
absence of recorded rows and a measured zero
are not interchangeable.

## Regressions and unanswered questions

- `tests/unit/test_m1_asof_rolling_backtest.py::test_late_weekly_observation_causes_three_safe_abstentions`
- `tests/unit/test_m1_asof_rolling_backtest.py::test_origin_inputs_use_only_full_last_seven_available_dates`
- `tests/unit/test_m1_asof_rolling_backtest.py::test_all_origins_can_abstain_without_fake_scores`
- `tests/integration/test_m1_asof_rolling_backtest_cli.py::test_asof_rolling_cli_scores_only_published_history`

These prove an invented as-of policy, not permission,
source history, causal effects, forecast generalization
or business impact. A real, released model would need
the full [forecast evaluation template](../FORECAST_MODEL_CARD_TEMPLATE.md),
an authorized snapshot, locked holdout independent of
model tuning, temporal feature provenance, robust metrics
and human review before decision support.
