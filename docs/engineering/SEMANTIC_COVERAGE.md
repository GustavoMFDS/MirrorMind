# Semantic learning and implementation status — source-reviewed map

This matrix separates **implemented methods** from **interface-only**
and **planned** work. It is a qualitative learning map, not a percentage
of source, assertion, or business correctness coverage. All 11 current
Python source files appear in the generated
[source catalog](generated/SYMBOLS.md) and the
[linked repository atlas](REPOSITORY_ATLAS.md).

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
| [`src/mirrormind/modules/__init__.py`](../../src/mirrormind/modules/__init__.py) | I | Feature module namespace |
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
