"""Evidence-backed regressions for the composed synthetic retail workflow."""
from __future__ import annotations

import copy
import hashlib
import json
from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from mirrormind.core.decision_trace import DecisionTrace
from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)
from mirrormind.domains.retail.uci_transactions import ProductDayUnits

AS_OF = date(2011, 1, 26)


def test_successful_workflow_produces_valid_trace_and_explicit_gaps():
    request = SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=2, seed=17)
    result = run_synthetic_decision_workflow(request)

    assert result["schema_version"] == "mirrormind.synthetic_retail_decision_workflow.v1"
    assert result["status"] == "synthetic_comparison_ready_experimental"
    assert result["source_status"] == "fictional_fixture_not_authenticated_or_authorized"
    assert result["decision_status"] == "comparison_only_no_policy_selection_or_authorization"
    assert result["worldkernel_execution"] == "worldkernel_not_invoked"
    assert result["human_review"] == "not_requested"
    assert result["action_authorized"] is False
    assert result["writes_performed"] is False

    evaluation = result["evaluation"]
    assert evaluation["evaluation_cutoff"] == "2011-01-19"
    assert evaluation["model_selection_from_holdout"] is False
    assert evaluation["result"]["baseline_evaluation"]["scored_origins"] >= 2
    uncertainty = result["uncertainty"]
    assert uncertainty["status"] == "heuristic_envelope_not_prediction_interval"
    assert uncertainty["calibration_holdout_targets_disjoint"] is True
    assert uncertainty["nominal_coverage"] is None
    assert uncertainty["calibrated_prediction_interval"] is None
    assert uncertainty["attached_to_forecast"] is False

    forecast = result["forecast"]
    assert forecast["model"] == "seasonal_naive_lag7"
    assert forecast["status"] == "experimental_synthetic_profile_not_empirically_validated"
    assert forecast["history_start"] == "2011-01-20"
    assert forecast["history_end"] == "2011-01-26"
    assert len(forecast["profile_units"]) == 28
    assert len(forecast["history_fact_refs"]) == 7
    assert forecast["profile_units"] == forecast["profile_units"][:7] * 4

    trace = DecisionTrace.model_validate(result["trace"])
    assert trace.result_sha256 == result["trace_sha256"]
    assert trace.cutoff_at.date() == AS_OF
    assert len(trace.observations) == 26
    assert len(trace.forecasts) == 28
    assert len(trace.outcomes) == 9
    assert trace.human_review.status == "not_requested"
    assert all(item.evidence_refs for item in trace.observations)
    assert all(item.available_at <= trace.cutoff_at for item in trace.evidence)
    facts = {item.fact_id for item in trace.observations}
    forecasts = {item.forecast_id for item in trace.forecasts}
    assumptions = {item.assumption_id for item in trace.assumptions}
    outcomes = {item.outcome_id for item in trace.outcomes}
    assert all(len(item.fact_refs) == 7 and set(item.fact_refs) <= facts
               for item in trace.forecasts)
    policy_caveats = {
        item.assumption_id
        for item in trace.assumptions
        if item.assumption_id.startswith("assumption-policy-caveat-")
    }
    base_assumptions = assumptions - policy_caveats
    assert all(set(item.forecast_refs) == forecasts for item in trace.outcomes)
    assert all(base_assumptions <= set(item.assumption_refs) for item in trace.outcomes)
    assert all(
        (set(item.assumption_refs) - base_assumptions) == policy_caveats
        if item.alternative_ref.startswith(
            "retail_policy:forecast_aware_order_up_to:"
        )
        else not (set(item.assumption_refs) & policy_caveats)
        for item in trace.outcomes
    )
    assert all(set(item.blocks_refs) <= forecasts | outcomes
               for item in trace.missing_evidence)

    simulation = result["simulation"]
    assert simulation["status"] == "experimental_local_test_double_only"
    assert simulation["policy_test_double_invoked"] is True
    assert len(simulation["result"]["lead_time_sensitivity"]) == 3
    assert all(
        policy["ranking"] is None and policy["ranking_status"] == "not_computed"
        for scenario in simulation["result"]["lead_time_sensitivity"]
        for policy in scenario["policies"]
    )


