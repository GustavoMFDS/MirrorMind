# Milestones

- **MM-M0 — Completed scaffold:** FastAPI, `/health`, `/v1/capabilities`, scenario contract validation, tests, Docker and CI, decision log.
- **MM-M1 — Planned retail fundamentals:** ingest permitted M5 subset, validate cutoff, backtest two demand models, run first inventory simulation through gateway.
- **MM-M2 — Planned AI application:** evidence/RAG, agent tool workflow, traceable scenario analysis, UI and human review.
- **MM-M3 — Planned engineering:** durable async jobs, token/call and compute budgets enforced, tracing, RBAC, tenant separation, failure recovery and load tests.
- **MM-M4 — Planned generalization:** at least one *different* domain adapter, versioned contracts and validated WorldKernel integration.

Acceptance gates: working runnable example, tests, clear metrics, provenance, resource limits and a truthful status statement. No production claims until validated.

- **MM-DOC-A1 — Completed (documentation and Python CI validated):** enforce a committed
  AST index, human-reviewed linked repository atlas, real tracked-file inventory
  and local Markdown link integrity in documentation CI. This is strictly
  structural; it does not certify semantic understanding, data lineage,
  privacy, quality of forecasts or security. Next gates: source-reviewed
  method lessons, curated test evidence and stricter claim/decision traceability.

- **MM-DOC-A2 — In progress (semantic and evidence teaching):** source-reviewed
  [ScenarioSpec walkthrough](engineering/CONTRACT_WALKTHROUGH.md),
  [API walkthrough](engineering/API_WALKTHROUGH.md) and 11-module
  [semantic map](engineering/SEMANTIC_COVERAGE.md). A curated
  [claim-to-test index](engineering/EVIDENCE_MAP.json) records precise
  pytest function references and limitations; CI checks structural
  integrity only, not reasoning validity or product readiness.

- **MM-DOC-A3 — Capability truth guard (CI validation required):**
  maintain a reviewed [capability ledger](engineering/CAPABILITY_LEDGER.json)
  with strict implemented/experimental/interface-only/planned statuses,
  source/test evidence and explicit caveats. A structural checker and
  live API regression must catch claims that diverge from the actual
  `GET /v1/capabilities` response. This protects against overclaiming,
  but does not certify the implementation, scientific validity or security.

- **MM-M1a — Experimental groundwork (not the M1 acceptance gate):**
  standalone, bounded [synthetic daily-observation preflight](engineering/M1_DATA_PREFLIGHT.md)
  with canonical dates, future-cutoff rejection, duplicate and
  missing-day diagnosis, safe CLI errors and regression tests.
  No source license/provenance verification, real-data connector,
  temporal backtest, demand forecast, AI agent or WorldKernel
  integration. `GET /v1/capabilities` labels the example
  **experimental**; all real evidence/forecast functionality stays
  planned until independently validated.

- **MM-DOC-A4 — Research-quality review protocol (documentation-only):**
  checked-in [dataset cards](engineering/DATASET_CARD_TEMPLATE.md)
  for rights, snapshots and availability-time cutoffs; a
  [forecast model evaluation template](engineering/FORECAST_MODEL_CARD_TEMPLATE.md)
  with rolling temporal holdouts, baselines and calibration;
  a [decision trace](engineering/DECISION_TRACE_TEMPLATE.md)
  separating sources, model estimates, conditional simulations
  and human review; plus a
  [WorldKernel gateway acceptance gate](engineering/WORLDKERNEL_GATEWAY_GATE.md).
  See the [M1 delivery plan](engineering/M1_EXECUTION_PLAN.md).
  These documents are design and future-review gates, **not**
  implemented evidence, forecasting, integration or agents.

- **MM-M1c-exp — Synthetic one-step baseline experiment (not full MM-M1c):**
  reviewed [rolling-origin benchmark](engineering/M1_TEMPORAL_BACKTEST.md)
  with predeclared lag-7 seasonal naive and trailing-mean
  heuristics, a 35-day invented weekly fixture, deterministic
  MAE/RMSE/bias/WAPE, no-lookahead prefix regressions and
  zero-denominator abstention. Synthetic [dataset](engineering/datasets/SYNTHETIC_WEEKLY_CARD.md)
  and [model](engineering/model_cards/SYNTHETIC_WEEKLY_BASELINES.md)
  cards record evaluation boundaries. **Real authorized data,
  availability-time controls, untouched empirical holdout,
  validated forecast accuracy and deployable inference remain planned.**

