# M1E-04 — WorldKernel retail policy world

This guide describes the opt-in local WorldKernel execution path for the same
fictional 28-day replenishment comparison used by the M1F workflow. It is a
source walkthrough and reproducible compatibility check, not evidence of real
retail performance, an optimized policy, a production sandbox or permission to
place orders.

See the implementation scope in the [M1E-04 change request](changes/M1E_04_WORLDKERNEL_POLICY_WORLD.md),
the [WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md), and the original
[policy test-double guide](M1_RETAIL_POLICY_SIMULATION.md).

## 1. Goal and boundary

WorldKernel's bundled `retail.inventory.demo@demo-1` is useful to prove that
MirrorMind can call the pinned exchange API. Its handler assumes constant
daily demand and immediate replenishment. It cannot express the three M1E-03
rules, their paired random demand, delayed arrivals or abstract cost
assumptions. M1E-04 registers one fixed MirrorMind-owned handler in the local
worker to run those already-reviewed rules through WorldKernel's event loop.

The contract remains one way and versioned:

```text
MirrorMind M1E-03 policy request
    -> strict M1E-04 mapper
    -> worldkernel.simulation.v1
    -> exact-pin local worker
    -> fixed trusted MirrorMind step handler
    -> worldkernel.result.v1
    -> parent validation and reference parity check
```

The handler name and revision are constants in MirrorMind source. JSON cannot
provide a Python module, file path, callable, registry name or revision. The
worker registers the upstream demos and this one code-owned handler, then
requires the exchange's declared revision to equal the trusted registration
metadata. That metadata is not a signature or attestation of installed code.
The exact package source SHA is checked separately through PEP 610 metadata.

Only the local CLI's explicit `--engine worldkernel` option selects this path.
The default CLI and HTTP endpoint continue to use the in-process test double;
the HTTP request has no engine selector and cannot start a worker. The pinned
SDK is imported only inside the child process, so importing the API does not
require the optional package.

## 2. Components and data flow

```mermaid
sequenceDiagram
  participant CLI as Local M1 CLI
  participant WF as Synthetic decision workflow
  participant GW as Local policy gateway
  participant MAP as Strict policy mapper
  participant WK as Fixed worker
  participant ENG as Pinned WorldKernel
  CLI->>WF: request + trusted comparator
  WF->>WF: synthetic evidence, fixed diagnostics, 28-day profile
  WF->>GW: RetailPolicyComparisonRequest
  GW->>MAP: revalidated request + operator limits
  MAP-->>GW: fixed policy world + state/parameters + limits
  GW->>WK: canonical JSON on stdin, fixed worker path
  WK->>WK: verify package version and exact PEP 610 commit
  WK->>ENG: register trusted worlds; run 28 steps per replication
  ENG-->>WK: worldkernel.result.v1 final states
  WK-->>GW: bounded JSON output or sanitized failure
  GW->>GW: validate stream, state, inventory balance, exact parity
  GW-->>WF: engine-derived policy metrics + exact result digest
  WF->>WF: bind simulation artifact into DecisionTrace and digests
  WF-->>CLI: deterministic synthetic result
```

| Component | Responsibility | Boundary |
| --- | --- | --- |
| `policy_simulation.py` | Own request/assumption contracts, demand stream rule, daily inventory transition and aggregation | Synthetic caller inputs only; no source, forecast, ranking or engine import |
| `worldkernel_policy_world.py` | Validate the fixed world state/parameters, draw one exogenous demand value and advance all policy/sensitivity states | Trusted handler shipped by MirrorMind; no handler code comes from request JSON |
| `worldkernel_policy_mapping.py` | Revalidate M1E-03 input, map exact world/version, build initial state, calculate event ceilings | Reject unsupported or over-budget input before process launch |
| `worldkernel_worker.py` | Verify pinned distribution metadata, register built-ins and the fixed handler, call the exchange | Child process is not a hostile-code sandbox |
| `worldkernel_runner.py` | Enforce parent timeout/output bounds, validate the exchange envelope and sanitize worker failures | Does not enforce CPU, memory or child-process-tree limits |
| `worldkernel_policy_gateway.py` | Validate every returned stream/state, recompute output metrics, compare all scenarios with the test-double reference | WorldKernel-derived state is returned only after exact synthetic parity |
| `synthetic_decision_workflow.py` | Inject a trusted local comparator only when selected by CLI; bind its result into existing artifacts and trace | API calls omit the comparator and stay test-double-only |
| `examples/m1_retail_decision_workflow.py` | Select `test-double` by default or the opt-in pinned local engine | No file, network, source workbook or business write |

## 3. Versioned request and resource limits

Source contract: `RetailPolicyComparisonRequest`, schema
`mirrormind.retail.policy_comparison.v1`.

