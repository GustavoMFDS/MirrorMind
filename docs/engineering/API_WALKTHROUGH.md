# FastAPI scaffold by function — truthful capability reporting

This guide traces the implemented methods in
[`api/app.py`](../../src/mirrormind/api/app.py),
[`api/routes/system.py`](../../src/mirrormind/api/routes/system.py),
[`api/routes/scenarios.py`](../../src/mirrormind/api/routes/scenarios.py)
and [`api/routes/decisions.py`](../../src/mirrormind/api/routes/decisions.py),
plus the [shared contracts](CONTRACT_WALKTHROUGH.md).

## 1. Application composition and route handlers

| Symbol | HTTP behavior | What it does NOT imply |
| --- | --- | --- |
| `mirrormind.api.app:app` | Creates one FastAPI instance; attaches system, scenario and decision routers | Running a worker, starting an agent, retrieving documents or creating a database |
| `system.health()` | `GET /health`, HTTP 200 and `{"status":"ok","service":"mirrormind-api"}` | Readiness of a future datastore/forecast/WorldKernel engine |
| `system.capabilities()` | `GET /v1/capabilities`, reports `status="scaffold"`, two currently implemented API functions, experimental local-library capabilities (including the optional pinned WorldKernel adapter and fictional evidence retrieval) and planned capabilities | It does not certify that experimental data are authorized, or that planned modules exist or execute |
| `scenarios.validate_scenario(spec)` | `POST /v1/scenarios/validate`; Pydantic validates v0.1 `ScenarioSpec`, returns a summary with `validated_not_executed` | Forecast, RAG, simulation, approval, audit or budget enforcement |
| `decisions.compare_synthetic_retail_decisions(request)` | `POST /v1/decision-workflows/retail/synthetic`; invokes one bounded in-memory fictional evidence-to-comparison service with the policy test double and returns an experimental trace or explicit abstention | Real data, source authorization, empirical forecast, calibrated interval, WorldKernel call, policy ranking, persistence, human approval or operational writes |

`mirrormind.api:app` is the stable import expected by uvicorn.
The API layer contains no statistical model or domain-specific
inventory rules. There is **no authentication** in this M0
scaffold, and it currently has no explicit HTTP request body-size,
rate or concurrency controls. Pydantic/domain bounds do not replace
transport or shared-capacity limits, so the scaffold must not be
exposed as a public or production API.

## 2. Four requests; four different claims

```bash
python -m uvicorn mirrormind.api:app --host 127.0.0.1 --port 8000
# Then, in a separate local terminal:
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/v1/capabilities
curl -X POST http://127.0.0.1:8000/v1/scenarios/validate \
  -H "Content-Type: application/json" \
  --data @examples/retail-scenario.json
curl -X POST http://127.0.0.1:8000/v1/decision-workflows/retail/synthetic \
  -H "Content-Type: application/json" \
  --data '{"as_of":"2011-01-26","replications":12,"seed":317}'
```

The scenario route returns `validated_not_executed` deliberately. The
synthetic decision route executes the local Python policy test double on
generated fixture bytes, emits a typed trace and remains explicitly
experimental. HTTP composition never injects the trusted local comparator and
cannot start a WorldKernel worker; only the local CLI has an explicit
`--engine worldkernel` option. Neither path writes business state.

FastAPI generates HTTP 422 for invalid Pydantic body
validation. The scaffold does not currently add a durable
job store, independent authentication/authorization, a request
body-size limit, rate/concurrency controls or a domain-specific
source-validation layer.

## 3. Curated observations (not certifications)

| Claim ID | Test and observed behavior | Limitation |
| --- | --- | --- |
| **MM-API-001** | `tests/integration/test_api.py::test_scenario_validation_only` confirms a valid JSON request returns `validated_not_executed` | It does not prove execution or successful decision support |
| **MM-API-002** | `tests/integration/test_api.py::test_capabilities_do_not_overstate_implementation` verifies the scaffold lists the pinned local WorldKernel adapter under `experimental`, not `planned` | This test alone does not verify all future capability claims or the engine execution path |
| **MM-API-003** | `tests/integration/test_api.py::test_runs_cannot_exceed_budget` returns HTTP 422 for excess declared run count | A rejected request is not evidence of enforced runtime quotas |
| **MM-API-004** | `tests/integration/test_api.py::test_synthetic_retail_decision_route_returns_the_shared_service_result` matches the HTTP response to the local service result | Only the generated fixture and local policy test double execute; it is not a real decision or an authorized forecast |