- **MM-M1b-exp — Synthetic as-of availability preflight
  (not authorized ingestion):** a local
  [two-timestamp teaching exercise](engineering/M1_AVAILABILITY_PRECHECK.md)
  separates observed date from declared publication date,
  excludes late releases and future events at a fixed
  retrospective cutoff and reports eligible synthetic
  counts without imputation. Regressions cover unexpected
  publication order, withheld-value independence,
  missing/duplicate records and bounded generic CLI
  errors. This **does not** implement real M5 ingestion,
  authenticate source timestamps or establish data rights.

- **MM-M1b/M1c bridge — Synthetic as-of rolling assessment
  (still experimental):** source-reviewed
  [joint availability-aware evaluation](engineering/M1_ASOF_ROLLING_EVALUATION.md)
  reuses two simple historical baselines but refuses
  to score past origins that lacked a complete
  **published** seven-day history. A generated delayed
  publication causes three abstentions, leaving
  four matched synthetic origins for MAE/RMSE/WAPE.
  [Dataset](engineering/datasets/SYNTHETIC_ASOF_WEEKLY_CARD.md)
  and [model](engineering/model_cards/SYNTHETIC_ASOF_WEEKLY_BASELINES.md)
  cards record the 4/7 coverage and statistical
  limits. This does **not** complete real M1b ingestion,
  independent M1c model evaluation, production forecasting,
  decision support or WorldKernel integration.

- **MM-M1b-local — source-backed structural staging (experimental, not
  licensed data ingestion):** a real, reusable
  [in-memory CSV parser](engineering/M1_LOCAL_CSV_STAGING.md)
  now enforces 1 MiB/10k-row limits, exact header and
  integer/date validation, per-series uniqueness, a
  declared SHA-256 digest comparison and historical
  two-timestamp as-of selection. Unit and fixture
  integration regressions accompany its
  [reviewed data card](engineering/datasets/LOCAL_CSV_STAGING_FIXTURE.md).
  Its result explicitly states `not_authorized`:
  no provenance attestation, source license, real connector,
  retention policy, forecast model or WorldKernel execution
  has been delivered. **M1b remains open.**

- **MM-M1c-local — staged offline baselines (experimental, real
  forecasting still planned):** reusable source-level
  [one-step rolling evaluator](engineering/M1_STAGED_ROLLING_BASELINES.md)
  now consumes strict in-memory source-unverified CSV
  observations, applies per-origin publication cutoffs,
  abstains on incomplete seven-day history and compares
  fixed seasonal-naive versus trailing-mean baselines
  on **identical** eligible targets. A deliberately
  [invented data card](engineering/datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md)
  and [model card](engineering/model_cards/STAGED_WEEKLY_BASELINES.md)
  record 4/7 origins scored and clear provenance limits.
  No authorized M5 ingestion, untouched empirical model
  benchmark, calibrated uncertainty, production serving
  or WorldKernel integration has been delivered.

- **MM-M1b source-rights decision — blocked on permission evidence:**
  a [preliminary M5 access review](engineering/datasets/M5_ACCESS_REVIEW.md)
  records candidate official Kaggle competition
  pages and the Zenodo mirror but **does not establish
  an approved grant** for a future research/commercial
  MirrorMind data pipeline. No real files downloaded,
  bundled or used for claimed empirical forecasts.
  Next gate is independent human confirmation of
  source rights and original data publication metadata
  (or selection of a clearly licensed alternate source).
  Local structural validation and synthetic evaluation
  may continue without real source access.

- **MM-M1c audit improvement — origin-level diagnostics (experimental):**
  the [offline staged baseline evaluator](engineering/M1_STAGED_ROLLING_BASELINES.md)
  now records one deterministic status per requested
  target date, preserving the previous aggregate counters
  and distinguishing missing targets from late-published
  ones. [Focused regressions](../tests/unit/test_staged_rolling_baselines.py)
  verify a seven-origin accounting and null metrics
  on complete abstention. This is local review metadata,
  not durable audit storage or authenticated evidence;
  real data rights and model validity remain open.

- **MM-M1c negative precondition fix:** the
  [offline baseline evaluator](engineering/M1_STAGED_ROLLING_BASELINES.md)
  now requires the configured number of
  **recorded pre-holdout observations**, rather
  than relying on a single ancient event date.
  Sparse-history and earliest-calendar regressions
  cover fail-closed behavior. Historical
  source permissions and genuine predictive
  validation remain outstanding.
