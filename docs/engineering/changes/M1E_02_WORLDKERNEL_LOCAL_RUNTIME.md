# Change request — Version-pinned local WorldKernel runtime

**Status:** in progress on local branch `codex/m1e-02-worldkernel-local-runtime`; no new PR opened while the existing review queue is being consolidated.

## 1. Goal in plain language

**Prior behavior:** PR #55 provided a pure, fail-closed mapper from the one reviewed MirrorMind retail scenario to WorldKernel JSON exchange v1. That PR still contains mapping only.

**Desired behavior:** add an optional local subprocess runner that executes only the registered `retail.inventory.demo` at `demo-1` from an exact WorldKernel source commit. The runner must reuse the reviewed mapper, apply the lower scenario/operator limits, enforce a local timeout and output bound, validate the complete `worldkernel.result.v1` envelope, and return a MirrorMind `SimulationSummary`. The default API and test suite must work when WorldKernel is absent.

**Why:** M1E-02 is a named P0 dependency for the synthetic M1 decision workflow. An actual local invocation closes the gap between request translation and result evidence without deploying a service or changing the independent engine.

**Out of scope:** editing or vendoring WorldKernel; HTTP integration; remote execution; arbitrary/custom world registration; untrusted handler isolation; production CPU/memory guarantees; real demand/inventory claims; real source data; paid resources; automatic ordering or business writes.

### Capability status change

- Previous: `worldkernel_adapter` was `planned`; the capability ledger described a request mapper without execution.
- Current: `experimental`, limited to an optional locally installed package at exact SHA `9b133ef873f2b6a7206c9c5742d40df4fccdb04a` and one trusted synthetic demo world. Missing or mismatched runtime is an explicit failure.
- Evidence: focused parent-protocol regressions cover pin, limits, timeout, output and result validation; a separate integration test executes the pinned engine using fictional inputs. Exact local full-gate evidence is being recorded below.
- Limitation: no HTTP route, service-side admission, arbitrary-code sandbox, operational deployment, authentic forecast, approved data or business recommendation.
- `GET /v1/capabilities` lists the local adapter as experimental; no simulation endpoint was added.

## 2. Acceptance criteria

- [x] Pin the optional WorldKernel dependency to an exact reviewed commit; do not add it to core dependencies.
- [x] Verify installed package metadata identifies the exact repository and commit before execution.
- [x] Revalidate the mutable `ScenarioSpec` at the adapter boundary and use the existing strict world mapping; reject unsupported refs/interventions.
- [x] Enforce operator steps, runs and transitions; effective run count remains `min(scenario budget, operator cap)`.
- [x] Enforce an operator wall-time limit, capped further by `ScenarioSpec.budget.timeout_seconds`; terminate timed-out worker and return a sanitized error.
- [x] Bound stdout/stderr retention using concurrent readers; reject malformed, mismatched, non-finite, unexpected and inventory-inconsistent results.
- [x] Call WorldKernel with strict registered revision checking; require `worldkernel.result.v1`, expected world/revision, seed, step/run counts, exact non-negative inventory-state fields, non-decreasing cumulative counters and the pinned demo's stock-conservation equation.
- [x] Derive a stable MirrorMind scenario identity from canonical synthetic scenario/request data and pinned engine commit; keep the external result's assumptions and conditional semantics.
- [x] Keep imports lazy and API bootable without the optional package; no HTTP route or import-time engine discovery.
- [x] Add normal, adverse and actual-engine tests; all test inputs remain synthetic.
- [x] Update change docs, source walkthrough, system map, atlas, symbols, evidence and capability ledger; explain run/debug/recovery steps.
- [ ] Run the exact clean-head local six-check gate after commit; report local versus official CI separately.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Composition | `src/mirrormind/modules/simulation/gateway.py::SimulationGateway` | Keep the existing interface; local runner is an optional implementation | Import/API regression with optional package absent |
| Existing mapping | `src/mirrormind/modules/simulation/worldkernel_mapping.py::build_worldkernel_exchange_request` | Reuse; do not weaken its world, state, ref or budget rejections | Existing `tests/unit/test_worldkernel_mapping.py` |
| Runner | `src/mirrormind/modules/simulation/worldkernel_runner.py::run_worldkernel_scenario` | Add local subprocess execution, operator timeout/output bounds, result validator and stable summary identity | New unit and integration selectors |
| Worker | `src/mirrormind/modules/simulation/worldkernel_worker.py::main` | Add minimal JSON/stdin worker that verifies package pin, registers only upstream built-ins and enables strict revision checking | Worker protocol, wrong-pin and real-engine regressions |
| Dependency | `pyproject.toml` optional extra | Add exact Git SHA in an optional extra; preserve empty core dependency boundary | Packaging metadata check and isolated install |
| Example | `examples/m1e_02_worldkernel_local_runner.py` | Add fictional runnable local example | Actual pinned engine produces repeatable `worldkernel.result.v1` |
| Capability API | capability ledger and `api/routes/system.py` | Promote only to `experimental` after real local execution evidence | API/ledger parity test; no execution endpoint |
| External project | `GustavoMFDS/WorldKernel` | Read-only contract/source inspection at pinned revision; no edits | Exact commit and source links in guide |

