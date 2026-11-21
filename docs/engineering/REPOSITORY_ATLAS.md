# MirrorMind repository atlas — reviewed source, evidence and operational surfaces

**Goal:** find every tracked component and understand its role, caller, test and
trust boundary. This atlas is human-reviewed; its linked **file inventory**
is checked by `scripts/docs/coverage.py`. It is not automatic behavioral
documentation, a dependency graph or proof of correctness.

Read [AGENTS](../../AGENTS.md), [architecture](../ARCHITECTURE.md),
[system map](SYSTEM_MAP.md), [change template](CHANGE_REQUEST_TEMPLATE.md),
and the [generated AST catalog](generated/SYMBOLS.md) before modifying code.

## 1. Runtime source — modules, symbols, consumers

| Source | What it does / where to inspect next |
| --- | --- |
| [`src/mirrormind/__init__.py`](../../src/mirrormind/__init__.py) | Package boundary; no automatic agent or engine execution |
| [`src/mirrormind/api/__init__.py`](../../src/mirrormind/api/__init__.py) | Stable `mirrormind.api:app` export |
| [`src/mirrormind/api/app.py`](../../src/mirrormind/api/app.py) | FastAPI composition; routes remain thin |
| [`src/mirrormind/api/routes/__init__.py`](../../src/mirrormind/api/routes/__init__.py) | Route package |
| [`src/mirrormind/api/routes/system.py`](../../src/mirrormind/api/routes/system.py) | `/health` and truthful `/v1/capabilities` declarations |
| [`src/mirrormind/api/routes/scenarios.py`](../../src/mirrormind/api/routes/scenarios.py) | `POST /v1/scenarios/validate`: Pydantic validation **only**, no simulation |
| [`src/mirrormind/core/__init__.py`](../../src/mirrormind/core/__init__.py) | Shared contracts package |
| [`src/mirrormind/core/contracts.py`](../../src/mirrormind/core/contracts.py) | `EvidenceRef`, `ForecastRef`, `Intervention`, `ExecutionBudget`, `ScenarioSpec` and cross-field budget/horizon validation |
| [`src/mirrormind/modules/__init__.py`](../../src/mirrormind/modules/__init__.py) | Capability modules package |
| [`src/mirrormind/modules/simulation/__init__.py`](../../src/mirrormind/modules/simulation/__init__.py) | Simulation capability boundary |
| [`src/mirrormind/modules/simulation/gateway.py`](../../src/mirrormind/modules/simulation/gateway.py) | `SimulationGateway` Protocol and `SimulationSummary` **interface**, no WorldKernel adapter |

### Follow a real request

```text
POST /v1/scenarios/validate
  -> mirrormind.api:app
  -> api/routes/scenarios.py:validate_scenario
  -> core/contracts.py:ScenarioSpec Pydantic validation
  -> response {status: "validated_not_executed", ...}
```

No forecast, retrieval, AI reasoning or WorldKernel call occurs.
`EvidenceRef` and `ForecastRef` currently validate **references supplied
by callers**. They do not resolve evidence, prove source permissions
or verify prediction quality. `ExecutionBudget` limits request fields,
**not** real runtime CPU, tokens, cost, memory or execution admission.

## 2. Tests and concrete evidence

| Test | Scope and limitation |
| --- | --- |
| [`tests/unit/test_contracts.py`](../../tests/unit/test_contracts.py) | Basic versioned input model and cross-field budget/forecast horizon rejections; no external data verification |
| [`tests/integration/test_api.py`](../../tests/integration/test_api.py) | FastAPI response and validation, including honest planned capability list; not an end-to-end decision engine |
| [`tests/unit/test_docs_coverage.py`](../../tests/unit/test_docs_coverage.py) | Link/atlas guard regressions; structural integrity, not semantic evidence |

As features are implemented, add **independent tests** before
labeling their capabilities as implemented. A passing catalog CI is
never evidence that statistical forecasts or RAG grounding work.

## 3. Examples, config and operational surfaces

| Path | Purpose |
| --- | --- |
| [`examples/retail-scenario.json`](../../examples/retail-scenario.json) | Example `ScenarioSpec` request; does not execute or verify stock observations |
| [`pyproject.toml`](../../pyproject.toml) | Python dependencies and unit/lint configuration |
| [`.env.example`](../../.env.example) | Example environment variables; never store live tokens |
| [`.gitignore`](../../.gitignore) | Local and sensitive artifact exclusions |
| [`Dockerfile`](../../Dockerfile) | Initial API image, not a separate simulation worker |
| [`compose.yml`](../../compose.yml) | Local scaffold process composition; not a production cluster |
| [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) | API unit/integration tests and Ruff |
| [`.github/workflows/docs.yml`](../../.github/workflows/docs.yml) | Source catalog, full atlas/link check; workflow success is not accuracy proof |
| [`scripts/docs/catalog.py`](../../scripts/docs/catalog.py) | Deterministic AST symbol index write/check |
| [`scripts/docs/coverage.py`](../../scripts/docs/coverage.py) | Fails when a tracked file lacks a **resolving Markdown link** here, or docs have broken local links |

## 4. Canonical, reviewed documents

