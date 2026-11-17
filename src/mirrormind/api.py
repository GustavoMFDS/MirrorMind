"""Minimal HTTP scaffold; no expensive or external operations are performed."""
from fastapi import FastAPI

from .contracts import ScenarioSpec

app = FastAPI(title="MirrorMind", version="0.0.1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "mirrormind-api"}


@app.get("/v1/capabilities")
def capabilities() -> dict[str, object]:
    return {
        "status": "scaffold",
        "implemented": ["scenario_contract_validation", "health"],
        "planned": [
            "evidence_and_rag",
            "forecasting",
            "agentic_orchestration",
            "worldkernel_adapter",
            "decision_evaluation",
            "cost_governance_enforcement",
        ],
    }


@app.post("/v1/scenarios/validate")
def validate_scenario(spec: ScenarioSpec) -> dict[str, object]:
    return {
        "valid": True,
        "status": "validated_not_executed",
        "schema_version": spec.schema_version,
        "world_type": spec.world_type,
        "runs": spec.runs,
    }
