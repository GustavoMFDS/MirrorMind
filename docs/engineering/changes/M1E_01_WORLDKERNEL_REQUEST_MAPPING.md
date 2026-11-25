# Change request — Strict WorldKernel request mapping

## 1. Goal in plain language

**Current behavior:** MirrorMind validates `ScenarioSpec` values, while
`SimulationGateway` is only a protocol. WorldKernel independently exposes a
local JSON exchange, but its request is not interchangeable with
`ScenarioSpec`.

**Desired behavior:** add a pure, deterministic mapper for the one reviewed
built-in retail world. Require an exact MirrorMind world/version pair, an
explicit compatible unit context, a supported state and parameter shape, and
operator-configured step/run/transition limits. Revalidate mutable scenario
state at the mapping boundary and ensure the emitted run ceiling is the lower
of scenario and operator budgets. Reject references or interventions that the
exchange cannot faithfully represent. The mapper must not import, install,
start or call WorldKernel.

**Why:** M1E-01 is a P0 dependency for an actual optional engine adapter. A
tested translation boundary can be completed independently while the engine
pin and runtime acceptance remain blocked by B-04.

**Out of scope:** installing or vendoring WorldKernel, execution, result
parsing, HTTP or process adapters, timeout/cancellation enforcement, model
validity, forecasts, recommendations, persistence, public API changes and
real retail data.

### External contract inspected

The connected `GustavoMFDS/WorldKernel` `main` contents were inspected on
2026-11-24: `docs/EXCHANGE.md`, `docs/TRUSTED_WORLD_VERSIONS.md`,
`docs/RESOURCE_LIMITS.md`, `src/worldkernel/adapters/exchange.py`,
`src/worldkernel/examples/bootstrap.py` and
`src/worldkernel/examples/inventory.py`. The v1 request has a strict root
field set, and the built-in `retail.inventory.demo` world is registered as
`demo-1`. Its step uses daily demand, stock, reorder point and reorder
quantity; replenishment is immediate and does not model lead time. The
registration revision is metadata, not a signed or immutable release. This
review is not a runtime pin or compatibility certification.

## 2. Acceptance criteria

- [x] Map only `retail.inventory` version `0.1` to the exact trusted exchange
  world `retail.inventory.demo` version `demo-1`.
- [x] Require explicit `item`, `day` and `order` unit declarations; validate
  required inventory state and parameters as non-negative integers.
- [x] Reject unknown/missing state or parameters, every unsupported
  intervention, evidence or forecast references, and unit/world revisions
  outside the allowlist.
- [x] Enforce operator-owned limits supplied separately from `ScenarioSpec`;
  reject horizon and total transitions over those limits, revalidate the
  current mutable scenario, and cap requested/emitted runs by both the
  scenario budget and operator ceiling.
- [x] Produce a deterministic JSON-compatible request without importing or
  requiring the WorldKernel package; do not execute the request.
- [x] Keep API responses and capability claims unchanged; the adapter remains
  planned and actual engine execution remains unverified.
- [x] Add positive and adverse unit tests, a runnable mapping example, a
  source walkthrough, learning/debugging guidance, precise evidence limits,
  and reviewed atlas/catalog coverage.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| HTTP/API | `api/routes/scenarios.py`, `api/routes/system.py` | No route or capability change | Existing API contract remains authoritative; no engine import path added |
| Core input | `core/contracts.py::ScenarioSpec` | No schema change | Existing contract tests; mapper rejects unrepresentable values |
| Simulation mapping | `modules/simulation/worldkernel_mapping.py::build_worldkernel_exchange_request` | Add pure strict mapping and operator-limit/unit context types | New unit test module proves allowlist, deterministic construction and fail-closed cases |
| Optional dependency | `pyproject.toml` | No WorldKernel dependency | Import guard in unit tests |
| Documentation/evidence | engineering maps, guide, CR, atlas, evidence map | Update | Catalog, atlas, evidence and capability guards |
| External project | WorldKernel | Read-only contract inspection | No cross-repository edit; B-04 remains for pinned runtime acceptance |

## Data and trust review