The `local_retail_synthetic_evidence_flow`,
`local_retail_evidence_evaluation` and `local_retail_policy_test_double`
labels describe local library experiments. The new
`synthetic_retail_decision_workflow` route composes them only over a generated
fixture and reports `worldkernel_not_invoked`, no ranking, no writes and
`human_review=not_requested`. Its strict body accepts only an ISO date, a
bounded replication count (1..198) and an integer seed. Unknown fields and
invalid values return 422. It cannot ingest an uploaded source or execute
caller-supplied code. The parity regression
`tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger`
checks that the API's implemented/experimental/planned lists match the
reviewed ledger; matching labels do not establish the semantic truth of a
capability claim. The canonical local gate passed on PR #53 SHA
`210f0f382938a67e518df688cc4e19c03d3d7af6`, including the HTTP integration
module. An earlier restricted execution timed out before the handler; its
root cause was not established. Local test-client evidence is not a deployed
service or production-readiness claim.

The experimental `worldkernel_adapter` capability is an optional local
subprocess path pinned to WorldKernel source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. M1E-02 executes the upstream
synthetic inventory demo; M1E-04 registers one fixed MirrorMind policy handler
to preserve the existing synthetic policy contract. Both validate
`worldkernel.result.v1`. The HTTP route remains on the test double and does not
accept an engine choice. See the [M1E-04 guide](WORLDKERNEL_POLICY_WORLD.md)
for the handler flow and actual-engine regressions. Exact pin, bounded output
and timeout do not provide hostile-code isolation, source permission,
CPU/memory quotas or production readiness.

The separate `local_fictional_evidence_retrieval` capability is an
experimental local library/CLI over generated documents. It filters a
caller-declared demo scope before tokenization and ranking, then emits
untrusted excerpts with exact fixture offsets and an excerpt digest. There is
no retrieval HTTP route, authenticated identity, real-source permission or
model call. See the [M2 walkthrough](M2_EVIDENCE_RETRIEVAL.md) for the
contracts, BM25 calculation, tamper regressions and reproducible CLI.

```bash
python -m pytest -q tests/integration/test_api.py
python -m ruff check src tests
python scripts/docs/evidence.py --check
```

Use these commands against the exact review head. A passing local
`TestClient` suite verifies the tested handlers in-process; it does not
establish deployed-service availability, authentication or production
readiness.

## 4. Gateway interface and pure request mapping are not execution

[`modules/simulation/gateway.py`](../../src/mirrormind/modules/simulation/gateway.py)
declares `SimulationSummary` and a `SimulationGateway` Protocol with
`execute(ScenarioSpec) -> SimulationSummary`. The generic M1E-02 implementation
executes one mapped inventory scenario; the separate M1E-04 retail gateway
executes the strict M1 synthetic policy request. Neither is used by the HTTP
route or persists results. The independent
[`worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py)
module constructs a strict request for one world/revision when explicit units,
state, parameters and operator limits are supplied. It rejects unsupported
interventions and unresolved evidence/forecast references. Its limits are
request preflight values, not server-enforced quotas; it does not send a
request or validate a response. The [local synthetic retail policy
comparison](M1_RETAIL_POLICY_SIMULATION.md) remains available as the default
in-process test double. The M1E-04 engine uses the code-owned revision
`mm-retail-policy-v1`; the handler is shipped by MirrorMind and cannot be
selected by request JSON. Its parent checks every demand stream, inventory
state and policy outcome against the reference implementation, failing closed
on drift. Both adapters preserve the one-way dependency MirrorMind ->
WorldKernel.

## 5. Synthetic route data flow and boundary

The handler validates `SyntheticDecisionWorkflowRequest` before entering
`run_synthetic_decision_workflow`. The service keeps historical evaluation at
`as_of - 7 days`, checks the current last-seven release window, and returns an
abstention before policy simulation if a date is missing or late. On success,
the exact same service builds the result trace used by the CLI. Read the
[M1F-02 workflow walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) for
the date split, trace-reference algorithm, modeling caveat propagation,
request-sensitive decision identity, artifact digests and failure paths. Its
trace digest covers the typed trace; a separate whole-workflow digest covers
the response envelope. Neither digest authenticates the producer or adds
request transport protections.

The workflow emits schema v2 and a `DecisionTraceV2`. The HTTP route and
default CLI identify the Python test double as the selected result source. The
explicit WorldKernel CLI result uses the WorldKernel contract for every
outcome and links each outcome to a selected-engine record plus a separate
test-double parity record. Their result digests must match. The trace digest
binds both records, while the whole-workflow digest also covers the versioned
simulation artifact. These local digests do not authenticate either producer.

## 6. Independent exercise

Draw the actual HTTP request graph. For each route
distinguish 200 **liveness**, 200 **validated data**
and 422 **rejected input** from execution readiness,
resource budgets and permissions. Propose one
negative regression before adding a future simulation
route. State which existing source modules would change,
which must remain independent, and what evidence would
be required before `worldkernel_adapter` can be moved
from `planned` to `implemented`.
