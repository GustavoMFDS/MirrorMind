"""Compose the bounded fictional retail path into one reviewable result.

This local workflow joins existing evidence, evaluation, residual, policy and
decision-trace contracts. A trusted local caller may inject an opt-in WorldKernel
comparator; the HTTP route never does. The workflow does not authorize data,
claim forecast validity, rank policies or write business state.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from datetime import UTC, date, datetime, time, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator

from mirrormind.core.decision_trace import (
    ConditionalOutcomeV2,
    CostMeasurement,
    DecisionTraceV2,
    EvidenceReference,
    ExecutionEvidence,
    ForecastEstimate,
    MissingEvidence,
    ModelingAssumption,
    ObservedFact,
    OutcomeMetric,
)
from mirrormind.domains.retail.evaluation_flow import evaluate_retail_evidence_flow
from mirrormind.domains.retail.policy_simulation import (
    HORIZON_DAYS,
    MAX_REPLICATIONS,
    MAX_TOTAL_POLICY_TRANSITIONS,
    POLICY_IDS,
    RetailPolicyAssumptions,
    RetailPolicyComparisonRequest,
    compare_synthetic_retail_policies,
)
from mirrormind.domains.retail.residual_envelope import (
    evaluate_retail_residual_envelopes,
)
from mirrormind.domains.retail.synthetic_fixtures import (
    LAST_FIXTURE_DAY,
    START,
    SYNTHETIC_STOCK_CODE,
    build_synthetic_evidence_flow,
)
from mirrormind.domains.retail.worldkernel_policy_world import (
    POLICY_TEST_DOUBLE_CONTRACT_REF,
    POLICY_WORLD_ENGINE_CONTRACT_REF,
    POLICY_WORLD_NAME,
    POLICY_WORLD_VERSION,
)
from mirrormind.modules.forecasting.baselines import project_seasonal_naive_lag7

DEFAULT_AS_OF = START + timedelta(days=25)
DIAGNOSTIC_HOLDOUT_DAYS = 7
_MAX_REQUEST_REPLICATIONS = min(
    MAX_REPLICATIONS,
    MAX_TOTAL_POLICY_TRANSITIONS // (HORIZON_DAYS * len(POLICY_IDS) * 3),
)
_MAX_SEED = (1 << 32) - 1 - MAX_REPLICATIONS
MODEL_CARD_REF = (
    "docs/engineering/model_cards/SYNTHETIC_RETAIL_DECISION_WORKFLOW.md"
)
LOCAL_ENGINE_CONTRACT_REF = POLICY_TEST_DOUBLE_CONTRACT_REF
WORKFLOW_SCHEMA_VERSION = "mirrormind.synthetic_retail_decision_workflow.v2"
DECISION_IDENTITY_SCHEMA_VERSION = "mirrormind.synthetic_retail_decision_identity.v1"
_ARTIFACT_SCHEMA_VERSIONS = {
    "evaluation": "mirrormind.synthetic_retail_evaluation_artifact.v1",
    "uncertainty": "mirrormind.synthetic_retail_uncertainty_artifact.v1",
    "forecast_evidence_receipt": (
        "mirrormind.synthetic_retail_forecast_evidence_receipt.v1"
    ),
    "forecast": "mirrormind.synthetic_retail_forecast_profile.v1",
    "simulation": "mirrormind.synthetic_retail_policy_simulation_artifact.v2",
}
_UTC = UTC


class SyntheticDecisionWorkflowRequest(BaseModel):
    """Strict bounded options for the generated local decision example."""

    # ISO dates arrive as JSON strings; StrictInt fields still reject booleans
    # and coercion for resource bounds while Pydantic parses calendar dates.
    model_config = ConfigDict(extra="forbid", frozen=True)

    as_of: date = DEFAULT_AS_OF
    replications: StrictInt = Field(default=12, ge=1, le=_MAX_REQUEST_REPLICATIONS)
    seed: StrictInt = Field(default=317, ge=0, le=_MAX_SEED)

    @field_validator("as_of")
    @classmethod
    def validate_as_of(cls, value: date) -> date:
        if type(value) is not date:
            raise ValueError("as_of must be a calendar date")
        # The seven-day historical diagnostic must precede the forecast's
        # seven-day feature window, and the fixture ends on 2011-02-04.
        if not DEFAULT_AS_OF <= value <= LAST_FIXTURE_DAY:
            raise ValueError("as_of must be a fixture date in 2011-01-26..2011-02-04")
        return value


def _default_policy_assumptions() -> RetailPolicyAssumptions:
    """Return the same explicit fictional controls used by the M1E-03 demo."""
    return RetailPolicyAssumptions(
        initial_stock_units=65,
        lead_time_days=2,
        fixed_order_quantity_units=70,
        reorder_point_units=55,
        review_period_days=7,
        safety_stock_units=15,
        procurement_cost_per_unit=2,
        holding_cost_per_unit_day=1,
        fixed_order_cost=12,
        unmet_demand_penalty_per_unit=8,
    )


def _cutoff_timestamp(value: date) -> datetime:
    return datetime.combine(value, time(23, 59, 59, tzinfo=_UTC))


def _canonical_json_sha256(value: object) -> str:
    """Hash a JSON value using the workflow's sorted-key UTF-8 encoding."""
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _versioned_artifact_digests(
    result: dict[str, object],
) -> dict[str, dict[str, str]]:
    """Bind each returned evaluation artifact to its declared local schema."""
    return {
        artifact_id: {
            "schema_version": schema_version,
            "sha256": _canonical_json_sha256(
                {
                    "schema_version": schema_version,
                    "artifact": result[artifact_id],
                }
            ),
        }
        for artifact_id, schema_version in _ARTIFACT_SCHEMA_VERSIONS.items()
    }


