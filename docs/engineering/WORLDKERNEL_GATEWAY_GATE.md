# WorldKernel integration gate — strict mapping implemented, execution pending

MirrorMind and WorldKernel are independent repositories and
release lifecycles. MirrorMind owns evidence, forecasting,
governance and human review; WorldKernel owns general-purpose
simulation. The dependency direction must remain **one way**:
MirrorMind -> `SimulationGateway` -> optional WorldKernel adapter.
No WorldKernel runtime import of MirrorMind.

**Current code:** [`gateway.py`](../../src/mirrormind/modules/simulation/gateway.py)
defines `SimulationGateway.execute(ScenarioSpec) -> SimulationSummary` and the
Pydantic summary shape. The separate
[`worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py)
module now builds one strict WorldKernel v1 retail request. There is still no
executor, execution endpoint, forecast sampler or live engine result.

## 1. Two contracts that are not directly interchangeable

| MirrorMind `ScenarioSpec` v0.1 | WorldKernel exchange v1 | Required adapter decision |
| --- | --- | --- |
| `world_type="retail.inventory"` | Trusted built-in `world="retail.inventory.demo"` | Exact local allowlist entry; other names fail |
| `world_version="0.1"` | Registered built-in `"demo-1"` | Exact local mapping; mismatch fails. Remote `demo-1` is registration metadata, not an immutable artifact |
| `horizon_days` | `steps` | Mapped only with explicit `step_unit="day"`; the demo's step uses daily demand |
| `runs`, `seed` | `runs`, `seed` | Deterministic construction; operator limits independently cap steps, runs and transitions |
| `budget.max_simulation_runs` | v1 `limits.max_runs` and additional step/transition limits | Mapping revalidates the mutable scenario and sends `min(scenario budget, operator max_runs)`; neither declaration is an independently enforced worker quota |
| `budget.timeout_seconds`, `max_model_calls`, `max_output_tokens` | No v1 request fields | Pure mapping does not execute or enforce these budgets; a future adapter must enforce them at execution or reject the request before execution |
| `interventions` | Built-in inventory world parameters/state | All interventions currently fail closed; no transformation is reviewed |
| `evidence`, `forecast` references | v1 exchange does not authenticate source or forecast | All such references fail closed until MirrorMind resolves them before mapping |
| `initial_state`, `parameters` | Trusted world expects integer stock/counters and demand/reorder keys | `stock`, daily demand and reorder values are required; only known counters may be omitted |
| `SimulationSummary.scenario_id` | WorldKernel result has no matching public ID guarantee | MirrorMind must define its own stable identity/provenance rule |
| Summary `results`, `assumptions` | Versioned result v1 final states and model assumptions | Preserve engine revision, seed, run count, model limits and output mapping |

WorldKernel already implements the v1 JSON exchange in its
independent project. That **does not** make the MirrorMind
gateway automatically operational.

## 2. Staged integration acceptance

1. **Pure mapping unit tests (M1E-01):** explicit known-world/revision map,
   deterministic request construction, strict rejection of unsupported
   interventions, units and provenance references, and independent operator
   limits. No network and no engine import.
2. **SDK integration (optional):** pinned compatible WorldKernel
   version on a trusted local runtime, real registered world,
   strict world-version checking, server-authoritative budgets. Revalidate
   the current `ScenarioSpec` state at the boundary, cap runs by both scenario
   and operator limits, and enforce every applicable budget that v1 cannot
   represent (or reject before execution).
   It must return actual `worldkernel.result.v1` results.
3. **Domain validity:** data/forecast availability, units,
   initial state and scenario assumptions must be reviewed.
   The demo inventory world has synthetic demand/immediate
   replenishment; it is **not** a calibrated real model.
4. **Service integration (optional later):** authenticated HTTP
   adapter, timeouts, cancellation, retries/idempotency,
   exact model/engine versions and durable result handling.
   Do not assume that SQLite/PostgreSQL/Docker availability
   certifies untrusted-code safety or production HA.
5. **Human review and honest status:** add precise negative
   regressions, a decision trace and capability ledger entry;
   only then promote `worldkernel_adapter` from planned.

## 3. Fail-closed test design (future)

| Input | Required future behavior |
| --- | --- |
| World alias absent or revision mismatch | Reject before execution |
| Unsupported intervention or unit | Return explicit compatibility error |
| Unresolved evidence or forecast reference | Refuse numeric result rather than synthesize missing data |
| Caller requests more runs than server cap | Reject; do not increase resource limits |
| WorldKernel missing/disabled | MirrorMind API remains bootable, reports adapter unavailable |
| Non-finite/unknown result or failed worker | Reject result, retain safe error metadata |
| Repeated request with different provenance version | Preserve version-specific identity, no accidental result reuse |

Local unit tests now prove the pure request mapping only. No current test
proves a live MirrorMind -> WorldKernel simulation; the SDK/execution rows
remain pending and `worldkernel_adapter` remains planned.

## 4. Independent exercise

Use [the contract walkthrough](CONTRACT_WALKTHROUGH.md),
[the API walkthrough](API_WALKTHROUGH.md) and
[the decision trace](DECISION_TRACE_TEMPLATE.md), then trace the
[WorldKernel mapping](WORLDKERNEL_MAPPING_WALKTHROUGH.md).
Write down all fields of `examples/retail-scenario.json`
that cannot currently be translated without
unverified assumptions or unsupported features.
Explain why an ordinary WorldKernel synthetic demo
cannot be presented as a forecast or as validated
retail business advice.

## 5. B-04 proposal — optional pinned local SDK adapter

### Source inspection and compatibility finding

The expected local checkout `C:\Dev\WorldKernel` was not present in this
environment. The inspection below used only the read-only GitHub source at
commit [`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`](https://github.com/GustavoMFDS/WorldKernel/tree/9b133ef873f2b6a7206c9c5742d40df4fccdb04a):
`pyproject.toml`, `docs/EXCHANGE.md`, `docs/RESOURCE_LIMITS.md`,
`src/worldkernel/adapters/exchange.py`,
`src/worldkernel/examples/bootstrap.py`,
`src/worldkernel/core/registry.py`, and
`src/worldkernel/examples/inventory.py`. No file in that repository was
changed, and no runtime/package test was executed here.

The inspected package declares version `0.0.1`, Python `>=3.11`, and no
runtime dependencies. Its local Python/CLI exchange accepts
`worldkernel.simulation.v1` and returns `worldkernel.result.v1`.
`register_builtin_worlds()` registers `retail.inventory.demo` at
`demo-1`; `execute_exchange(..., require_registered_version=True)` checks
that registration metadata before calling the trusted handler. The current
MirrorMind mapping covers the request fields used by this path: world and
revision, steps, runs, seed, explicit initial state, parameters and declared
limits. Unsupported MirrorMind interventions and evidence/forecast references
remain unrepresentable and must continue to fail closed.

The exact target is **technically compatible as a request mapping**, but it
does not satisfy a conventional lead-time inventory simulation. The reviewed
handler randomly perturbs daily demand by up to two units and replenishes
immediately when stock falls below a threshold; its module states that it does
not model lead times. The exchange's `limits` are caller-declared preflight,
not an independently authoritative server budget. Registered `demo-1` is
trusted Python metadata, not a signed package identity. These facts rule out
using this handler as the actual execution engine for M1E-03's separate
lead-time policy comparison without a new, reviewed world model.

### Proposed MirrorMind integration boundary

If the owner accepts this exact candidate, implement M1E-02 in MirrorMind as
an optional, versioned adapter:

1. Declare a separate optional dependency using a direct VCS reference pinned
   to the full commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, and commit a
   resolver lock. Do not make WorldKernel a core/runtime requirement.
2. Keep SDK imports lazy inside the selected adapter path. With the extra
   absent or the adapter disabled, MirrorMind API import, health and current
   capabilities must work without importing `worldkernel`.
3. Revalidate the current `ScenarioSpec` at the boundary. Apply the lower of
   scenario and trusted operator run ceilings and the operator transition
   ceiling before calling the SDK. Register the built-in worlds explicitly,
   then invoke the reviewed request with
   `require_registered_version=True`.
4. Validate the returned schema, engine, world, declared and registered
   versions, match flag, seed, steps, run count, final-state count and every
   final-state field before constructing a `SimulationSummary`. Reject
   booleans, floats, unknown fields and version mismatches; never turn a
   malformed engine result into a successful summary.
5. Record the package commit separately from `demo-1` in the local run
   provenance. Treat outcomes as conditional on that exact trusted handler;
   do not claim the exchange itself proves code identity or policy quality.
6. Treat `timeout_seconds` as unsupported for an in-process SDK call: either
   execute it inside a separately reviewed killable worker or reject before
   execution. This demo makes no model calls or token output; keep those
   budgets explicitly not applicable rather than implying that the SDK
   enforces them.

### Reproducible acceptance plan

The dependency-pinned integration extra should be tested without network
access after installation and without downloading any retail dataset:

- **Disabled import:** existing subprocess guard still proves core/API startup
  does not import WorldKernel.
- **Registered request:** register built-ins, map one fictional scenario and
  execute strict revision checking; assert the v1 result metadata, expected
  run/step/seed values and exact final-state shape.
- **Fail-closed cases:** missing package, wrong schema, unknown world/revision,
  malformed state, limit violation and handler exception must produce an
  unavailable or generic typed failure, never a numeric success.
- **Replay and conservation:** repeat the same pinned request and compare
  results; for each run verify
  `initial_stock + new_orders * reorder_quantity = final_stock + newly_sold`
  using the initial counters and returned cumulative order/sold counts.
- **Provenance and limits:** assert package commit and registration revision
  are both present and distinct; prove scenario/operator ceilings are applied
  before SDK invocation and no unsupported input is discarded.

The exact external pin, optional-extra layout and trusted local execution
mode are the remaining owner/maintainer decision for B-04. This proposal is
not an adapter implementation or certification; no WorldKernel dependency,
test fixture, workflow or external repository change was added here.
