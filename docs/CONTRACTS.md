# Interoperability contracts — version 0.1

Current implemented **Pydantic validation only**: `ScenarioSpec` with `world_type`, `world_version`, `initial_state`, `parameters`, interventions, horizon, seed, runs, evidence/forecast references and a declared budget.

`EvidenceRef` fields: source ID, snapshot ID, observation cutoff and provenance. The service does not yet fetch data.
`ForecastRef` fields: ID, model version and forecast horizon. The service does not yet forecast.
`ExecutionBudget`: max simulation runs, model calls, output tokens, timeout. Current API rejects run-count over declaration; execution quotas are not yet implemented.
`SimulationGateway` Protocol: `execute(ScenarioSpec) -> SimulationSummary`. A versioned WorldKernel adapter will implement this in a later milestone.

## Example
```bash
curl -X POST http://127.0.0.1:8000/v1/scenarios/validate \
  -H "Content-Type: application/json" \
  --data @examples/retail-scenario.json
```

The response indicates `validated_not_executed`. No numbers presented as simulation outputs. Later contract versions must document data types/units, distributions, provenance hashes, engine/model versions, interventions, replay metadata and failures.
