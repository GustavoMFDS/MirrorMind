# Semantic learning and implementation status — source-reviewed map

This matrix separates **implemented methods** from **interface-only**
and **planned** work. It is a qualitative learning map, not a percentage
of source, assertion, or business correctness coverage. The generated
[source catalog](generated/SYMBOLS.md) and the
[linked repository atlas](REPOSITORY_ATLAS.md) index the current Python
sources without relying on a manually maintained file-count assertion.

## Labels

- **G — guided:** source-reviewed method/route explanation, example and
  test references exist. This does **not** mean every symbol or path was tested.
- **R — reference / interface only:** a contract or module boundary is
  described, but does not implement the named future capability.
- **I — index only:** small export/namespace files, or future learning
  work, for which the AST index remains the main navigation tool.

| Source module | Level | Current behavior and learning guide |
| --- | :---: | --- |
| [`src/mirrormind/__init__.py`](../../src/mirrormind/__init__.py) | I | Package marker; no automatic execution |
| [`src/mirrormind/api/__init__.py`](../../src/mirrormind/api/__init__.py) | I | Stable `app` export |
| [`src/mirrormind/api/app.py`](../../src/mirrormind/api/app.py) | G | Route composition; [API walkthrough](API_WALKTHROUGH.md) |
| [`src/mirrormind/api/routes/__init__.py`](../../src/mirrormind/api/routes/__init__.py) | I | Package boundary |
| [`src/mirrormind/api/routes/system.py`](../../src/mirrormind/api/routes/system.py) | G | Health and truthful capabilities; [API walkthrough](API_WALKTHROUGH.md) |
| [`src/mirrormind/api/routes/scenarios.py`](../../src/mirrormind/api/routes/scenarios.py) | G | Data validation only; [API walkthrough](API_WALKTHROUGH.md) |
| [`src/mirrormind/api/routes/decisions.py`](../../src/mirrormind/api/routes/decisions.py) | G | Strict experimental route for the generated retail decision workflow; no real ingestion, engine or write path; [API walkthrough](API_WALKTHROUGH.md) |
| [`src/mirrormind/core/__init__.py`](../../src/mirrormind/core/__init__.py) | I | Core package marker |
| [`src/mirrormind/core/contracts.py`](../../src/mirrormind/core/contracts.py) | G | Versioned Pydantic fields and two cross-field rules; [contracts walkthrough](CONTRACT_WALKTHROUGH.md) |
| [`src/mirrormind/core/decision_trace.py`](../../src/mirrormind/core/decision_trace.py) | G | Immutable v1 decision-result contract with local reference, time and review-digest validation; used by one synthetic producer; [walkthrough](DECISION_TRACE_RESULT.md) |
| [`src/mirrormind/domains/__init__.py`](../../src/mirrormind/domains/__init__.py) | I | Domain package only; no automatic sector adapter |
| [`src/mirrormind/domains/retail/__init__.py`](../../src/mirrormind/domains/retail/__init__.py) | I | Retail namespace without source acquisition |
| [`src/mirrormind/domains/retail/calendar_coverage.py`](../../src/mirrormind/domains/retail/calendar_coverage.py) | G | Strict caller-declared date schedule compared with positive-line observations; [guide](DECLARED_CALENDAR_COVERAGE.md), no verified operating calendar |
| [`src/mirrormind/domains/retail/declared_releases.py`](../../src/mirrormind/domains/retail/declared_releases.py) | G | Hypothetical source-unverified per-product release declarations at retrospective cutoff; [guide](DECLARED_RETAIL_RELEASES.md) |
| [`src/mirrormind/domains/retail/release_backtest.py`](../../src/mirrormind/domains/retail/release_backtest.py) | G | Fictional positive-line baseline comparison with per-origin abstention and caller-declared releases; [method](RETAIL_RELEASE_BACKTEST.md) |
| [`src/mirrormind/domains/retail/evaluation_flow.py`](../../src/mirrormind/domains/retail/evaluation_flow.py) | G | Compose a prepared retail evidence flow with fixed matched-origin baselines; [M1 evaluation guide](M1_RETAIL_SYNTHETIC_EVALUATION.md), experimental and source-unverified |
| [`src/mirrormind/domains/retail/policy_simulation.py`](../../src/mirrormind/domains/retail/policy_simulation.py) | G | Own strict synthetic request/assumption contracts, shared day transition and paired seeded comparison for three policies; [M1 guide](M1_RETAIL_POLICY_SIMULATION.md), no forecast, ranking or engine import |
| [`src/mirrormind/domains/retail/coverage_gate.py`](../../src/mirrormind/domains/retail/coverage_gate.py) | G | Gate conditional fictional model ranking on exact scored-origin coverage; no calibrated uncertainty; [guide](RETAIL_COVERAGE_GATE.md) |
| [`src/mirrormind/domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py) | G | Retrospective maximum-absolute-residual heuristic with a fixed pre-holdout calibration target interval, disjoint holdout labels, origin-specific release checks and an independent quadratic oracle; no calibration guarantee; [guide](RETAIL_RESIDUAL_ENVELOPE.md) |
| [`src/mirrormind/domains/retail/eligibility_drift.py`](../../src/mirrormind/domains/retail/eligibility_drift.py) | G | Adjacent-window eligible-origin and abstention counts at distinct cutoffs; source-unverified; [guide](RETAIL_ELIGIBILITY_DRIFT.md) |
| [`src/mirrormind/domains/retail/eligible_values.py`](../../src/mirrormind/domains/retail/eligible_values.py) | G | Gated mean/median comparison on observed eligible fictional retail proxies, no actual distribution shift claim; [guide](RETAIL_ELIGIBLE_VALUES.md) |
| [`src/mirrormind/domains/retail/selection_sensitivity.py`](../../src/mirrormind/domains/retail/selection_sensitivity.py) | G | Bounded fictional excluded-date counterfactual scenarios with explicit unverifiable ceiling; [guide](RETAIL_SELECTION_SENSITIVITY.md) |
| [`src/mirrormind/domains/retail/sensitivity_sweep.py`](../../src/mirrormind/domains/retail/sensitivity_sweep.py) | G | Coverage-gated bounded sweep that reuses two independently cutoff-audited summaries for all ceilings; no genuine demand shift claim; [guide](RETAIL_SENSITIVITY_SWEEP.md) |
| [`src/mirrormind/domains/retail/coverage.py`](../../src/mirrormind/domains/retail/coverage.py) | G | Internal positive-line product-day calendar gaps, aggregate-only and no imputation; [reviewed guide](RETAIL_COVERAGE.md) |
| [`src/mirrormind/domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py) | G | Bounded transaction-to-day positive-unit projection on fictional mappings; [source walkthrough](UCI_RETAIL_PROJECTION.md) |
| [`src/mirrormind/domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py) | G | Optional bounded local UCI-shaped XLSX reader; [source guide](UCI_WORKBOOK_READER.md), **not authorized real-file ingestion** |
| [`src/mirrormind/domains/retail/uci_xlsx_xml.py`](../../src/mirrormind/domains/retail/uci_xlsx_xml.py) | G | Selective bounded OOXML stream parser with excluded-cell character callbacks disabled; [reader guide](UCI_WORKBOOK_READER.md), not hostile-file isolation |
| [`src/mirrormind/domains/retail/uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py) | G | Fixed event-time retrospective over caller-declared synthetic complete dates; [research guide](M1_UCI_EVENT_TIME_RESEARCH.md); no historical publication or point-in-time claim |
| [`src/mirrormind/domains/retail/census_vintages.py`](../../src/mirrormind/domains/retail/census_vintages.py) | G | Pure bounded selector over normalized fictional monthly vintage records; [adapter guide](CENSUS_VINTAGE_ADAPTER.md); no source parser, byte verification, authorization or forecast scoring |
| [`src/mirrormind/domains/retail/evidence_flow.py`](../../src/mirrormind/domains/retail/evidence_flow.py) | G | Experimental composition of bounded CSV/XLSX readers, review-only packets, declared calendar/release checks and CSV as-of selection; [M1 flow guide](M1_SYNTHETIC_EVIDENCE_FLOW.md), no authorization or forecast eligibility |
| [`src/mirrormind/domains/retail/synthetic_fixtures.py`](../../src/mirrormind/domains/retail/synthetic_fixtures.py) | G | Canonical in-memory fictional workbook and release dates reused by examples/API; no external data or publisher proof |
| [`src/mirrormind/domains/retail/synthetic_decision_workflow.py`](../../src/mirrormind/domains/retail/synthetic_decision_workflow.py) | G | Compose synthetic evidence, diagnostics, release-gated profile, selected policy engine and DecisionTrace v2 with outcome-linked selected execution and optional parity evidence; [M1F-02 guide](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md), API remains test-double-only |
| [`src/mirrormind/domains/retail/worldkernel_policy_world.py`](../../src/mirrormind/domains/retail/worldkernel_policy_world.py) | G | Fixed code-owned `mm-retail-policy-v1` handler reuses the tested daily transition across paired policy and lead-time states; [M1E-04 guide](WORLDKERNEL_POLICY_WORLD.md), no request-supplied code or real-data claim |
| [`src/mirrormind/modules/__init__.py`](../../src/mirrormind/modules/__init__.py) | I | Feature module namespace |
| [`src/mirrormind/modules/agents/__init__.py`](../../src/mirrormind/modules/agents/__init__.py) | I | M2-03 local orchestration namespace; no provider or route is created on import |
| [`src/mirrormind/modules/agents/contracts.py`](../../src/mirrormind/modules/agents/contracts.py) | G | Strict request, provider-turn, tool-call, observation, receipt and report contracts with bounded JSON and human-review/non-authorization invariants; [M2-03 walkthrough](M2_TOOL_ORCHESTRATION.md) |
| [`src/mirrormind/modules/agents/registry.py`](../../src/mirrormind/modules/agents/registry.py) | G | Frozen tool definitions, immutable registry, exact input/output validation, canonical JSON digests and size ceilings; no runtime plugin loading; [M2-03 walkthrough](M2_TOOL_ORCHESTRATION.md) |
| [`src/mirrormind/modules/agents/synthetic_tools.py`](../../src/mirrormind/modules/agents/synthetic_tools.py) | G | Two adapters over existing fictional retrieval and M1F-02 workflow; model output is not accepted as forecast/simulation input; [M2-03 walkthrough](M2_TOOL_ORCHESTRATION.md) |
| [`src/mirrormind/modules/agents/orchestrator.py`](../../src/mirrormind/modules/agents/orchestrator.py) | G | Sequential local test-double loop with fixed tool/turn/context budgets, sanitized refusal codes and observed citation-reference membership; no semantic entailment; [M2-03 walkthrough](M2_TOOL_ORCHESTRATION.md) |
| [`src/mirrormind/modules/evidence/__init__.py`](../../src/mirrormind/modules/evidence/__init__.py) | I | Evidence package marker; no connectors or authorization |
| [`src/mirrormind/modules/evidence/atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py) | G | Experimental new shared SQLite file, atomic current policy admission and signed publication CAS; [guide](ATOMIC_GOVERNED_PUBLISHER.md); no external authority or source grant |
| [`src/mirrormind/modules/evidence/operator_governance.py`](../../src/mirrormind/modules/evidence/operator_governance.py) | G | Experimental dual-admin local key policy, expiry and revocation ledger; [guide](OPERATOR_GOVERNANCE.md); not enforced by publisher or externally anchored |
| [`src/mirrormind/modules/evidence/local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py) | G | Local SQLite CAS for externally signed witness and operator commands; [guide](LOCAL_CHECKPOINT_PUBLISHER.md); no independent head/identity or ingestion rights |
| [`src/mirrormind/modules/evidence/authority_transcript.py`](../../src/mirrormind/modules/evidence/authority_transcript.py) | G | Offline linked witness receipts and dual-signed rotation; [guide](AUTHORITY_TRANSCRIPT.md); no live authority, global non-equivocation or authorization |
| [`src/mirrormind/modules/evidence/head_checkpoints.py`](../../src/mirrormind/modules/evidence/head_checkpoints.py) | G | Domain-separated signed checkpoint vs SQLite head and caller-provided sequence; [guide](SIGNED_HEAD_CHECKPOINTS.md); no independent freshness or permission |
| [`src/mirrormind/modules/evidence/sqlite_review_registry.py`](../../src/mirrormind/modules/evidence/sqlite_review_registry.py) | G | Transactional local review log, signed-history revalidation and restart recovery; [guide](SQLITE_REVIEW_REGISTRY.md); no independent head or source permission |
| [`src/mirrormind/modules/evidence/local_review_registry.py`](../../src/mirrormind/modules/evidence/local_review_registry.py) | G | Thread-safe in-process signed event CAS, terminal revocation; [guide](LOCAL_REVIEW_REGISTRY.md); no persistence or authority |
| [`src/mirrormind/modules/evidence/review_decisions.py`](../../src/mirrormind/modules/evidence/review_decisions.py) | G | Offline signed reviewer chain, denial and revocation; [guide](SIGNED_SOURCE_REVIEW.md); no ingestion authorization or trusted registry |
| [`src/mirrormind/modules/evidence/remote_fence_head_protocol.py`](../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py) | G | Shared challenged-head record, signing domain, parser and compact wire encoder; [protocol guide](REMOTE_FENCE_HEAD_CLIENT.md); canonical bytes do not establish remote truth |
| [`src/mirrormind/modules/evidence/remote_fence_head_client.py`](../../src/mirrormind/modules/evidence/remote_fence_head_client.py) | G | Optional fixed-path HTTPS read and local signed-head comparison; [client guide](REMOTE_FENCE_HEAD_CLIENT.md); no deployed authority or access grant |
| [`src/mirrormind/modules/evidence/remote_fence_head_service.py`](../../src/mirrormind/modules/evidence/remote_fence_head_service.py) | G | Experimental in-process signed response over a read-only `Protocol`; [G-01 service guide](REMOTE_FENCE_HEAD_SERVICE.md); no HTTP transport, persistence, authenticated access or independent custody |
| [`src/mirrormind/modules/evidence/intake_review.py`](../../src/mirrormind/modules/evidence/intake_review.py) | G | Bind staged CSV/XLSX digests to caller-declared review refs, never authorize; [guide](SOURCE_INTAKE_REVIEW.md) |
| [`src/mirrormind/modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py) | G | Strict local staging/as-of semantics in [M1 snapshot guide](M1_LOCAL_CSV_STAGING.md); no approved ingestion |
| [`src/mirrormind/modules/retrieval/__init__.py`](../../src/mirrormind/modules/retrieval/__init__.py) | I | Package namespace for the experimental local retrieval slice |
| [`src/mirrormind/modules/retrieval/contracts.py`](../../src/mirrormind/modules/retrieval/contracts.py) | G | Frozen strict query, scope, document and citation contracts; [M2 retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md); caller scope is not authentication |
| [`src/mirrormind/modules/retrieval/fictional_fixture.py`](../../src/mirrormind/modules/retrieval/fictional_fixture.py) | G | Generated fictional documents and a fixed demo scope; [M2 retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md) |
| [`src/mirrormind/modules/retrieval/index.py`](../../src/mirrormind/modules/retrieval/index.py) | G | Scope-first in-memory BM25, deterministic ties and exact citation mapping; [M2 retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md); no persistent or authenticated index |
| [`src/mirrormind/modules/forecasting/__init__.py`](../../src/mirrormind/modules/forecasting/__init__.py) | I | Offline forecast module marker, no model registry |
| [`src/mirrormind/modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py) | G | Matched one-step baselines and a bounded repeated lag-seven profile using the same one-step rule; [method guide](M1_STAGED_ROLLING_BASELINES.md) and [M1F-02 workflow](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) |
| [`src/mirrormind/modules/simulation/__init__.py`](../../src/mirrormind/modules/simulation/__init__.py) | I | Simulation module namespace |
| [`src/mirrormind/modules/simulation/gateway.py`](../../src/mirrormind/modules/simulation/gateway.py) | R | `SimulationGateway` Protocol and `SimulationSummary` model, **no live adapter**; [API guide](API_WALKTHROUGH.md) |
| [`src/mirrormind/modules/simulation/worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py) | G | Pure allowlisted `ScenarioSpec` to WorldKernel v1 request construction with explicit units and operator limits; no execution; [walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md) |
| [`src/mirrormind/modules/simulation/worldkernel_policy_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_policy_mapping.py) | G | Strict revalidation and fixed exchange-v1 mapping for the M1 synthetic policy world; enforces step/run/fan-out limits before launch; [M1E-04 guide](WORLDKERNEL_POLICY_WORLD.md) |
| [`src/mirrormind/modules/simulation/worldkernel_policy_gateway.py`](../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py) | G | Optional local policy executor; validates WorldKernel states/demand streams, records engine and reference result digests, and returns engine-derived metrics only after parity; [M1E-04 guide](WORLDKERNEL_POLICY_WORLD.md), CLI opt-in only |
| [`src/mirrormind/modules/simulation/worldkernel_runner.py`](../../src/mirrormind/modules/simulation/worldkernel_runner.py) | G | Fixed pinned worker launch with timeout/output bounds and strict exchange result validation; [runtime guide](WORLDKERNEL_MAPPING_WALKTHROUGH.md), not a hostile-code sandbox |
| [`src/mirrormind/modules/simulation/worldkernel_worker.py`](../../src/mirrormind/modules/simulation/worldkernel_worker.py) | G | Verifies optional package metadata then registers only fixed trusted worlds; never accepts modules or registration values from request JSON |