All test/example values are synthetic. The mapping does not verify source
rights, unit provenance, world code identity or registered-world trust. The
unit context is an explicit caller assertion. `demo-1` identifies the remote
trusted registration manifest entry, not a cryptographic artifact. Caller
data cannot raise the separately supplied operator caps. The outgoing run
limit is the minimum of the scenario budget and operator ceiling, and the
mapper reconstructs the scenario from its current serialized fields so
post-construction mutation cannot bypass cross-field validation. The mapper
alone does not authenticate who constructed the operator limits or enforce
wall-clock, worker, memory or server budgets. WorldKernel exchange v1 has no
fields for `timeout_seconds`, `max_model_calls` or `max_output_tokens`; a
future execution adapter must enforce applicable values or reject before
execution.

## 4. Compatibility and risks

No `ScenarioSpec` or HTTP schema changes. Existing inputs that include an
unsupported intervention or omit a required model input continue to validate
as scenarios but fail at the new mapping boundary. This is intentional
fail-closed behavior: the current WorldKernel demo otherwise supplies its own
default demand/reorder values. A scenario that was mutated into an invalid
state after construction now fails at mapping with `WorldKernelMappingError`.
The mapper returns a plain request object only; it makes no runtime, forecast,
business-validity or security guarantee.

## 5. Implementation plan

1. Confirm the MirrorMind scenario, gateway and M1 backlog plus the current
   WorldKernel exchange/handler contract. Keep the cross-repository boundary
   read-only.
2. Write tests for an exact mapping, unit and version checks, unrepresentable
   references/interventions, strict state/parameter shapes and operator caps.
3. Implement one pure module with no WorldKernel import and run the example.
4. Document the execution boundary, limitations, source trace, tests and
   exercises; keep capability status planned.
5. Regenerate and check the symbol catalog, reviewed atlas, evidence and
   capability metadata; run focused and applicable local gates.

## 6. Evidence after implementation

