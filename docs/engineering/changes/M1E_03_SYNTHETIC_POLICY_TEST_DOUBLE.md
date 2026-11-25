# Change request — M1E-03 synthetic retail policy comparison

## 1. Goal in plain language

**Current behavior:** MirrorMind has a `SimulationGateway` protocol and a strict WorldKernel request mapper, but no policy simulator or comparison workflow. The mapper only prepares one exact `retail.inventory.demo` request and never executes it. See [the gateway contract](../../../src/mirrormind/modules/simulation/gateway.py), [the WorldKernel mapping](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py), and [the M1 backlog](../TASK_BACKLOG.md).

**Desired behavior:** add a deterministic local test double that compares three explicit retail replenishment policies over a 28-day synthetic horizon. Every policy in a replication must receive the same pre-generated demand sequence. The report includes inventory, service and synthetic cost outcomes, assumptions, seeds, sensitivity to lead time and a digest that binds each policy to the paired stream.

**Why:** the M1 plan explicitly permits a clearly labeled test double while an actual adapter is unavailable. This advances the central retail workflow without presenting synthetic outcomes as measured business facts or claiming WorldKernel execution.

**Out of scope:** real data, forecasts, source approval, actual WorldKernel execution, API simulation routes, durable jobs, recommendations, policy ranking, automatic writes, credentials and deployment.

## Capability status change

- Previous: `worldkernel_adapter` remains `planned`; no simulation capability is implemented.
- Proposed: add `local_retail_policy_test_double` as `experimental`. Keep `worldkernel_adapter` planned and distinguish this test double from M1E-02.
- Production behavior: deterministic in-process simulation from an explicitly supplied synthetic demand profile and explicit assumptions; no external side effects.
- Tests: deterministic replay, shared paired-demand digest, policy mechanics, failure validation and lead-time sensitivity. These prove only this local simulator and fixture contract.
- Update `GET /v1/capabilities` through the existing capability ledger and verify handler/ledger parity. Add no simulation route.

## 2. Acceptance criteria

