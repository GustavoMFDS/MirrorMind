# WorldKernel integration gate — versioned optional adapter (not implemented)

MirrorMind and WorldKernel are independent repositories and
release lifecycles. MirrorMind owns evidence, forecasting,
governance and human review; WorldKernel owns general-purpose
simulation. The dependency direction must remain **one way**:
MirrorMind -> `SimulationGateway` -> optional WorldKernel adapter.
No WorldKernel runtime import of MirrorMind.

**Current code:** [`gateway.py`](../../src/mirrormind/modules/simulation/gateway.py)
defines only `SimulationGateway.execute(ScenarioSpec) -> SimulationSummary`
and the Pydantic summary shape. No adapter, execution endpoint,
forecast sampler or approved domain mapping exists yet.

## 1. Two contracts that are not directly interchangeable

| MirrorMind `ScenarioSpec` v0.1 | WorldKernel exchange v1 | Required adapter decision |
| --- | --- | --- |
| `world_type="retail.inventory"` in example | Trusted built-in `world="retail.inventory.demo"` | **Explicit approved allowlist**, not a string replacement or dynamic import |
| `world_version="0.1"` | Registered built-in `"demo-1"` | Exact verified mapping; mismatch must fail, not silently coerce |
| `horizon_days` | `steps` | Only map if model step means exactly one calendar day |
| `runs`, `seed` | `runs`, `seed` | Validate caps and reproducibility; server-owned bounds remain independent |
| `budget.max_simulation_runs` | v1 `limits.max_runs` and additional step/transition limits | Enforce **operator-owned** limits, not caller-imposed increases |
| `interventions` | Built-in inventory world parameters/state | Explicitly supported transformations and unit checks; reject unknown kind |
| `evidence`, `forecast` references | v1 exchange does not authenticate source or forecast | Resolve and authorize through MirrorMind first; do **not** drop unresolved refs silently |
| `initial_state`, `parameters` | Trusted world expects its defined state/parameter keys | Domain adapter validation; no invented stock or lead times |
| `SimulationSummary.scenario_id` | WorldKernel result has no matching public ID guarantee | MirrorMind must define its own stable identity/provenance rule |
| Summary `results`, `assumptions` | Versioned result v1 final states and model assumptions | Preserve engine revision, seed, run count, model limits and output mapping |

WorldKernel already implements the v1 JSON exchange in its
independent project. That **does not** make the MirrorMind
gateway automatically operational.

## 2. Staged integration acceptance

1. **Adapter unit tests:** explicit known-world/revision map,
   deterministic request construction, strict rejection of unsupported
   interventions and provenance references. No network.
2. **SDK integration (optional):** pinned compatible WorldKernel
   version on a trusted local runtime, real registered world,
   strict world-version checking, server-authoritative budgets.
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

**Verification is pending:** no current test proves a
live MirrorMind -> WorldKernel simulation. Do not
claim this table is implemented.

## 4. Independent exercise

Use [the current contract walkthrough](CONTRACT_WALKTHROUGH.md),
[the API walkthrough](API_WALKTHROUGH.md) and
[the decision trace](DECISION_TRACE_TEMPLATE.md).
Write down all fields of `examples/retail-scenario.json`
that cannot currently be translated without
unverified assumptions or unsupported features.
Explain why an ordinary WorldKernel synthetic demo
cannot be presented as a forecast or as validated
retail business advice.