def test_post_cutoff_fixture_mutation_does_not_change_forecast_or_comparison():
    request = SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=1, seed=17)
    baseline = run_synthetic_decision_workflow(request, future_units=9)
    mutated = run_synthetic_decision_workflow(request, future_units=999)

    assert baseline["forecast"]["profile_units"] == mutated["forecast"]["profile_units"]
    assert baseline["simulation"]["result"] == mutated["simulation"]["result"]
    assert baseline["evaluation"]["result"]["baseline_evaluation"]["metrics"] == (
        mutated["evaluation"]["result"]["baseline_evaluation"]["metrics"]
    )
    assert baseline["trace"]["forecasts"] == mutated["trace"]["forecasts"]
    assert baseline["trace_sha256"] != mutated["trace_sha256"]


def test_trace_identity_includes_replications_and_exact_replay_is_stable():
    request = SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=1, seed=17)
    first = run_synthetic_decision_workflow(request)
    replay = run_synthetic_decision_workflow(request)
    changed_replications = run_synthetic_decision_workflow(
        SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=2, seed=17)
    )

    first_trace = DecisionTrace.model_validate(first["trace"])
    replay_trace = DecisionTrace.model_validate(replay["trace"])
    changed_trace = DecisionTrace.model_validate(changed_replications["trace"])

    assert first_trace.trace_id == replay_trace.trace_id
    assert first_trace.decision_ref == replay_trace.decision_ref
    assert first_trace.revision == replay_trace.revision == 1
    assert first["trace_sha256"] == replay["trace_sha256"]
    assert first_trace.trace_id != changed_trace.trace_id
    assert first_trace.decision_ref != changed_trace.decision_ref
    assert first["trace_sha256"] != changed_replications["trace_sha256"]


def test_versioned_artifact_and_workflow_digests_bind_the_complete_response():
    result = run_synthetic_decision_workflow(
        SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=1, seed=17)
    )

    def canonical_digest(value: object) -> str:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    artifact_values = {
        "evaluation": result["evaluation"],
        "uncertainty": result["uncertainty"],
        "forecast_evidence_receipt": result["forecast_evidence_receipt"],
        "forecast": result["forecast"],
        "simulation": result["simulation"],
    }
    assert set(result["artifact_digests"]) == set(artifact_values)
    for artifact_id, payload in artifact_values.items():
        binding = result["artifact_digests"][artifact_id]
        assert binding["schema_version"].startswith("mirrormind.")
        assert binding["sha256"] == canonical_digest(
            {"schema_version": binding["schema_version"], "artifact": payload}
        )

    envelope = {
        key: value
        for key, value in result.items()
        if key != "workflow_result_sha256"
    }
    assert result["workflow_result_sha256"] == canonical_digest(envelope)
    assert result["workflow_result_sha256"] != result["trace_sha256"]

    tampered = copy.deepcopy(envelope)
    tampered["simulation"]["result"]["modeling_caveats"][0] = "tampered"
    assert canonical_digest(tampered) != result["workflow_result_sha256"]


def test_profile_aware_policy_modeling_caveats_are_bound_into_trace():
    result = run_synthetic_decision_workflow(
        SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=1, seed=17)
    )
    trace = DecisionTrace.model_validate(result["trace"])
    caveats = result["simulation"]["result"]["modeling_caveats"]
    caveat_assumptions = {
        assumption.assumption_id: assumption.statement
        for assumption in trace.assumptions
        if assumption.assumption_id.startswith("assumption-policy-caveat-")
    }
    assert set(caveat_assumptions.values()) == set(caveats)

    profile_aware = [
        outcome
        for outcome in trace.outcomes
        if outcome.alternative_ref.startswith(
            "retail_policy:forecast_aware_order_up_to:"
        )
    ]
    other_policies = [
        outcome
        for outcome in trace.outcomes
        if not outcome.alternative_ref.startswith(
            "retail_policy:forecast_aware_order_up_to:"
        )
    ]
    assert len(profile_aware) == 3
    assert len(other_policies) == 6
    caveat_refs = set(caveat_assumptions)
    assert all(caveat_refs <= set(outcome.assumption_refs) for outcome in profile_aware)
    assert all(not caveat_refs.intersection(outcome.assumption_refs) for outcome in other_policies)