def _decision_identity_sha256(
    request: SyntheticDecisionWorkflowRequest,
    artifact_digests: dict[str, dict[str, str]],
) -> str:
    """Create a deterministic identity for this exact request/result pair."""
    return _canonical_json_sha256(
        {
            "schema_version": DECISION_IDENTITY_SCHEMA_VERSION,
            "workflow_schema_version": WORKFLOW_SCHEMA_VERSION,
            "request": request.model_dump(mode="json"),
            "artifact_digests": artifact_digests,
        }
    )


def _flow_snapshot_digest(flow: Any) -> str:
    review_receipt = flow.review_packet.receipt()
    digest = review_receipt.get("snapshot_sha256")
    if type(digest) is not str or len(digest) != 64:
        raise ValueError("synthetic evidence receipt is missing its snapshot digest")
    return digest


def _eligible_observation_rows(flow: Any, *, as_of: date) -> tuple[tuple[date, int, date], ...]:
    if flow.release_audit.origin_on != as_of:
        raise ValueError("forecast evidence audit cutoff does not match the workflow cutoff")
    releases = {
        item.observed_on: item.available_on
        for item in flow.declared_releases
        if item.stock_code == SYNTHETIC_STOCK_CODE
    }
    projection = {
        item.observed_on: item.units
        for item in flow.workbook.projection.days
        if item.stock_code == SYNTHETIC_STOCK_CODE
    }
    rows = []
    for observed_on in sorted(set(releases) & set(projection)):
        available_on = releases[observed_on]
        if observed_on <= as_of and available_on <= as_of:
            rows.append((observed_on, projection[observed_on], available_on))
    selected = tuple(rows)
    if len(selected) != flow.release_audit.available_product_days:
        raise ValueError("row-level eligibility does not match the declared release audit")
    return selected


def _requested_history_window(as_of: date) -> tuple[date, ...]:
    return tuple(as_of - timedelta(days=offset) for offset in range(6, -1, -1))


