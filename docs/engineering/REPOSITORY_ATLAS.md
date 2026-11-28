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
| [`docs/engineering/changes/ENG_02_EXAMPLES_RUFF_MAINTENANCE.md`](changes/ENG_02_EXAMPLES_RUFF_MAINTENANCE.md) | Impact map, behavior-preserving lint correction, and sequence-boundary regressions |

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
| [`src/mirrormind/domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py) | Fixed pre-holdout calibration target interval, disjoint holdout labels, origin-specific release eligibility, conservative abstention and aggregate retrospective hits; no calibrated interval |
| [`tests/unit/test_retail_residual_envelope.py`](../../tests/unit/test_retail_residual_envelope.py) | Fictional hidden-value invariance, fixed-split non-overlap, late release, independent oracle, exact denominator and malformed-input checks |
| [`docs/engineering/RETAIL_RESIDUAL_ENVELOPE.md`](RETAIL_RESIDUAL_ENVELOPE.md) | Temporal rules, split metadata, test evidence, superseded cache history and non-production limitations |
| [`docs/engineering/changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md`](changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md) | Scoped acceptance criteria, impact map, trust review and compatibility notes |

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

## 34. Historical forecast reuse and rolling window (superseded)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py) | Current code supersedes the historical call-local cache and rolling target-label window with a fixed disjoint calibration/holdout split; see section 28 |
| [`tests/unit/test_retail_residual_envelope.py`](../../tests/unit/test_retail_residual_envelope.py) | Current tests cover the fixed split; prior PR #34/#35 cache and rolling-window assertions have been removed |
| [`docs/engineering/RETAIL_RESIDUAL_BENCHMARK.md`](RETAIL_RESIDUAL_BENCHMARK.md) | Preserves a historical two-revision benchmark whose results do not describe the current algorithm |

The old 154-to-28 call-count and timing comparison remain historical evidence
for those exact revisions only. They do not establish an optimization in the
current implementation, authenticated vintages, calibrated intervals or
operational forecasting.

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

## 37. Signed source reviewer history and revocation (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/review_decisions.py`](../../src/mirrormind/modules/evidence/review_decisions.py) | Verify bounded Ed25519 event history, chained head, expiry and permanent same-packet revocation; no grant |
| [`tests/unit/test_signed_source_review.py`](../../tests/unit/test_signed_source_review.py) | Fictional signed approvals, revocation, reordered/truncated logs, scope and key mismatches, explicit denial and privacy regressions |
| [`docs/engineering/SIGNED_SOURCE_REVIEW.md`](SIGNED_SOURCE_REVIEW.md) | Human review vs signature and external key/head/freshness requirements |
| [`docs/engineering/changes/M1B_SIGNED_REVIEW_REVOCATION.md`](changes/M1B_SIGNED_REVIEW_REVOCATION.md) | Acceptance gates, impact map, known spoofed-root risks and rollback |

Trusted signer/private keys, current independently anchored review history,
source rights and authorization to ingest are **not** implemented.

## 38. Local signed-review revision coordination (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/local_review_registry.py`](../../src/mirrormind/modules/evidence/local_review_registry.py) | Compare-and-swap with per-process lock, signed-chain checks and permanent same-packet revocation |
| [`tests/unit/test_local_review_registry.py`](../../tests/unit/test_local_review_registry.py) | Concurrent stale writes, old head refusal, signature tampering, restart loss, bounds and key-copy tests |
| [`docs/engineering/LOCAL_REVIEW_REGISTRY.md`](LOCAL_REVIEW_REGISTRY.md) | Source-bound revision format, limits, missing durable trust and nonauthorizing receipts |
| [`docs/engineering/changes/M1B_LOCAL_REVIEW_REGISTRY.md`](changes/M1B_LOCAL_REVIEW_REGISTRY.md) | Change request, acceptance and rollback constraints |

The registry is process-only and does **not** supply trusted reviewer
identity, an append-only external head, source permissions, or ingestion.

## 39. SQLite signed-review transaction and restart recovery (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/sqlite_review_registry.py`](../../src/mirrormind/modules/evidence/sqlite_review_registry.py) | Local SQLite schema v1, signed event replay verification, transactional revision/head CAS and restart persistence |
| [`tests/unit/test_sqlite_review_registry.py`](../../tests/unit/test_sqlite_review_registry.py) | Recovery, cross-interpreter CAS, injected rollback, tampering, expiry, budgets and restored old database checks |
| [`docs/engineering/SQLITE_REVIEW_REGISTRY.md`](SQLITE_REVIEW_REGISTRY.md) | Exact local persistence contract, external fresh-head dependency and nonauthorizing receipts |
| [`docs/engineering/changes/M1B_SQLITE_REVIEW_REGISTRY.md`](changes/M1B_SQLITE_REVIEW_REGISTRY.md) | Scope, acceptance, trust boundary and rollback plan |

SQLite local persistence is **not** a tamper-proof or independently
attested registry and does not enable M5/UCI source ingestion.

## 40. Signed review-head checkpoint verification (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/head_checkpoints.py`](../../src/mirrormind/modules/evidence/head_checkpoints.py) | Offline domain-separated signer record, limited dates and sequence floor, SQLite review head equality; never authorizes |
| [`tests/unit/test_head_checkpoints.py`](../../tests/unit/test_head_checkpoints.py) | Signed revocation, restored older SQLite, replay with stale floor, key/scope/date tampering and identifier minimization |
| [`docs/engineering/SIGNED_HEAD_CHECKPOINTS.md`](SIGNED_HEAD_CHECKPOINTS.md) | Precise trust requirements, missing external high-water service and replay counterexample |
| [`docs/engineering/changes/M1B_SIGNED_HEAD_CHECKPOINTS.md`](changes/M1B_SIGNED_HEAD_CHECKPOINTS.md) | Scoped change, source/test mapping, acceptance and rollback |

A signed checkpoint proves a signature under supplied public keys, not
independent currentness, original source rights or data use permission.