@pytest.mark.parametrize("case", ["missing", "late", "unpublished"])
def test_incomplete_or_late_history_abstains_without_running_policy_test_double(
    case: str, monkeypatch: pytest.MonkeyPatch
):
    import mirrormind.domains.retail.synthetic_decision_workflow as workflow

    dates = tuple(AS_OF - timedelta(days=offset) for offset in range(6, -1, -1))
    projection_days = []
    releases = []
    for index, observed_on in enumerate(dates, start=1):
        if case == "missing" and index == 4:
            continue
        available_on = observed_on
        if case == "late" and index == 6:
            available_on = AS_OF + timedelta(days=1)
        if case == "unpublished":
            available_on = AS_OF + timedelta(days=1)
        projection_days.append(
            ProductDayUnits("SYNTHETIC-SKU", observed_on, index)
        )
        releases.append(
            DeclaredProductRelease("SYNTHETIC-SKU", observed_on, available_on)
        )
    fake_flow = SimpleNamespace(
        workbook=SimpleNamespace(
            projection=SimpleNamespace(days=tuple(projection_days))
        ),
        declared_releases=tuple(releases),
        release_audit=SimpleNamespace(
            origin_on=AS_OF,
            available_product_days=sum(
                item.observed_on <= AS_OF and item.available_on <= AS_OF
                for item in releases
            ),
        ),
        receipt=lambda: {"status": "synthetic-test-flow"},
    )
    monkeypatch.setattr(workflow, "build_synthetic_evidence_flow", lambda **_: fake_flow)
    monkeypatch.setattr(
        workflow,
        "evaluate_retail_evidence_flow",
        lambda *_, **__: {"status": "fixture_diagnostic"},
    )
    monkeypatch.setattr(
        workflow,
        "evaluate_retail_residual_envelopes",
        lambda *_, **__: {
            "uncertainty_status": "heuristic_envelope_not_prediction_interval",
            "calibration_holdout_targets_disjoint": True,
        },
    )
    monkeypatch.setattr(
        workflow,
        "compare_synthetic_retail_policies",
        lambda *_: pytest.fail("policy test double must not run after abstention"),
    )

    result = run_synthetic_decision_workflow(
        SyntheticDecisionWorkflowRequest(as_of=AS_OF, replications=1)
    )

    assert result["status"] == "abstained_required_history_unavailable"
    assert result["forecast"]["status"] == "not_run_due_to_incomplete_history"
    assert result["simulation"] == {
        "status": "not_run_due_to_forecast_abstention",
        "policy_test_double_invoked": False,
    }
    assert result["trace"] is None
    assert result["trace_sha256"] is None
    assert result["decision_identity_sha256"] is None
    assert len(result["workflow_result_sha256"]) == 64
    assert set(result["artifact_digests"]) == {
        "evaluation",
        "uncertainty",
        "forecast_evidence_receipt",
        "forecast",
        "simulation",
    }
    if case == "missing":
        assert result["abstention"]["missing_or_unprojected_days"] == ["2011-01-23"]
    elif case == "late":
        assert result["abstention"]["unpublished_days"] == ["2011-01-25"]
    else:
        assert result["abstention"]["unpublished_days"] == [
            day.isoformat() for day in dates
        ]


@pytest.mark.parametrize(
    "payload",
    [
        {"as_of": date(2011, 1, 25)},
        {"as_of": date(2011, 2, 5)},
        {"as_of": AS_OF, "replications": True},
        {"as_of": AS_OF, "seed": True},
        {"as_of": AS_OF, "unexpected": "field"},
    ],
)
def test_workflow_request_rejects_out_of_range_and_untyped_options(payload):
    with pytest.raises(ValueError):
        SyntheticDecisionWorkflowRequest.model_validate(payload)