def _execution_evidence_records(
    comparison: dict[str, object], *, produced_at: datetime
) -> tuple[tuple[ExecutionEvidence, ...], tuple[str, ...], str, str, dict[str, object]]:
    """Validate selected-engine metadata and create replayable trace records."""
    selected_source = comparison.get("selected_result_source")
    engine_contract_ref = comparison.get("engine_contract_ref")
    engine_execution = comparison.get("engine_execution")
    parity = comparison.get("reference_parity")
    if type(parity) is not dict:
        raise ValueError("policy comparison is missing reference-parity metadata")

    selected_digest = _canonical_json_sha256(comparison["lead_time_sensitivity"])
    records: list[ExecutionEvidence] = []
    if selected_source == "policy_test_double":
        if (
            engine_execution != "worldkernel_not_invoked"
            or engine_contract_ref != LOCAL_ENGINE_CONTRACT_REF
            or parity.get("reference_simulator_invoked") is not False
            or parity.get("status") != "not_run"
            or parity.get("result_sha256") is not None
        ):
            raise ValueError("test-double result has inconsistent engine provenance")
        records.append(
            ExecutionEvidence(
                execution_id="execution-selected-policy-result",
                engine_contract_ref=LOCAL_ENGINE_CONTRACT_REF,
                role="selected_output",
                result_sha256=selected_digest,
                provenance_ref=(
                    "python:function="
                    "mirrormind.domains.retail.policy_simulation."
                    "compare_synthetic_retail_policies"
                ),
                produced_at=produced_at,
            )
        )
        return (
            tuple(records),
            (records[0].execution_id,),
            selected_source,
            LOCAL_ENGINE_CONTRACT_REF,
            parity,
        )

    if selected_source != "worldkernel_policy_world":
        raise ValueError("policy comparison selected an unsupported result source")
    if (
        engine_execution != "worldkernel_invoked"
        or engine_contract_ref != POLICY_WORLD_ENGINE_CONTRACT_REF
        or parity.get("reference_simulator_invoked") is not True
        or parity.get("reference_engine_contract_ref") != LOCAL_ENGINE_CONTRACT_REF
        or parity.get("status") != "exact_match"
        or parity.get("result_sha256") != selected_digest
    ):
        raise ValueError("WorldKernel result has inconsistent parity metadata")

    engine = comparison.get("worldkernel_execution")
    if type(engine) is not dict:
        raise ValueError("WorldKernel result is missing its execution receipt")
    required_engine_fields = {
        "package_version",
        "source_commit",
        "result_schema",
        "world",
        "registered_world_version",
        "result_sha256",
        "selected_result_sha256",
    }
    if set(engine) != required_engine_fields or any(
        type(engine[key]) is not str or not engine[key]
        for key in required_engine_fields
    ):
        raise ValueError("WorldKernel execution receipt fields are invalid")
    if (
        engine["world"] != POLICY_WORLD_NAME
        or engine["registered_world_version"] != POLICY_WORLD_VERSION
        or engine["result_schema"] != "worldkernel.result.v1"
        or engine["selected_result_sha256"] != selected_digest
        or len(engine["source_commit"]) != 40
        or any(char not in "0123456789abcdef" for char in engine["source_commit"])
        or len(engine["result_sha256"]) != 64
        or any(char not in "0123456789abcdef" for char in engine["result_sha256"])
    ):
        raise ValueError("WorldKernel execution receipt does not match its policy contract")

    provenance_ref = (
        f"wk:pkg={engine['package_version']}"
        f";commit={engine['source_commit']}"
        f";world={engine['world']}"
        f";rev={engine['registered_world_version']}"
        f";schema={engine['result_schema']}"
        f";raw={engine['result_sha256']}"
    )
    if len(provenance_ref) > 256:
        raise ValueError("WorldKernel provenance reference exceeds the trace limit")
    selected = ExecutionEvidence(
        execution_id="execution-selected-policy-result",
        engine_contract_ref=POLICY_WORLD_ENGINE_CONTRACT_REF,
        role="selected_output",
        result_sha256=selected_digest,
        provenance_ref=provenance_ref,
        produced_at=produced_at,
    )
    oracle = ExecutionEvidence(
        execution_id="execution-policy-test-double-parity",
        engine_contract_ref=LOCAL_ENGINE_CONTRACT_REF,
        role="parity_oracle",
        result_sha256=parity["result_sha256"],
        provenance_ref=(
            "python:parity_oracle="
            "mirrormind.domains.retail.policy_simulation."
            "compare_synthetic_retail_policies"
        ),
        produced_at=produced_at,
    )
    return (
        (selected, oracle),
        (selected.execution_id, oracle.execution_id),
        selected_source,
        POLICY_WORLD_ENGINE_CONTRACT_REF,
        parity,
    )


