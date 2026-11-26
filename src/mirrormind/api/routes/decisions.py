"""Experimental local-only decision comparison endpoints."""
from fastapi import APIRouter, HTTPException

from ...domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)

router = APIRouter()


@router.post("/v1/decision-workflows/retail/synthetic")
def compare_synthetic_retail_decisions(
    request: SyntheticDecisionWorkflowRequest,
) -> dict[str, object]:
    """Return a deterministic fictional comparison without writes or engine I/O."""
    try:
        return run_synthetic_decision_workflow(request)
    except (OSError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail="synthetic retail decision workflow could not be evaluated",
        ) from exc
