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

- [ ] Given a 28-day integer demand profile, initial stock, lead time, cost coefficients, replication count and seed, the runner returns results for fixed-cycle, reorder-point and forecast-aware order-up-to policies.
- [ ] Each replication pre-generates one bounded synthetic daily demand stream and reuses it unchanged across all three policies; the report exposes one matching stream digest per policy and replication.
- [ ] Arrival timing, lost-sales proxy, order policy, item/day units and cost coefficients have explicit documented semantics.
- [ ] Results report fulfilled/unmet units, fill rate, stockout days, ending stock, orders, procurement/holding/order/unmet-demand costs and total synthetic cost units.
- [ ] A deterministic lead-time sensitivity sweep runs the same policies and paired-seed procedure for the base lead time and its bounded adjacent values.
- [ ] Inputs reject unsupported horizon, profile length, unit, cost, stock, seed and replication values; work is bounded before loops execute.
- [ ] A no-argument CLI runs a fictional scenario and prints stable, sanitized JSON with explicit experimental/test-double labels.
- [ ] The capability ledger, live capability handler, evidence map, atlas, generated symbol catalog and relevant architecture, API, debugging and learning docs agree.
- [ ] Focused tests, full repository validation and documentation guards pass. Official CI state is recorded separately.
- [ ] Mark M1E-03 `partial`: this test double does not satisfy its actual-engine dependency M1E-02 or the M1 completion gate.

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

- Commit / PR: pending.
- Modified symbols and files: pending.
- Tests executed, result, environment: pending.
- Claim IDs and cited test path/function: pending.
- Evidence/provenance/cutoff and uncertainty: fictional profile and explicit model assumptions only; no real-world forecast or calibrated uncertainty.
- Scope of human review and approval: local experimental capability only; no real-data, operational, production or engine approval.
- New or changed contracts: pending implementation.
- Docs updated: pending implementation.
- Known limitations / follow-up: M1E-02 actual engine, M1B/M1C empirical data and M1F end-to-end decision trace remain separate gates.
- Independent explanation: pending implementation.
