# Model card — offline staged lag-7 baselines

**Status: local experimental evaluation on invented rows.**
The data are not authenticated and the models are fixed heuristics,
not trained statistical or AI models.

## Inputs, methods and protocol

- **Source fixture:** [staged weekly CSV card](../datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md).
- **Code:** [`src/mirrormind/modules/forecasting/baselines.py`](../../../src/mirrormind/modules/forecasting/baselines.py).
- **Target:** next calendar day's arbitrary generated
  nonnegative units for one synthetic series.
- **Baselines:** `seasonal_naive_lag7` (the value from
  one week earlier) versus `trailing_mean_lag7`
  (mean of the seven previous published values).
- **Horizon:** exactly one day, reissued at each origin,
  **not** one seven-day forecast from January 28.
- **Evaluation cutoff:** February 4, 2025.
- **Origins:** January 28–February 3 for next-day
  targets January 29–February 4.
- **History:** at least 14 event-calendar days before
  the holdout; the exact seven most recent consecutive
  **available** past days feed both heuristics.
- **Source availability:** one fictional late-published
  January 27 row leads to three abstentions.
- **Scoring:** identical four eligible origins for
  both baselines; no imputation or model tuning.

## Observed synthetic metrics

| Measure (four scored origins) | Seasonal lag 7 | Trailing mean lag 7 |
| --- | ---: | ---: |
| MAE | 0 | 3 |
| RMSE | 0 | sqrt(14) ≈ 3.7417 |
| Bias (prediction - actual) | 0 | -3 |
| WAPE ratio | 0 | 3/11 ≈ 0.2727 |
| Scored out of requested | 4/7 | 4/7 |

**Interpretation:** the data were purposely constructed
with perfect seven-day periodicity, making seasonal
naive exact. This cannot establish accuracy on
independent retail demand. Comparing models scored
on differently selected days would be misleading;
the code deliberately scores on one matched subset.

When there are fewer than two evaluated origins,
the report has `metrics: null` and no winner.
WAPE is `null` for zero total actuals.
No predictive intervals, calibration, uncertainty
estimates, model search, drift monitoring or
business stockout costs are estimated.

## Concrete tests and limitations

- `tests/unit/test_staged_rolling_baselines.py::test_staged_rolling_baselines_score_four_of_seven_after_late_publication`
- `tests/unit/test_staged_rolling_baselines.py::test_all_forecast_inputs_precede_origin_and_have_available_seven_day_window`
- `tests/unit/test_staged_rolling_baselines.py::test_zero_denominator_wape_is_null_for_scored_zero_targets`
- `tests/integration/test_staged_rolling_flow.py::test_staged_csv_to_matched_rolling_backtest_without_runtime_io`

These tests establish chosen local arithmetic
and no-lookahead selection under *declared* availability
dates, not rights, publisher provenance, generalization,
independent holdouts, causal benefit or production
reliability. See the [full evaluation template](../FORECAST_MODEL_CARD_TEMPLATE.md)
for the requirements of a real forecast release.

## Origin-level accountability in the local evaluator

A further regression now verifies exactly seven
nonvalue audit records for the seven requested
one-step origins, three `required_history_unavailable`
and four `scored`. This supplements the 4/7
aggregate coverage rather than silently reporting
only the selected scored subset. Separate
`target_missing` and
`target_not_published_by_cutoff` statuses help
distinguish absent events from withheld labels;
neither may be imputed. Tests:
`tests/unit/test_staged_rolling_baselines.py::
test_every_requested_origin_has_one_reproducible_nonvalue_audit_record`
and
`tests/unit/test_staged_rolling_baselines.py::
test_missing_target_is_not_conflated_with_unpublished_target`.

This is **not a tamper-proof audit system**, and the
status-only report does not certify source
authenticity, consent, model generalization or
business decision validity.
