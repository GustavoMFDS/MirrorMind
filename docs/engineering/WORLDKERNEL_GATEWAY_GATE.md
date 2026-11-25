# WorldKernel integration gate — experimental pinned local execution

MirrorMind and WorldKernel remain separate projects with independent release
lifecycles. MirrorMind owns evidence, forecasts, budgets and human review;
WorldKernel owns the simulation engine. The dependency direction is one way:
MirrorMind → `SimulationGateway` → optional local WorldKernel worker. The
WorldKernel repository is not modified or vendored.

**Verified scope:** M1E-01 builds one strict request mapping. M1E-02 adds an
optional local subprocess runner pinned to WorldKernel commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. The runner executes only the
registered synthetic `retail.inventory.demo` world at `demo-1`, validates
`worldkernel.result.v1`, and returns a deterministic `SimulationSummary`.
`worldkernel_adapter` is **experimental**. No HTTP simulation endpoint, remote
service, arbitrary-world execution, real demand, forecast or business decision
is implemented.

## 1. Contracts and compatibility boundary

| MirrorMind input | WorldKernel exchange v1 | Adapter rule |
| --- | --- | --- |
| `ScenarioSpec.world_type="retail.inventory"`, version `0.1` | `world="retail.inventory.demo"`, registered revision `demo-1` | Exact allowlist pair; aliases and revisions fail closed. `demo-1` is registry metadata, not package attestation. |
| `horizon_days`, `runs`, `seed` | `steps`, `runs`, `seed` | Explicit day units; mapping revalidates mutable input and applies operator ceilings. |
| `initial_state`, `parameters` | Inventory state and demand/reorder parameters | Only integer allowlisted fields; no invented starting stock or demand. |
| `EvidenceRef`, `ForecastRef`, `interventions` | No reviewed equivalent | Reject before process launch. |
| Scenario `timeout_seconds` | No exchange-v1 timeout field | Parent process enforces `min(scenario timeout, operator timeout)`. |
| `max_model_calls`, `max_output_tokens` | No WorldKernel model/token interface | Require zero; nonzero values reject before launch. |
| WorldKernel result v1 | MirrorMind `SimulationSummary` | Verify exact envelope, engine/world/revision, run/step/seed, states and assumptions before conversion. |

The exchange request's declared `limits` are not a server-enforced quota.
MirrorMind therefore applies its own trusted local operator limits before
calling the worker. No v1 field silently discards an unsupported scenario
input or budget.

## 2. Runtime architecture and execution

```mermaid
sequenceDiagram
  participant C as Trusted local caller
  participant R as LocalWorldKernelGateway / runner
  participant M as Strict M1E-01 mapper
  participant W as Pinned one-shot worker
  participant K as WorldKernel built-in registry
  C->>R: ScenarioSpec + operator-owned limits/units
  R->>R: Revalidate scenario; reject model/token budgets
  R->>M: Allowlisted scenario snapshot
  M-->>R: worldkernel.simulation.v1 JSON
  R->>W: stdin JSON, fixed script, exact source commit
  W->>W: Verify package version + PEP 610 VCS URL/commit
  W->>K: Register built-ins; execute strict registered revision
  K-->>W: worldkernel.result.v1
  W-->>R: bounded stdout JSON; sanitized stderr on failure
  R->>R: Validate exact result; hash request/result; build summary
  R-->>C: SimulationSummary or typed local error
```

1. `LocalWorldKernelGateway.execute` delegates to
   `run_worldkernel_scenario`; the caller supplies trusted
   `WorldKernelOperatorLimits`, explicit unit context and optional local
   runtime configuration. A scenario cannot choose an executable, worker
   path, Python module or external world.
2. `_scenario_snapshot` reconstructs `ScenarioSpec` from current values at the
   execution boundary. `build_worldkernel_exchange_request` then enforces the
   reviewed world mapping, item/day/order units, state/parameter allowlists,
   no unresolved evidence/forecast references and
   `min(scenario.max_simulation_runs, operator.max_runs)`.
3. Nonzero model-call or output-token budgets fail before process launch. The
   effective wall-clock timeout is the lower of the operator maximum and the
   scenario timeout. Exchange v1 does not carry either control.
