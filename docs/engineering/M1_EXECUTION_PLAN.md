# MirrorMind M1 delivery plan — evidence before intelligence claims

**Goal:** demonstrate one honest, reproducible retail replenishment
decision workflow while keeping MirrorMind domain-neutral.
An accepted architecture is not equivalent to implemented AI.

Current state: API scaffold and ScenarioSpec validation are
implemented; bounded synthetic preflights, review-only staging,
offline retail baselines, release-aware evaluation, a pure WorldKernel
request mapper and a local three-policy test double exist as
**experimental or interface-only slices**. Authorized evidence ingestion,
empirical forecasting/uncertainty, actual WorldKernel execution and the
integrated human-reviewed decision workflow remain unimplemented.

## 1. Dependency-ordered milestones

| Slice | Deliverable | Independent gate | Capability claim |
| --- | --- | --- | --- |
| **M1a — existing teaching slice** | Pure synthetic count/daily cutoff preflight, missing day summary and safe CLI | Unit/CLI regressions; no real source or model evaluation | `experimental`, not ingestion |
| **M1b — authorized observation input** | Read a bounded, approved dataset snapshot with explicit entity/time/units, license, provenance, availability date and no silent imputation | Data card, permission evidence, duplicate/late publication/leakage tests, deterministic sanitized fixture | Do not call it `implemented` until tested and reviewed |
| **M1c — forecast baselines** | Seasonal-naive benchmark and a second honest baseline, both with fixed temporal splits | Rolling-origin test, documented MAE/RMSE and zero-safe metrics, comparison on the same holdout, model cards | Experimental forecasts **only** with scope and empirical backtest |
| **M1d — uncertainty and sensitivity** | Calibrated or explicitly uncalibrated interval procedure and robustness across missing days/lead times | Interval-coverage tests, drift/abstention cases, forecast card update | Do not present intervals as guaranteed |
| **M1e — first simulation gateway** | Concrete, optional WorldKernel adapter over explicit version mapping and trusted worlds | SDK contract tests, unsupported input rejections, server-owned budgets, real fixture E2E without fabricating stock | `worldkernel_adapter` may become experimental after tests |
| **M1f — reviewable decision comparison** | Trace observations, forecasts and conditional scenario outcomes without automatic business writes | Decision trace, approval gates, cost budgets and independent replay | No agentic automation or operational promise until implemented |

## Current synthetic M1 path — 2026-11-24

The M1B-02 [evidence flow](M1_SYNTHETIC_EVIDENCE_FLOW.md) composes local
CSV/XLSX staging, review-only metadata, declared calendar/release checks and
as-of selection. Its implementation is proposed in draft PR #52. The M1C-01
[retail evidence-to-evaluation flow](M1_RETAIL_SYNTHETIC_EVALUATION.md) now
composes the UCI-shaped evidence flow with the existing fixed baselines and
per-origin release abstentions; its generated CLI uses only fictional bytes.
Both remain experimental. The exact PR #52 implementation SHA passed its
canonical local gate with 696 tests; exact PR #53 head
`210f0f382938a67e518df688cc4e19c03d3d7af6` passed with 700 tests, including
the API integration module. Official Actions is separately blocked before
jobs by [B-08](BLOCKERS.md). M1E-03 now has a partial local test-double
proposal; it does not satisfy M1E-02 or the actual-engine gate. These
synthetic slices do not satisfy M1b's real-source rights and availability
gate, M1c's empirical holdout or M1d's calibrated uncertainty requirements.

M1F-01 adds a versioned local decision-result contract on the current
stacked branch. It keeps facts, estimates, modeled outcomes, assumptions,
gaps, costs and human review separate, with local reference/cutoff checks and
an exact-result digest. Its docs head passed the canonical local gate with
712 tests, including API; official checks remain blocked by B-08. It is
interface-only: no producer, ranking, API, storage, actual engine output or
action permission exists. M1F-02 can compose a clearly labeled local test
double for an end-to-end synthetic demonstration, but remains partial until
actual engine integration and its other named M1 predecessors pass.

M1E-01 now has a pure, fail-closed request mapping for the inspected
`retail.inventory` `0.1` to WorldKernel `retail.inventory.demo` `demo-1`
contract. It requires explicit item/day/order units and operator-configured
limits, and rejects unresolved evidence/forecast refs, interventions and
unknown state or parameters. It constructs JSON only. M1E-02 remains blocked
on B-04 for a pinned compatible engine and actual SDK execution; no simulation
capability is promoted. The current docs head passed the canonical local gate
with 737 tests, including API; official checks remain blocked by B-08.