Registered target: `mirrormind.retail.policy_comparison`, revision
`mm-retail-policy-v1`. Exchange schema: `worldkernel.simulation.v1`.
Result schema: `worldkernel.result.v1`. The worker accepts only the reviewed
WorldKernel commit
[`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`](https://github.com/GustavoMFDS/WorldKernel/tree/9b133ef873f2b6a7206c9c5742d40df4fccdb04a).

The mapped envelope contains exactly:

- `schema_version`, fixed `world` and `world_version`;
- `steps=28`, caller-declared bounded `runs`, and the declared synthetic seed;
- initial state with a policy state for each of the three lead-time scenarios
  and each of the three policy identifiers;
- parameters with one 28-day expected-demand profile, the derived lead-time
  sensitivity values, explicit assumptions and schema identifier;
- `limits` with operator-owned step, run and total-event ceilings.

The handler updates nine policy/sensitivity states in each WorldKernel event.
Therefore the mapper calculates application work as
`28 × replications × 3 policies × number_of_lead_time_cases`; this must fit
both the request's existing 50,000 policy-transition ceiling and the stricter
operator limit. The exchange event ceiling is the operator budget divided by
that fixed fan-out. A limit in exchange JSON is not a server quota, so the
parent also checks the mapped request before launching the worker.

Unknown fields, a wrong model type/revision, an unsupported unit/assumption,
too few operator steps/runs, excessive total policy transitions, or a result
whose world/revision/count/seed differs are rejected. No missing value is
filled in to make it fit. The generic worker boundary allows only the two
reviewed registered worlds and their exact versions.

## 4. How one simulation step works

`create_policy_world_initial_state` creates empty inventory and cumulative
counters for every policy and lead-time case. At each event,
`mirrormind_retail_policy_step` validates the exact state and parameter keys,
then calls `rng.randrange(3)` once. `sample_demand_units` applies one of the
fixed 75%, 100% or 125% multipliers with integer half-up rounding:

```text
actual_units = (expected_units × multiplier_percent + 50) // 100
```

The same daily draw is applied to all nine policy states. WorldKernel's
`run_scenario` creates each run with seed `request.seed + run_index`, matching
the original `_build_demand_streams`. This pairing controls exogenous demand
when comparing policies; it does not establish that the random profile
resembles a retailer.

For each policy state, `advance_retail_policy_day` preserves the M1E-03 order:

1. Receive orders scheduled for the current day.
2. Fulfill demand from on-hand stock; unmet units are a lost-sales proxy.
3. Accrue holding cost on remaining on-hand stock.
4. Compute inventory position and apply the selected policy rule.
5. Record a new order and its future arrival, if inside the 28-day horizon.

The `forecast_aware_order_up_to` rule intentionally sums profile positions
`[day + 1, arrival_day)`. It excludes arrival-day demand. With a one-day lead
time, that target interval is empty; this is a retained toy rule, not a
standard or optimized order-up-to policy. Its caveat stays in every output.

Each state retains `ordered_units`, fulfilled units, on-hand stock and pending
units. `finalize_retail_policy_metrics` rejects a broken item balance:

```text
initial_stock + ordered_units = fulfilled_units + ending_on_hand + pending_orders
```

It derives procurement, holding, fixed-order and unmet-demand costs from the
declared abstract cost assumptions. `summarize_retail_policy_runs` aggregates
replication rows and keeps ranking unset. The gateway reconstructs each
replication's demand digest and metrics from WorldKernel's final state, then
requires exact equality with `compare_synthetic_retail_policies` for all
policies, replications and lead times. A mismatch fails closed.

## 5. Output and reproducible example

The gateway returns the existing `mirrormind.retail.policy_comparison.v1`
fields with:

- `simulation_status=experimental_local_worldkernel_policy_world`;
- `engine_execution=worldkernel_invoked`;
- policy metrics derived from the engine final states after parity checks;
- `worldkernel_execution` containing package version, source commit, result
  schema, fixed world/revision and SHA-256 of the exact worker result bytes.

The M1F workflow sets `policy_test_double_invoked=false` for this selected
simulation result. It does still run the reference test double inside the
gateway strictly as a parity oracle; no oracle value is substituted for the
engine-returned state. The outer response and decision-trace digests include
the selected simulation artifact. A digest detects content changes when
recomputed; it is not a signature, provenance proof or reviewer identity.

Default synthetic workflow:

```powershell
python -m examples.m1_retail_decision_workflow --as-of 2011-01-26 --replications 12 --seed 317
```

Opt in to the pinned local engine:

```powershell
python -m examples.m1_retail_decision_workflow --as-of 2011-01-26 --replications 12 --seed 317 --engine worldkernel
```

Both commands read generated in-memory fixture data only. The second fails
with a sanitized local error if the optional exact-pin package is absent or
mismatched. It does not silently fall back to the test double.

## 6. Tests and what they prove

Run the focused suite:

```powershell
python -m pytest -q tests/unit/test_retail_policy_simulation.py tests/unit/test_worldkernel_policy_world.py
python -m pytest -q tests/integration/test_worldkernel_runner_engine.py tests/integration/test_worldkernel_policy_world_engine.py
python -m ruff check src tests
```

- `tests/unit/test_retail_policy_simulation.py` preserves the original demand,
  lead-time caveat, determinism, item balance and cost summaries after the
  shared transition was extracted.
- `tests/unit/test_worldkernel_policy_world.py::test_policy_mapper_targets_fixed_world_and_bounds_all_policy_transitions`
  checks the code-owned mapping and fan-out budget.
- `tests/unit/test_worldkernel_policy_world.py::test_policy_gateway_rejects_budget_before_starting_worker`
  proves an invalid operator ceiling is rejected before `Popen`.
- `tests/unit/test_worldkernel_policy_world.py::test_registered_handler_matches_reference_policy_metrics_and_shared_stream`
  applies 28 transitions with a seeded `random.Random` and compares the shared
  demand stream and all nine metric sets with the previous implementation.
- `tests/unit/test_worldkernel_policy_world.py::test_policy_gateway_rejects_malformed_world_state_from_worker`
  rejects a synthetic fake worker's incomplete final state.
- `tests/unit/test_worldkernel_policy_world.py::test_registration_uses_only_code_owned_exact_world_revision`
  proves the only registered name, handler and version are constants in
  MirrorMind code.
- `tests/integration/test_worldkernel_policy_world_engine.py::test_pinned_engine_policy_gateway_matches_synthetic_reference`
  executes the exact installed SHA and verifies engine-derived outcomes equal
  the reference for all replications and cases. It skips when that exact
  optional package is absent; a skip is not engine evidence.
- `tests/integration/test_worldkernel_policy_world_engine.py::test_m1_cli_worldkernel_option_runs_end_to_end_with_synthetic_data`
  invokes the actual CLI option, parses the trace-bearing response and checks
  that the engine was selected.
- `tests/integration/test_api.py` continues to verify capability parity and
  the default API path. The HTTP route does not accept an engine selector or
  invoke the subprocess.

All fixtures are invented. These tests prove local code-path behavior only;
they do not prove license acceptance, source permission, privacy compliance
for real data, empirical forecasts, policy optimality, cloud runner behavior,
or production isolation.

The curated evidence map links `MM-WKPW-001` to strict mapping and transition
limits, `MM-WKPW-002` to deterministic shared-stream handler parity,
`MM-WKPW-003` to actual execution at the pinned WorldKernel package,
`MM-WKPW-004` to the opt-in M1 CLI trace, and `MM-WKPW-005` to malformed
worker-state rejection. Read each limitation before extending the claim.

## 7. Failure diagnosis and security

| Symptom | Check | Safe interpretation |
| --- | --- | --- |
| Optional runtime unavailable | Verify installed version and PEP 610 URL/commit through the fixed worker | Do not switch revision or fall back silently |
| Mapping rejects before launch | Inspect request model, exact world/version, operator limits and 28-day profile | Correct the caller-owned synthetic contract; do not widen allowlists to accept unknown fields |
| Timeout/output limit | Inspect `WorldKernelRuntimeConfig`, the typed exception and fake-worker regression | Keep limits intact; do not expose raw worker stderr or rows |
| Result envelope mismatch | Compare exchange/result schema and registered world metadata at the pinned source SHA | Reject; revise the versioned contract and tests before changing the pin |
| Demand or policy parity mismatch | Compare seed plus replication index, one draw per day, arrival order and the half-open order-up-to interval | Treat as semantic drift; do not overwrite engine results with reference values |
| API does not run WorldKernel | This is expected; only the local CLI option has the comparator | Keep route behavior and capability wording truthful |

The worker uses `shell=False`, a fixed script, a reduced environment,
temporary working directory, bounded output and a parent wall-clock timeout.
The process still runs with the user's OS identity. These controls do not
provide hostile-code isolation, CPU/memory caps, network denial, safe
process-tree termination or installed-file attestation. Never feed arbitrary
WorldKernel packages or handler code to this worker. No WorldKernel source,
real data, credential or network call is part of the automated tests.

## 8. Learning and evolution

1. Trace the CLI `--engine` choice through
   `run_synthetic_decision_workflow(policy_comparator=...)`. Explain why the
   API route omits that trusted Python dependency seam.
2. Compare `create_policy_world_initial_state`, the strict mapper and
   `_validate_mapped_exchange_request`. Identify which guarantees belong to
   MirrorMind and which limits are only echoed in exchange JSON.
3. Run the handler for one day with each multiplier index. Trace a lead-time
   arrival through `advance_retail_policy_day`, then explain why an order
   arriving outside the horizon remains counted in pending units.
4. Mutate the fake worker to change one demand value, one registered revision
   and one inventory counter. Predict which validator rejects each result and
   run the associated regression.
5. Inspect upstream `register_world`, `run_scenario`, `EventRuntime` and
   `execute_exchange` at the exact pinned SHA. Explain why registration is
   trusted process-local metadata rather than source attestation.

Future changes must preserve the M1E-03 caveat and item balance, use a new
registered revision for changed simulation semantics, keep the engine optional
and off HTTP, review the exact upstream exchange contract, and rerun the full
six-check local gate on a clean integrated candidate. A later service
execution path needs separate authentication, admission and resource-isolation
acceptance.