| Document | Responsibility |
| --- | --- |
| [`README.md`](../../README.md) | Project identity, runnable current scaffold and truthful claims |
| [`AGENTS.md`](../../AGENTS.md) | Mandatory contributions, threat/truth guardrails and evidence rules |
| [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md) | Modules, boundaries and proposed design versus implementation |
| [`docs/CONTRACTS.md`](../CONTRACTS.md) | Current versioned input, gateway and budget validation scope |
| [`docs/DECISIONS.md`](../DECISIONS.md) | Accepted/proposed/deferred decisions; not completion certificates |
| [`docs/RETAIL_MVP.md`](../RETAIL_MVP.md) | First reference domain, temporal testing and synthetic-assumption obligations |
| [`docs/ROADMAP.md`](../ROADMAP.md) | Completed/planned milestones and acceptance gates |
| [`docs/SECURITY.md`](../SECURITY.md) | Authorization, privacy, safe tool use and deliberate lack of production guarantees |
| [`docs/STRUCTURE.md`](../STRUCTURE.md) | Modular monolith boundaries and folder policy |
| [`docs/engineering/README.md`](README.md) | Hub for future development and independent study |
| [`docs/engineering/SYSTEM_MAP.md`](SYSTEM_MAP.md) | Actual runtime path and change-location guide |
| [`docs/engineering/LEARNING.md`](LEARNING.md) | Exercises to independently explain contracts and changes |
| [`docs/engineering/DEBUGGING.md`](DEBUGGING.md) | Evidence-first safe reproduction and failure diagnosis |
| [`docs/engineering/CHANGE_REQUEST_TEMPLATE.md`](CHANGE_REQUEST_TEMPLATE.md) | Pre-change scope, acceptance and implementation evidence |
| [`docs/engineering/REPOSITORY_ATLAS.md`](REPOSITORY_ATLAS.md) | This reviewed inventory; all tracked code/config/docs/test files must be linked |
| [`docs/engineering/generated/SYMBOLS.md`](generated/SYMBOLS.md) | Generated declarations/imports; never hand-edit |

## 5. Evidence hierarchy and future additions

| Evidence | What it can support | What it cannot support |
| --- | --- | --- |
| AST index | Symbol/path/signature existence | Behavior, runtime calls, security |
| Linked atlas | Tracked file navigation and link validity | Completeness of explanations |
| Unit/integration test result | Observed behavior under a named environment | Generalization outside tested conditions |
| Actual source review | Intended code paths and important edge cases | Mathematical or security validation alone |
| Forecast backtest | Measured performance for an explicitly held-out period | Future accuracy guarantee or causal effect |
| Authorized evidence snapshot | Provenance and scope **once real ingestion exists** | Universal truth or unrestricted reuse |
| Simulation | Output conditional on model assumptions | An observation, causal proof or prediction without evaluation |

**Future source files must be added to this atlas** in the same PR.
When adding evidence, forecasting, tool-using agents or the optional
WorldKernel adapter, record where authorization occurs, where data
and results originate, the cutoff used, validation limitations,
the exact tests, and safe failure/rollback behavior.

The **current** first practical exercise is to follow
`api/routes/scenarios.py:validate_scenario` to
`core/contracts.py:ScenarioSpec.check_budget`, then inspect
`tests/unit/test_contracts.py::test_exceeding_budget_rejected` and
`tests/integration/test_api.py::test_scenario_validation_only`.
Predict which invalid inputs return HTTP 422. Then explain
why a validation response is **not** a completed decision.

## 6. Reproduce structural checks

```bash
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python -m pytest -q tests/unit/test_docs_coverage.py
python -m pytest -q
python -m ruff check src tests
```

The atlas guard verifies existence and navigability, not runtime
tests or semantic completeness. The Python API CI runs tests separately.


## 7. Reviewed semantic lessons and curated evidence integrity

The initial learning guides are **source-reviewed explanations of what
exists today**, not descriptions of hypothetical deployed AI systems:

| File | Purpose and limits |
| --- | --- |
| [`docs/engineering/CONTRACT_WALKTHROUGH.md`](CONTRACT_WALKTHROUGH.md) | Pydantic version 0.1 field and cross-field rules, unverified evidence/forecast references, independent exercises |
| [`docs/engineering/API_WALKTHROUGH.md`](API_WALKTHROUGH.md) | Real FastAPI route handlers, expected statuses, declared capabilities and interface-only simulation gateway |
| [`docs/engineering/SEMANTIC_COVERAGE.md`](SEMANTIC_COVERAGE.md) | Qualitative current-module guide versus interface/index-only status, explicit planned feature gaps |
| [`docs/engineering/EVIDENCE_MAP.json`](EVIDENCE_MAP.json) | Curated claim identifiers linking guides and real test function declarations with **limitations**, not semantic proof |
| [`scripts/docs/evidence.py`](../../scripts/docs/evidence.py) | Verify claim IDs, guide/test path existence, cited paths and actual top-level pytest declarations |
| [`tests/unit/test_docs_evidence.py`](../../tests/unit/test_docs_evidence.py) | Regression tests for missing/broken evidence and deliberate negative cases |

```bash
python scripts/docs/evidence.py --check
```

A passing guard means references **exist**. It does not
run tests, inspect assertions, validate scientific reasoning,
prove consent/retention or certify AI decisions. Each
functional PR still requires an independently reviewed,
actually executed regression and truthful status.

## 8. Capability-claim integrity and the API-facing truth boundary

| File | What it enforces |
| --- | --- |
| [`docs/engineering/CAPABILITY_LEDGER.json`](CAPABILITY_LEDGER.json) | Reviewed statuses `implemented`, `interface_only`, `planned`, `experimental`, `deferred` with source/test pointers and caveats |
| [`docs/engineering/CAPABILITY_GATES.md`](CAPABILITY_GATES.md) | When a capability may legitimately be promoted, including provenance, trust, budgets and empirical evidence |
| [`scripts/docs/capabilities.py`](../../scripts/docs/capabilities.py) | Schema/status, duplicate ID and source/pytest selector integrity checks; **not** behavior verification |
| [`tests/unit/test_docs_capabilities.py`](../../tests/unit/test_docs_capabilities.py) | Negative regressions for missing evidence, unknown status and duplicate claims |