## 41. Offline witnessed checkpoint succession (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/authority_transcript.py`](../../src/mirrormind/modules/evidence/authority_transcript.py) | Bounded signed witness chain, explicit dual-signed rotation, exact endpoint fences, fail-closed missing history and final SQLite comparison |
| [`tests/unit/test_authority_transcript.py`](../../tests/unit/test_authority_transcript.py) | Fictional witness handoff, signed replay, missing/duplicate sequence, stale endpoint and privacy checks |
| [`docs/engineering/AUTHORITY_TRANSCRIPT.md`](AUTHORITY_TRANSCRIPT.md) | Protocol domain separation, independently supplied fences, unseen fork and outage limits |
| [`docs/engineering/changes/M1B_AUTHORITY_TRANSCRIPT.md`](changes/M1B_AUTHORITY_TRANSCRIPT.md) | Scope, acceptance, impact and rollback |

No external checkpoint publisher, independently current witness history,
key management, legal rights approval or actual data ingestion exists.

## 42. Local signer-gated checkpoint publication ledger (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py) | Local SQLite transactional publication journal, separate operator signatures, witness rotation, chain replay and sanitized receipts |
| [`tests/unit/test_local_checkpoint_publisher.py`](../../tests/unit/test_local_checkpoint_publisher.py) | Fictional signer and role checks, two writer CAS, crash rollback, handoff, restart and coherent old backup tests |
| [`docs/engineering/LOCAL_CHECKPOINT_PUBLISHER.md`](LOCAL_CHECKPOINT_PUBLISHER.md) | Local publication contract, operator identity gap and untrusted restored backup counterexample |
| [`docs/engineering/changes/M1B_LOCAL_CHECKPOINT_PUBLISHER.md`](changes/M1B_LOCAL_CHECKPOINT_PUBLISHER.md) | Change scope, acceptance, risk and rollback |

Local publication is **not** an independently managed witness, globally
current head, licensed-source ingestion or operator identity service.

## 43. Local dual-admin operator-key governance (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/operator_governance.py`](../../src/mirrormind/modules/evidence/operator_governance.py) | SQLite dual-admin signed operator enrollment/expiry/revocation, immutable tombstones, CAS and local chain replay |
| [`tests/unit/test_operator_governance.py`](../../tests/unit/test_operator_governance.py) | Fictional admin signatures, fresh-key replacement, concurrent writers, SQL rollback and restored-old-policy regressions |
| [`docs/engineering/OPERATOR_GOVERNANCE.md`](OPERATOR_GOVERNANCE.md) | Key management prototype and explicit absence of publisher admission and trusted external head |
| [`docs/engineering/changes/M1B_OPERATOR_GOVERNANCE.md`](changes/M1B_OPERATOR_GOVERNANCE.md) | Change impact, acceptance, trust boundary and rollback |

No identity authority, real operator entitlement, publisher integration,
globally current policy or source-ingestion permission exists.

## 44. Atomic local operator-policy gated checkpoint publication (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py) | Opt-in new combined SQLite schema, same-transaction dual-signed policy admission, publication and external-head comparisons |
| [`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py) | Fictional post-revocation refusal, concurrent revocation/publish serialization, legacy bypass rejection, injected rollback and old backup tests |
| [`docs/engineering/ATOMIC_GOVERNED_PUBLISHER.md`](ATOMIC_GOVERNED_PUBLISHER.md) | Local atomic admission semantics, compatibility, external trust and source rights limitations |
| [`docs/engineering/changes/M1B_ATOMIC_GOVERNED_PUBLISHER.md`](changes/M1B_ATOMIC_GOVERNED_PUBLISHER.md) | Change request, safety acceptance, impact and rollback conditions |

The integrated local path **does not** provide operator identities,
externally attested currentness or actual source-ingestion permission.

## 45. Policy-bound signed integrated publications (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py) | Canonical legacy v1 history plus separate governed v2 signing domain and standalone-v2 rejection |
| [`src/mirrormind/modules/evidence/atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py) | Same-transaction validation of exact operator-signed policy revision/head and current policy |
| [`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py) | Domain swap refusal, wrong or stale policy binding, old v1 historical replay, standalone refusal and tamper detection |
| [`docs/engineering/ATOMIC_GOVERNED_PUBLISHER.md`](ATOMIC_GOVERNED_PUBLISHER.md) | v1/v2 compatibility, signature coverage and remaining external trust boundary |
| [`docs/engineering/changes/M1B_POLICY_BOUND_PUBLICATION.md`](changes/M1B_POLICY_BOUND_PUBLICATION.md) | Scope, acceptance, backward compatibility and rollback hazards |

The signed policy epoch is a **local verification invariant**, not a
trusted current-head attestation, authenticated real-world operator or
permission to ingest datasets or run empirical forecasts.

## 46. Supplied signed integrated-state fence (experimental)

| Tracked file | Review boundary |
| --- | --- |
| [`src/mirrormind/modules/evidence/integrated_head_fence.py`](../../src/mirrormind/modules/evidence/integrated_head_fence.py) | Read-only exact policy/publication signed-fence verification against one transactional local snapshot and externally pinned digest/sequence |
| [`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py) | Synthetic signer tampering, stale pinned fence, old coherent backup, publication-head drift, bounds and refusal tests |
| [`docs/engineering/INTEGRATED_HEAD_FENCE.md`](INTEGRATED_HEAD_FENCE.md) | Signed fields, conditional rollback detection, signer/currentness trust assumptions |
| [`docs/engineering/changes/M1B_INTEGRATED_HEAD_FENCE.md`](changes/M1B_INTEGRATED_HEAD_FENCE.md) | Scoped acceptance, impact map and intentionally deferred external service |

No trusted externally fetched latest head, independent signer custody,
live policy admission, source rights or authorized ingestion is proven.

## 47. Signed dual-witness integrated-fence continuity (experimental)

