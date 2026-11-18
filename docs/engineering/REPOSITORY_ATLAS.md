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
