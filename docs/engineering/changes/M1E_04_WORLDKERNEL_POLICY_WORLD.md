# Change request — MirrorMind-owned WorldKernel retail policy world

**Status:** implementation in progress on the local M1 integration candidate.
No change to the independent WorldKernel repository is included.

## 1. Goal in plain language

**Current behavior:** MirrorMind can execute the pinned WorldKernel
retail.inventory.demo at demo-1 through its optional local runner, and PR #58
contains a separate synthetic comparison for three replenishment policies.
The built-in demo models constant daily demand with immediate replenishment;
it cannot represent the policy comparison's 28-day demand profile, arrival
timing, three policy rules or explicit cost model.

**Desired behavior:** register one fixed, trusted MirrorMind retail policy
handler inside the isolated local worker, using WorldKernel's existing
register_world(name, handler, version=...) API. Map an exact versioned
MirrorMind policy request to worldkernel.simulation.v1, execute all 28 daily
transitions and paired replications through the pinned engine, then validate
worldkernel.result.v1 and the complete synthetic outcome against the
independent PR #58 reference implementation. The default M1F workflow
continues to use the in-process test double. Engine execution is opt-in for
the local CLI and unavailable through HTTP.

**Why:** the checked WorldKernel source already supports fixed trusted Python
handlers registered by code, without loading a handler from JSON. A
MirrorMind-owned handler can express the reviewed PR #58 rules while keeping
the external project unchanged and the dependency one way.

**Out of scope:** editing or vendoring WorldKernel, dynamic plugin loading,
HTTP or remote execution, untrusted-handler isolation, production resource
guarantees, real data, forecast claims, policy ranking, persistence, business
writes or automatic approval.

## 2. Versioned contract

MirrorMind source scenario: retail.policy_comparison version 1.

WorldKernel registered target: mirrormind.retail.policy_comparison
version mm-retail-policy-v1.

The adapter sends the existing worldkernel.simulation.v1 envelope:

- steps: exactly 28 daily transitions.
- runs: the bounded PR #58 replication count.
- seed: the declared synthetic seed.
- initial_state: the fixed empty policy-world state.
- parameters: exactly one 28-value demand profile, one lead-time
  sensitivity value, the complete validated inventory/cost assumption
  object, and the MirrorMind policy-world schema identifier.
- limits: operator-owned maxima for steps, runs and total transitions.

The handler returns serializable state only. The upstream exchange wraps
each run in worldkernel.result.v1, including its declared and registered
world revision. The revision label is trusted registration metadata; it is
not a package signature or source attestation. The exact upstream package
source SHA remains separately verified by the worker's PEP 610 metadata check.

The engine's per-run seed rule (scenario.seed + run_index) and one bounded
randrange(3) draw per day must reproduce the existing paired 75%, 100% and
125% demand multipliers. The parent verifies every returned demand sequence
and recomputes its digest. A result with an unsupported field, wrong revision,
wrong horizon, wrong seed, malformed policy metrics or a reference mismatch
is rejected; the adapter never fills missing values or changes policy
semantics to fit an engine.

## 3. Acceptance criteria

- [ ] Keep the optional exact WorldKernel SHA and default API independent of
  the package; the handler is registered only in the fixed local worker.
- [ ] Register exactly the MirrorMind policy-world name and version using
  trusted local Python code; never accept a module, path, callable, world name
  or registration version from the request.
- [ ] Map only the declared retail.policy_comparison@1 contract, revalidate
  all Pydantic input, reject unsupported fields, and enforce operator limits
  before process launch.
- [ ] Apply the shared PR #58 transition function once per day to all three
  policies using the same exogenous demand value and preserve its arrival-day
  caveat, units, costs and inventory conservation semantics.
- [ ] Bound the total three-scenario execution deadline and worker output;
  reject malformed JSON, wrong engine/world/revision, incomplete states,
  non-finite values and any mismatch against the reference simulator.
- [ ] Keep the current in-process test double as the no-engine default and
  add an explicit CLI opt-in. Do not let the HTTP route start local workers.