## Synthetic Census vintage evaluation

| Source module | Level | Current behavior and learning guide |
| --- | :---: | --- |
| [census_evaluation.py](../../src/mirrormind/domains/retail/census_evaluation.py) | G | Fixed lag-12 and trailing-12 monthly baselines on date-selected fictional vintages; [evaluation guide](CENSUS_VINTAGE_EVALUATION.md); no real-source or empirical forecast claim |

## Capability readiness — do not confuse existence with deployment

| Capability | Current status | Evidence needed before promotion |
| --- | --- | --- |
| Health endpoint | Implemented in scaffold | Actual endpoint regression; not a dependency readiness probe |
| Scenario contract shape and two cross-field rules | Implemented validation only | Pydantic unit and API tests; still no authorization or execution |
| Local retail synthetic evidence flow | Experimental composition only | Generated fixture tests; no real-source rights, publisher provenance, authorized ingestion or API execution |
| Synthetic retail decision workflow | Experimental local CLI/API composition | V2 trace references the selected engine contract and output digest; WorldKernel path separately links parity-oracle evidence and replays deterministically; source and empirical gates remain open |
| SimulationGateway Protocol | Interface only | A concrete executor and validated engine result; pure request translation now has separate unit evidence |
| WorldKernel request mapping | Pure local translation only | A pinned optional SDK adapter, registered-world execution, result validation and runtime failure evidence |
| WorldKernel execution | Experimental local-only | Exact pin, fixed inventory demo and M1 policy worlds, bounded worker, validated results, synthetic parity and local CLI integration; no HTTP, arbitrary handler, CPU/memory sandbox or production claim |
| Evidence ingestion/RAG | Planned | Permission checks, provenance, retention, source-specific tests |
| Forecasting | Planned | Temporal holdout, leakage prevention, baselines, uncertainty evaluation |
| Agentic workflow | Planned | Tool privilege boundaries, approval and cost limits, audit |
| Decision evaluation | Planned | Reproducible objectives/assumptions and comparison outputs |
| Tenant isolation/production auth | Planned | Threat model, authorization tests, audit and security review |