| Tracked file | Reviewed responsibility |
| --- | --- |
| [`src/mirrormind/modules/evidence/integrated_fence_transcript.py`](../../src/mirrormind/modules/evidence/integrated_fence_transcript.py) | Bounded offline forward chain, dual independent configured witnesses, terminal transactional local equality, supplied-fork classifier |
| [`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py) | Generated-key linked states, old backup/current pin, forgery, role/key replay, supplied-fork, counter/date/bounds tests |
| [`docs/engineering/INTEGRATED_FENCE_TRANSCRIPT.md`](INTEGRATED_FENCE_TRANSCRIPT.md) | Witness signing contract, externally pinned anchors, detectable supplied forks and limits |
| [`docs/engineering/changes/M1B_DUAL_WITNESS_FENCE_CONTINUITY.md`](changes/M1B_DUAL_WITNESS_FENCE_CONTINUITY.md) | Scope, acceptance, impact map and non-goals |

The existing [single-fence verifier](INTEGRATED_HEAD_FENCE.md)
is unchanged; no independent service or trustworthy latest-state
delivery is provided, and none of these results grants permission.

## 48. Separate durable local signed integrated-fence registry

| Tracked path | Reviewed intent |
| --- | --- |
| [`src/mirrormind/modules/evidence/local_integrated_fence_registry.py`](../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py) | Separate SQLite file, strict packet/key marker, complete signed chain replay, guarded CAS and local combined-head comparison |
| [`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py) | Generated-key reopen, publisher-only vs paired rollback, tamper, replay, concurrency, missing/expired and drift tests |
| [`docs/engineering/LOCAL_INTEGRATED_FENCE_REGISTRY.md`](LOCAL_INTEGRATED_FENCE_REGISTRY.md) | Local-file trust assumptions, signed-event storage, two-file consistency and recovery caveats |
| [`docs/engineering/changes/M1B_SEPARATE_DURABLE_FENCE_REGISTRY.md`](changes/M1B_SEPARATE_DURABLE_FENCE_REGISTRY.md) | Scoped acceptance and explicit service/authorization non-goals |

No independently operated current-head service, source permission
grant, production custody or cross-file atomicity is implied.

## 49. Experimental nonce-challenged current-head protocol, client and responder

| Tracked file | Reviewed responsibility |
| --- | --- |
| [`src/mirrormind/modules/evidence/remote_fence_head_protocol.py`](../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py) | One shared response type, signing domain, strict canonical signing message, compact JSON wire encoder and response parser |
| [`src/mirrormind/modules/evidence/remote_fence_head_client.py`](../../src/mirrormind/modules/evidence/remote_fence_head_client.py) | Fixed HTTPS read, OS-generated nonce, separately verified signed service reply, bounded canonical wire format and exact local signed-registry comparison |
| [`src/mirrormind/modules/evidence/remote_fence_head_service.py`](../../src/mirrormind/modules/evidence/remote_fence_head_service.py) | In-process request responder with typed clock/store operational errors and propagation of unrelated programming errors; no listener, authentication or persistence |
| [`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py) | Generated-key nonce/replay/forgery, typed operational clock/store failure, programming-error propagation, packet/role/paired rollback tests and fake HTTPS transport; no real endpoint contacted |
| [`docs/engineering/REMOTE_FENCE_HEAD_CLIENT.md`](REMOTE_FENCE_HEAD_CLIENT.md) | Request-response contract, trust boundaries, replay resistance and no independently deployed service |
| [`docs/engineering/REMOTE_FENCE_HEAD_SERVICE.md`](REMOTE_FENCE_HEAD_SERVICE.md) | G-01 source walkthrough, store/request/response contracts, signing flow, reproduction, failure modes and learning exercise |
| [`docs/engineering/changes/M1B_CHALLENGED_HTTPS_HEAD_READER.md`](changes/M1B_CHALLENGED_HTTPS_HEAD_READER.md) | Scope, acceptance, impact map and deferred service operation |
| [`docs/engineering/changes/G01_CURRENT_HEAD_SERVICE_RESPONSE.md`](changes/G01_CURRENT_HEAD_SERVICE_RESPONSE.md) | G-01 acceptance, impact map, compatibility, safety and evidence record |

The client does not grant source rights, publish or ingest data. The responder
does not provide a live server, managed key custody, durable current state or
globally current external authority.

## 50. Composed synthetic retail evidence preflight

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/evidence_flow.py`](../../src/mirrormind/domains/retail/evidence_flow.py) | Composes existing bounded local CSV/XLSX readers, review metadata, declared calendar/release checks and CSV as-of selection; no authorization or persistence |
| [`tests/integration/test_retail_evidence_flow.py`](../../tests/integration/test_retail_evidence_flow.py) | Generated/synthetic fixture integration tests for normal flow, abstention, receipt minimization and fail-closed declarations |
| [`docs/engineering/M1_SYNTHETIC_EVIDENCE_FLOW.md`](M1_SYNTHETIC_EVIDENCE_FLOW.md) | Architecture, contracts, reproducible CSV example, safety boundaries, test interpretation, exercises and diagnosis |
| [`docs/engineering/changes/M1B_02_SYNTHETIC_EVIDENCE_FLOW.md`](changes/M1B_02_SYNTHETIC_EVIDENCE_FLOW.md) | Scoped M1B-02 change request, acceptance criteria, impact map and evidence record |

The capability remains `experimental`; a syntactically valid review packet
does not verify data rights, source identity or actual publisher availability.

