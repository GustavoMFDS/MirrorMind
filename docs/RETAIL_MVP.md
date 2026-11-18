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