**No function in the repository currently provides** live forecasting,
retrieval, authorized source connectors, autonomous actions, verified business
provenance, service-enforced shared quotas or production-grade security.
A typed reference does not imply its target exists.

## Independent teaching goals

First: follow `POST /v1/scenarios/validate` from
`api/app.py` to `ScenarioSpec.check_budget` and
`tests/integration/test_api.py`. Predict valid, invalid
and *valid but non-executed* cases.

Second: inspect `SimulationGateway.execute` in
`modules/simulation/gateway.py`. Explain why a Python
Protocol signature does not implement or authorize any
engine call. Find the mismatch between `ScenarioSpec`
and WorldKernel's v1 exchange; plan a safe translator
without inventing data, unsupported interventions or model revisions.

Third: for a future evidence/forecast/agent module, record
the caller, input authority, observable output, failure paths,
consent and retention, temporal cutoff, resource budget,
precise regression and a human-review gate **before**
claiming the capability is implemented.

For tracked test references see
[EVIDENCE_MAP.json](EVIDENCE_MAP.json). That map verifies
claim identifiers and test names, **not the semantic truth
of a claimed effect**.

## Initial M1 demonstration outside the production Python package

| Experiment | Status and evidence |
| --- | --- |
| [`examples/m1_observation_preflight.py`](../../examples/m1_observation_preflight.py) | **Experimental** standalone CLI; see [M1_DATA_PREFLIGHT](M1_DATA_PREFLIGHT.md) and [unit tests](../../tests/unit/test_m1_observation_preflight.py). This is **not** a new production `src/mirrormind/modules/evidence` implementation. |
| [`examples/m2_evidence_retrieval.py`](../../examples/m2_evidence_retrieval.py) | **Experimental** deterministic CLI over generated fictional documents; see [M2_EVIDENCE_RETRIEVAL](M2_EVIDENCE_RETRIEVAL.md), [unit tests](../../tests/unit/test_evidence_retrieval.py) and [CLI integration test](../../tests/integration/test_m2_evidence_retrieval_cli.py). It is not authenticated retrieval or RAG. |

