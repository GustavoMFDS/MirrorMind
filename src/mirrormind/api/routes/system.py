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
        "experimental": [
            "synthetic_observation_preflight",
            "synthetic_rolling_backtest",
            "synthetic_asof_availability",
            "synthetic_asof_rolling_backtest",
            "local_csv_snapshot_preflight",
            "local_staged_rolling_baselines",
            "local_uci_transaction_projection",
            "local_uci_xlsx_reader",
            "local_retail_coverage_diagnostics",
            "local_declared_calendar_coverage",
            "local_declared_retail_asof_audit",
            "local_retail_release_backtest",
            "local_retail_backtest_coverage_gate",
        ],
        "planned": [
            "evidence_and_rag",
            "forecasting",
            "agentic_orchestration",
            "worldkernel_adapter",
            "decision_evaluation",
            "cost_governance_enforcement",
        ],
    }