M1E-03 has a local synthetic policy test double in the current continuation.
It compares fixed-cycle, reorder-point and profile-aware rules over 28 days,
using a shared seeded demand stream for each replication and lead-time
sensitivity case. It reports stock/service/order and abstract cost metrics
without ranking the policies. The detailed [walkthrough](M1_RETAIL_POLICY_SIMULATION.md)
and [change request](changes/M1E_03_SYNTHETIC_POLICY_TEST_DOUBLE.md) mark
this slice partial: no forecast is consumed, no actual WorldKernel result is
present, and M1E-02 still depends on B-04.

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
The local policy test double addresses only the conditional policy-arithmetic
portion. It does not join authorized evidence, forecast evaluation, actual
engine output or the decision-result contract into an end-to-end user story.

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

## Reusable offline baseline experiment (MM-M1c still open)

The [staged rolling evaluator](M1_STAGED_ROLLING_BASELINES.md)
now composes the experimental local CSV
stage with two fixed one-step baselines, per-origin
publication-date filtering, abstention and
aligned MAE/RMSE/bias/WAPE. Its 35-day repeating
sample is [invented](datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md)
and its [model card](model_cards/STAGED_WEEKLY_BASELINES.md)
records 4/7 coverage. This validates an offline
algorithmic slice, **not** the full M1c requirement
for independently approved data, locked empirical
holdout and real predictive quality.

## M5 source review — permission decision still pending

A preliminary [source due-diligence record](datasets/M5_ACCESS_REVIEW.md)
links the original Kaggle competition data/rules
and the Zenodo copy. This review **did not establish**
a verifiable grant allowing the future MirrorMind
use case, so no real M5 data were ingested, copied
into Git or used for benchmark scores. M1b remains
blocked on independently reviewed source rights,
distribution scope, snapshot lineage and data
availability assumptions. A mirror's availability
is not a rights approval; consider another source
if M5 terms cannot be confirmed.

## Minimum-history invariant, independent of model accuracy

The offline staged evaluator now interprets
`min_history_days` as a **minimum number of
recorded pre-holdout event dates**, not as
elapsed age from one old row. See
[negative history regressions](M1_STAGED_ROLLING_BASELINES.md).
Even a complete pre-holdout row count is not
proof that a publisher had released those values
at each forecast origin; the separate as-of
seven-day checks still determine which
individual predictions may be scored.

## Bounded stream entrypoint for a future approved local source

The [local CSV staging module](M1_LOCAL_CSV_STAGING.md)
now accepts a caller-opened binary stream
via `read_staged_csv` and reads no more than
1 MiB+1 bytes before strict parsing. This is
a useful resource boundary for a **future**
source-specific adapter and reduces the risk
of reading an entire oversized file first.
It still does not open, authenticate, approve,
retain or govern real datasets. M1b permission
and availability verification remain open.

## An officially licensed alternate candidate — no data collected yet

The [UCI Online Retail source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
identifies an official 541,909-transaction UK retail
dataset with a CC BY 4.0 license statement at
the original UCI source (ID 352). This is
more actionable than M5's currently unresolved
competition-specific grant, but it is **not
a source-adapter acceptance**: attribution,
customer-identifying fields, retention, signed
capture, cancellation/quantity conventions
and the absence of verified original
publication-time vintages all require review.
There are no real source bytes in the repository
and no empirical model scores from this dataset.

## Staged-quality review is not an ingestion approval

The [local evidence staging guide](M1_LOCAL_CSV_STAGING.md)
now includes a source-level aggregate quality
report of observed calendar gaps, declared
publication delays and recorded zeros, with
strict tests and no imputation. This is
additional engineering readiness for a
**future approved-source** adapter, not
verification of publisher rights, snapshots,
actual opening schedules, returns, lost
sales or real historical availability.

## UCI-shaped retail product/day projection — M1b remains open

A bounded, reusable [retail-domain projection](UCI_RETAIL_PROJECTION.md)
now validates invented UCI-shaped transaction
rows, counts cancellation/negative/zero
entries separately and emits sorted
product-day positive invoice-line units,
**without** copying customer or invoice IDs.
It never invents `available_on` from
`InvoiceDate`, and does not open the
original XLSX or establish source approval.
A [fictional fixture card](datasets/SYNTHETIC_UCI_ROWS_CARD.md)
records test-only semantics. Licensed real-data
ingestion, privacy signoff, attribution and
publisher availability remain independent,
unfulfilled acceptance gates.

## Optional local XLSX edge — rights/availability gates remain open

The [bounded UCI-shaped XLSX reader](UCI_WORKBOOK_READER.md)
now accepts a caller-opened, locally selected
stream using an optional `openpyxl` extra,
strict ZIP and SHA-256 checks and an exact
synthetic workbook sheet/header before
using the existing product/day projection.
Its [invented-fixture card](datasets/SYNTHETIC_UCI_XLSX_CARD.md)
records tests without real source files.
The original 541,909-row dataset exceeds
the present 10k-row acceptance budget.
This does **not** complete the M1b real
data-source gate, solve cancellations,
grant source rights, certify customer privacy
or establish historical publication times.