- [x] Given a 28-day integer demand profile, initial stock, lead time, cost coefficients, replication count and seed, the runner returns results for fixed-cycle, reorder-point and forecast-aware order-up-to policies.
- [x] Each replication pre-generates one bounded synthetic daily demand stream and reuses it unchanged across all three policies; the report exposes one matching stream digest per policy and replication.
- [x] Arrival timing, lost-sales proxy, order policy, item/day units and cost coefficients have explicit documented semantics.
- [x] Results report fulfilled/unmet units, fill rate, stockout days, ending stock, orders, procurement/holding/order/unmet-demand costs and total synthetic cost units.
- [x] A deterministic lead-time sensitivity sweep runs the same policies and paired-seed procedure for the base lead time and its bounded adjacent values.
- [x] Inputs reject unsupported horizon, profile length, unit, cost, stock, seed and replication values; work is bounded before loops execute.
- [x] A no-argument CLI runs a fictional scenario and prints stable, sanitized JSON with explicit experimental/test-double labels.
- [x] The capability ledger, live capability handler, evidence map, atlas, generated symbol catalog and relevant architecture, API, debugging and learning docs agree.
- [x] Focused tests, full repository validation and documentation guards pass. Official CI state is recorded separately.
- [x] Mark M1E-03 `partial`: this test double does not satisfy its actual-engine dependency M1E-02 or the M1 completion gate.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m1_retail_policy_test_double.py` | Add fictional CLI | Integration test runs twice and checks deterministic, labeled output |
| Core implementation | `src/mirrormind/domains/retail/policy_simulation.py` | Add typed assumptions, paired streams, policy runner, aggregation and sensitivity | Unit tests for mechanics, determinism, pairing, bounds and sensitivity |
| Capability declaration | `docs/engineering/CAPABILITY_LEDGER.json` | Add only experimental local test-double capability | `scripts/docs/capabilities.py --check` |
| API metadata | `src/mirrormind/api/routes/system.py` | Add capability ID to the existing metadata response; no execution route | `tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger` |
| State / persistence | None | No persistence | Import and filesystem boundary tests |
| Calling components | Existing retail evidence/evaluation and `SimulationGateway` | No implicit join or forecast claim | Existing consumers unchanged; test-double guide describes manual boundary |
| Downstream consumers | `docs/engineering/SYSTEM_MAP.md`, `API_WALKTHROUGH.md`, `DEBUGGING.md`, `LEARNING.md`, M1 plan/status/backlog, `REPOSITORY_ATLAS.md`, ledgers and catalog | Update | Relevant guards and cited test functions |
| External project/contracts | WorldKernel `simulation.v1` | No change; this runner is not the WorldKernel adapter | Import guard and explicit limitation |

## Data, modeling and decision review

- Dataset card: not applicable; all demand values are caller supplied and the CLI uses fictional values.
- Forecast model card: not applicable; the profile is an explicit synthetic assumption, not a forecast or model output.
- Decision trace: no recommendation or action is produced. Outcomes must not be labeled as an approved business decision.
- WorldKernel gate: actual engine execution remains governed by M1E-02 and [the gateway acceptance gate](../WORLDKERNEL_GATEWAY_GATE.md). The test double must not be passed off as a compatible engine result.
- Leakage and fabricated measurements: generated demand draws are paired exogenous inputs. Synthetic coefficients, results and costs are labeled; no observed stock, sales, lead time, costs or service level are inferred.

## 4. Constraints and risks

The calculation must be pure, bounded, deterministic and free of network, filesystem, database and optional-engine imports. Validate all caller-controlled bounds before allocating streams. Use one shared demand stream per replication to support paired policy comparison. Use integer item counts and abstract synthetic cost units to avoid accidental currency claims. Clearly define arrival and daily ordering boundaries. The forecast-aware policy may use only the caller supplied expected-demand profile; its label is algorithmic and does not certify forecast quality.

## 5. Implementation plan

1. Trace `SimulationGateway`, `ScenarioSpec`, capability registration and existing retail examples/tests.
2. Add a typed local retail experiment contract and explicit policy algorithms with strict bounds.
3. Add focused unit and integration regressions, including determinism and paired-stream invariants.
4. Add the experimental capability, regenerate the symbol catalog, link every new path in the reviewed atlas, and update human-written walkthrough, architecture, debugging and learning docs.
5. Run the exact-head local quality gate, relevant tests and all required documentation checks; report CI separately.

## 6. Evidence after implementation

- Commit / PR: code commit `09d047b431cc4c50fb6d1abdb88a494a4c7f6f7f`; draft [PR #58](https://github.com/GustavoMFDS/MirrorMind/pull/58), stacked on PR #55.
- Modified symbols and files: `RetailPolicyAssumptions`, `RetailPolicyComparisonRequest`, `_build_demand_streams`, `_order_quantity`, `_simulate_replication`, `_aggregate_policy`, `_lead_time_scenarios`, `compare_synthetic_retail_policies`, the fictional CLI, capability metadata, tests, catalog, atlas and walkthroughs listed below.
- Tests executed, result, environment: focused unit + CLI tests passed 10/10; `tests/integration/test_api.py` passed 6/6 with one existing Starlette/httpx deprecation warning. The exact code commit passed the canonical local gate: 747 pytest tests, Ruff, symbol catalog, atlas, evidence and capability checks. The local gate ran in the approved unrestricted Windows checkout; it is not official CI.
- Official CI for the PR #58 code head: Actions `test` [45440111223](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45440111223) and `symbol-catalog` [45440111132](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45440111132) failed before job steps with the B-08 account payment/spending-limit annotation. No remote repository test result exists.
- Claim IDs and cited test path/function: `MM-SIM-001` cites `tests/unit/test_retail_policy_simulation.py::test_three_policies_share_each_reproducible_demand_stream`; `local_retail_policy_test_double` cites `tests/integration/test_retail_policy_simulation_cli.py::test_synthetic_policy_cli_replays_paired_comparison`.
- Evidence/provenance/cutoff and uncertainty: fictional profile and explicit model assumptions only; no real-world forecast or calibrated uncertainty.
- Scope of human review and approval: local experimental capability only; no real-data, operational, production or engine approval.
- New or changed contracts: experimental capability `local_retail_policy_test_double`; local output schema `mirrormind.retail.policy_comparison.v1`. `GET /v1/capabilities` reports the capability; no simulation HTTP route or WorldKernel contract changed.
- Docs updated: `M1_RETAIL_POLICY_SIMULATION.md`, `SYSTEM_MAP.md`, `API_WALKTHROUGH.md`, `DEBUGGING.md`, `LEARNING.md`, `M1_EXECUTION_PLAN.md`, `PROJECT_STATUS.md`, `TASK_BACKLOG.md`, `CAPABILITY_LEDGER.json`, `EVIDENCE_MAP.json`, `REPOSITORY_ATLAS.md`, `SEMANTIC_COVERAGE.md`, `ARCHITECTURE.md`, `CONTRACTS.md`, `RETAIL_MVP.md`, `ROADMAP.md`, `STRUCTURE.md`, engineering README and generated `SYMBOLS.md`.
- Known limitations / follow-up: M1E-02 actual engine, M1B/M1C empirical data and M1F end-to-end decision trace remain separate gates.
- Independent explanation: run `python -m examples.m1_retail_policy_test_double`, compare per-replication demand digests across the three policy rows, then change the seed and rerun `tests/unit/test_retail_policy_simulation.py` to see pairing and replay guarantees.

## Independent review correction — arrival-day demand caveat

Review of PR #58 identified that the profile-aware policy sums expected demand
over `[day + 1, arrival_day)`. The existing boundary test confirmed this is
the documented toy rule, rather than an accidental discrepancy, but the
comparison did not expose the limitation in its output. For a one-day lead
time the interval is empty; at zero inventory position and zero safety stock,
the target and order are zero even when expected arrival-day demand is
positive. The name `forecast_aware_order_up_to` must not be read as a claim
that this is a conventional protection-period or optimized policy.

The correction preserves the half-open interval and the existing
`test_profile_aware_target_stops_before_arrival_day` boundary. The result now
includes `modeling_caveats` with the excluded arrival-day demand, the concrete
one-day case and the toy-policy limitation. The CLI integration test checks
that the caveat remains visible in the emitted JSON. A separate mass-balance
regression verifies item conservation for each policy, scenario and
replication under the local event order. This metadata does not establish
that downstream consumers persist it; PR #59 must carry the caveat into its
decision trace, with a focused integration test.

- Reproduction: `tests/unit/test_retail_policy_simulation.py::test_one_day_zero_safety_stock_exclusion_is_exposed_as_caveat` first failed because the output had no `modeling_caveats`, after confirming positive arrival-day demand and a zero order. After the correction, the regression passes and checks the exact output caveats.
- Conservation: `tests/unit/test_retail_policy_simulation.py::test_inventory_mass_balance_holds_for_every_policy_replication` checks initial stock plus procurement equals fulfilled demand, ending stock and pending orders when the fixture uses a unit procurement coefficient of one.
- Consumer contract: `tests/integration/test_retail_policy_simulation_cli.py::test_synthetic_policy_cli_replays_paired_comparison` asserts the caveat is present and does not call the rule standard or optimized.
- Focused validation: `python -m pytest -q tests/unit/test_retail_policy_simulation.py tests/integration/test_retail_policy_simulation_cli.py` passed 12 tests; focused Ruff passed.
- Integrated validation: merge commit `2f4822eafb768f289d03b10b6581c1e87c57bc4d` reconciles the corrected #55 dependency into #58 and carries the review correction. Exact integrated heads `b7d226f41d17f4db3f1b220b417309cc0872b614` and `624fd5a8f01b9063da739c4f6e3864336978ad95` passed the complete local gate: 768 tests, Ruff, symbol catalog, atlas, evidence and capability checks. The final receipt is `mirrormind-624fd5a8f01b-quality.json` under the local temporary directory. One existing Starlette/httpx deprecation warning appeared. The published #58 head's Actions `test` [run 45522497099](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522497099) and `symbol-catalog` [run 45522497076](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522497076) failed before job steps with the explicit B-08 account payment/spending-limit annotation. They provide no remote code-test result.
- Limitations: no algorithm semantics changed; this does not make the policy a conventional order-up-to method or establish inventory quality. The local test double still does not invoke WorldKernel. Actual execution remains gated by B-04.

Learning exercise: reproduce the zero-stock/one-day case, inspect the result
metadata, and trace it through `_order_quantity`. Then explain why preserving
the implementation boundary is different from claiming the boundary is a
retail standard. A future protection-period policy would require a separately
reviewed change request and distinct acceptance tests.

## PR #55 dependency synchronization and exact-head gate — 2026-11-25

Merge `5544bc0c2116d825a37d49a3ec75960e9896dd23` synchronizes PR #58 with
the published PR #55 head `56aa92a6920a429b83458380231642fe59feaf08`. This
retains PR #55's mutation-safe `ScenarioSpec` validation and effective minimum
run ceiling, with no duplicate cherry-picks. It also retains the PR #53 nested
receipt authority regressions. The exact merge head passed the complete local
gate at 2026-11-25 05:12:21 UTC: 768 tests, Ruff, symbol catalog, atlas,
evidence and capability checks. One existing Starlette/httpx deprecation
warning appeared. This is local evidence, not official Actions.

The review caveat remains visible in `test_profile_aware_target_stops_before_arrival_day`
and `test_one_day_zero_safety_stock_exclusion_is_exposed_as_caveat`; conservation
and paired-stream behavior remain checked by
`test_inventory_mass_balance_holds_for_every_policy_replication`,
`test_three_policies_share_each_reproducible_demand_stream`, and
`test_sensitivity_reuses_the_same_paired_streams`. The one-day rule is still a
toy heuristic, not an optimized or conventional inventory policy. The latest
published PR #58 head before this sync was `46b07a0`; its Actions test
[45522848614](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522848614)
and symbol-catalog
[45522848658](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522848658)
checks failed before job steps with an annotation listing alternative account
conditions. It did not identify the cause and ran no repository tests. Actual
WorldKernel execution remains blocked by B-04.
