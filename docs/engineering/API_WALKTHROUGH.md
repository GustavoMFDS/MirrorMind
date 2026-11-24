# FastAPI scaffold by function — truthful capability reporting

This guide traces the implemented methods in
[`api/app.py`](../../src/mirrormind/api/app.py),
[`api/routes/system.py`](../../src/mirrormind/api/routes/system.py),
[`api/routes/scenarios.py`](../../src/mirrormind/api/routes/scenarios.py)
and the [shared contracts](CONTRACT_WALKTHROUGH.md).

## 1. Application composition and route handlers

| Symbol | HTTP behavior | What it does NOT imply |
| --- | --- | --- |
| `mirrormind.api.app:app` | Creates one FastAPI instance; attaches system and scenario routers | Running a worker, starting an agent, retrieving documents or creating a database |
| `system.health()` | `GET /health`, HTTP 200 and `{"status":"ok","service":"mirrormind-api"}` | Readiness of a future datastore/forecast/WorldKernel engine |
| `system.capabilities()` | `GET /v1/capabilities`, reports `status="scaffold"`, two currently implemented API functions, experimental local-library capabilities (including synthetic retail flows and `local_fictional_evidence_retrieval`) and planned capabilities | It does not certify that experimental data are authorized, or that planned modules exist or execute |
| `scenarios.validate_scenario(spec)` | `POST /v1/scenarios/validate`; Pydantic validates v0.1 `ScenarioSpec`, returns a summary with `validated_not_executed` | Forecast, RAG, simulation, approval, audit or budget enforcement |

`mirrormind.api:app` is the stable import expected by uvicorn.
The API layer contains no statistical model or domain-specific
inventory rules. There is **no authentication** in this M0
scaffold, so it must not be exposed as a production API.

## 2. Three requests; three different claims

```bash
python -m uvicorn mirrormind.api:app --host 127.0.0.1 --port 8000
# Then, in a separate local terminal:
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/capabilities
curl -X POST http://127.0.0.1:8000/v1/scenarios/validate \
  -H "Content-Type: application/json" \
  --data @examples/retail-scenario.json
```

The last route returns the word `validated_not_executed`
deliberately. It is a truthful anti-overclaiming signal,
not a task status to poll.

FastAPI generates HTTP 422 for invalid Pydantic body
validation. The scaffold does not currently add a durable
job store, independent authentication/authorization, or
a domain-specific source-validation layer.

## 3. Curated observations (not certifications)

| Claim ID | Test and observed behavior | Limitation |
| --- | --- | --- |
| **MM-API-001** | `tests/integration/test_api.py::test_scenario_validation_only` confirms a valid JSON request returns `validated_not_executed` | It does not prove execution or successful decision support |
| **MM-API-002** | `tests/integration/test_api.py::test_capabilities_do_not_overstate_implementation` verifies the scaffold lists the WorldKernel adapter under `planned` | This test alone does not verify all future capability claims |
| **MM-API-003** | `tests/integration/test_api.py::test_runs_cannot_exceed_budget` returns HTTP 422 for excess declared run count | A rejected request is not evidence of enforced runtime quotas |

The `local_retail_synthetic_evidence_flow` and
`local_retail_evidence_evaluation` labels describe Python library
experiments and a local example CLI only. No evidence payload or evaluation
execution is exposed by an HTTP route. The parity regression
`tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger`
checks that the API's implemented/experimental/planned lists match the
reviewed ledger; matching labels do not establish the semantic truth of a
capability claim. A focused attempt once stalled in the restricted sandbox;
the later canonical gate on M2-01 SHA
`e151f9d9925d83d2b3e27fb88683672a93b48c30` passed this HTTP test as part of
the 720-test suite. See [B-07](BLOCKERS.md) for the bounded environment
history and exact-SHA evidence.

`local_fictional_evidence_retrieval` follows the same library-only boundary:
its fixed demo example uses generated text and a caller-declared scope. There
is no retrieval HTTP route, authentication or real-source authorization.
The broader `evidence_and_rag` capability remains `planned`; see the
[M2 walkthrough](M2_EVIDENCE_RETRIEVAL.md) and [capability ledger](CAPABILITY_LEDGER.json).

```bash
python -m pytest -q tests/integration/test_api.py
python -m ruff check src tests
python scripts/docs/evidence.py --check
```

These are reproduction instructions, **not claims of local execution**
for this docs-only change.

## 4. Gateway is an interface, not an adapter

[`modules/simulation/gateway.py`](../../src/mirrormind/modules/simulation/gateway.py)
declares `SimulationSummary` and a `SimulationGateway` Protocol with
`execute(ScenarioSpec) -> SimulationSummary`. It does not instantiate
WorldKernel, map world revisions, enforce compute budgets or persist results.
The optional future adapter must translate MirrorMind's
`ScenarioSpec(world_type, horizon_days, interventions, evidence, forecast)`
to WorldKernel's independent `worldkernel.simulation.v1` contract,
reject unsupported or fabricated fields, and preserve the
one-way dependency MirrorMind -> WorldKernel.

## 5. Independent exercise

Draw the actual HTTP request graph. For each route
distinguish 200 **liveness**, 200 **validated data**
and 422 **rejected input** from execution readiness,
resource budgets and permissions. Propose one
negative regression before adding a future simulation
route. State which existing source modules would change,
which must remain independent, and what evidence would
be required before `worldkernel_adapter` can be moved
from `planned` to `implemented`.
