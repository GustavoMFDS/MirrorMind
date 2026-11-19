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
| [`src/mirrormind/core/__init__.py`](../../src/mirrormind/core/__init__.py) | I | Core package marker |
| [`src/mirrormind/core/contracts.py`](../../src/mirrormind/core/contracts.py) | G | Versioned Pydantic fields and two cross-field rules; [contracts walkthrough](CONTRACT_WALKTHROUGH.md) |
| [`src/mirrormind/domains/__init__.py`](../../src/mirrormind/domains/__init__.py) | I | Domain package only; no automatic sector adapter |
| [`src/mirrormind/domains/retail/__init__.py`](../../src/mirrormind/domains/retail/__init__.py) | I | Retail namespace without source acquisition |
| [`src/mirrormind/domains/retail/calendar_coverage.py`](../../src/mirrormind/domains/retail/calendar_coverage.py) | G | Strict caller-declared date schedule compared with positive-line observations; [guide](DECLARED_CALENDAR_COVERAGE.md), no verified operating calendar |\n| [`src/mirrormind/domains/retail/declared_releases.py`](../../src/mirrormind/domains/retail/declared_releases.py) | G | Hypothetical source-unverified per-product release declarations at retrospective cutoff; [guide](DECLARED_RETAIL_RELEASES.md) |\n| [`src/mirrormind/domains/retail/release_backtest.py`](../../src/mirrormind/domains/retail/release_backtest.py) | G | Fictional positive-line baseline comparison with per-origin abstention and caller-declared releases; [method](RETAIL_RELEASE_BACKTEST.md) |\n| [`src/mirrormind/domains/retail/coverage_gate.py`](../../src/mirrormind/domains/retail/coverage_gate.py) | G | Gate conditional fictional model ranking on exact scored-origin coverage; no calibrated uncertainty; [guide](RETAIL_COVERAGE_GATE.md) |\n| [`src/mirrormind/domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py) | G | Retrospective maximum-absolute-residual envelope with strict past-publication checks; no calibration guarantee; [guide](RETAIL_RESIDUAL_ENVELOPE.md) |\n| [`src/mirrormind/domains/retail/eligibility_drift.py`](../../src/mirrormind/domains/retail/eligibility_drift.py) | G | Adjacent-window eligible-origin and abstention counts at distinct cutoffs; source-unverified; [guide](RETAIL_ELIGIBILITY_DRIFT.md) |\n| [`src/mirrormind/domains/retail/eligible_values.py`](../../src/mirrormind/domains/retail/eligible_values.py) | G | Gated mean/median comparison on observed eligible fictional retail proxies, no actual distribution shift claim; [guide](RETAIL_ELIGIBLE_VALUES.md) |\n| [`src/mirrormind/domains/retail/selection_sensitivity.py`](../../src/mirrormind/domains/retail/selection_sensitivity.py) | G | Bounded fictional excluded-date counterfactual scenarios with explicit unverifiable ceiling; [guide](RETAIL_SELECTION_SENSITIVITY.md) |\n| [`src/mirrormind/domains/retail/coverage.py`](../../src/mirrormind/domains/retail/coverage.py) | G | Internal positive-line product-day calendar gaps, aggregate-only and no imputation; [reviewed guide](RETAIL_COVERAGE.md) |\n| [`src/mirrormind/domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py) | G | Bounded transaction-to-day positive-unit projection on fictional mappings; [source walkthrough](UCI_RETAIL_PROJECTION.md) |
| [`src/mirrormind/domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py) | G | Optional bounded local UCI-shaped XLSX reader; [source guide](UCI_WORKBOOK_READER.md), **not authorized real-file ingestion** |
| [`src/mirrormind/modules/__init__.py`](../../src/mirrormind/modules/__init__.py) | I | Feature module namespace |
| [`src/mirrormind/modules/evidence/__init__.py`](../../src/mirrormind/modules/evidence/__init__.py) | I | Evidence package marker; no connectors or authorization |
| [`src/mirrormind/modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py) | G | Strict local staging/as-of semantics in [M1 snapshot guide](M1_LOCAL_CSV_STAGING.md); no approved ingestion |
| [`src/mirrormind/modules/forecasting/__init__.py`](../../src/mirrormind/modules/forecasting/__init__.py) | I | Offline forecast module marker, no model registry |
| [`src/mirrormind/modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py) | G | Matched one-step staged rolling origin baselines and abstentions; [method guide](M1_STAGED_ROLLING_BASELINES.md) |
| [`src/mirrormind/modules/simulation/__init__.py`](../../src/mirrormind/modules/simulation/__init__.py) | I | Simulation module namespace |
| [`src/mirrormind/modules/simulation/gateway.py`](../../src/mirrormind/modules/simulation/gateway.py) | R | `SimulationGateway` Protocol and `SimulationSummary` model, **no live adapter**; [API guide](API_WALKTHROUGH.md) |

## Capability readiness — do not confuse existence with deployment

| Capability | Current status | Evidence needed before promotion |
| --- | --- | --- |
| Health endpoint | Implemented in scaffold | Actual endpoint regression; not a dependency readiness probe |
| Scenario contract shape and two cross-field rules | Implemented validation only | Pydantic unit and API tests; still no authorization or execution |
| SimulationGateway Protocol | Interface only | A concrete adapter, translation/compatibility tests and engine execution |
| WorldKernel execution | Planned | Optional pinned adapter, trusted world registry, budgets, actual results |
| Evidence ingestion/RAG | Planned | Permission checks, provenance, retention, source-specific tests |
| Forecasting | Planned | Temporal holdout, leakage prevention, baselines, uncertainty evaluation |
| Agentic workflow | Planned | Tool privilege boundaries, approval and cost limits, audit |
| Decision evaluation | Planned | Reproducible objectives/assumptions and comparison outputs |
| Tenant isolation/production auth | Planned | Threat model, authorization tests, audit and security review |

**No function in the repository currently provides** live forecasting,
retrieval, data connectors, autonomous actions, verified business
provenance, budgeted simulation execution or production-grade security.
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

The reviewed capability ledger declares
`synthetic_observation_preflight` `experimental`;
all live evidence/RAG and forecasting capabilities remain
`planned`. The generated catalog still indexes the
11 production source modules; example scripts are navigated
through the full repository atlas.

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
The full official file has many more rows
than this reader's cap, and privacy,
attribution and original source identity are
not approved. This feature remains
`local_uci_xlsx_reader` **experimental**;
authorized ingestion and genuine forecasting
stay planned.