def _policy_outcomes(
    comparison: dict[str, object], *,
    engine_contract_ref: str,
    execution_evidence_refs: tuple[str, ...],
    forecast_refs: tuple[str, ...],
    assumption_refs: tuple[str, ...],
    policy_caveat_refs: tuple[str, ...],
) -> tuple[ConditionalOutcomeV2, ...]:
    outcomes: list[ConditionalOutcomeV2] = []
    seed = comparison["seed"]
    runs = comparison["replications"]
    if type(seed) is not int or type(runs) is not int:
        raise TypeError("policy comparison returned invalid execution counts")
    scenarios = comparison["lead_time_sensitivity"]
    if not isinstance(scenarios, list):
        raise TypeError("policy comparison returned an invalid sensitivity result")
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            raise TypeError("policy comparison returned an invalid scenario")
        lead_time_days = scenario["lead_time_days"]
        policies = scenario["policies"]
        if not isinstance(policies, list):
            raise TypeError("policy comparison returned invalid policy outcomes")
        for policy in policies:
            if not isinstance(policy, dict):
                raise TypeError("policy comparison returned an invalid policy")
            policy_id = policy["policy_id"]
            means = policy["mean_metrics_per_replication"]
            if not isinstance(means, dict):
                raise TypeError("policy comparison returned invalid mean metrics")
            policy_assumption_refs = assumption_refs
            if policy_id == "forecast_aware_order_up_to":
                policy_assumption_refs += policy_caveat_refs
            fill_rate = means["fill_rate_basis_points"]
            if fill_rate is None:
                raise ValueError("positive forecast profile must produce a fill-rate denominator")
            metrics = (
                OutcomeMetric(
                    name="mean_total_cost",
                    value=means["total_cost_units"],
                    unit="synthetic_cost_unit",
                ),
                OutcomeMetric(
                    name="mean_fill_rate_basis_points",
                    value=fill_rate,
                    unit="basis_points",
                ),
                OutcomeMetric(
                    name="mean_stockout_days_per_replication",
                    value=means["stockout_days_per_replication"],
                    unit="days_per_replication",
                ),
                OutcomeMetric(
                    name="mean_ending_on_hand_units",
                    value=means["ending_on_hand_units"],
                    unit="items_per_replication",
                ),
                OutcomeMetric(
                    name="mean_order_count",
                    value=means["order_count"],
                    unit="orders_per_replication",
                ),
            )
            outcomes.append(
                ConditionalOutcomeV2(
                    outcome_id=(
                        f"outcome-{policy_id}-lead-{lead_time_days}"
                    ),
                    alternative_ref=(
                        f"retail_policy:{policy_id}:lead_time_{lead_time_days}"
                    ),
                    engine_contract_ref=engine_contract_ref,
                    execution_evidence_refs=execution_evidence_refs,
                    forecast_refs=forecast_refs,
                    assumption_refs=policy_assumption_refs,
                    metrics=metrics,
                    seed=seed,
                    runs=runs,
                )
            )
    return tuple(outcomes)


