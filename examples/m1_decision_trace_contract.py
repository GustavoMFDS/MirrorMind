"""Print a deterministic fictional v1 trace; references have no authority."""

import json

from mirrormind.core.decision_trace import DecisionTrace


def build_synthetic_trace() -> DecisionTrace:
    """Construct one complete, pending-review trace using fictional records."""
    return DecisionTrace.model_validate(
        {
            "trace_id": "trace-demo-001",
            "decision_ref": "decision-demo-001",
            "revision": 1,
            "question": "Which fictional replenishment policy has lower modeled cost?",
            "cutoff_at": "2026-11-24T13:00:00-03:00",
            "created_at": "2026-11-24T14:00:00-03:00",
            "evidence": [
                {
                    "evidence_id": "evidence-demo-001",
                    "source_ref": "fictional-source-001",
                    "snapshot_ref": "fictional-snapshot-001",
                    "provenance_ref": "fictional-dataset-card-001",
                    "available_at": "2026-11-24T12:45:00-03:00",
                }
            ],
            "observations": [
                {
                    "fact_id": "fact-demo-001",
                    "value": 7,
                    "unit": "units",
                    "observed_at": "2026-11-24T12:00:00-03:00",
                    "evidence_refs": ["evidence-demo-001"],
                }
            ],
            "forecasts": [
                {
                    "forecast_id": "forecast-demo-001",
                    "target_ref": "fictional-product-day-2026-11-25",
                    "value": 8,
                    "unit": "units",
                    "model_card_ref": "fictional-model-card-001",
                    "fact_refs": ["fact-demo-001"],
                }
            ],
            "assumptions": [
                {
                    "assumption_id": "assumption-demo-001",
                    "statement": "Fictional supplier lead time stays at two days.",
                }
            ],
            "outcomes": [
                {
                    "outcome_id": "outcome-demo-001",
                    "alternative_ref": "fictional-policy-a",
                    "engine_contract_ref": "fictional-engine-v1",
                    "forecast_refs": ["forecast-demo-001"],
                    "assumption_refs": ["assumption-demo-001"],
                    "metrics": [
                        {"name": "remaining_stock", "value": 2, "unit": "units"}
                    ],
                    "seed": 42,
                    "runs": 10,
                }
            ],
            "missing_evidence": [
                {
                    "gap_id": "gap-demo-001",
                    "description": "Opening stock is not independently measured.",
                    "blocks_refs": ["outcome-demo-001"],
                }
            ],
            "costs": [
                {
                    "cost_id": "cost-demo-001",
                    "category": "simulation_compute",
                    "amount": "0.10",
                    "unit": "USD",
                    "status": "declared",
                    "source_ref": "fictional-cost-assumption-001",
                },
                {
                    "cost_id": "cost-demo-002",
                    "category": "model_tokens",
                    "amount": None,
                    "unit": "tokens",
                    "status": "unavailable",
                    "source_ref": None,
                },
                {
                    "cost_id": "cost-demo-003",
                    "category": "fictional_model_calls",
                    "amount": "0",
                    "unit": "calls",
                    "status": "metered",
                    "source_ref": "fictional-meter-receipt-001",
                },
            ],
            "human_review": {"status": "pending", "reviewer_ref": "reviewer-demo-001"},
        }
    )


def render_example() -> str:
    """Return canonical, repeatable example JSON for review and regression tests."""
    trace = build_synthetic_trace()
    return json.dumps(
        {"trace": trace.model_dump(mode="json"), "result_sha256": trace.result_sha256},
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        indent=2,
    )


def main() -> None:
    print(render_example())


if __name__ == "__main__":
    main()
