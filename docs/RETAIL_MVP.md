# Retail inventory — first use case

## Question
Which replenishment policy best balances stockout risk, storage/ordering cost and service level over the next 28 days?

## Dataset
Start with a **bounded** subset of the historical M5 Forecasting dataset (product-store sales, price and calendar); obey dataset usage terms. This is *historical sales*, not current stock or internal Walmart inventory. Lead times, stock, operational constraints and unmet demand will require explicit **synthetic assumptions** unless a permitted source is available.

## Evaluation plan
1. Define a date cutoff and temporal train/validation/test splits; no future information as features.
2. Compare simple seasonal-naive baseline to one additional forecasting model on multiple rolling windows.
3. Feed forecast distributions/assumptions to a simple inventory model.
4. Simulate fixed reorder vs threshold vs forecast-aware policies under paired random streams.
5. Report total modeled cost, stockout/fulfillment rates, variability and sensitivity to lead times.
6. Explain assumptions, uncertainties and limits; no causal claim about promotions without a valid causal design.

## MVP acceptance criteria (planned)
- One reproducible end-to-end scenario with a documented, permitted dataset.
- Real held-out backtest vs baseline with published error metric.
- At least three inventory strategies and a sensitivity analysis with identical exogenous random streams where appropriate.
- Per-result provenance, model versions, assumptions, execution cost, no missing-data fabrication.
- API/integration tests, resource budgets and clear demo limitations.

These criteria are targets, not current capabilities.

## Synthetic-only preflight while M1 remains incomplete

A small, local example can validate date labels and count gaps
before any licensed dataset is obtained:
[M1_DATA_PREFLIGHT](engineering/M1_DATA_PREFLIGHT.md).
It runs only on explicitly invented fixture data, does
**not** download M5 or customer data, and supplies no
actual demand forecast. Its `usage_note`, source ID and
snapshot ID are caller text; a real source's permission,
publication latency, revisions and temporal availability
require additional validation and independent evidence.

## Delivery sequence and research acceptance

Follow the reviewed [M1 execution plan](engineering/M1_EXECUTION_PLAN.md).
Any permitted real source must have a completed
[dataset card](engineering/DATASET_CARD_TEMPLATE.md)
and permission evidence, including first-available timestamp.
Both baseline and candidate forecasts require a
[model card](engineering/FORECAST_MODEL_CARD_TEMPLATE.md)
with locked temporal holdout and honestly reported
uncertainty. Future policy comparisons require the
[WorldKernel gateway gate](engineering/WORLDKERNEL_GATEWAY_GATE.md)
and a [decision trace](engineering/DECISION_TRACE_TEMPLATE.md).
These reviews precede implementation claims; they do
not imply the proposed M1 flow already runs.

## Educational rolling-origin baseline comparison

The [M1 synthetic rolling backtest](engineering/M1_TEMPORAL_BACKTEST.md)
compares two simple one-day-ahead heuristics on a generated
35-day weekly pattern and reports transparent MAE/RMSE/bias/WAPE
scores. It has **no real demand, source permissions, stock/lead
time measurements or predictive validity**, and does not satisfy
the retail MVP criteria for a permitted M5 snapshot, independent
holdout, uncertainty or WorldKernel scenario evaluation.

## Event time and publication time are separate

The [synthetic as-of example](engineering/M1_AVAILABILITY_PRECHECK.md)
now illustrates how data dated before a forecast cutoff
could nevertheless be published later and must not enter
past-origin features. Both times are invented and
**not** verified from a real dataset. Genuine M5 or
other authorized data will require a reviewed
[dataset card](engineering/DATASET_CARD_TEMPLATE.md)
and an independently enforced temporal availability rule.