## 51. Fixed-split retail evidence evaluation

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/evaluation_flow.py`](../../src/mirrormind/domains/retail/evaluation_flow.py) | Composes a prepared UCI-shaped evidence flow with the existing fixed release-aware backtest; requires matching declared audit and evaluation cutoffs |
| [`examples/m1_retail_synthetic_evaluation.py`](../../examples/m1_retail_synthetic_evaluation.py) | Generates canonical fictional XLSX bytes in memory, supplies explicit synthetic releases and prints a versioned aggregate receipt |
| [`tests/integration/test_retail_synthetic_evaluation.py`](../../tests/integration/test_retail_synthetic_evaluation.py) | Checks deterministic CLI output, cutoff mismatch, withheld-target mutation, per-origin abstentions and identifier minimization |
| [`docs/engineering/M1_RETAIL_SYNTHETIC_EVALUATION.md`](M1_RETAIL_SYNTHETIC_EVALUATION.md) | Architecture, algorithm, result contract, tests, security, diagnostics and learning exercises |
| [`docs/engineering/changes/M1C_01_SYNTHETIC_RETAIL_EVALUATION.md`](changes/M1C_01_SYNTHETIC_RETAIL_EVALUATION.md) | M1C-01 scope, acceptance, impact map and implementation evidence |
| [`docs/engineering/datasets/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md`](datasets/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md) | Fictional workbook, explicit availability declarations, privacy and provenance limits |
| [`docs/engineering/model_cards/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md`](model_cards/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md) | Fixed baselines, temporal holdout, metrics and no-uncertainty boundary |

The experimental result is not an empirical forecast or recommendation;
release dates and positive-line units remain unverified proxies.

## 52. Versioned decision trace result contract (interface-only)

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/core/decision_trace.py`](../../src/mirrormind/core/decision_trace.py) | Frozen Pydantic v1 result models, local cross-reference/cutoff checks and SHA-256 content binding for a supplied human-review record; no authentication or action authorization |
| [`examples/m1_decision_trace_contract.py`](../../examples/m1_decision_trace_contract.py) | Prints one deterministic, entirely fictional trace with pending human review and declared/unavailable costs |
| [`tests/unit/test_decision_trace.py`](../../tests/unit/test_decision_trace.py) | Valid fixture, reproducibility, reference, temporal, cost, approval-digest and immutability regressions |
| [`docs/engineering/DECISION_TRACE_RESULT.md`](DECISION_TRACE_RESULT.md) | Architecture, fields, data flow, digest algorithm, failure behavior, reproducible example, tests, exercises and limits |
| [`docs/engineering/changes/M1F_01_DECISION_TRACE_CONTRACT.md`](changes/M1F_01_DECISION_TRACE_CONTRACT.md) | M1F-01 scope, acceptance criteria, impact map and evidence record |

The capability remains `interface_only`; `decision_evaluation` remains
`planned`. The schema neither creates traces nor validates external records.

## 53. Strict WorldKernel request mapping (pure; no execution)

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/modules/simulation/worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py) | Exact retail world/revision allowlist, explicit unit context, strict state/parameter checks and separate operator ceilings; constructs JSON only |
| [`examples/m1e_01_worldkernel_mapping.py`](../../examples/m1e_01_worldkernel_mapping.py) | Reproducible fictional request printer; does not import or execute WorldKernel |
| [`tests/unit/test_worldkernel_mapping.py`](../../tests/unit/test_worldkernel_mapping.py) | Exact request, deterministic limits, version/unit/reference/intervention/value failures and import guard |
| [`docs/engineering/WORLDKERNEL_MAPPING_WALKTHROUGH.md`](WORLDKERNEL_MAPPING_WALKTHROUGH.md) | Architecture, source contract, flow, exercises, diagnostics, test meaning and runtime limits |
| [`docs/engineering/changes/M1E_01_WORLDKERNEL_REQUEST_MAPPING.md`](changes/M1E_01_WORLDKERNEL_REQUEST_MAPPING.md) | M1E-01 scope, explicit acceptance, impact map and evidence |
| [`docs/engineering/CHANGE_REQUEST_TEMPLATE.md`](CHANGE_REQUEST_TEMPLATE.md) | Reusable required-scope template referenced by the engineering workflow |

The mapper itself does not execute the request or prove `demo-1` identifies
immutable code. The following local runtime is a separate experimental path.

## 54. Optional pinned local WorldKernel execution (experimental)

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/modules/simulation/worldkernel_runner.py`](../../src/mirrormind/modules/simulation/worldkernel_runner.py) | `LocalWorldKernelGateway`, `run_worldkernel_scenario`; revalidate/map, enforce local timeout and bounded output, validate exact result/inventory balance and form a provenance-bound summary |
| [`src/mirrormind/modules/simulation/worldkernel_worker.py`](../../src/mirrormind/modules/simulation/worldkernel_worker.py) | One-shot optional worker; verifies distribution version and exact VCS origin, registers upstream built-ins plus one fixed code-owned policy world and calls strict registered-revision execution |
| [`pyproject.toml`](../../pyproject.toml) | Optional `worldkernel` extra pinned to one reviewed full source commit; no core dependency |
| [`examples/m1e_02_worldkernel_local_runner.py`](../../examples/m1e_02_worldkernel_local_runner.py) | Reproducible fictional scenario; prints a local conditional summary and performs no input-file or network access |
| [`tests/unit/test_worldkernel_runner.py`](../../tests/unit/test_worldkernel_runner.py) | Synthetic fake-worker protocol, pin metadata, result/balance, timeout, output and missing-runtime regressions |
| [`tests/integration/test_worldkernel_runner_engine.py`](../../tests/integration/test_worldkernel_runner_engine.py) | Executes the actual optional engine only when exact package metadata pin is installed; otherwise skips |
| [`docs/engineering/WORLDKERNEL_GATEWAY_GATE.md`](WORLDKERNEL_GATEWAY_GATE.md) | Runtime architecture, contracts, installation, security boundaries, reproduction and residual acceptance gates |
| [`docs/engineering/changes/M1E_02_WORLDKERNEL_LOCAL_RUNTIME.md`](changes/M1E_02_WORLDKERNEL_LOCAL_RUNTIME.md) | Scoped M1E-02 change request, impact map and exact-head evidence |

The M1E-02 local path executes the upstream `retail.inventory.demo@demo-1`
example at the exact WorldKernel source pin. M1E-04's separate code-owned
policy handler is described below. Neither is an HTTP capability, hostile-code
sandbox or production service. The API remains bootable with the optional
package absent.


## 55. Synthetic retail policy comparison (test double only)

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/policy_simulation.py`](../../src/mirrormind/domains/retail/policy_simulation.py) | Validates bounded 28-day assumptions, generates paired seeded demand streams, applies three replenishment rules and reports lead-time sensitivity; no forecast, ranking or external engine |
| [`examples/m1_retail_policy_test_double.py`](../../examples/m1_retail_policy_test_double.py) | Prints a deterministic fictional policy-comparison report; no real data or network access |
| [`tests/unit/test_retail_policy_simulation.py`](../../tests/unit/test_retail_policy_simulation.py) | Tests deterministic streams, policy outcomes, metric accounting, invalid inputs, bounded work and the optional-engine import boundary |
| [`tests/integration/test_retail_policy_simulation_cli.py`](../../tests/integration/test_retail_policy_simulation_cli.py) | Replays the no-argument CLI and checks the local-only/no-selection contract |
| [`docs/engineering/M1_RETAIL_POLICY_SIMULATION.md`](M1_RETAIL_POLICY_SIMULATION.md) | Walkthrough, assumptions, algorithms, flow, examples, test evidence, safety, debugging and learning exercises |
| [`docs/engineering/changes/M1E_03_SYNTHETIC_POLICY_TEST_DOUBLE.md`](changes/M1E_03_SYNTHETIC_POLICY_TEST_DOUBLE.md) | M1E-03 scoped change request, acceptance criteria, impact map and partial-delivery boundary |

