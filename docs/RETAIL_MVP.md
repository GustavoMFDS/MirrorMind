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

## Experimental synthetic policy test double

The [M1 retail policy comparison](engineering/M1_RETAIL_POLICY_SIMULATION.md)
now exercises three replenishment rules for 28 days against paired seeded
fictional demand streams, with explicit starting stock, lead time and abstract
cost assumptions. It demonstrates local policy mechanics and lead-time
sensitivity only. The input profile is not an evaluated forecast, the cost
units are not currency or measured business costs, and the result is not a
WorldKernel execution or policy recommendation. The full M1 policy acceptance
still requires the separate [WorldKernel gateway gate](engineering/WORLDKERNEL_GATEWAY_GATE.md),
validated forecasts/assumptions and a human-reviewed decision trace.

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

## Synthetic rolling scores require complete as-of history

The [as-of rolling example](engineering/M1_ASOF_ROLLING_EVALUATION.md)
demonstrates how a deliberately late publication causes
three of seven toy forecast origins to abstain, leaving
four scored synthetic days. This is **not** an
empirical forecasting result. Real evaluation must
preserve both temporal availability and scored-origin
coverage across models, source revisions, permission
constraints and genuinely held-out periods.

## Reusable offline one-day baselines (not retail forecasts)

The experimental [staged rolling baseline evaluator](engineering/M1_STAGED_ROLLING_BASELINES.md)
now uses a reusable source module rather than
only standalone demonstration scripts. It applies
as-of publication cutoffs, reports abstention
coverage and calculates matched MAE/RMSE/bias/WAPE
on invented weekly observations. It does **not**
establish allowed M5 access, true sales or demand,
stockout costs, lead times or real forecasting
skill. These remain separate retail MVP gates.

## Original M5 permissions must be independently confirmed

The [M5 due-diligence card](engineering/datasets/M5_ACCESS_REVIEW.md)
remains `proposed / permission-unverified`.
The fact that historical retail data are offered
through a competition or third-party archive
does not itself license MirrorMind's intended use,
permit redistribution or establish publication
time vintages for leakage-free rolling validation.
Do not download or commit M5 observations until
a rights holder's applicable grant and source
approval have been reviewed.

## Alternative with a published source license: UCI Online Retail

The original [UCI Online Retail candidate](engineering/datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
publishes CC BY 4.0 on its official dataset page.
It may provide historical **transaction sales**
for a limited research baseline once attribution,
privacy and source handling are approved.
It does **not** provide stock on hand, lead
time, lost sales, verified day-by-day publication
availability or a ready-made M5-like demand
forecast. Do not substitute it for M5 without
recording a new dataset snapshot and objective.