def _build_trace(
    *,
    as_of: date,
    identity_sha256: str,
    snapshot_sha256: str,
    observations: tuple[tuple[date, int, date], ...],
    history: tuple[tuple[date, int, date], ...],
    forecast_profile: tuple[int, ...],
    comparison: dict[str, object],
    engine_contract_ref: str,
    execution_evidence: tuple[ExecutionEvidence, ...],
    execution_evidence_refs: tuple[str, ...],
) -> DecisionTraceV2:
    cutoff_at = _cutoff_timestamp(as_of)
    created_at = cutoff_at + timedelta(microseconds=1)
    evidence: list[EvidenceReference] = []
    facts: list[ObservedFact] = []
    fact_id_by_date: dict[date, str] = {}
    for observed_on, units, available_on in observations:
        suffix = observed_on.isoformat()
        evidence_id = f"evidence-{suffix}"
        fact_id = f"fact-{suffix}"
        available_at = _cutoff_timestamp(available_on)
        evidence.append(
            EvidenceReference(
                evidence_id=evidence_id,
                source_ref="synthetic_fixture_generator",
                snapshot_ref=f"sha256:{snapshot_sha256}",
                provenance_ref="synthetic_fixture_generator_v1",
                available_at=available_at,
            )
        )
        facts.append(
            ObservedFact(
                fact_id=fact_id,
                value=units,
                unit="positive_invoice_line_units",
                observed_at=datetime.combine(
                    observed_on, time(12, 0, tzinfo=_UTC)
                ),
                evidence_refs=(evidence_id,),
            )
        )
        fact_id_by_date[observed_on] = fact_id

    history_fact_refs = tuple(fact_id_by_date[day] for day, _, _ in history)
    forecasts = tuple(
        ForecastEstimate(
            forecast_id=f"forecast-{(as_of + timedelta(days=step)).isoformat()}",
            target_ref=(
                f"{SYNTHETIC_STOCK_CODE}/{(as_of + timedelta(days=step)).isoformat()}"
            ),
            value=value,
            unit="positive_invoice_line_units",
            model_card_ref=MODEL_CARD_REF,
            fact_refs=history_fact_refs,
        )
        for step, value in enumerate(forecast_profile, start=1)
    )
    forecast_refs = tuple(item.forecast_id for item in forecasts)

    base_assumptions = (
        ModelingAssumption(
            assumption_id="assumption-demand-semantics",
            statement=(
                "Positive invoice-line units are only a fictional proxy and do not "
                "measure complete latent demand."
            ),
        ),
        ModelingAssumption(
            assumption_id="assumption-forecast-method",
            statement=(
                "seasonal_naive_lag7 repeats the last seven eligible fictional "
                "product-day values for exactly 28 steps."
            ),
        ),
        ModelingAssumption(
            assumption_id="assumption-initial-stock",
            statement="Initial on-hand stock is caller-independent fixture assumption: 65 items.",
        ),
        ModelingAssumption(
            assumption_id="assumption-base-lead-time",
            statement="Base supplier lead time is an assumed two days; sensitivity uses adjacent days.",
        ),
        ModelingAssumption(
            assumption_id="assumption-fixed-order-quantity",
            statement="Fixed order quantity is assumed to be 70 items.",
        ),
        ModelingAssumption(
            assumption_id="assumption-reorder-point",
            statement="Reorder point is assumed to be 55 items.",
        ),
        ModelingAssumption(
            assumption_id="assumption-review-period",
            statement="Fixed-cycle review interval is assumed to be seven days.",
        ),
        ModelingAssumption(
            assumption_id="assumption-safety-stock",
            statement="Profile-aware policy safety stock is assumed to be 15 items.",
        ),
        ModelingAssumption(
            assumption_id="assumption-synthetic-costs",
            statement=(
                "Procurement=2, holding=1 per item-day, fixed order=12, and unmet "
                "demand penalty=8 synthetic cost units."
            ),
        ),
        ModelingAssumption(
            assumption_id="assumption-random-streams",
            statement=(
                f"Paired synthetic demand uses seed {comparison['seed']} and "
                f"{comparison['replications']} replications; each day is scaled "
                "by one of the fixed 75%, 100%, or 125% multipliers."
            ),
        ),
    )
    modeling_caveats = comparison.get("modeling_caveats")
    if (
        not isinstance(modeling_caveats, list)
        or not modeling_caveats
        or len(modeling_caveats) > 8
        or any(type(item) is not str for item in modeling_caveats)
    ):
        raise TypeError("policy comparison returned invalid modeling caveats")
    policy_caveat_assumptions = tuple(
        ModelingAssumption(
            assumption_id=f"assumption-policy-caveat-{index:03d}",
            statement=statement,
        )
        for index, statement in enumerate(modeling_caveats, start=1)
    )
    assumptions = base_assumptions + policy_caveat_assumptions
    policy_caveat_refs = tuple(
        item.assumption_id for item in policy_caveat_assumptions
    )
    outcomes = _policy_outcomes(
        comparison,
        engine_contract_ref=engine_contract_ref,
        execution_evidence_refs=execution_evidence_refs,
        forecast_refs=forecast_refs,
        assumption_refs=tuple(item.assumption_id for item in base_assumptions),
        policy_caveat_refs=policy_caveat_refs,
    )
    outcome_refs = tuple(item.outcome_id for item in outcomes)

    gaps: tuple[MissingEvidence, ...] = (
        MissingEvidence(
            gap_id="gap-source-rights-and-vintages",
            description=(
                "The fixture's source, license, publication dates, completeness "
                "and rights are generated declarations, not independently verified evidence."
            ),
            blocks_refs=forecast_refs + outcome_refs,
        ),
        MissingEvidence(
            gap_id="gap-empirical-model-validation",
            description=(
                "No approved real-data holdout establishes forecast skill; the "
                "fixed method is not selected from the returned synthetic scores."
            ),
            blocks_refs=forecast_refs,
        ),
        MissingEvidence(
            gap_id="gap-uncertainty-calibration",
            description=(
                "The retrospective residual envelope is heuristic and is not a "
                "calibrated interval or a guarantee attached to these forecasts."
            ),
            blocks_refs=forecast_refs + outcome_refs,
        ),
    )
    if comparison.get("engine_execution") != "worldkernel_invoked":
        gaps += (
            MissingEvidence(
            gap_id="gap-worldkernel-execution",
            description=(
                "WorldKernel was not invoked; the policy outcomes come from the "
                "local experimental Python test double."
            ),
            blocks_refs=outcome_refs,
            ),
        )
    return DecisionTraceV2(
        trace_id=f"trace-retail-synthetic-{identity_sha256}",
        decision_ref=f"decision-retail-synthetic-{identity_sha256}",
        revision=1,
        question=(
            "How do three fictional replenishment policies compare under one "
            "predeclared seasonal-naive demand profile?"
        ),
        cutoff_at=cutoff_at,
        # This fixture timestamp is deterministic logical metadata, not a
        # wall-clock audit timestamp or proof of when a user ran the workflow.
        created_at=created_at,
        evidence=tuple(evidence),
        observations=tuple(facts),
        forecasts=forecasts,
        assumptions=assumptions,
        outcomes=outcomes,
        execution_evidence=execution_evidence,
        missing_evidence=gaps,
        costs=(
            CostMeasurement(
                cost_id="cost-local-runtime",
                category="local_runtime_measurement",
                unit="runtime_seconds",
                status="unavailable",
            ),
            CostMeasurement(
                cost_id="cost-worldkernel-execution",
                category="worldkernel_execution",
                unit="USD",
                status="unavailable",
            ),
        ),
    )