`local_retail_policy_test_double` is experimental. It does not satisfy the
M1E-02 actual WorldKernel engine gate or produce an operational decision.

## 56. WorldKernel-backed synthetic policy world (experimental, local CLI only)

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/domains/retail/worldkernel_policy_world.py`](../../src/mirrormind/domains/retail/worldkernel_policy_world.py) | Fixed registered handler; one shared random demand draw advances all policies and lead-time cases through the common M1E-03 transition |
| [`src/mirrormind/modules/simulation/worldkernel_policy_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_policy_mapping.py) | Strict policy contract mapping with exact world/version and operator fan-out bounds before launch |
| [`src/mirrormind/modules/simulation/worldkernel_policy_gateway.py`](../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py) | Validates engine final states, paired streams and metrics against the synthetic reference before returning engine-derived outcomes |
| [`tests/unit/test_worldkernel_policy_world.py`](../../tests/unit/test_worldkernel_policy_world.py) | Synthetic contract, limit-before-launch, handler parity, fixed registration and malformed result regressions |
| [`tests/integration/test_worldkernel_policy_world_engine.py`](../../tests/integration/test_worldkernel_policy_world_engine.py) | Exact-pin engine parity and end-to-end explicit CLI execution; skips if the reviewed optional package is absent |
| [`docs/engineering/WORLDKERNEL_POLICY_WORLD.md`](WORLDKERNEL_POLICY_WORLD.md) | Architecture, state transition, contract, security, failure modes, reproductions, tests and learning exercises |
| [`docs/engineering/changes/M1E_04_WORLDKERNEL_POLICY_WORLD.md`](changes/M1E_04_WORLDKERNEL_POLICY_WORLD.md) | M1E-04 scope, acceptance criteria, impact map and exact-head evidence |
| [`docs/engineering/datasets/UCI_ONLINE_RETAIL_EVENT_TIME_CARD.md`](datasets/UCI_ONLINE_RETAIL_EVENT_TIME_CARD.md) | Approved source scope, dataset semantics, missingness discrepancy, privacy controls and group-limit stop; no empirical score |

The experimental handler is available only through explicit local CLI
composition. The API and default CLI remain on the in-process test double.
Exact parity on fictional input is not evidence of real forecasts, source
permission, policy optimality, hostile-code isolation or production safety.

## 57. Synthetic retail decision workflow (experimental, no action authority)

| Tracked path | Function / review boundary |
| --- | --- |
| [`src/mirrormind/api/routes/decisions.py`](../../src/mirrormind/api/routes/decisions.py) | Exposes one bounded synthetic workflow request and the same service result; no authentication, upload, persistence or business write |
| [`src/mirrormind/domains/retail/synthetic_fixtures.py`](../../src/mirrormind/domains/retail/synthetic_fixtures.py) | Builds deterministic fictional workbook bytes and declared releases while preserving M1C-01 fixture defaults |
| [`src/mirrormind/domains/retail/synthetic_decision_workflow.py`](../../src/mirrormind/domains/retail/synthetic_decision_workflow.py) | Applies strict request bounds and release checks, composes existing evaluation/diagnostics, fixed seasonal profile, trusted local comparator and M1F-01 trace; API omits the comparator |
| [`examples/m1_retail_decision_workflow.py`](../../examples/m1_retail_decision_workflow.py) | Runs the same fictional service with bounded date, seed, replication and explicit engine options; the default is the policy test double |
| [`tests/unit/test_synthetic_decision_workflow.py`](../../tests/unit/test_synthetic_decision_workflow.py) | Proves trace references/gaps, post-cutoff noninfluence, missing/late abstention before simulation and strict request bounds |
| [`tests/integration/test_retail_synthetic_decision_workflow_cli.py`](../../tests/integration/test_retail_synthetic_decision_workflow_cli.py) | Replays CLI output byte-for-byte and checks the no-action result contract |
| [`docs/engineering/M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md`](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) | Source walkthrough, sequence diagram, contracts, cutoffs, examples, tests, limits, diagnostics and exercises |
| [`docs/engineering/model_cards/SYNTHETIC_RETAIL_DECISION_WORKFLOW.md`](model_cards/SYNTHETIC_RETAIL_DECISION_WORKFLOW.md) | Records the synthetic baseline and evaluation scope; explicitly does not establish predictive performance or calibrated uncertainty |
| [`docs/engineering/changes/M1F_02_SYNTHETIC_DECISION_WORKFLOW.md`](changes/M1F_02_SYNTHETIC_DECISION_WORKFLOW.md) | Change request, acceptance criteria, impact map, compatibility and implementation evidence |
| [`docs/engineering/changes/M1F_03_ENGINE_EXECUTION_PROVENANCE.md`](changes/M1F_03_ENGINE_EXECUTION_PROVENANCE.md) | Versioned trace change request, selected-engine/parity contract, exact-pin regressions and gate evidence |

`synthetic_retail_decision_workflow` is experimental. The generated fixture
is not authorized data; the seasonal profile is not an empirical forecast;
the residual diagnostic is uncalibrated; and the policy test double is not
WorldKernel. The trace supports inspection and replay only, not approval,
ranking, persistence or operational action.

## 58. UCI event-time retrospective and source preflight (experimental)

