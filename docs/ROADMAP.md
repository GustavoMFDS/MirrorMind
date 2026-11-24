# Milestones

For the current dependency-ordered implementation queue, see the
[master execution plan](engineering/MASTER_EXECUTION_PLAN.md),
[task backlog](engineering/TASK_BACKLOG.md) and
[milestone acceptance gates](engineering/DEFINITION_OF_DONE.md).
The [dated status baseline](engineering/PROJECT_STATUS.md) distinguishes
verified implementation from planned work; the [blocker register](engineering/BLOCKERS.md)
records external decisions. This roadmap retains milestone scope and
historical development notes, not a second mutable task tracker.

- **MM-M0 — Completed scaffold:** FastAPI, `/health`, `/v1/capabilities`, scenario contract validation, tests, Docker and CI, decision log.
- **MM-M1 — In progress; acceptance remains open:** synthetic evidence/evaluation slices and a local three-policy test double are available in draft branch proposals. Authorized source ingestion, empirical forecasting/uncertainty, actual WorldKernel execution and the integrated human-review workflow remain open.
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

- **MM-M1E-01 — Strict simulation request mapping (branch proposal,
  execution still planned):** MirrorMind now maps one explicit
  `retail.inventory` v0.1 scenario shape to WorldKernel's trusted
  `retail.inventory.demo` `demo-1` exchange contract. It requires declared
  units and separate operator ceilings, and rejects unsupported inputs. This
  is request construction only; no engine was imported or run, so the
  `worldkernel_adapter` capability remains planned. See the
  [mapping walkthrough](engineering/WORLDKERNEL_MAPPING_WALKTHROUGH.md) and
  [M1 plan](engineering/M1_EXECUTION_PLAN.md).

- **MM-M1E-03 — Synthetic policy test double (partial branch proposal):** a
  [local 28-day policy comparison](engineering/M1_RETAIL_POLICY_SIMULATION.md)
  runs fixed-cycle, reorder-point and profile-aware rules on paired seeded
  demand streams, with explicit item/day units, stock, abstract costs and
  lead-time sensitivity. It is not a WorldKernel adapter, forecast,
  recommendation or measured retail result. M1E-02 remains blocked on B-04.

- **MM-M1F-02 — Synthetic decision workflow (partial continuation, 2026-11-24):**
  a bounded local service and API/CLI now join fictional release-aware
  evidence, a repeated lag-7 profile, residual diagnostics, the M1E-03 test
  double and an M1F-01 decision trace. This does not complete M1 or its
  authorized-source, empirical-forecast, actual-engine or human-review gates.
  See the [workflow walkthrough](engineering/M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md).

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

- **MM-M1b bounded reader — experimental local primitive:**
  `read_staged_csv` adds chunked reads and
  fail-closed 1 MiB input enforcement
  before the [existing snapshot parser](engineering/M1_LOCAL_CSV_STAGING.md),
  with tests for partial data, oversize
  streams, incorrect read types, generic
  errors and digest integrity. This avoids
  using an unbounded file read in later
  approved-source adapters but does **not**
  add one, authenticate publishers, license
  M5 or make the Evidence Engine operational.

