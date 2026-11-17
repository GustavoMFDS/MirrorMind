"""Validate a scenario without executing a simulation."""
from fastapi import APIRouter

from ...core.contracts import ScenarioSpec

router = APIRouter()


@router.post("/v1/scenarios/validate")
def validate_scenario(spec: ScenarioSpec) -> dict[str, object]:
    return {
        "valid": True,
        "status": "validated_not_executed",
        "schema_version": spec.schema_version,
        "world_type": spec.world_type,
        "runs": spec.runs,
    }