4. The parent starts the fixed `worldkernel_worker.py` with `shell=False`, a
   temporary working directory, closed inherited file descriptors and an
   allowlisted OS environment. It sends one canonical JSON request over stdin.
   Concurrent pipe readers retain no more than the configured stdout bound
   plus one detection byte and 4 KiB of stderr; overflow or timeout terminates
   the worker. Errors returned to callers omit request rows and third-party
   tracebacks.
5. The worker verifies distribution version `0.0.1`, canonical repository
   identity and the exact PEP 610 VCS commit before importing the optional SDK.
   It registers only upstream built-ins and calls
   `execute_exchange(..., require_registered_version=True)`.
6. The parent accepts only the exact `worldkernel.result.v1` root field set,
   expected engine and adapter versions, exact mapped world/revision, a true
   registration-match flag, integer run/step/seed matches, one nonnegative
   integer state per run with exactly `stock`, `sold`, `unmet`, and `orders`,
   and a nonempty list of string assumptions. Cumulative sold/unmet/order
   counters cannot decrease; per-run stock conservation must satisfy
   `starting_stock + new_orders * reorder_quantity = final_stock + new_sold`.
   NaN, infinities, extra fields, booleans as integers, mismatches and
   malformed JSON fail closed.
7. The summary binds the canonical scenario/request and engine source commit
   into a stable SHA-256 `scenario_id`; `result_sha256` records the exact
   returned JSON bytes. The engine commit and `demo-1` registration revision
   are distinct provenance values. The summary preserves conditional engine
   assumptions and limitations.

## 3. Install and reproduce

Python 3.11+ is required by the inspected WorldKernel package. The core
MirrorMind install remains independent of it. To opt in locally:

```powershell
python -m pip install -e ".[worldkernel]"
python -m examples.m1e_02_worldkernel_local_runner
```