- Branch: `codex/m1e-01-worldkernel-mapping`, stacked on the M1F-01 branch;
  draft [PR #55](https://github.com/GustavoMFDS/MirrorMind/pull/55), source
  commit `87692412606e65b5e1500164b2c8708bb98cf120`.
- Modified symbols: `SUPPORTED_WORLD_MAPPINGS`,
  `WorldKernelOperatorLimits`, `InventoryWorldUnitContext` and
  `build_worldkernel_exchange_request` in
  `src/mirrormind/modules/simulation/worldkernel_mapping.py`.
- Tests at the original implementation head:
  `tests/unit/test_worldkernel_mapping.py` passed **25 tests**. The
  canonical local gate on docs head
  `2330dc50a49bb80abc601b0635e5e7d4916ee283` passed **737 tests**, including
  `tests/integration/test_api.py`; Ruff, symbol catalog, atlas, evidence and
  capability checks also passed. Pytest reported one existing
  Starlette/httpx deprecation warning. The API import guard loads FastAPI
  while rejecting every `worldkernel` package import.
- Example: `python examples/m1e_01_worldkernel_mapping.py` ran twice with
  identical output. It prints a request; it does not execute one.
- Quality: Ruff passed for `src`, `tests` and the new example. Symbol catalog,
  atlas coverage, evidence and capability guards, direct capability-handler /
  ledger parity, and `git diff --check` passed.
- Evidence claim: `MM-WKMAP-001` cites
  `tests/unit/test_worldkernel_mapping.py::test_supported_inventory_scenario_maps_to_exact_v1_request`.
- Local versus official: the exact PR #55 docs head passed the complete
  local gate outside the restricted sandbox, resolving B-07 for this stack.
  PR #52 implementation SHA `c51ab30370db47e9f7105c97f870008e4fc442c5`
  separately passed the canonical gate with 696 tests including API. On PR
  #55 docs head `2330dc50a49bb80abc601b0635e5e7d4916ee283`, official `test` run
  [45330280291](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45330280291)
  and `symbol-catalog` run
  [45330280468](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45330280468)
  failed before job start with the verified B-08 billing/spending-limit
  annotation; no repository job ran. No CI success is claimed.
- Capability and compatibility: no API or capability ledger changes;
  `worldkernel_adapter` remains planned. `ScenarioSpec` schema is unchanged.
- Data and provenance: fictional values; explicit unit context is an
  assertion, not source evidence. WorldKernel `demo-1` is registration
  metadata, not immutable code identity.
- Deferred work / blockers: B-04 still blocks a pinned compatible SDK,
  registered-world execution and actual result validation. The mapper does
  not enforce worker/server quotas, timeout, cancellation, memory or CPU.
- Reproduction:
  `python -m pytest -q tests/unit/test_worldkernel_mapping.py`;
  `python examples/m1e_01_worldkernel_mapping.py`;
  `python scripts/docs/catalog.py --check`;
  `python scripts/docs/coverage.py --check`;
  `python scripts/docs/evidence.py --check`;
  `python scripts/docs/capabilities.py --check`.

## 7. Independent review correction — scenario budget boundary

Review of PR #55 identified that `ScenarioSpec` is mutable: a caller could
construct a scenario that satisfies its nested run budget, mutate `runs`, and
then map the invalid object. It also found that the request's declared
`max_runs` could exceed the scenario's own lower budget when the operator cap
was higher. Both cases were reproduced before the correction.

The mapper now revalidates a Python-mode snapshot at entry, converts only
Pydantic `ValidationError` into the generic mapping-boundary error, and emits
`min(operator_limits.max_runs, scenario.budget.max_simulation_runs)`. Focused
regressions are named
`test_mapping_revalidates_mutated_scenario_before_budget_mapping` and
`test_mapping_preserves_lower_scenario_or_operator_run_ceiling`. They prove
local validation and request declaration only. The pure mapper still does not
execute WorldKernel or enforce worker resources. Mapping and execution budgets
not representable in exchange v1 remain an explicit future-adapter contract.

The review correction is in the integrated PR #55 candidate at
`07c405b0d49ab05611413acce61af1123111fb48`; documentation follow-up
`4d1d5b92e990f6d771209097fde1622c3c88958f` preserves the same source state.
The exact clean SHAs `07c405b`, `4d1d5b9`, `970843e`, `3f9bbb8` and the
reconciled merge `fd72b76` passed the complete integrated local gate: 756 tests, Ruff, symbol catalog, atlas,
evidence and capability checks. Pytest reported one existing Starlette/httpx
deprecation warning. A restricted replay of `07c405b` timed out at 900 seconds
in pytest; complete passes ran outside that sandbox and did not skip tests.
Pre-sync branch head `3f9bbb876336334aac9abe289f9f9c0161d42b72` was
fast-forward-pushed. Its [test run 45518147296](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518147296)
and [symbol-catalog run 45518147363](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518147363)
failed before repository steps under B-08. The reconciled merge
`fd72b76` has a full local pass but is not yet published. None of this
verifies WorldKernel execution, server resource enforcement, or official CI
success.

## 8. PR #54 dependency synchronization — 2026-11-25

Merge commit `b9eba02` synchronizes PR #55 with published PR #54 head
`4d220066c3e9ab83a321ac9517bbabc8fc22e293`. It preserves the original review
fix ancestry and carries PR #53's nested-receipt regressions without
cherry-picking duplicate commits. Shared blocker, status and backlog records
were reconciled; the WorldKernel mapping behavior and its acceptance boundary
remain unchanged.

The complete local quality gate passed on merge commit
`b9eba02eb9dab228215ef2f731e693ae086d5751` and documentation follow-up
`cc9bdb4739507baa55cb857579ef70f7c92430d8`. On exact head `cc9bdb4` at
2026-11-25 04:37:00 UTC, 756 pytest tests, Ruff, symbol catalog, repository
atlas, evidence map and capability checks passed. The API suite ran; one
existing Starlette/httpx TestClient deprecation warning appeared. This is
local evidence, not official CI. The
latest published PR #55 pre-sync head `b292db0` had failed Actions before
repository steps under B-08; checks on the synchronized head remain pending
publication. B-04 still blocks actual WorldKernel execution and result
validation.