- **MM-M1b alternative source investigation (review pending):**
  the [official UCI Online Retail 352 dataset](engineering/datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
  publicly lists CC BY 4.0, enabling a stronger
  preliminary license assessment than the
  unresolved M5 competition conditions.
  Attribution, customer-ID minimization, workbook
  conversion, source hash/retention, cancellations
  and the gap between transaction time and real
  publication availability remain explicit
  approval blockers. No UCI data have been
  ingested or used to report model performance.

- **MM-M1b local quality preflight (experimental):**
  `snapshot_quality_summary` adds a deterministic,
  non-imputing aggregate over structurally
  staged records: row/series counts,
  per-series internal date gaps, recorded
  zero-unit observations and declared
  publication delays. [Method notes](engineering/M1_LOCAL_CSV_STAGING.md)
  and negative regressions distinguish
  absent records from measured zeros.
  It **does not** verify source authenticity,
  dataset rights, actual customer demand
  or readiness of a real Evidence Engine.

- **MM-M1b retail-domain UCI-shaped projection (experimental):**
  [source-method guide](engineering/UCI_RETAIL_PROJECTION.md)
  and negative regression tests accompany
  `domains/retail/uci_transactions.py`, which
  aggregates strictly positive fictional
  invoice-line counts by stock code/event
  calendar date, excluding cancelled and
  nonpositive rows with separate counters.
  Extra customer, invoice, description and
  price values are not emitted. The output's
  publication-time status remains **unknown**;
  this is **not** an XLSX reader, licensed
  real-data adapter or independently evaluated
  forecast. M1b authorization/provenance
  and M1c empirical holdout remain open.

- **MM-M1b optional XLSX edge (experimental only):**
  a bounded [local UCI-shaped workbook reader](engineering/UCI_WORKBOOK_READER.md)
  uses optional `openpyxl` in read-only mode
  with compressed-byte, ZIP metadata, exact
  schema, row and group caps. Fictional
  [workbook tests](../tests/unit/test_uci_workbook.py)
  cover path-independent byte reads, SHA-256
  matching, malicious ZIP metadata, unsupported
  sheets and immutable product/day projections.
  **Not delivered:** authorized source acquisition,
  full 541,909-row UCI processing, customer
  privacy clearance, deduplicated sales/returns,
  verified historical availability or actual
  empirical forecast scores.

- **MM-M1b positive-line event-day coverage (experimental):**
  [retail coverage review](engineering/RETAIL_COVERAGE.md) and
  synthetic [regressions](../tests/unit/test_retail_coverage.py)
  aggregate missing **internal** product-days between recorded positive
  transaction days without filling zeros, exposing customer/product
  identifiers in summary receipts, or inventing a publisher release date.
  It is not an authorized observation calendar, true demand history,
  source-provenanced as-of evidence, evaluated forecast or WorldKernel
  execution. Real M1b and M1c acceptance gates remain open.

- **MM-M1b hypothetical calendar comparison (experimental):**
  [declared operational calendar guide](engineering/DECLARED_CALENDAR_COVERAGE.md)
  and [fictional regressions](../tests/unit/test_declared_calendar_coverage.py)
  distinguish internal positive-line calendar gaps from days a caller
  explicitly declared as possible observation dates. Contradictory
  observed sales are rejected. No inferred shop opening days, real
  publisher vintage, true demand or operational readiness is asserted.

- **MM-M1b declared product-day release cutoffs (experimental):**
  [retail release audit](engineering/DECLARED_RETAIL_RELEASES.md) and
  [negative regressions](../tests/unit/test_declared_retail_releases.py)
  require a separate caller-asserted release day for every fictional
  positive product/day record. The as-of audit excludes future or
  declared-unpublished events without inventing publication timestamps.
  The release declarations are **not authenticated**; no authorized
  source, empirical model score or operational evidence integration exists.

- **MM-M1c retail declared-release baseline evaluation (experimental):**
  [release-aware offline guide](engineering/RETAIL_RELEASE_BACKTEST.md)
  and [fictional unit regressions](../tests/unit/test_retail_release_backtest.py)
  compare two fixed daily baselines on matched eligible one-day origins;
  absent positive-line dates and unpublished history cause abstention,
  never zero imputation or lookahead. Release dates and positive-line sales
  remain unverified proxies, not authorized real-demand evidence, empirical
  forecasts, calibrated intervals, API serving or WorldKernel execution.

- **MM-M1c retail evidence-to-evaluation composition (experimental):**
  [M1 evaluation guide](engineering/M1_RETAIL_SYNTHETIC_EVALUATION.md)
  and [generated fixture card](engineering/datasets/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md)
  connect the reviewed local workbook flow to the fixed release-aware
  baselines, preserve matched-origin abstentions and emit aggregate/per-origin
  receipts. The CLI uses deterministic fictional bytes; no real-source
  availability, demand completeness, empirical performance or calibrated
  uncertainty is established.

- **MM-M1c retail matched-origin coverage gate (experimental):**
  [coverage threshold review](engineering/RETAIL_COVERAGE_GATE.md) and
  [fictional regressions](../tests/unit/test_retail_coverage_gate.py)
  suppress conditional model ranking under a caller-defined minimum
  matched-origin fraction (80% default, two origins minimum), report
  exact abstention causes and never invent confidence or prediction
  intervals. This is **not** statistical calibration or empirical
  performance validation, and declared release data remain unverified.

- **MM-M1c prequential residual-envelope diagnostic (experimental):**
  [method and limitations](engineering/RETAIL_RESIDUAL_ENVELOPE.md)
  with [fictional negative controls](../tests/unit/test_retail_residual_envelope.py)
  compute retrospective coverage of maximum-absolute-error heuristic
  envelopes using only calibration outcomes declared published at each
  past origin. Missing history, target or calibration causes abstention.
  There is **no calibrated interval or nominal coverage guarantee**;
  release declarations remain unverified and empirical forecasting is open.

- **MM-M1c eligibility drift audit across adjacent fictional windows:**
  [method guide](engineering/RETAIL_ELIGIBILITY_DRIFT.md) and
  [negative tests](../tests/unit/test_retail_eligibility_drift.py)
  compare aggregate evaluated-origin denominators at each window's
  **own** cutoff. No late-release hindsight, real target distribution
  shift inference, selection bias correction, calibrated intervals or
  authorized ingestion is asserted.

- **MM-M1c eligible-value comparison (experimental):**
  [conditional value review](engineering/RETAIL_ELIGIBLE_VALUES.md)
  and [fictional regressions](../tests/unit/test_retail_eligible_values.py)
  compare positive-line mean/median on two separately cutoff-eligible
  adjacent windows only if both pass independently declared coverage
  gates. Missing or unpublished targets remain excluded, without zero
  imputation. Changes in selected proxies **do not identify a genuine
  demand distribution shift or correct selection bias**.

- **MM-M1c excluded-target counterfactual sensitivity (experimental):**
  [scenario method](engineering/RETAIL_SELECTION_SENSITIVITY.md)
  and [fictional regressions](../tests/unit/test_retail_selection_sensitivity.py)
  show how two-window proxy means and their difference may vary if
  excluded targets hypothetically lie between zero and a caller-supplied
  ceiling. Neither unknown targets nor missing dates are imputed.
  Scenario bounds are **not data-driven bounds**, statistically validated
  demand, selection-bias corrections, or a real distribution-shift claim.

- **MM-OPS-A1 — Temporary quality gate during GitHub Actions quota exhaustion:**
  [local execution guide](engineering/LOCAL_QUALITY_GATE.md) and
  [regressions](../tests/unit/test_local_quality_gate.py) bind a six-check
  local run to an exact clean Git commit. A passing local receipt **does
  not claim that GitHub Actions executed or passed**. Restore official
  CI once the quota is renewed, and retain explicit reviewer judgment.

- **MM-M1c bounded excluded-target scenario sweep (experimental):**
  [method](engineering/RETAIL_SENSITIVITY_SWEEP.md) and
  [synthetic regressions](../tests/unit/test_retail_sensitivity_sweep.py)
  compare 2–8 strictly increasing hypothetical exclusion bounds using
  the original as-of diagnostic. These are mathematical scenarios, not
  authenticated demand bounds or a distribution-shift inference.

- **MM-M1c sweep disclosure gate:** by default, scenario means are suppressed
  unless both independently cutoff-evaluated windows have at least three
  eligible dates and exact eligible-date coverage of 80% or more. A lower
  threshold requires an explicit synthetic-research override; it is **not**
  unbiased population inference or statistical disclosure control.
  [Guide](engineering/RETAIL_SENSITIVITY_SWEEP.md) and
  [gate regressions](../tests/unit/test_retail_sensitivity_sweep.py).

- **MM-M1c sweep efficiency (experimental):** the [bounded sensitivity
  sweep](engineering/RETAIL_SENSITIVITY_SWEEP.md) reuses two as-of eligible
  window summaries for all 2–8 hypothetical ceilings. Equality against
  individual scenarios and the two-audit call invariant are tested without
  claiming measured runtime acceleration, actual demand rights or drift.

- **Historical MM-M1c residual-evaluator work deduplication (superseded):**
  [prequential envelope method](engineering/RETAIL_RESIDUAL_ENVELOPE.md)
  recorded call-local caching of each target-date seasonal-naive prediction
  in that historical implementation. An invented 7-day holdout and 21-day
  calibration exercise verifies 28 prediction calculations rather than
  154 repeated forecast calls, without claiming wall-clock benchmarking,
  forecast calibration, source rights, or actual demand inference.

- **Historical MM-M1c adversarial cache parity (superseded):**
  [retail residual method](engineering/RETAIL_RESIDUAL_ENVELOPE.md)
  recorded cached and explicitly uncached execution in 18 deterministic
  histories with changing release delays, missing observations and distinct
  cutoff/calibration settings. The exact no-cache vs cached example confirms
  154 vs 28 baseline prediction calls and identical receipts. These receipts
  concern superseded code; they are a structural regression claim, not a
  measured latency or statistical claim for the current fixed split.

- **Historical MM-M1c release-aware rolling residuals (superseded):**
  [prequential calibration guide](engineering/RETAIL_RESIDUAL_ENVELOPE.md)
  described a bounded incremental activation/expiration algorithm for
  retrospective residual candidates. M1D-01 supersedes the rolling
  target-label policy with a fixed pre-holdout calibration interval. The
  historical tests do not establish source authority, forecast validity,
  calibrated coverage or wall-clock speedup.

- **MM-M1d disjoint uncertainty holdout (experimental, draft PR #56):**
  [uncertainty walkthrough](engineering/RETAIL_RESIDUAL_ENVELOPE.md) and
  [scoped M1D-01 change request](engineering/changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md)
  define a fixed pre-holdout calibration target interval, origin-specific
  publication eligibility and holdout-label disjointness. Synthetic tests
  compare the report with a separate quadratic oracle and verify late-data
  abstention. No publisher authenticity, empirical calibration, nominal
  coverage or future-performance guarantee is claimed.

- **Historical MM-M1c performance characterization (measurement only):**
  [two-revision synthetic benchmark](engineering/RETAIL_RESIDUAL_BENCHMARK.md)
  records the same fictional residual workload before and after incremental
  calibration for the exact PR #34/#35 revisions. It checked entire report
  hashes, measured median local elapsed time and peak traced Python
  allocations, and reported full-run limitations. These observations are
  **not** current-algorithm measurements, CI quality gates, actual
  demand/forecast evidence, whole-process memory measurements or guaranteed
  speedups.

- **MM-M1b review packet (experimental, still not licensed ingestion):**
  [source-intake metadata binder](engineering/SOURCE_INTAKE_REVIEW.md)
  joins an existing staged CSV/UCI-shaped XLSX digest to declared
  source/license/rights/privacy references, requested use, captured date
  and retention. Mismatches fail; receipts are identifier-minimized and
  **always refuse ingestion and forecasting**, regardless of claimed evidence.
  Human review of original rights, verified vintages and privacy policy
  remains mandatory before a separate real-source adapter is proposed.

- **MM-M1b signed review history (experimental, not an approval service):**
  [offline Ed25519 review verification](engineering/SIGNED_SOURCE_REVIEW.md)
  binds reviewer attestations to a specific declared manifest, usage scope,
  expiring approval, denial and permanent same-packet revocation; checks
  a chained log against an externally supplied expected head. Validating
  a signature never sets ingestion/forecast eligibility to true. Trusted
  reviewer keys, independently fresh append-only registry, human rights
  review, privacy, retention enforcement and lawful source acquisition
  remain **unimplemented**; real M1b ingestion stays blocked.

- **MM-M1b in-process review revision coordination (experimental only):**
  [local signed-review registry](engineering/LOCAL_REVIEW_REGISTRY.md)
  implements a bounded per-packet sequence and head with locked
  compare-and-swap updates, signed-event validation, immutable sanitized
  snapshots and terminal revocation for the **current process**. The
  [change request](engineering/changes/M1B_LOCAL_REVIEW_REGISTRY.md)
  identifies unimplemented independent trusted key/head provisioning,
  durability, restart/cross-worker anti-rollback, human permission review
  and ingestion enforcement. A local signed approval never permits
  dataset use or forecasting.

- **MM-M1b local SQLite signed decision storage (experimental):**
  [transactional review registry](engineering/SQLITE_REVIEW_REGISTRY.md)
  persists verified synthetic review records through restarts with
  SQLite `BEGIN IMMEDIATE` compare-and-swap, rollback tests and two
  independent interpreter writers. A coherent older database can
  **still be restored undetected** without an independently trusted
  current log head. This is neither a permission service nor lawful
  real-data ingestion; key/role authority, trusted fresh head,
  privacy/licensing review and ingestion controls remain blocked.

- **MM-M1b signed review-head witness format (experimental only):**
  [head-checkpoint verification](engineering/SIGNED_HEAD_CHECKPOINTS.md)
  binds a domain-separated signer attestation, bounded expiry and caller-
  supplied monotonic sequence minimum to one validated SQLite review head.
  An older signed checkpoint and matching old database remain acceptable
  if the externally supplied minimum is stale; no independent signer,
  monotonic authority, trusted clock, publisher rights, human legal review
  or operational M5/UCI ingestion has been implemented.

- **MM-M1b witnessed authority transcript contract (experimental only):**
  [offline checkpoint succession verifier](engineering/AUTHORITY_TRANSCRIPT.md)
  checks contiguous signed witness receipts and dual-signed key handoffs,
  missing history after outages, final SQLite head match and exact
  caller-provided start/end fences. It cannot independently obtain
  current fences or discover a concealed conflicting fork; no live
  authority, protected key custody, real reviewer identity, lawful
  source rights or M5/UCI ingestion has been added.

- **MM-M1b local operator-signed checkpoint publisher (experimental only):**
  [SQLite publication journal](engineering/LOCAL_CHECKPOINT_PUBLISHER.md)
  validates separately configured checkpoint, witness and operator
  public keys, retains signed metadata across restarts, and uses
  a per-database transactional compare-and-swap. A deliberately
  demonstrated old signed backup remains locally valid without an
  independent newer head. No live external authority, authenticated
  operator enrollment/role administration, key custody, cross-host
  non-equivocation, legal source approval or real ingestion is delivered.

- **MM-M1b dual-admin operator-key policy (experimental only):**
  [local operator governance registry](engineering/OPERATOR_GOVERNANCE.md)
  stores signed enrollment, expiration, revocation and fresh-key replacement
  under two configured admin public keys, with SQLite CAS and restart
  verification. It remains deliberately **unconnected** to the existing
  checkpoint publisher: cross-file policy reads/publication writes are
  not atomic. Identity and custody of admin private keys, independent
  current head, real key compromise recovery, source rights/retention
  and live publisher enforcement remain unimplemented.

- **MM-M1b atomic local policy-gated checkpoint publication (experimental):**
  [single-DB policy+publisher gate](engineering/ATOMIC_GOVERNED_PUBLISHER.md)
  composes signed dual-admin policy and signed checkpoint publication in
  one new SQLite file, using `BEGIN IMMEDIATE` to order revocation
  versus publication and reject stale or revoked operators. The former
  standalone static-key publisher refuses that marked file; previous
  standalone databases are not migrated. This does **not** fix
  coherent combined-DB rollback, global latest-head trust, real operator
  identity/credentials, licensed data access or ingestion permissions.

- **MM-M1b policy-bound operator publication signatures (experimental):**
  [local signing protocol v2](engineering/ATOMIC_GOVERNED_PUBLISHER.md)
  now binds the operator's Ed25519 signature to the exact dual-admin
  policy revision and hash, in addition to the existing publication
  predecessor and witnessed receipt. Stale signatures are rejected
  after any policy change, while preexisting v1 history can still be
  reverified and standalone v1 publication remains independent.
  [Scope and negative tests](engineering/changes/M1B_POLICY_BOUND_PUBLICATION.md)
  do not establish trusted external freshness, real key ownership,
  cross-host authority, legal source rights or live ingestion.

- **MM-M1b offline signed integrated-head fence (experimental only):**
  [signed-state verifier](engineering/INTEGRATED_HEAD_FENCE.md) can
  compare a supplied Ed25519-signed **combined** operator-policy and
  publication head against one consistent local SQLite read, with
  caller-pinned exact authority sequence and signed digest. An older
  coherent backup fails against a genuinely newer externally supplied
  fence; the same backup plus stale external pins still passes.
  No independently operated authority, trusted current-fence retrieval,
  key custody, cross-host consensus, licensed data use, admission
  tokens, real ingestion or empirical forecasts were delivered.

- **MM-M1b supplied dual-witness integrated-fence continuity (experimental):**
  The [offline signed transition verifier](engineering/INTEGRATED_FENCE_TRANSCRIPT.md)
  checks exact successor hashes/sequences and two independently configured
  witness signatures per combined policy+publication fence, and can
  classify *two supplied* signed conflicting successors without selecting
  a trusted branch. This extends but does not replace the
  [single-fence equality check](engineering/INTEGRATED_HEAD_FENCE.md).
  Neither trusted external latest-head retrieval nor actual key custody,
  fork discovery, independent timestamp authority, real source permission,
  live publication admission or forecasting is implemented.

- **MM-M1b separate durable signed-fence pin (experimental):**
  [local separate-file registry](engineering/LOCAL_INTEGRATED_FENCE_REGISTRY.md)
  persists complete dual-witness signed combined-head transitions with
  registry-local transactional CAS, full replay and read-only comparison
  to the governed SQLite publisher. A coherent publisher-only old-backup
  restore mismatches a more recent intact separate registry; restoring
  both databases or removing a valid signed suffix is not ruled out.
  **No** independently operated remote current-head authority, key
  custody, two-file atomic transaction, live admission, licensed real
  ingestion or production forecasting was introduced.

- **MM-M1b challenged HTTPS current-head read (experimental):**
  The [read-only remote-head client](engineering/REMOTE_FENCE_HEAD_CLIENT.md)
  can request a current sequence/digest using a per-request random nonce,
  verify a separate service Ed25519 signature with short UTC validity,
  and compare to the [local separately signed registry](engineering/LOCAL_INTEGRATED_FENCE_REGISTRY.md).
  A *genuinely independent honest signer* that reports a newer head could
  detect compatible rollback of both local SQLite files. No real service,
  independent custody, server endpoint, signer deployment, real-source
  ingestion or forecasts were implemented or contacted. A malicious
  remote signer can freshly attest an old head and still pass.