def run_synthetic_decision_workflow(
    request: SyntheticDecisionWorkflowRequest,
    *,
    future_units: int = 9,
    all_unpublished: bool = False,
    policy_comparator: Callable[
        [RetailPolicyComparisonRequest], dict[str, object]
    ]
    | None = None,
) -> dict[str, object]:
    """Run one deterministic, non-persisting synthetic decision comparison.

    ``future_units`` and ``all_unpublished`` are fixture-only test seams. The
    optional ``policy_comparator`` is a trusted local composition seam for an
    explicitly selected CLI gateway; it is absent from the HTTP request model.
    """
    if type(request) is not SyntheticDecisionWorkflowRequest:
        raise TypeError("request must be a validated SyntheticDecisionWorkflowRequest")
    evaluation_on = request.as_of - timedelta(days=DIAGNOSTIC_HOLDOUT_DAYS)
    diagnostic_flow = build_synthetic_evidence_flow(
        future_units=future_units,
        all_unpublished=all_unpublished,
        evaluation_on=evaluation_on,
    )
    evaluation = evaluate_retail_evidence_flow(
        diagnostic_flow,
        stock_code=SYNTHETIC_STOCK_CODE,
        evaluation_on=evaluation_on,
        holdout_days=DIAGNOSTIC_HOLDOUT_DAYS,
    )
    residual_diagnostic = evaluate_retail_residual_envelopes(
        diagnostic_flow.workbook.projection,
        diagnostic_flow.declared_releases,
        stock_code=SYNTHETIC_STOCK_CODE,
        evaluation_on=evaluation_on,
        holdout_days=DIAGNOSTIC_HOLDOUT_DAYS,
        calibration_days=21,
        min_calibration_residuals=5,
    )

    forecast_flow = build_synthetic_evidence_flow(
        future_units=future_units,
        all_unpublished=all_unpublished,
        evaluation_on=request.as_of,
    )
    observations = _eligible_observation_rows(forecast_flow, as_of=request.as_of)
    by_date = {day: (units, available_on) for day, units, available_on in observations}
    projected_by_date = {
        item.observed_on
        for item in forecast_flow.workbook.projection.days
        if item.stock_code == SYNTHETIC_STOCK_CODE
    }
    release_by_date = {
        item.observed_on: item.available_on
        for item in forecast_flow.declared_releases
        if item.stock_code == SYNTHETIC_STOCK_CODE
    }
    history_window = _requested_history_window(request.as_of)
    missing_history_days = tuple(
        day for day in history_window
        if day not in projected_by_date or day not in release_by_date
    )
    unpublished_history_days = tuple(
        day for day in history_window
        if day in projected_by_date
        and day in release_by_date
        and release_by_date[day] > request.as_of
    )

    result: dict[str, object] = {
        "schema_version": WORKFLOW_SCHEMA_VERSION,
        "as_of": request.as_of.isoformat(),
        "evaluation": {
            "role": "historical_diagnostic_before_forecast_feature_window",
            "evaluation_cutoff": evaluation_on.isoformat(),
            "model_selection_from_holdout": False,
            "result": evaluation,
        },
        "uncertainty": {
            "status": residual_diagnostic["uncertainty_status"],
            "calibration_holdout_targets_disjoint": (
                residual_diagnostic["calibration_holdout_targets_disjoint"]
            ),
            "nominal_coverage": None,
            "calibrated_prediction_interval": None,
            "attached_to_forecast": False,
            "diagnostic": residual_diagnostic,
        },
        "source_status": "fictional_fixture_not_authenticated_or_authorized",
        "forecast_evidence_receipt": forecast_flow.receipt(),
        "ingestion_authorized": False,
        "source_forecast_eligible": False,
        "decision_status": "comparison_only_no_policy_selection_or_authorization",
        "worldkernel_execution": "worldkernel_not_invoked",
        "human_review": "not_requested",
        "action_authorized": False,
        "writes_performed": False,
    }

    if missing_history_days or unpublished_history_days:
        result.update(
            {
                "status": "abstained_required_history_unavailable",
                "abstention": {
                    "reason": "seven_consecutive_published_days_are_required",
                    "required_history_start": history_window[0].isoformat(),
                    "required_history_end": history_window[-1].isoformat(),
                    "missing_or_unprojected_days": [
                        item.isoformat() for item in missing_history_days
                    ],
                    "unpublished_days": [
                        item.isoformat() for item in unpublished_history_days
                    ],
                    "eligible_history_count": len(history_window)
                    - len(missing_history_days)
                    - len(unpublished_history_days),
                },
                "forecast": {
                    "status": "not_run_due_to_incomplete_history",
                    "model": "seasonal_naive_lag7",
                    "horizon_days": HORIZON_DAYS,
                },
                "simulation": {
                    "status": "not_run_due_to_forecast_abstention",
                    "policy_test_double_invoked": False,
                    "policy_test_double_result_selected": False,
                    "selected_result_source": None,
                    "reference_parity": {
                        "reference_simulator_invoked": False,
                        "status": "not_run",
                        "result_sha256": None,
                    },
                },
                "trace": None,
                "trace_sha256": None,
            }
        )
        result["artifact_digests"] = _versioned_artifact_digests(result)
        result["decision_identity_sha256"] = None
        result["workflow_result_sha256"] = _canonical_json_sha256(result)
        return result

    history = tuple(
        (day, by_date[day][0], by_date[day][1]) for day in history_window
    )
    last_seven = tuple(units for _, units, _ in history)
    profile = project_seasonal_naive_lag7(
        last_seven, horizon_days=HORIZON_DAYS
    )
    assumptions = _default_policy_assumptions()
    comparison_request = RetailPolicyComparisonRequest(
        demand_profile_units=profile,
        assumptions=assumptions,
        replications=request.replications,
        seed=request.seed,
    )
    comparison = (
        {
            **compare_synthetic_retail_policies(comparison_request),
            "selected_result_source": "policy_test_double",
            "engine_contract_ref": LOCAL_ENGINE_CONTRACT_REF,
            "reference_parity": {
                "reference_simulator_invoked": False,
                "status": "not_run",
                "result_sha256": None,
            },
        }
        if policy_comparator is None
        else policy_comparator(comparison_request)
    )
    if type(comparison) is not dict:
        raise TypeError("policy comparator must return a comparison object")
    engine_execution = comparison.get("engine_execution", "worldkernel_not_invoked")
    if engine_execution not in {"worldkernel_not_invoked", "worldkernel_invoked"}:
        raise ValueError("policy comparator returned an unsupported engine status")
    execution_evidence, execution_evidence_refs, selected_source, engine_contract_ref, parity = (
        _execution_evidence_records(
            comparison,
            produced_at=_cutoff_timestamp(request.as_of)
            + timedelta(microseconds=1),
        )
    )
    result.update(
        {
            "worldkernel_execution": engine_execution,
            "forecast": {
                "status": "experimental_synthetic_profile_not_empirically_validated",
                "model": "seasonal_naive_lag7",
                "model_card_ref": MODEL_CARD_REF,
                "horizon_days": HORIZON_DAYS,
                "history_start": history_window[0].isoformat(),
                "history_end": history_window[-1].isoformat(),
                "history_fact_refs": [
                    f"fact-{day.isoformat()}" for day in history_window
                ],
                "profile_units": list(profile),
            },
            "simulation": {
                "status": comparison["simulation_status"],
                "policy_test_double_invoked": (
                    selected_source == "policy_test_double"
                    or parity["reference_simulator_invoked"] is True
                ),
                "policy_test_double_result_selected": (
                    selected_source == "policy_test_double"
                ),
                "selected_result_source": selected_source,
                "reference_parity": parity,
                "result": comparison,
            },
        }
    )
    artifact_digests = _versioned_artifact_digests(result)
    identity_sha256 = _decision_identity_sha256(request, artifact_digests)
    trace = _build_trace(
        as_of=request.as_of,
        identity_sha256=identity_sha256,
        snapshot_sha256=_flow_snapshot_digest(forecast_flow),
        observations=observations,
        history=history,
        forecast_profile=profile,
        comparison=comparison,
        engine_contract_ref=engine_contract_ref,
        execution_evidence=execution_evidence,
        execution_evidence_refs=execution_evidence_refs,
    )
    result.update(
        {
            "status": "synthetic_comparison_ready_experimental",
            "artifact_digests": artifact_digests,
            "decision_identity_sha256": identity_sha256,
            "trace": trace.model_dump(mode="json"),
            "trace_sha256": trace.result_sha256,
        }
    )
    result["workflow_result_sha256"] = _canonical_json_sha256(result)
    return result