The live `/v1/capabilities` endpoint is additionally compared against
the reviewed implemented/planned sets in
`tests/integration/test_api.py::
test_live_api_claims_equal_reviewed_capability_ledger`.
Adding a feature without updating the implementation, tests,
API claim list, atlas and ledger is now a review failure.
Structural checks are **not** authorization or research validation.

## 9. M1 experimental synthetic daily data preflight

**Synthetic-only teaching slice; not a real evidence/forecast/agent capability.**

| File | Purpose |
| --- | --- |
| [`examples/m1_observation_preflight.py`](../../examples/m1_observation_preflight.py) | Standalone bounded preflight and redacted CLI; never contacts a real source |
| [`examples/synthetic-daily-sales.json`](../../examples/synthetic-daily-sales.json) | Invented daily counts with explicit gaps/cutoff |
| [`tests/unit/test_m1_observation_preflight.py`](../../tests/unit/test_m1_observation_preflight.py) | Exact integer, canonical date, future cutoff, duplication and bounded array regressions |
| [`tests/integration/test_m1_observation_preflight_cli.py`](../../tests/integration/test_m1_observation_preflight_cli.py) | Successful subprocess summary, byte cap and non-echoed error input |
| [`docs/engineering/M1_DATA_PREFLIGHT.md`](M1_DATA_PREFLIGHT.md) | Reviewed source-method walkthrough and synthetic-data limitations |
| [`docs/engineering/changes/MM-M1A-synthetic-preflight.md`](changes/MM-M1A-synthetic-preflight.md) | Impact map, accepted bounded task, independent reproduction and trust gaps |

The `/v1/capabilities` route exposes this as `experimental`,
not as implemented external ingestion. No recorded values
are asserted to belong to any real retailer or authorized
dataset. A future production ingestion module must be
separately reviewed, authorized and tested.

## 10. AI research, model evaluation and human decision review templates

| Source | Mandatory review purpose before a future capability claim |
| --- | --- |
| [`docs/engineering/DATASET_CARD_TEMPLATE.md`](DATASET_CARD_TEMPLATE.md) | Rights, immutable snapshot, **event-time versus availability-time** lineage, leakage and retention |
| [`docs/engineering/FORECAST_MODEL_CARD_TEMPLATE.md`](FORECAST_MODEL_CARD_TEMPLATE.md) | Predeclared seasonal baseline, rolling temporal holdout, error metrics and uncertainty calibration |
| [`docs/engineering/DECISION_TRACE_TEMPLATE.md`](DECISION_TRACE_TEMPLATE.md) | Explicitly separate authorized observations, evaluated forecasts, conditional simulations and human approval |
| [`docs/engineering/WORLDKERNEL_GATEWAY_GATE.md`](WORLDKERNEL_GATEWAY_GATE.md) | Versioned contract mismatch, rejected unsupported interventions/references, optional adapter acceptance and boundaries |
| [`docs/engineering/M1_EXECUTION_PLAN.md`](M1_EXECUTION_PLAN.md) | Dependency-ordered M1a–M1f acceptance gates with actual versus planned status |

**All five documents are templates/plans, not executable implementations.**
They must be filled with reviewed facts and real test outcomes
when the corresponding modules are introduced. The atlas and
capability/evidence CI checks cannot independently certify
scientific rigor, authorization or model fairness.

## 10. M1 experimental rolling-origin evaluation (synthetic only)

| Tracked artifact | Scope and next reading |
| --- | --- |
| [`examples/m1_temporal_backtest.py`](../../examples/m1_temporal_backtest.py) | Fixed seasonal-naive and trailing-mean one-step forecasts; data and results remain synthetic |
| [`examples/synthetic-weekly-sales.json`](../../examples/synthetic-weekly-sales.json) | Invented 35-day seven-day repeating teaching fixture, no real source |
| [`tests/unit/test_m1_temporal_backtest.py`](../../tests/unit/test_m1_temporal_backtest.py) | Prefix-only predictions, exact metric arithmetic, gaps, cutoffs, zero denominator |
| [`tests/integration/test_m1_temporal_backtest_cli.py`](../../tests/integration/test_m1_temporal_backtest_cli.py) | Local CLI replay, bounded bytes and generic failure responses |
| [`docs/engineering/M1_TEMPORAL_BACKTEST.md`](M1_TEMPORAL_BACKTEST.md) | Source-reviewed methods, worked scores, caveats and independent exercise |
| [`docs/engineering/datasets/SYNTHETIC_WEEKLY_CARD.md`](datasets/SYNTHETIC_WEEKLY_CARD.md) | Synthetic-only data card; no permission, provenance or real data claims |
| [`docs/engineering/model_cards/SYNTHETIC_WEEKLY_BASELINES.md`](model_cards/SYNTHETIC_WEEKLY_BASELINES.md) | Transparent evaluation protocol and metric table for invented periodic data |
| [`docs/engineering/changes/MM-M1C-synthetic-rolling-backtest.md`](changes/MM-M1C-synthetic-rolling-backtest.md) | Bounded change request, tests and unfulfilled production requirements |

This **local teaching evaluation is not a real forecasting service**.
`GET /v1/capabilities` and the capability ledger mark
`synthetic_rolling_backtest` experimental; `forecasting`
remains planned. No licensed dataset, deployed prediction endpoint
or WorldKernel integration has been established.

## 11. Experimental retrospective availability filter (synthetic only)

