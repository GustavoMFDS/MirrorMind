"""Synthetic contract tests; no evidence, model or engine is authenticated here."""
import json
from copy import deepcopy

import pytest
from pydantic import ValidationError

from examples.m1_decision_trace_contract import build_synthetic_trace, render_example
from mirrormind.core.decision_trace import DecisionTrace


def _valid_trace_payload() -> dict[str, object]:
    return build_synthetic_trace().model_dump(mode="json")


def test_valid_trace_keeps_decision_evidence_categories_separate():
    trace = DecisionTrace.model_validate(_valid_trace_payload())

    assert trace.schema_version == "mirrormind.decision_trace.v1"
    assert trace.observations[0].fact_id == "fact-demo-001"
    assert trace.forecasts[0].fact_refs == ("fact-demo-001",)
    assert trace.outcomes[0].assumption_refs == ("assumption-demo-001",)
    assert trace.costs[1].amount is None
    assert trace.costs[2].status == "metered"
    assert len(trace.result_sha256) == 64


def test_synthetic_example_json_is_reproducible():
    first = render_example()
    second = render_example()

    assert first == second
    document = json.loads(first)
    assert document["trace"]["schema_version"] == "mirrormind.decision_trace.v1"
    assert document["trace"]["human_review"]["status"] == "pending"
    assert len(document["result_sha256"]) == 64


def test_unknown_local_references_are_rejected():
    payload = _valid_trace_payload()
    payload["forecasts"][0]["fact_refs"] = ["fact-missing"]  # type: ignore[index]

    with pytest.raises(ValidationError, match="unknown fact reference"):
        DecisionTrace.model_validate(payload)

    evidence = _valid_trace_payload()
    evidence["observations"][0]["evidence_refs"] = ["evidence-missing"]  # type: ignore[index]
    with pytest.raises(ValidationError, match="unknown evidence reference"):
        DecisionTrace.model_validate(evidence)


def test_outcome_requires_known_forecasts_and_assumptions():
    forecast = _valid_trace_payload()
    forecast["outcomes"][0]["forecast_refs"] = ["forecast-missing"]  # type: ignore[index]
    with pytest.raises(ValidationError, match="unknown forecast reference"):
        DecisionTrace.model_validate(forecast)

    assumption = _valid_trace_payload()
    assumption["outcomes"][0]["assumption_refs"] = ["assumption-missing"]  # type: ignore[index]
    with pytest.raises(ValidationError, match="unknown assumption reference"):
        DecisionTrace.model_validate(assumption)


def test_duplicate_record_identifiers_are_rejected_across_sections():
    payload = _valid_trace_payload()
    payload["assumptions"][0]["assumption_id"] = "fact-demo-001"  # type: ignore[index]

    with pytest.raises(ValidationError, match="duplicate record identifier"):
        DecisionTrace.model_validate(payload)


def test_future_or_naive_evidence_times_are_rejected():
    future = _valid_trace_payload()
    future["evidence"][0]["available_at"] = "2026-11-24T13:01:00-03:00"  # type: ignore[index]
    with pytest.raises(ValidationError, match="available after the trace cutoff"):
        DecisionTrace.model_validate(future)

    naive = _valid_trace_payload()
    naive["observations"][0]["observed_at"] = "2026-11-24T12:00:00"  # type: ignore[index]
    with pytest.raises(ValidationError, match="timezone-aware"):
        DecisionTrace.model_validate(naive)

    future_observation = _valid_trace_payload()
    future_observation["observations"][0]["observed_at"] = "2026-11-24T13:01:00-03:00"  # type: ignore[index]
    with pytest.raises(ValidationError, match="observation occurs after the trace cutoff"):
        DecisionTrace.model_validate(future_observation)

    after_observation = _valid_trace_payload()
    after_observation["evidence"][0]["available_at"] = "2026-11-24T11:59:00-03:00"  # type: ignore[index]
    with pytest.raises(ValidationError, match="availability precedes its observation"):
        DecisionTrace.model_validate(after_observation)


def test_missing_evidence_must_point_to_a_record_it_limits():
    payload = _valid_trace_payload()
    payload["missing_evidence"][0]["blocks_refs"] = ["outcome-missing"]  # type: ignore[index]

    with pytest.raises(ValidationError, match="unknown blocked record reference"):
        DecisionTrace.model_validate(payload)


def test_unavailable_cost_cannot_be_encoded_as_zero():
    payload = _valid_trace_payload()
    payload["costs"][1]["amount"] = "0"  # type: ignore[index]

    with pytest.raises(ValidationError, match="unavailable cost must omit amount"):
        DecisionTrace.model_validate(payload)


def test_metered_cost_requires_a_meter_reference():
    payload = _valid_trace_payload()
    payload["costs"][2]["source_ref"] = None  # type: ignore[index]

    with pytest.raises(ValidationError, match="metered cost requires amount and source_ref"):
        DecisionTrace.model_validate(payload)


def test_approved_review_requires_identity_time_and_result_digest():
    payload = _valid_trace_payload()
    payload["human_review"] = {"status": "approved"}

    with pytest.raises(ValidationError, match="approved review requires"):
        DecisionTrace.model_validate(payload)


def test_review_digest_binds_approval_to_exact_result_content():
    draft = DecisionTrace.model_validate(_valid_trace_payload())
    approved_payload = _valid_trace_payload()
    approved_payload["human_review"] = {
        "status": "approved",
        "reviewer_ref": "reviewer-001",
        "decided_at": "2026-11-24T14:05:00-03:00",
        "reviewed_result_sha256": draft.result_sha256,
    }
    approved = DecisionTrace.model_validate(approved_payload)
    assert approved.human_review.status == "approved"
    assert approved.result_sha256 == draft.result_sha256

    changed = deepcopy(approved_payload)
    changed["forecasts"][0]["value"] = 9  # type: ignore[index]
    with pytest.raises(ValidationError, match="does not match result digest"):
        DecisionTrace.model_validate(changed)


def test_trace_models_are_immutable_after_validation():
    trace = DecisionTrace.model_validate(_valid_trace_payload())

    with pytest.raises(ValidationError):
        trace.revision = 2  # type: ignore[misc]