The reviewed capability ledger declares
`synthetic_observation_preflight` `experimental`;
all live evidence/RAG and forecasting capabilities remain
`planned`. The generated catalog indexes current Python
declarations; example scripts and the G-01 service boundary are
navigated through the full repository atlas. These index and guide
levels do not imply deployment or operational acceptance.

## M1c local evaluation, not source-model deployment

| Experiment | Reviewed behavior and limitation |
| --- | --- |
| [`examples/m1_temporal_backtest.py`](../../examples/m1_temporal_backtest.py) | **Experimental** source-reviewed one-step rolling evaluation; [guide](M1_TEMPORAL_BACKTEST.md), [synthetic model card](model_cards/SYNTHETIC_WEEKLY_BASELINES.md) and [unit regressions](../../tests/unit/test_m1_temporal_backtest.py). No real-data forecasting module has been added under `src/`. |

The `forecasting` capability remains **planned**; the
new `synthetic_rolling_backtest` is **experimental** and
evaluates exactly two predeclared heuristics on invented data.
Its outcome does not generalize to actual retail demand.

## M1b local as-of availability learning

| Experiment | Scope |
| --- | --- |
| [`examples/m1_availability_preflight.py`](../../examples/m1_availability_preflight.py) | **Experimental** source-backed publication-time gate for generated records; see [guide](M1_AVAILABILITY_PRECHECK.md) and [unit tests](../../tests/unit/test_m1_availability_preflight.py). No verified real source or executable evidence module. |

