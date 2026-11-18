# MirrorMind M1 delivery plan — evidence before intelligence claims

**Goal:** demonstrate one honest, reproducible retail replenishment
decision workflow while keeping MirrorMind domain-neutral.
An accepted architecture is not equivalent to implemented AI.

Current state: API scaffold and ScenarioSpec validation are
implemented; a bounded [synthetic daily preflight](M1_DATA_PREFLIGHT.md)
is an **experimental local example**. Evidence ingestion,
forecasting, decision evaluation and WorldKernel adapter
remain planned.

## 1. Dependency-ordered milestones

| Slice | Deliverable | Independent gate | Capability claim |
| --- | --- | --- | --- |
| **M1a — existing teaching slice** | Pure synthetic count/daily cutoff preflight, missing day summary and safe CLI | Unit/CLI regressions; no real source or model evaluation | `experimental`, not ingestion |
| **M1b — authorized observation input** | Read a bounded, approved dataset snapshot with explicit entity/time/units, license, provenance, availability date and no silent imputation | Data card, permission evidence, duplicate/late publication/leakage tests, deterministic sanitized fixture | Do not call it `implemented` until tested and reviewed |
| **M1c — forecast baselines** | Seasonal-naive benchmark and a second honest baseline, both with fixed temporal splits | Rolling-origin test, documented MAE/RMSE and zero-safe metrics, comparison on the same holdout, model cards | Experimental forecasts **only** with scope and empirical backtest |
| **M1d — uncertainty and sensitivity** | Calibrated or explicitly uncalibrated interval procedure and robustness across missing days/lead times | Interval-coverage tests, drift/abstention cases, forecast card update | Do not present intervals as guaranteed |
| **M1e — first simulation gateway** | Concrete, optional WorldKernel adapter over explicit version mapping and trusted worlds | SDK contract tests, unsupported input rejections, server-owned budgets, real fixture E2E without fabricating stock | `worldkernel_adapter` may become experimental after tests |
| **M1f — reviewable decision comparison** | Trace observations, forecasts and conditional scenario outcomes without automatic business writes | Decision trace, approval gates, cost budgets and independent replay | No agentic automation or operational promise until implemented |

M1b should use only a **permitted subset** of M5 or another
authorized source. Historical product-store *sales* are not
proof of current stock, stockouts or true latent demand.
Lead time and inventory starting points require separately
sourced evidence or explicit synthetic assumptions.

## 2. Risk and quality gates that cannot be skipped

**Data:** source rights, privacy, immutable snapshot identity,
observation and *availability* time, reporting delay,
revision history, missingness and entity constraints.

**Forecasting:** temporal holdout locked before tuning,
sane baseline, a second evaluated model, calibrated or
honestly uncalibrated uncertainty, negative controls
and reproducibility in a named environment.

**Simulation:** model assumption register, scenario
feasibility/units, versioned WorldKernel exchange,
paired exogenous conditions where appropriate,
runtime resource caps and error/timeout paths.

**Decision:** separated facts, estimates and conditional
outcomes, measurable objective, risk tradeoffs,
review ownership, abstention and independent human
authorization before sensitive writes.

Use the review templates:
[dataset card](DATASET_CARD_TEMPLATE.md),
[model card](FORECAST_MODEL_CARD_TEMPLATE.md),
[WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md),
[decision trace](DECISION_TRACE_TEMPLATE.md) and
[capability promotion](CAPABILITY_GATES.md).

## 3. Minimum demonstrable first user story (not yet built)

A user asks, *"Among three inventory replenishment
policies, what is the tradeoff between lost-sales proxy,
remaining stock and ordering frequency over 28 days?"*

A conforming eventual response must show:
1. Which **authorized** historical data existed at the
   forecast cutoff and what it could not measure.
2. The baseline and second model's held-out scores.
3. The source and calibration of uncertainty assumptions.
4. How each policy was mapped into a trusted, versioned
   simulation world with reproducible random seeds.
5. The conditional comparison, costs and unknowns.
6. Why a human should review before any operational action.

No current API route delivers that story. In particular,
`POST /v1/scenarios/validate` remains `validated_not_executed`.

## 4. Developer and learner acceptance

For every slice, add one source walkthrough, an
independent exercise, a normal path, at least one
adversarial regression, explicit CI evidence and
a known-limitation note. Update the
[semantic matrix](SEMANTIC_COVERAGE.md),
[capability ledger](CAPABILITY_LEDGER.json),
[reviewed atlas](REPOSITORY_ATLAS.md),
and [roadmap](../ROADMAP.md) in the same PR.

Before shipping any capability, an engineer should
be able to answer:
**What data is this based on? What was knowable then?
Which assumptions and costs govern it? What test
would disprove this conclusion? What does the
system still not know?**

## Synthetic as-of training slice (does not complete M1b)

The [M1 availability preflight](M1_AVAILABILITY_PRECHECK.md)
now tests claimed observation versus publication dates
on a **generated** fixture. This is useful groundwork
for preventing a simple form of temporal leakage, but
the M1b acceptance gate remains unchanged: real
dataset rights, provenance, availability proof,
revision history, privacy and retention checks.

## New experimental local staging primitive — M1b remains open

The reusable [local CSV staging module](M1_LOCAL_CSV_STAGING.md)
now validates strict daily CSV bytes, a declared content digest,
duplicate per-series dates, chronological publication order and
two-timestamp as-of queries. It does not download or persist
data and always describes its receipt as **not authorized**.

This closes a narrow **structural** preflight dependency,
not the M1b authorized-ingestion milestone. A real-data
release still requires documented legal source rights,
independent trusted snapshot hash/provenance, publisher
availability and revision history, privacy/retention controls,
source-specific bounded I/O and approval before modeling.
