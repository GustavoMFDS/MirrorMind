"""Health and declared capability routes."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "mirrormind-api"}


@router.get("/v1/capabilities")
def capabilities() -> dict[str, object]:
    return {
        "status": "scaffold",
        "implemented": ["scenario_contract_validation", "health"],
        "experimental": ["synthetic_observation_preflight"],
        "planned": [
            "evidence_and_rag",
            "forecasting",
            "agentic_orchestration",
            "worldkernel_adapter",
            "decision_evaluation",
            "cost_governance_enforcement",
        ],
    }