The `evidence_and_rag` capability remains **planned**;
`synthetic_asof_availability` is a self-contained local
teaching example, not an authorized data ingestion service.

## Per-origin availability-aware synthetic learning

| Experiment | Review boundary |
| --- | --- |
| [`examples/m1_asof_rolling_backtest.py`](../../examples/m1_asof_rolling_backtest.py) | **Experimental** only. Combines the declared two-timestamp gate with one-step lag-7 forecasts, including explicit abstentions. See [source-method guide](M1_ASOF_ROLLING_EVALUATION.md) and [unit tests](../../tests/unit/test_m1_asof_rolling_backtest.py). No real source data or production inference. |

Neither the `forecasting` nor the `evidence_and_rag`
capability is implemented by these teaching scripts.

## Local CSV staging at source level

[`src/mirrormind/modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py)
is a **guided** reusable primitive, not a new
source-authorized Evidence Engine. Read the
[staging guide](M1_LOCAL_CSV_STAGING.md) and
[adverse tests](../../tests/unit/test_evidence_snapshots.py)
to identify byte/row limits, strict headers,
two-date as-of behavior and the receipt's
`not_authorized` status. The API registers
`local_csv_snapshot_preflight` as experimental;
`evidence_and_rag` remains planned.

## First reusable offline baseline evaluator

The [forecasting source](../../src/mirrormind/modules/forecasting/baselines.py)
implements **fixed** temporal comparisons with
[unit regression evidence](../../tests/unit/test_staged_rolling_baselines.py).
Read [the reviewed guide](M1_STAGED_ROLLING_BASELINES.md)
for its documented 4/7 synthetic coverage.
This is only `local_staged_rolling_baselines`
**experimental**; real `forecasting` in the
capability ledger stays **planned** until independent
data/provenance/model validation and a safe deployment
are established.

## Sector-specific schema projection does not authenticate data

The [retail projection source](../../src/mirrormind/domains/retail/uci_transactions.py)
accepts UCI-shaped **already supplied** row mappings, not
`Online Retail.xlsx`. Its [method guide](UCI_RETAIL_PROJECTION.md)
and [unit tests](../../tests/unit/test_uci_retail_projection.py)
explain cancelled/nonpositive lines, bounded
grouping, customer-field minimization and
the deliberately missing publication timestamp.
The capability is `local_uci_transaction_projection`
**experimental** only. Actual authorized ingestion,
historically proven release vintages, deployed
forecasting and simulation remain **planned**.

## Experimental optional XLSX parser is not the entire UCI source pipeline

[`domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py)
provides a **bounded local** XLSX stream reader
that passes only needed transaction fields
into the preexisting projection.
Read [method guide](UCI_WORKBOOK_READER.md),
[fictional data card](datasets/SYNTHETIC_UCI_XLSX_CARD.md)
and [unit security cases](../../tests/unit/test_uci_workbook.py).
The reader defaults remain deliberately small;
explicit caps can represent the catalog's 541,909 rows,
but original bytes have not been tested. Privacy,
attribution and source identity are not approved. This remains
`local_uci_xlsx_reader` **experimental**;
authorized ingestion and genuine forecasting
stay planned.