- [ ] Add synthetic unit regressions for strict mapping, registration,
  transition parity, run/step limits, deterministic pairing and invalid
  results. Add an exact-pin optional integration test that compares all
  returned policy metrics and demand digests with PR #58.
- [ ] Keep automated data fictional. No real workbook, customer row,
  credential, network fetch or WorldKernel source change is part of testing.
- [ ] Update the system map, API/debugging/learning guides, gateway contract,
  atlas, symbol catalog, evidence map, capability ledger, status, backlog and
  blocker register. Run the exact clean-head six-check local gate.

## 4. Architecture and data flow

~~~text
Explicit local CLI option
  -> M1F synthetic evidence and fixed profile
  -> RetailPolicyComparisonRequest (strict, fictional, 28 days)
  -> fail-closed MirrorMind mapping + operator limits
  -> fixed child worker verifies the pinned WorldKernel source
  -> register built-ins and one code-owned MirrorMind policy world/version
  -> WorldKernel run_scenario / event runtime (28 transitions per run)
  -> worldkernel.result.v1 (final state per paired replication)
  -> parent checks envelope, stream, policy metrics and reference parity
  -> existing M1F trace records the selected engine and conditional outcomes
~~~

The JSON request contains business inputs only. It cannot select executable
code. The parent retains a wall-clock deadline and bounded stdout/stderr;
WorldKernel's SDK is treated as a trusted local dependency, not as a sandbox.
The API route always uses the test double and never launches a subprocess.

## 5. Main symbols and contracts

- RetailPolicyComparisonRequest and RetailPolicyAssumptions remain the
  authoritative strict input models.
- advance_retail_policy_day is the one-day state transition reused by the
  local test double and WorldKernel handler, so day order and cost arithmetic
  do not drift.
- mirrormind_retail_policy_step translates one WorldKernel step into that
  shared transition for each policy, using one shared demand draw.
- build_worldkernel_policy_exchange_request accepts only the exact source
  contract and constructs the fixed registered target plus capped limits.
- LocalWorldKernelRetailPolicyGateway.compare executes the three lead-time
  sensitivity scenarios, validates each response, checks every stream against
  seed + replication, and compares policy metrics with the reference result.
- The M1F workflow receives this gateway only from explicit local composition;
  its HTTP handler has no gateway parameter and remains test-double-only.

Errors are sanitized at the worker boundary. Raw input, customer identifiers,
exception details and worker stderr are never included in output artifacts.
Missing or mismatched optional runtime, timeout, output overflow, invalid
JSON, registration failure and schema mismatch fail closed.

## 6. Verification and learning

The exact-pin integration regression proves that WorldKernel invoked the
registered MirrorMind handler, completed 28 steps for each configured run,
reproduced the paired streams and returned policy metrics identical to the
reference implementation. Unit fake-worker regressions prove parent-side
failure handling without requiring WorldKernel installation. They do not
prove source permission, forecast quality, hostile-code isolation or
production suitability.

Reproduce locally with the documented optional exact-SHA dependency and the
explicit --engine worldkernel CLI option. Compare its engine_execution
revision and output digest with the default test-double run. Then inspect
run_scenario, register_world and the event runtime at the pinned upstream
SHA; explain why a locally registered trusted handler is compatible while
the built-in immediate-replenishment demo is not. Finally, change the target
revision in a synthetic mapper test and verify that the adapter rejects it
before launching a worker.

## 7. Risks and follow-up

The external project supports trusted Python handlers but does not attest
their source or isolate them. This worker imports one handler shipped inside
MirrorMind and never loads a handler from request data. The parent timeout and
output caps are local bounds only; they do not provide general CPU, memory or
process-tree isolation. The optional exact SHA is not a redistribution
license. No HTTP route may execute this adapter until authentication,
admission and service resource controls receive a separate change request.

The comparison is still fictional. It does not establish historical demand,
inventory accuracy, calibrated forecasts, optimal policy semantics, source
rights, production compatibility or authority to place an order. Any change
to the PR #58 half-open lead-time interval requires a separate reviewed
contract and new regression.