| Tracked artifact | Role and review boundary |
| --- | --- |
| [`examples/m1_availability_preflight.py`](../../examples/m1_availability_preflight.py) | Safe local as-of preflight, separating event date from declared publication date |
| [`examples/synthetic-asof-sales.json`](../../examples/synthetic-asof-sales.json) | Invented events and publication dates, one deliberately delayed |
| [`tests/unit/test_m1_availability_preflight.py`](../../tests/unit/test_m1_availability_preflight.py) | Adverse cases for late publication, future events, duplicate data and impossible dates |
| [`tests/integration/test_m1_availability_preflight_cli.py`](../../tests/integration/test_m1_availability_preflight_cli.py) | Local CLI evidence of bounded safe summaries and redacted failures |
| [`docs/engineering/M1_AVAILABILITY_PRECHECK.md`](M1_AVAILABILITY_PRECHECK.md) | Reviewed date-pair semantics, toy walkthrough and reproducibility |
| [`docs/engineering/datasets/SYNTHETIC_AVAILABILITY_CARD.md`](datasets/SYNTHETIC_AVAILABILITY_CARD.md) | Source/snapshot labels are claims; no real rights or reporting timestamps verified |
| [`docs/engineering/changes/MM-M1B-synthetic-availability.md`](changes/MM-M1B-synthetic-availability.md) | Bounded request, safe acceptance and future ingestion dependencies |

`synthetic_asof_availability` is **experimental**, not
a production evidence connector. The `evidence_and_rag`
capability stays planned; this example intentionally
does not attest source availability or permissions.

## 12. Joint as-of and rolling synthetic evaluation

This local exercise is still **experimental**. It reuses the
generated data availability guard and the two baseline
calculations, abstaining instead of backfilling
unavailable history.

| Tracked artifact | Why it matters |
| --- | --- |
| [`examples/m1_asof_rolling_backtest.py`](../../examples/m1_asof_rolling_backtest.py) | Only score one-day origins when seven past records were published by each origin |
| [`examples/synthetic-asof-weekly-sales.json`](../../examples/synthetic-asof-weekly-sales.json) | Invented weekly series with Jan 27 data released Jan 31 |
| [`tests/unit/test_m1_asof_rolling_backtest.py`](../../tests/unit/test_m1_asof_rolling_backtest.py) | Covers 3/7 abstention, historical prefixes, null scores and invalid final targets |
| [`tests/integration/test_m1_asof_rolling_backtest_cli.py`](../../tests/integration/test_m1_asof_rolling_backtest_cli.py) | Bounded/redacted CLI behavior and synthetic score output |
| [`docs/engineering/M1_ASOF_ROLLING_EVALUATION.md`](M1_ASOF_ROLLING_EVALUATION.md) | Source-backed methods, coverage-dependent results, independent exercise |
| [`docs/engineering/datasets/SYNTHETIC_ASOF_WEEKLY_CARD.md`](datasets/SYNTHETIC_ASOF_WEEKLY_CARD.md) | Dataset generated for testing known-as-of history; no real permission |
| [`docs/engineering/model_cards/SYNTHETIC_ASOF_WEEKLY_BASELINES.md`](model_cards/SYNTHETIC_ASOF_WEEKLY_BASELINES.md) | Evaluation scores on only four synthetic origins, with abstention caveats |
| [`docs/engineering/changes/MM-M1C-asof-rolling-abstention.md`](changes/MM-M1C-asof-rolling-abstention.md) | Scope, risk and regression acceptance for the experimental slice |

`synthetic_asof_rolling_backtest` is reported only
as an **experimental** local program. The real
`forecasting` and `evidence_and_rag` capabilities
remain planned; verified publication timestamps
and empirically valid forecasts still do not exist.

## 13. Source-backed local CSV snapshot staging (not authorization)

A reusable **in-memory** `evidence/` library module now
exists independently of the synthetic command-line demos.
It validates a strict byte/schema contract and
historical publication-date selection but is **not**
an ingestion service, a rights checker, a deployed Evidence
Engine or a source-provenance validator.

| Tracked artifact | Function / review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/__init__.py`](../../src/mirrormind/modules/evidence/__init__.py) | Evidence package marker; no automatic source connections |
| [`src/mirrormind/modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py) | Strict bounded local byte parser, declared hash comparison, immutable rows, two-timestamp as-of query |
| [`tests/unit/test_evidence_snapshots.py`](../../tests/unit/test_evidence_snapshots.py) | Negative cases for digest, header, duplicate rows, date and count validation; source rights explicitly unverified |
| [`tests/integration/test_local_snapshot_flow.py`](../../tests/integration/test_local_snapshot_flow.py) | Installable package stage/receipt/as-of flow on invented fixture bytes |
| [`examples/staged-daily-observations.csv`](../../examples/staged-daily-observations.csv) | Four invented rows; one late-declared publication and one measured zero |
| [`docs/engineering/M1_LOCAL_CSV_STAGING.md`](M1_LOCAL_CSV_STAGING.md) | Method-by-method walkthrough, SHA-256 trust limits, reproduction and independent exercise |
| [`docs/engineering/datasets/LOCAL_CSV_STAGING_FIXTURE.md`](datasets/LOCAL_CSV_STAGING_FIXTURE.md) | Synthetic-only data card, no publisher or permission claims |
| [`docs/engineering/changes/MM-M1B-local-csv-staging.md`](changes/MM-M1B-local-csv-staging.md) | Bounded acceptance, impact, tests and unresolved authorization concerns |

The API capability register labels `local_csv_snapshot_preflight`
**experimental**. The full `evidence_and_rag` remains
**planned**. This new code has no network, persistence,
forecasting, simulation or authorization feature.

## 14. Source-level offline rolling baselines (still experimental)

The first reusable `forecasting/` module composes the
strict local evidence-staging primitive with two fixed
one-day estimators. It **does not** ingest an authorized
dataset, fit a model, serve forecasts or simulate
WorldKernel. Its scores come from an invented fixture.

