# ScenarioSpec and validation — contract-by-contract walkthrough

**Implemented status:** validation only. No data is fetched, no forecasts
are calculated, no WorldKernel simulation runs and no compute/model quotas
are enforced during execution. Read
[`core/contracts.py`](../../src/mirrormind/core/contracts.py),
[the API guide](API_WALKTHROUGH.md), [the version 0.1 contract](../CONTRACTS.md)
and [the current security obligations](../SECURITY.md).

This walkthrough covers an **input** contract. A separate immutable,
interface-only [decision result contract](DECISION_TRACE_RESULT.md)
demonstrates local trace shape and reference validation; it does not change
this route or imply that a result has been produced.

## 1. Exact route from JSON to a validated object

```text
POST /v1/scenarios/validate
  -> FastAPI parses an incoming JSON body
  -> Pydantic builds ScenarioSpec and its nested values
      -> EvidenceRef, ForecastRef, Intervention, ExecutionBudget
      -> ScenarioSpec.check_budget (model_validator after)
  -> API returns {valid, status, schema_version, world_type, runs}
       status = "validated_not_executed"
```

No code path calls `SimulationGateway.execute`. A successful 200
means *the declared shape and two cross-field rules passed*, not
that the evidence is authorized or that a decision is justified.

## 2. Contract fields, caller authority and blind spots

| Symbol / field | What the current source checks | What is **not** checked |
| --- | --- | --- |
| `EvidenceRef` | Nonempty `source_id`, `snapshot_id`, `observed_until`, `provenance` strings | Actual source rights, genuine snapshot, ISO timestamp parsing, cutoff ordering or content authenticity |
| `ForecastRef` | Nonempty forecast ID/model revision and horizon 1–366 | Forecast existence, training data, backtest, uncertainty calibration or whether a model can be called |
| `Intervention` | Nonempty kind, dictionary parameters | Whether intervention is meaningful, safe, authorized or supported by a specific world |
| `ExecutionBudget` | Run limit 1–10000, nonnegative model-call/token fields, timeout 1–3600 | **Runtime** CPU, dollars, model tokens, concurrency or worker cancellation |
| `ScenarioSpec` | Schema `0.1`, nonempty world/version, horizon 1–366, runs 1–10000, optional seed, state, parameters, references and budget | World handler registration, stock data, real forecast distribution, executable scenario compatibility |
| `ScenarioSpec.check_budget` | `runs <= max_simulation_runs`; referenced forecast horizon covers scenario horizon | Forecast correctness, per-tenant quotas or elapsed-time enforcement |

These are ordinary Pydantic models, not frozen security tokens.
Pydantic's default coercion and handling of extra fields are part of
the current behavior: **do not infer exact-int strict validation,
a blanket unknown-key rejection, or cryptographic provenance**.
Any move to strict field types or `extra="forbid"` is a contract
compatibility decision requiring focused tests and migration review.

### Why an evidence cutoff string is not evidence validation

The current `observed_until` uses `Field(min_length=1)`.
This accepts a nonempty arbitrary string; it does **not**
establish a genuine UTC cutoff or prevent temporal leakage.
Before live ingestion or forecasting, add explicit timestamp
and provenance checks in a separate reviewed feature module.
Do not backfill missing observations with generative guesses.

## 3. Minimal, safe reproduction

```python
from pydantic import ValidationError
from mirrormind.core.contracts import ScenarioSpec

valid = ScenarioSpec(
    world_type="retail.inventory",
    world_version="0.1",
    horizon_days=28,
    runs=2,
    budget={"max_simulation_runs": 2},
)
assert valid.horizon_days == 28

try:
    ScenarioSpec(
        world_type="retail.inventory",
        world_version="0.1",
        horizon_days=28,
        runs=5,
        budget={"max_simulation_runs": 4},
    )
except ValidationError:
    pass
else:
    raise AssertionError("budget declaration should reject 5 > 4")
```

Even the valid object is **not** a simulation job.
It contains inputs that later services must authorize and validate.

## 4. Review real tests before believing a claim

| Claim ID | Test and concrete observation | Important limitation |
| --- | --- | --- |
| **MM-CON-001** | `tests/unit/test_contracts.py::test_exceeding_budget_rejected` checks excess declared runs are rejected | No actual runtime budget enforcement or resource metering |
| **MM-CON-002** | `tests/unit/test_contracts.py::test_forecast_coverage_rejected` rejects a forecast horizon shorter than the scenario horizon | It does not verify forecast provenance, statistical validity, cutoff or even existence |
| **MM-CON-003** | `tests/unit/test_contracts.py::test_valid_scenario` accepts a simple `ScenarioSpec` | It does not execute the scenario or make a prediction |

Run in a disposable local environment:

```bash
python -m pytest -q tests/unit/test_contracts.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
```

The commands are reproduction instructions, not a claim of
local execution at documentation authoring time. The curated
map checks file paths/pytest function presence and claim IDs,
**not** whether these tests prove all surrounding prose.

## 5. Independent practice: distinguish form from truth

Predict the validation result for: a five-run scenario with a
four-run declaration; a seven-day forecast reference for a
28-day scenario; an evidence reference with `observed_until="later"`;
an intervention with kind `"unknown"`; and a valid request that
names a world with no actual registered simulator.

For each, explain **whether the code validates structure or
authenticates real-world truth**. Locate the relevant test,
then write *What I understood / What I can now change /
What remains unclear*. No domain conclusion may be stated
without sourced evidence and validated predictive/simulation
assumptions.