| Tracked path | Reviewed responsibility |
| --- | --- |
| [`src/mirrormind/domains/retail/uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py) | Freezes the `StockCode`-category cohort from fit dates, uses fixed validation/holdout origins, requires declared complete dates, abstains on unknown coverage and emits ordinal-only category summaries |
| [`src/mirrormind/domains/retail/uci_xlsx_xml.py`](../../src/mirrormind/domains/retail/uci_xlsx_xml.py) | Bounded Expat OOXML reader disables Python character callbacks for excluded cell content, captures only header/approved fields, and rejects unsupported XML structure |
| [`examples/m1_uci_event_time_research.py`](../../examples/m1_uci_event_time_research.py) | Creates a deterministic fictional workbook in memory and runs the bounded parser/evaluator without source download or persistent data files |
| [`tests/unit/test_uci_event_time.py`](../../tests/unit/test_uci_event_time.py) | Covers fixed split/cohort, coverage and missing-date abstention, zero-safe metrics, holdout noninterference, validation and output minimization |
| [`tests/integration/test_uci_event_time_cli.py`](../../tests/integration/test_uci_event_time_cli.py) | Replays the generated CLI and verifies deterministic parsing, cancellation/quantity classification and honest limitations |
| [`docs/engineering/M1_UCI_EVENT_TIME_RESEARCH.md`](M1_UCI_EVENT_TIME_RESEARCH.md) | Explains source/event-time boundaries, data flow, algorithms, metric eligibility, examples, errors, tests and learning exercises |
| [`docs/engineering/changes/M1B_01_UCI_EVENT_TIME_PILOT.md`](changes/M1B_01_UCI_EVENT_TIME_PILOT.md) | Defines scope, impact map, acceptance criteria and source-specific approval boundary |
| [`docs/engineering/changes/M1B_01_UCI_REAL_SOURCE_PILOT.md`](changes/M1B_01_UCI_REAL_SOURCE_PILOT.md) | Owner-approved local source scope, reviewed limits, privacy/retention requirements, impact map and current group-cap stop |
| [`docs/engineering/datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md`](datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md) | Describes generated rows and fixture limits; no original source bytes or permission claims |
| [`docs/engineering/datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json`](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json) | Path-free source hashes, acquisition/preflight metadata, privacy discrepancy, bounded profile, failed projection state and deletion deadline |
| [`docs/engineering/datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md`](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) | Official source/license review, owner-approved local scope, parser limits, Census separation and evidence boundaries |
| [`docs/engineering/datasets/UCI_ONLINE_RETAIL_EVENT_TIME_CARD.md`](datasets/UCI_ONLINE_RETAIL_EVENT_TIME_CARD.md) | UCI source semantics, approved projection, temporal protocol and current no-score status |
| [`docs/engineering/model_cards/SYNTHETIC_UCI_EVENT_TIME.md`](model_cards/SYNTHETIC_UCI_EVENT_TIME.md) | Records fixed splits, matched baselines and metric rules; makes no empirical or uncertainty claim |
| [`docs/engineering/CENSUS_ALFRED_VINTAGE_PROTOCOL.md`](CENSUS_ALFRED_VINTAGE_PROTOCOL.md) | Keeps the independent aggregate release-vintage proposal separate from SKU demand and UCI event-time evaluation |

Automated evaluation remains synthetic-only. The approved #352 snapshot
passed metadata preflight, but the corrected parser refused after exceeding
the 250,000-group cap; the path-free manifest records that stop. No empirical
metrics or complete exclusion counts exist. The evaluator does not infer
publication time from `InvoiceDate`, authenticate a source manifest or prove
ledger completeness or predictive performance.

## 59. Synthetic aggregate Census vintage selector (experimental)

| Tracked path | Reviewed responsibility |
| --- | --- |
| [`src/mirrormind/domains/retail/census_vintages.py`](../../src/mirrormind/domains/retail/census_vintages.py) | Provides immutable normalized vintage records and a bounded, pure date-only as-of selector; preserves release IDs and digest strings without authenticating source bytes |
| [`tests/unit/test_census_vintages.py`](../../tests/unit/test_census_vintages.py) | Regresses strict release cutoff, revision selection, missing history, duplicate ambiguity, metadata conflicts, malformed values, mixed series and input budgets |
| [`docs/engineering/CENSUS_VINTAGE_ADAPTER.md`](CENSUS_VINTAGE_ADAPTER.md) | Walks through the contract, algorithm, data flow, failure boundaries, examples, test evidence and learning exercises |
| [`docs/engineering/datasets/SYNTHETIC_CENSUS_VINTAGES.md`](datasets/SYNTHETIC_CENSUS_VINTAGES.md) | Identifies every fixture value as fictional and records that no real source rights, snapshot or retention has been reviewed |
| [`docs/engineering/changes/M1B_04_CENSUS_VINTAGE_ADAPTER.md`](changes/M1B_04_CENSUS_VINTAGE_ADAPTER.md) | Defines the bounded change request, acceptance criteria, impact map and evidence for a local synthetic-only adapter |

The selector consumes caller-supplied normalized records in memory. It makes no
source request, reads no file or credential, and cannot establish source
authenticity, permission, completeness or forecast eligibility.

## 60. Synthetic aggregate Census vintage evaluation (experimental)

| Tracked path | Reviewed responsibility |
| --- | --- |
| [src/mirrormind/domains/retail/census_evaluation.py](../../src/mirrormind/domains/retail/census_evaluation.py) | Selects each origin's visible vintage and computes fixed matched monthly baselines, reason-specific abstention and privacy-limited lineage |
| [tests/unit/test_census_vintage_evaluation.py](../../tests/unit/test_census_vintage_evaluation.py) | Regresses strict origin cutoffs, revisions, first-estimate labels, horizons, zero-safe metrics, missing history and malformed origin schedules |
| [tests/integration/test_census_vintage_evaluation_cli.py](../../tests/integration/test_census_vintage_evaluation_cli.py) | Replays fictional validation and holdout commands and checks deterministic, disjoint, minimized output |
| [examples/m1_census_vintage_evaluation.py](../../examples/m1_census_vintage_evaluation.py) | Generates an in-memory 21-month aggregate series, one later revision and fixed non-overlapping synthetic origin splits |
| [docs/engineering/CENSUS_VINTAGE_EVALUATION.md](CENSUS_VINTAGE_EVALUATION.md) | Explains the source walk, contract, baselines, metric rules, receipt, tests, diagnostics and exercises |
| [docs/engineering/model_cards/SYNTHETIC_CENSUS_VINTAGE_EVALUATION.md](model_cards/SYNTHETIC_CENSUS_VINTAGE_EVALUATION.md) | Records synthetic split semantics, fixed baselines, no empirical results and real-source review gates |
| [docs/engineering/changes/M1C_04_CENSUS_SYNTHETIC_VINTAGE_EVALUATION.md](changes/M1C_04_CENSUS_SYNTHETIC_VINTAGE_EVALUATION.md) | Defines the scoped evaluator change, impact map, acceptance and evidence boundary |

The evaluator fingerprints normalized inputs and each selected vintage for
replay, but these digests do not verify publisher bytes or grant rights.
Missing targets, visible targets and incomplete history remain explicit
abstentions. No real source parser or production forecast capability is added.

## 61. Permission-filtered fictional evidence retrieval (experimental)

| Tracked path | Reviewed responsibility |
| --- | --- |
| [`src/mirrormind/modules/retrieval/__init__.py`](../../src/mirrormind/modules/retrieval/__init__.py) | Namespace only; no import-time indexing or network activity |
| [`src/mirrormind/modules/retrieval/contracts.py`](../../src/mirrormind/modules/retrieval/contracts.py) | Strict bounded retrieval contracts; recomputes exact UTF-8 excerpt digest during result validation |
| [`src/mirrormind/modules/retrieval/fictional_fixture.py`](../../src/mirrormind/modules/retrieval/fictional_fixture.py) | Generated corpus and fixed demo principal/collection |
| [`src/mirrormind/modules/retrieval/index.py`](../../src/mirrormind/modules/retrieval/index.py) | Scope-first in-memory BM25 ranking, stable ties and exact citation spans |
| [`src/mirrormind/modules/retrieval/evaluation.py`](../../src/mirrormind/modules/retrieval/evaluation.py) | Bounded per-case scope-first synthetic evaluation; verifies citation lineage/span/digest and emits query-free aggregate metrics |
| [`examples/m2_evidence_retrieval.py`](../../examples/m2_evidence_retrieval.py) | Bounded deterministic CLI over fictional text; no route, writes or arbitrary file access |
| [`examples/m2_evidence_retrieval_evaluation.py`](../../examples/m2_evidence_retrieval_evaluation.py) | Replays the fixed synthetic evaluation set and emits a deterministic query-free JSON report |
| [`tests/unit/test_evidence_retrieval.py`](../../tests/unit/test_evidence_retrieval.py) | Scope-before-tokenization, citation integrity, deterministic ranking, bounds and untrusted-text regressions |
| [`tests/integration/test_m2_evidence_retrieval_cli.py`](../../tests/integration/test_m2_evidence_retrieval_cli.py) | CLI replay, citation presence, query omission and oversized-input failure |
| [`tests/unit/test_evidence_retrieval_evaluation.py`](../../tests/unit/test_evidence_retrieval_evaluation.py) | Metric arithmetic, bounded-input/type rejection, hidden/unknown-hit redaction, scope validation, exact result/top-k contracts and citation support regressions |
| [`tests/integration/test_m2_evidence_retrieval_evaluation_cli.py`](../../tests/integration/test_m2_evidence_retrieval_evaluation_cli.py) | Deterministic query-free evaluator CLI replay and metric schema regression |
| [`docs/engineering/M2_EVIDENCE_RETRIEVAL.md`](M2_EVIDENCE_RETRIEVAL.md) | Source walkthrough, contracts, BM25, safety, reproduction, tests and exercises |
| [`docs/engineering/changes/M2_01_PERMISSION_FILTERED_EVIDENCE_RETRIEVAL.md`](changes/M2_01_PERMISSION_FILTERED_EVIDENCE_RETRIEVAL.md) | Scoped acceptance criteria, impact map, compatibility and evidence |
| [`docs/engineering/changes/M2_02_RETRIEVAL_EVALUATION.md`](changes/M2_02_RETRIEVAL_EVALUATION.md) | M2-02 scope, acceptance criteria, impact map, constraints, and evidence record |

The capability is experimental. Its access context is a caller assertion,
not authenticated identity; `evidence_and_rag` remains planned and no real
source permission or retrieval route is provided.

## Continuous engineering handoff and execution register

| Tracked document | Reviewed responsibility |
| --- | --- |
| [`MASTER_EXECUTION_PLAN.md`](MASTER_EXECUTION_PLAN.md) | Cross-milestone dependency order, intended architecture, delivery focus and document ownership |
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Dated commit-pinned implementation and verification baseline; not live status |
| [`TASK_BACKLOG.md`](TASK_BACKLOG.md) | Stable task IDs, priorities, dependencies, acceptance slices and claims |
| [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md) | Work-item and milestone acceptance, verification and owner review requirements |
| [`BLOCKERS.md`](BLOCKERS.md) | External dependency, approval evidence, decision owner and safe independent work |
| [`CODEX_HANDOFF.md`](CODEX_HANDOFF.md) | Safe parallel work, source walkthrough and learning standard, resume instructions |

These are engineering planning and navigation documents. They do not
add a runtime capability or authorize real ingestion, deployment,
forecast claims or cross-repository changes.

## Public portfolio entrypoints

- [README.md](../../README.md): English public overview, executable synthetic demo and live CI.
- [README.pt-BR.md](../../README.pt-BR.md): Brazilian Portuguese counterpart with identical demo and evidence boundaries.

## Public portfolio visuals and community policies

- [Architecture artwork](../assets/mirrormind-architecture.svg): editable static SVG of reviewed experimental boundaries.
- [Synthetic comparison artwork](../assets/mirrormind-synthetic-comparison.svg): measured fictional CLI example; no decision ranking.
- [CONTRIBUTING.md](../../CONTRIBUTING.md): reporting and contribution boundaries under Apache-2.0.
- [SECURITY.md](../../SECURITY.md): private disclosure channel and experimental support limits.

## Public licensing

- [LICENSE](../../LICENSE): standard Apache-2.0 license text for original project material.
- [Third-party licensing](../THIRD_PARTY.md): dependency metadata and separate engine/data boundaries.

## Local interactive portfolio report

- [Generator](../../examples/m2_portfolio_demo.py): bounded request, exact result embedding and explicit new HTML file.
- [HTML template](../../examples/portfolio_demo.html): offline client-side exploration of precomputed cases.
- [Report tests](../../tests/integration/test_portfolio_demo.py): exact JSON, escaping and failure contracts.
- [Report guide](PORTFOLIO_DEMO.md) and [change request](changes/PORT_07_LOCAL_INTERACTIVE_REPORT.md): walkthrough, limits and acceptance.

## First public alpha release

- [Changelog](../../CHANGELOG.md): source-release scope and limitations.
- [Alpha release guide](ALPHA_RELEASE.md): version alignment, reproduction and evidence.

## Repository Excellence

- [REX plan](REPOSITORY_EXCELLENCE.md): independent maintenance track.
- [Branch inventory](REX_BRANCH_AUDIT.md): exact-head snapshot and deletion safety boundaries.

- [REX CI governance](REX_CI_GOVERNANCE.md): workflow triggers, compatibility, least privilege and main protection policy.

## Security and community workflow

- [REX security and community](REX_SECURITY_COMMUNITY.md): free security settings and review scope.
- [Bug template](../../.github/ISSUE_TEMPLATE/bug_report.md), [feature template](../../.github/ISSUE_TEMPLATE/feature_request.md), [research template](../../.github/ISSUE_TEMPLATE/research_proposal.md), [issue configuration](../../.github/ISSUE_TEMPLATE/config.yml).
- [PR template](../../.github/pull_request_template.md): integration evidence and boundaries.

## Quality and packaging

- [Repository quality workflow](../../.github/workflows/quality.yml): coverage, scoped strict typing and wheel smoke.
- [REX quality and packaging](REX_QUALITY_PACKAGING.md): measured baseline and reproduction limits.

## Public portal

- [Portal builder](../../examples/build_portfolio_site.py), [landing template](../assets/portfolio_site.html) and [contract tests](../../tests/integration/test_portfolio_site.py): allowlisted synthetic site.
- [Pages workflow](../../.github/workflows/pages.yml) and [deployment guide](REX_PUBLIC_PORTAL.md): scoped build and manual main deployment.

## Research maintenance

- [Benchmark](../../examples/synthetic_benchmark.py), [release rehearsal](../../examples/prepare_alpha_release.py), [tests](../../tests/integration/test_research_maintenance.py), [workflow](../../.github/workflows/research-maintenance.yml) and [guide](REX_BENCHMARK_RELEASE.md).

## Developer experience

- [Developer quick start](DEVELOPER_QUICK_START.md): clean public checkout, validation and local container workflow.
- [Docker context allowlist](../../.dockerignore): restricted local image inputs.

- [REX quality floor change](changes/REX_QUALITY_FLOOR.md): bounded coverage and type-narrowing follow-up.

## M2-03 bounded local tool orchestration

- [Package boundary](../../src/mirrormind/modules/agents/__init__.py): no import-time provider or route.
- [Typed contracts](../../src/mirrormind/modules/agents/contracts.py): bounded provider, tool and report values.
- [Immutable tool registry](../../src/mirrormind/modules/agents/registry.py): exact input/output validation and digest receipts.
- [Synthetic tool adapters](../../src/mirrormind/modules/agents/synthetic_tools.py): existing fictional retrieval and M1F-02 workflow only.
- [Bounded orchestrator](../../src/mirrormind/modules/agents/orchestrator.py): sequential scripted-provider control loop; revalidates exact provider turns from plain data so nested Pydantic `model_copy(update=...)` changes fail closed before dispatch.
- [Reproducible example](../../examples/m2_bounded_tool_orchestration.py): local deterministic CLI.
- [Unit regressions](../../tests/unit/test_bounded_tool_orchestration.py): failure paths, budgets, scope, prompt injection, receipt limits and nested provider-turn revalidation.
- [CLI integration regression](../../tests/integration/test_m2_tool_orchestration_cli.py): output minimization and deterministic replay.
- [Technical and learning walkthrough](M2_TOOL_ORCHESTRATION.md): architecture, contracts, data flow, security, tests and exercises.
- [Scoped change request](changes/M2_03_BOUNDED_TOOL_ORCHESTRATION.md): acceptance criteria and impact map.

- [Public dependency input](../../requirements/public-dev.in), [hash lock](../../requirements/public-dev.txt), [input drift checker](../../scripts/check_public_lock.py): reproducible public developer environment.

- [Public lock tests](../../tests/unit/test_public_lock.py): input drift and private-source exclusion.

### M1C-04 descriptive follow-up

| Path | Responsibility |
|---|---|
| [docs/engineering/changes/M1C_04_CENSUS_DESCRIPTIVE.md](changes/M1C_04_CENSUS_DESCRIPTIVE.md) | Scoped experimental paired-loss receipt, acceptance and impact map |

### Census split preparation

| Path | Responsibility |
|---|---|
| [src/mirrormind/domains/retail/census_split.py](../../src/mirrormind/domains/retail/census_split.py) | Experimental schedule fingerprint, split boundaries and descriptive evaluation wrapper |
| [tests/unit/test_census_split.py](../../tests/unit/test_census_split.py) | Synthetic partition, fingerprint, embargo and replay regressions |
| [docs/engineering/changes/M1C_04_CENSUS_FROZEN_SPLIT.md](changes/M1C_04_CENSUS_FROZEN_SPLIT.md) | Scoped acceptance and impact map |

### Census experiment preparation

| Path | Responsibility |
|---|---|
| [src/mirrormind/domains/retail/census_experiment.py](../../src/mirrormind/domains/retail/census_experiment.py) | Pure fictional experiment commitment and exact receipt replay |
| [tests/unit/test_census_experiment.py](../../tests/unit/test_census_experiment.py) | Synthetic commitment, replay and forgery regressions |
| [docs/engineering/changes/M1C_04_CENSUS_EXPERIMENT.md](changes/M1C_04_CENSUS_EXPERIMENT.md) | Scoped acceptance and impact map |