| Tracked path | Source/test responsibility |
| --- | --- |
| [`src/mirrormind/modules/forecasting/__init__.py`](../../src/mirrormind/modules/forecasting/__init__.py) | Package marker; no automatic model loading or service |
| [`src/mirrormind/modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py) | Bounded historic as-of lag-7 and trailing-average evaluation with aligned scores and abstentions |
| [`tests/unit/test_staged_rolling_baselines.py`](../../tests/unit/test_staged_rolling_baselines.py) | Honest scoring on four of seven generated origins; negative controls for unavailable history and undefined metrics |
| [`tests/integration/test_staged_rolling_flow.py`](../../tests/integration/test_staged_rolling_flow.py) | Compose installed library snapshot stage and evaluation on invented data without runtime file/network I/O |
| [`examples/staged-weekly-availability.csv`](../../examples/staged-weekly-availability.csv) | 35 generated rows, one late-declared publication and a repeating artificial weekly pattern |
| [`docs/engineering/M1_STAGED_ROLLING_BASELINES.md`](M1_STAGED_ROLLING_BASELINES.md) | Reviewed methods, risk limits, numerical example and independent exercise |
| [`docs/engineering/datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md`](datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md) | Invented source/snapshot card, no real rights or original release verification |
| [`docs/engineering/model_cards/STAGED_WEEKLY_BASELINES.md`](model_cards/STAGED_WEEKLY_BASELINES.md) | Model evaluation card with scored-origin denominator and explicit 4/7 coverage |
| [`docs/engineering/changes/MM-M1C-staged-offline-backtest.md`](changes/MM-M1C-staged-offline-backtest.md) | Accepted scope, compatibility, test evidence and unresolved scientific/permission gates |

The public `/v1/capabilities` register declares
`local_staged_rolling_baselines` **experimental** while
`forecasting` stays **planned**. No external data,
trained forecasting service or WorldKernel execution
is provided by these primitives.

## 15. Permission-sensitive candidate: M5 (no data acquired)

| File | Review responsibility |
| --- | --- |
| [`docs/engineering/datasets/M5_ACCESS_REVIEW.md`](datasets/M5_ACCESS_REVIEW.md) | **Proposed/not approved** M5 source access; reconcile the official competition rules, mirror, permitted research/commercial usage and original data rights before any download |

An accessible Kaggle or Zenodo page is not a
license attestation. The staged CSV parser and
offline baseline evaluator **do not** approve
source rights and should not be used to bypass
this no-go gate.

## 16. Per-origin diagnostics for existing offline evaluation

No additional source module is introduced. The
[`backtest_staged_snapshot`](../../src/mirrormind/modules/forecasting/baselines.py)
return value now includes a **bounded, deterministic**
`origin_audit` with nonvalue status records for
each requested evaluation day, distinguishing
missing targets, delayed publication and unavailable
history from scored origins.

| New tracked artifact | Purpose |
| --- | --- |
| [`docs/engineering/changes/MM-M1C-origin-audit-ledger.md`](changes/MM-M1C-origin-audit-ledger.md) | Accepted scope and adverse regression criteria for the local diagnostic |

See the [source-method guide](M1_STAGED_ROLLING_BASELINES.md),
[updated unit tests](../../tests/unit/test_staged_rolling_baselines.py)
and [claim references](EVIDENCE_MAP.json).
The list is internal diagnostic metadata, **not**
an authenticated, immutable external audit log or
permission grant. Source rights and production inference
remain unimplemented.

## 17. Observed minimum-history contract correction

The existing [staged rolling evaluator](../../src/mirrormind/modules/forecasting/baselines.py)
now validates that `min_history_days` represents
the **number of recorded pre-holdout dates**, not
the age of the oldest row. The [method walkthrough](M1_STAGED_ROLLING_BASELINES.md)
cites the sparse-history and early-calendar
negative tests. Its per-origin release-date
abstentions are unchanged.

| Newly tracked file | Why it matters |
| --- | --- |
| [`docs/engineering/changes/MM-M1C-min-history-regression.md`](changes/MM-M1C-min-history-regression.md) | Reproduction, acceptance and trust boundaries for the corrected minimum-history precondition |

Neither a row count nor a passing date check
authenticates real source records, data rights,
or forecasting validity.

## 18. Bounded local stream stage — limit bytes before CSV parsing

The existing [evidence staging module](../../src/mirrormind/modules/evidence/snapshots.py)
now exposes `read_staged_csv(stream, expected_sha256)`
for a **caller-opened** binary stream. It reads
in 64 KiB-or-smaller chunks with a 1 MiB+1 sentinel,
then invokes the unchanged strict in-memory
CSV/row/date/digest parser. It is not a source
opener, license gate or authenticated ingester.

| New tracked file | Review role |
| --- | --- |
| [`docs/engineering/changes/MM-M1B-bounded-stream.md`](changes/MM-M1B-bounded-stream.md) | Byte-cap and failure-mode acceptance; source permission must be independently approved |

The [method guide](M1_LOCAL_CSV_STAGING.md),
[unit tests](../../tests/unit/test_evidence_snapshots.py),
[integration test](../../tests/integration/test_local_snapshot_flow.py)
and [claim-to-test map](EVIDENCE_MAP.json)
cover partial reads, byte limits, generic errors
and complete digest matching. **No real-data
access permission is established here.**

## 19. Officially licensed retail-source candidate (review still pending)

| Tracked review | What it establishes — and what it does not |
| --- | --- |
| [`docs/engineering/datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md`](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) | Official UCI dataset 352 page states CC BY 4.0, with DOI, attribution and privacy checks; **not** approved data acquisition, verified row availability, model skill or a production connector |

This source is distinct from the blocked
[M5 review](datasets/M5_ACCESS_REVIEW.md).
An explicitly published Creative Commons
license is stronger evidence of reuse rights,
but customer identifiers, downstream processing
and historical publication dates still require
a separate human-reviewed acceptance.

## 20. Non-imputing quality metrics for structurally staged records

[`snapshot_quality_summary`](../../src/mirrormind/modules/evidence/snapshots.py)
now provides a **read-only, in-memory** aggregate
of per-series observed calendar gaps, explicitly
recorded zeros, declared late publications,
row counts and overall observation date boundaries.
It never invents missing sales or authenticates
source rights.

| Newly tracked file | Purpose |
| --- | --- |
| [`tests/unit/test_evidence_quality.py`](../../tests/unit/test_evidence_quality.py) | Distinguishes zero from missing, declared availability delays, invalid staging and minimized output |
| [`docs/engineering/changes/MM-M1B-staged-quality-summary.md`](changes/MM-M1B-staged-quality-summary.md) | Review gates and acceptance for source-unverified aggregate diagnostics |

See the [revised staging walkthrough](M1_LOCAL_CSV_STAGING.md),
[bounded reader integration](../../tests/integration/test_local_snapshot_flow.py)
and [evidence map](EVIDENCE_MAP.json).
An internal calendar gap is not proof of
lost sales, source outage or a real
business demand gap. No API source connector,
real data ingestion or production model
has been added.

## 21. Retail-only UCI-shaped transaction projection (offline, experimental)

This **retail-domain** module has no automatic external
data acquisition, workbook parser, model call or source
permission checks. It accepts only bounded UCI-shaped
row mappings supplied by a trusted caller, separates
positive invoice lines from cancellations and nonpositive
lines, and returns aggregate product-day counts **without**
original invoice or customer IDs. It never supplies a
made-up first-availability date.

| Tracked file | Role / next source for review |
| --- | --- |
| [`src/mirrormind/domains/__init__.py`](../../src/mirrormind/domains/__init__.py) | Sector-specific package boundary; no automatic ingestion |
| [`src/mirrormind/domains/retail/__init__.py`](../../src/mirrormind/domains/retail/__init__.py) | Retail transformation namespace only |
| [`src/mirrormind/domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py) | Source-backed immutable product-day aggregation, cancellation/negative/zero counters, resource caps and unknown release-time status |
| [`tests/unit/test_uci_retail_projection.py`](../../tests/unit/test_uci_retail_projection.py) | Generated rows: privacy minimization, cancellation/duplicate semantics, date/type validation and bounded iteration |
| [`tests/integration/test_uci_retail_projection_flow.py`](../../tests/integration/test_uci_retail_projection_flow.py) | In-memory integration; rejects direct use as time-authorized staged evidence |
| [`docs/engineering/UCI_RETAIL_PROJECTION.md`](UCI_RETAIL_PROJECTION.md) | Function-by-function behavior, privacy/time gates, independent exercise |
| [`docs/engineering/datasets/SYNTHETIC_UCI_ROWS_CARD.md`](datasets/SYNTHETIC_UCI_ROWS_CARD.md) | Invented UCI-shaped fixtures; no real data or publication evidence |
| [`docs/engineering/changes/MM-M1B-uci-shaped-transaction-projection.md`](changes/MM-M1B-uci-shaped-transaction-projection.md) | Bounded change request, acceptance and explicit non-goals |