## Synthetic UCI event-time retrospective

[`domains/retail/uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py)
compares two fixed one-day baselines on a frozen
fit-period product cohort. Matched target eligibility,
declared-date abstention, MAE/RMSE and zero-safe WAPE
are exercised by
[`test_uci_event_time.py`](../../tests/unit/test_uci_event_time.py)
and the
[`synthetic CLI test`](../../tests/integration/test_uci_event_time_cli.py).
This capability is experimental and event-time-only:
`InvoiceDate` does not establish source publication,
and no original UCI records were processed. See the
[dataset card](datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md)
and [model card](model_cards/SYNTHETIC_UCI_EVENT_TIME.md).

## Synthetic aggregate Census vintage selector

[`domains/retail/census_vintages.py`](../../src/mirrormind/domains/retail/census_vintages.py)
validates normalized in-memory records and selects the latest publication
strictly before an exclusive target-release date for each reference month.
It rejects any release dated inside or before its reference month and verifies
anchored revision chronology; the lower bound does not authenticate a real
publisher schedule.
[`test_census_vintages.py`](../../tests/unit/test_census_vintages.py)
checks revisions, same-day leakage rejection, period-close boundaries,
missing-month preservation, malformed metadata and deterministic receipt
behavior. It consumes invented records only, validates digest syntax rather
than source bytes, and keeps
ingestion/forecast authorization false. The [adapter walkthrough](CENSUS_VINTAGE_ADAPTER.md)
is not a Census or ALFRED file/API parser; source rights, archive completeness,
source-specific parsing, target cross-checks and empirical evaluation remain
open under B-01/B-02.

The separate census_evaluation.py consumes these selected vintages at fixed
synthetic origins, uses lag-12 and trailing-12 baselines at horizons 1, 3 and
6, and scores only later first-estimate labels. [Unit tests](../../tests/unit/test_census_vintage_evaluation.py)
cover revisions, same-day exclusion, matched metrics, zero-safe WAPE, split
abstention and no-leakage behavior. The [source walkthrough](CENSUS_VINTAGE_EVALUATION.md)
and [model card](model_cards/SYNTHETIC_CENSUS_VINTAGE_EVALUATION.md) explain
that all scores are fixture arithmetic, not empirical forecasting evidence.