The optional extra points to the full reviewed Git SHA. The example uses a
fictional five-day scenario, three runs, fixed seed `2026`, and explicit
item/day/order units; it reads no workbook and makes no network call at run
time. It prints a JSON `SimulationSummary`, including exact engine pin,
result schema, final states, result digest and caveats. Without the optional
package or when the installed commit differs, the API can still import and the
local runner returns a sanitized unavailable error.
For the checked-in example, expected stable summary fields are engine
`worldkernel/0.0.1@9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, world
`retail.inventory.demo`, revision `demo-1`, 5 steps, 3 runs and seed 2026.
Repeated execution yields the same `scenario_id`, result digest and final
states for that exact synthetic input/pin; these values are not forecast
scores or measured business performance.

Focused regressions:

```powershell
python -m pytest -q tests/unit/test_worldkernel_mapping.py
python -m pytest -q tests/unit/test_worldkernel_runner.py
python -m pytest -q tests/integration/test_worldkernel_runner_engine.py
python -m ruff check src tests
```

`tests/unit/test_worldkernel_mapping.py` proves the strict pure translation,
mutable-scenario revalidation and operator/scenario run ceiling.
`tests/unit/test_worldkernel_runner.py` exercises deterministic summary
construction with a synthetic fake worker; revision/field/budget rejection;
operator and scenario timeouts; stdout/stderr bounds; inventory balance;
sanitized failures; missing executable and optional-distribution behavior;
exact/mismatched PEP 610 metadata; and API import without the optional
package. The mocked metadata tests verify local comparison logic, not package
file integrity.
`tests/integration/test_worldkernel_runner_engine.py::test_pinned_local_runner_executes_synthetic_inventory_world_deterministically`
executes the actual SHA-pinned upstream engine twice with fictional values and
compares the summaries. It skips unless that exact optional package is
installed; a skip is not actual-engine evidence. The tests do not prove source
rights, forecast quality, general sandboxing or production suitability.

Evidence map links:

- `MM-WKR-001` — `tests/unit/test_worldkernel_runner.py::test_local_runner_bounds_worker_output`
- `MM-WKR-002` — `tests/integration/test_worldkernel_runner_engine.py::test_pinned_local_runner_executes_synthetic_inventory_world_deterministically`
- `MM-WKR-003` — `tests/unit/test_worldkernel_runner.py::test_worker_accepts_exact_pep610_repository_and_commit`
- `MM-WKR-004` — `tests/unit/test_worldkernel_runner.py::test_local_runner_rejects_inventory_result_that_breaks_balance`

The repository's six-check exact-head procedure is
[`LOCAL_QUALITY_GATE.md`](LOCAL_QUALITY_GATE.md). Record its local receipt
separately from GitHub Actions. This documentation does not claim official CI
success.

## 4. Security, privacy and model limitations

- The worker uses a fixed built-in demo; scenario JSON cannot register code or
  choose a Python import. `shell=False`, a reduced environment, strict package
  pin check, strict registered revision, capped pipe buffers and wall-clock
  timeout reduce accidental exposure.
- The subprocess is **not** a hostile-code sandbox. It has the user's local
  OS identity and may use that identity's filesystem/network access. The
  timeout does not cap CPU or memory, and termination does not establish safe
  behavior for arbitrary plugins or child processes. Never run untrusted
  WorldKernel code through this adapter.
- PEP 610 metadata confirms the installed distribution's declared VCS origin
  and commit; it is not installed-file attestation. The inspected upstream
  revision has no root `LICENSE` file. This integration makes no redistribution
  claim; packaging beyond local opt-in needs a separate licensing decision.
- The built-in inventory model uses fictional daily demand, random perturbation
  and immediate replenishment. It does not model supplier lead time, real stock,
  source data, forecast uncertainty or causal policy effects. Results are
  conditional simulation outputs, not observations, forecasts or advice.
- No HTTP route invokes this worker. API startup remains independent of the
  optional package. No data source, API key, credential or other repository
  was accessed or changed for the local integration.

## 5. Tests and independent investigation

Trace `LocalWorldKernelGateway.execute` → `run_worldkernel_scenario` →
`build_worldkernel_exchange_request` → `_run_worker` → worker `main` →
`execute_exchange` → `_parse_result` / `_validate_result` → `SimulationSummary`.
Explain why strict validation occurs in both the mapper and the worker parent:
the mapper protects semantic compatibility, while the parent treats the
subprocess result as untrusted protocol data.

Investigation exercises:

1. Change a fake result's `registered_world_version`, then run
   `test_local_runner_rejects_result_revision_mismatch`. Explain why the
   upstream registration flag alone is not enough for the parent contract.
2. Set `budget.max_model_calls=1` and verify rejection happens before
   `subprocess.Popen`. Explain why silently ignoring an unrepresentable budget
   would make the adapter misleading.
3. Lower `WorldKernelRuntimeConfig.max_output_bytes` and make a fake worker
   write excess data to stdout, then stderr. Verify bounded rejection and
   that error text contains no scenario values.
4. Run the example twice and compare its output. Then inspect the source pin
   separately from the `demo-1` registration string; explain why one does not
   cryptographically prove the other.
5. Inspect the pinned inventory handler and identify which M1E-03 lead-time
   requirements cannot be represented by this demo. Do not modify the separate
   WorldKernel repository.

For a local diagnosis, distinguish `WorldKernelRuntimeUnavailable`,
`WorldKernelExecutionTimeout`, `WorldKernelOutputLimitExceeded`, malformed
result failures and a valid but conditional summary. Preserve the exact
scenario fixture and runtime SHA; do not log source rows or expand exception
details into public API responses.

## 6. Evolution gate and remaining decisions

Before changing the external exchange or registered handler, inspect the
exact WorldKernel revision and add a reviewed compatibility regression.
Unsupported fields must remain rejected. A future HTTP or service adapter
needs its own change request, authenticated admission, cancellation,
concurrency/CPU/memory quotas, durable result handling, privacy review and
independent operational tests. A different simulation model needs separate
unit/lead-time semantics and must not inherit the demo's capability claim.

M1E-02 establishes local experimental execution at one exact source pin.
Broader B-04 acceptance for isolation, service operation or a lead-time model
remains open. No changes were made to WorldKernel itself.