Capability `local_uci_transaction_projection` is
**experimental**. The official [UCI candidate](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
has not been imported or approved for this code path.
The platform's `evidence_and_rag` and
`forecasting` remain **planned**.

## 22. Optional bounded local XLSX reader (synthetic and unapproved)

The new [UCI-shaped workbook reader](../../src/mirrormind/domains/retail/uci_workbook.py)
uses `openpyxl` as an **optional** dependency
and accepts only a trusted caller's already-opened
binary stream. It checks compressed bytes,
the caller-provided digest, ZIP metadata,
a fixed worksheet/header and row/group caps
before returning the existing privacy-minimized
retail projection. **No original UCI dataset
was downloaded or made available.**

| Tracked path | Review responsibility |
| --- | --- |
| [`src/mirrormind/domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py) | Bounded XLSX byte/ZIP read and fixed UCI-shaped sheet validation; no external file or URL opening |
| [`tests/unit/test_uci_workbook.py`](../../tests/unit/test_uci_workbook.py) | Synthetic Excel, short/oversized reads, ZIP metadata, wrong sheet/header, digest, formula and customer-field guards |
| [`tests/integration/test_uci_workbook_flow.py`](../../tests/integration/test_uci_workbook_flow.py) | Small temporary fictional XLSX to product/day records with publication-time unknown |
| [`docs/engineering/UCI_WORKBOOK_READER.md`](UCI_WORKBOOK_READER.md) | Source-reviewed contracts, exact budgets, caveats and independent learning exercise |
| [`docs/engineering/datasets/SYNTHETIC_UCI_XLSX_CARD.md`](datasets/SYNTHETIC_UCI_XLSX_CARD.md) | Test-generated fictional workbook card, no real customer source or rights claim |
| [`docs/engineering/changes/MM-M1B-bounded-uci-xlsx-reader.md`](changes/MM-M1B-bounded-uci-xlsx-reader.md) | Accepted narrow scope and outstanding authorization/security blockers |

The optional `uci` extra is declared in
[`pyproject.toml`](../../pyproject.toml);
the regular Python package has no mandatory XLSX
dependency. The `local_uci_xlsx_reader` capability
is **experimental**; this supports neither the
complete original UCI dataset nor production
evidence ingestion or historical forecast claims.

## 23. Aggregate internal retail event-day coverage (experimental)

| New path | Purpose and limitation |
| --- | --- |
| [`src/mirrormind/domains/retail/coverage.py`](../../src/mirrormind/domains/retail/coverage.py) | Bounded immutable aggregate of internal missing positive-invoice product-days without inventing demand or availability |
| [`tests/unit/test_retail_coverage.py`](../../tests/unit/test_retail_coverage.py) | Synthetic regression coverage for gaps, cancellation-only days, privacy, invalid ordering and empty results |
| [`docs/engineering/RETAIL_COVERAGE.md`](RETAIL_COVERAGE.md) | Source walkthrough, reproduction and independent review exercise |

This is **not authorized ingestion**, a proof of zero demand, a
publisher-availability timeline or an operational forecast input.

## 24. Optional declared calendar comparison (experimental)

| Tracked file | Role and limitation |
| --- | --- |
| [`src/mirrormind/domains/retail/calendar_coverage.py`](../../src/mirrormind/domains/retail/calendar_coverage.py) | Strict hypothetical date schedule: compare scheduled internal missing product-days without making data availability claims |
| [`tests/unit/test_declared_calendar_coverage.py`](../../tests/unit/test_declared_calendar_coverage.py) | Fictional closed-day assumptions, contrary positive observations, privacy and budget regressions |
| [`docs/engineering/DECLARED_CALENDAR_COVERAGE.md`](DECLARED_CALENDAR_COVERAGE.md) | Method and risk review, exercise and operational-calendar verification gate |

A declared schedule is **not authenticated** as an opening, collection
or publisher calendar. Missing positive sales are never replaced by zeros.

## 25. Hypothetical as-of retail release audit (experimental)

| New tracked path | Reviewed scope |
| --- | --- |
| [`src/mirrormind/domains/retail/declared_releases.py`](../../src/mirrormind/domains/retail/declared_releases.py) | Exact caller-declared release per positive product-day and source-unverified as-of counters |
| [`tests/unit/test_declared_retail_releases.py`](../../tests/unit/test_declared_retail_releases.py) | Fictional cutoff, withheld/future, missing, duplicate, contradictory and privacy regressions |
| [`docs/engineering/DECLARED_RETAIL_RELEASES.md`](DECLARED_RETAIL_RELEASES.md) | Method walkthrough and source/provenance/non-production gates |

A supplied release date is **not authenticated publisher provenance**,
permission to ingest UCI, or proof of point-in-time forecast readiness.

## 26. Source-unverified retail rolling release evaluation (experimental)

| Tracked path | Behavior and review scope |
| --- | --- |
| [`src/mirrormind/domains/retail/release_backtest.py`](../../src/mirrormind/domains/retail/release_backtest.py) | Bounded one-step daily comparison, no missing=zero or publication-time invention |
| [`tests/unit/test_retail_release_backtest.py`](../../tests/unit/test_retail_release_backtest.py) | Fictional origins, withheld values, no-history abstentions, validation failures |
| [`docs/engineering/RETAIL_RELEASE_BACKTEST.md`](RETAIL_RELEASE_BACKTEST.md) | Method limitations, matched-model scores, example and independent exercise |

This **does not** create authentic point-in-time records, a real forecast,
stockout diagnosis, calibrated uncertainty or an operational decision path.

## 27. Retail model comparison coverage gate (experimental)

| Tracked path | Reviewed scope |
| --- | --- |
| [`src/mirrormind/domains/retail/coverage_gate.py`](../../src/mirrormind/domains/retail/coverage_gate.py) | Exact matched-origin coverage threshold that can withhold conditional ranking |
| [`tests/unit/test_retail_coverage_gate.py`](../../tests/unit/test_retail_coverage_gate.py) | Invented incomplete/full histories, exact percentage boundary, false interval refusal and negative gates |
| [`docs/engineering/RETAIL_COVERAGE_GATE.md`](RETAIL_COVERAGE_GATE.md) | Reviewed method, toy example, limitations and independent exercise |

This **does not** calibrate uncertainty, approve sources, infer zero
sales or validate forecasting skill on an empirical dataset.

## 28. Prequential residual envelope diagnostic (experimental)

| Tracked path | Behavior and review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py) | Past-only eligible absolute residuals, conservative abstention, aggregate retrospective hits, no calibrated interval |
| [`tests/unit/test_retail_residual_envelope.py`](../../tests/unit/test_retail_residual_envelope.py) | Fictional hidden-value invariance, residual insufficiency, missing targets, malformed dates |
| [`docs/engineering/RETAIL_RESIDUAL_ENVELOPE.md`](RETAIL_RESIDUAL_ENVELOPE.md) | Causal time cutoffs, traceable claims and non-production limitations |

No nominal uncertainty target, statistical calibration, source rights,
true demand or WorldKernel inference is asserted here.

## 29. Consecutive-window retail eligibility drift audit (experimental)

| Tracked path | Scope and limitation |
| --- | --- |
| [`src/mirrormind/domains/retail/eligibility_drift.py`](../../src/mirrormind/domains/retail/eligibility_drift.py) | Adjacent window coverage denominators at each authentic-to-the-code but unverified caller-declared cutoff |
| [`tests/unit/test_retail_eligibility_drift.py`](../../tests/unit/test_retail_eligibility_drift.py) | Fictional complete/incomplete windows and nonretrospective publisher-release invariant |
| [`docs/engineering/RETAIL_ELIGIBILITY_DRIFT.md`](RETAIL_ELIGIBILITY_DRIFT.md) | Method, source-provenance caveats, synthetic exercise and empirical prerequisites |

Eligibility changes do not establish selection-bias mechanisms, source
rights, demand distribution shift, or operational forecast reliability.

## 30. Conditional retail eligible-value comparison (experimental)

| Tracked file | Purpose and limitation |
| --- | --- |
| [`src/mirrormind/domains/retail/eligible_values.py`](../../src/mirrormind/domains/retail/eligible_values.py) | Separately dated eligible-subset means and medians with conservative two-window abstention |
| [`tests/unit/test_retail_eligible_values.py`](../../tests/unit/test_retail_eligible_values.py) | Fictional complete/partial exposures, withheld-value invariance and threshold refusal tests |
| [`docs/engineering/RETAIL_ELIGIBLE_VALUES.md`](RETAIL_ELIGIBLE_VALUES.md) | Method, toy example and explicit nonidentifiability of distribution shift |

No selection-bias correction, source verification, calibrated interval or
operational forecast capability is introduced.

## 31. Excluded-target counterfactual sensitivity (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/selection_sensitivity.py`](../../src/mirrormind/domains/retail/selection_sensitivity.py) | Disjoint-window hypothetical mean/difference bounds without reading excluded values |
| [`tests/unit/test_retail_selection_sensitivity.py`](../../tests/unit/test_retail_selection_sensitivity.py) | Fictitious hidden-value invariance, sign reversal, budget and validation cases |
| [`docs/engineering/RETAIL_SELECTION_SENSITIVITY.md`](RETAIL_SELECTION_SENSITIVITY.md) | Explicit assumption, algebra, limitations and review exercise |

No source authorization, selection-bias identification, statistical
confidence interval, actual demand shift, or WorldKernel integration.

## 32. Temporary local QA gate (Actions quota exhaustion)

| Tracked file | Purpose and limitation |
| --- | --- |
| [`scripts/local_quality_gate.py`](../../scripts/local_quality_gate.py) | Fail-closed clean checkout verification at a full commit SHA; run pytest, Ruff and four documentation checks, no official CI claim |
| [`tests/unit/test_local_quality_gate.py`](../../tests/unit/test_local_quality_gate.py) | Mocked process/checkout controls and honest receipt tests |
| [`docs/engineering/LOCAL_QUALITY_GATE.md`](LOCAL_QUALITY_GATE.md) | Temporary owner-authorized local QA policy, invocation and limitations |

Local validation is not equivalent to GitHub Actions: restore official CI
as soon as the monthly quota becomes available.

## 33. Counterfactual excluded-target scenario sweep (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/sensitivity_sweep.py`](../../src/mirrormind/domains/retail/sensitivity_sweep.py) | Two historical audits reused across 2–8 bounded ceilings, with a default two-window minimum and exact-coverage disclosure gate; no excluded-target observations |
| [`tests/unit/test_retail_sensitivity_sweep.py`](../../tests/unit/test_retail_sensitivity_sweep.py) | Exact parity with independent scenarios, two-evaluation spy, monotone bounds, hidden-value nonleakage, exact coverage thresholds and sparse-window abstention |
| [`docs/engineering/RETAIL_SENSITIVITY_SWEEP.md`](RETAIL_SENSITIVITY_SWEEP.md) | Hypothetical assumptions, negative controls and source-rights caveats |

These scenarios do not identify true demand distribution shifts.

## 34. Scoped historical forecast reuse (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py) | Call-local forecast caching and release-aware incremental residual selection; each target forecast remains governed by its own origin |
| [`tests/unit/test_retail_residual_envelope.py`](../../tests/unit/test_retail_residual_envelope.py) | Instrumented prior 154-vs-28 comparison, rolling-window independent naive oracle over 40 schedules, repeated-call isolation and late/missing-data regressions |
| [`docs/engineering/RETAIL_RESIDUAL_ENVELOPE.md`](RETAIL_RESIDUAL_ENVELOPE.md) | Describes the structural reduction and lack of calibrated intervals |

No global forecast cache, authenticated vintages or operational forecasting
are introduced by this optimization.

## 35. Reproducible synthetic residual-evaluator performance experiment

| Tracked file | Review boundary |
| --- | --- |
| [`scripts/benchmarks/retail_residual.py`](../../scripts/benchmarks/retail_residual.py) | Exact-revision full evaluator timing, separate traced Python allocation peak, SHA-256 report equivalence |
| [`tests/unit/test_retail_residual_benchmark.py`](../../tests/unit/test_retail_residual_benchmark.py) | Invented fixture bounds, stable digest and Git revision preflight refusal |
| [`docs/engineering/RETAIL_RESIDUAL_BENCHMARK.md`](RETAIL_RESIDUAL_BENCHMARK.md) | Reproduction protocol, baseline/optimized SHAs and limits on interpretation |

The optional measurement is not a test of real demand, calibrated intervals,
whole-process memory or production latency, and is not an Actions substitute.

## 36. Review-only source metadata binding (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/intake_review.py`](../../src/mirrormind/modules/evidence/intake_review.py) | Binds staged checksum to declared intended use and opaque permission/privacy refs; explicitly does **not** authorize |
| [`tests/unit/test_source_intake_review.py`](../../tests/unit/test_source_intake_review.py) | Synthetic CSV/XLSX paths, reference validation, mismatched hashes and privacy/authorization refusal |
| [`docs/engineering/SOURCE_INTAKE_REVIEW.md`](SOURCE_INTAKE_REVIEW.md) | Method, human go/no-go, unsupported actual data and historical availability |
| [`docs/engineering/changes/M1B_SOURCE_REVIEW_PACKET.md`](changes/M1B_SOURCE_REVIEW_PACKET.md) | Scoped behavior change request, acceptance, trust map and rollback |

A packet is **not** a verified license, source credential, permission
service, actual ingestion, publisher vintage or working Evidence Engine.