## Data, modeling and decision review

- Dataset card: not applicable; test/example uses fixed fictional scenario inputs only.
- Forecast model card: not applicable; no forecast is generated or evaluated.
- Decision trace: no recommendation, approval or business action is produced. The `SimulationSummary` describes conditional engine outcomes only.
- WorldKernel gate: map one exact registered world/revision; reject unsupported values. The external `demo-1` label is registration metadata, not signed artifact attestation.
- Temporal leakage: no time series or forecast enters the simulation; `EvidenceRef` and `ForecastRef` are rejected by the existing mapper.
- Source review: pinned WorldKernel `main` contract/source at `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, whose commit signature is reported verified by GitHub. Its retail demo uses synthetic daily demand and immediate replenishment; it does not represent lead time or a calibrated retailer.

## 4. Constraints and risks

WorldKernel remains a separate project with an optional one-way dependency. The runner invokes a fixed worker file using `shell=False`; scenario JSON cannot choose a module, executable, path or world registration. The worker uses the external SDK's strict registration-version mode. Caller-provided exchange limits are not a remote server quota, so this slice runs only locally and enforces its own small operator ceilings and wall time.

The local timeout and output-file bounds do not provide a general CPU/memory sandbox. The current pinned trusted inventory handler does not spawn child processes, but the runner makes no guarantee for arbitrary WorldKernel handlers. The optional package is fetched only when explicitly installed; no source is copied into MirrorMind. The external project has no root `LICENSE` file at the inspected revision, so this work makes no third-party redistribution claim; packaging, hosting and broader distribution remain separate owner decisions.

## 5. Implementation plan

1. Reconciled this branch with PR #55 head and inspected the pinned external contract without modifying WorldKernel.
2. Added this scoped change request before source edits.
3. Added synthetic regressions for runtime absence/pin mismatch, result fields/balance, limits, timeout, process failure, output overflow and malformed envelopes.
4. Implemented the pinned optional worker/runner pair; installed the optional dependency only in the local development environment and executed the synthetic engine scenario.
5. Updated capability/evidence/maps, source walkthrough, learning/debugging documentation, atlas and generated symbol catalog.
6. Focused tests and example passed. Exact clean-head full gate remains pending; do not call it GitHub Actions.

## 6. Evidence after implementation

- Commit / PR: local branch `codex/m1e-02-worldkernel-local-runtime`, based on PR #55 head `56aa92a6920a429b83458380231642fe59feaf08`; no PR opened pending separate review/integration decision.
- Modified symbols and files: `LocalWorldKernelGateway`, `WorldKernelRuntimeConfig`, `run_worldkernel_scenario`, worker `main`, `_verify_installed_runtime`, strict result parsing/validation, API capability status and synthetic tests.
- Tests and environment: Python 3.13.5; focused mapping/runner/actual-engine suite passed 44 tests in 5.01s; pinned package `0.0.1` at `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; example exited 0 and produced 3 runs × 5 steps with seed 2026. Exact full gate pending.
- Claim IDs and limitations: `MM-WKR-001` bounded output protocol, `MM-WKR-002` actual pinned-engine integration, `MM-WKR-003` PEP 610 metadata check and `MM-WKR-004` inventory balance regression. None establishes installed-file attestation, source rights, a lead-time model, CPU/memory isolation or production safety.
- Contract: MirrorMind `worldkernel.result.v1`-backed local `SimulationSummary`; no HTTP contract change.
- Docs updated: decision log; source review; gateway gate and mapper/runtime walkthrough; system/semantic maps; capability gates/ledger; evidence map; atlas; debugging/learning/API walkthrough; local gate and handoff; definition of done; master/M1 plans; project status, backlog and blockers.
- Known limitations: local trusted demo only, immediate replenishment, no hostile-code sandbox, no production deployment, no authentic data or forecast.
- Independent explanation: the worker executes only a preselected, pinned built-in world and the parent accepts only a bounded, version-matched result; the existing mapper remains the authority on representability.
