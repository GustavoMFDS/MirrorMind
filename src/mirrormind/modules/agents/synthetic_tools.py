"""Thin adapters from fixed agent tools to existing synthetic M1/M2 services."""
from __future__ import annotations

import json
from datetime import date
from hashlib import sha256
from typing import Annotated, Literal, TypedDict, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    StringConstraints,
    field_validator,
    model_validator,
)

from mirrormind.core.decision_trace import DecisionTraceV2
from mirrormind.domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)
from mirrormind.modules.retrieval.contracts import EvidenceCitation, EvidenceQuery
from mirrormind.modules.retrieval.fictional_fixture import build_fictional_index

from .registry import ToolDefinition, ToolRegistry

_POLICY_IDS = (
    "fixed_cycle_quantity",
    "reorder_point_fixed_quantity",
    "forecast_aware_order_up_to",
)


class _WorkflowMeanMetrics(TypedDict):
    total_cost_units: float
    stockout_days_per_replication: float
    ending_on_hand_units: float
    pending_order_units: float
    order_count: float
    fill_rate_basis_points: int | None


class _WorkflowReplication(TypedDict):
    demand_stream_sha256: str


class _WorkflowPolicy(TypedDict):
    policy_id: Literal[
        "fixed_cycle_quantity",
        "reorder_point_fixed_quantity",
        "forecast_aware_order_up_to",
    ]
    ranking_status: Literal["not_computed"]
    mean_metrics_per_replication: _WorkflowMeanMetrics
    replication_results: list[_WorkflowReplication]


class _WorkflowScenario(TypedDict):
    lead_time_days: int
    is_base_assumption: bool
    policies: list[_WorkflowPolicy]


class _WorkflowComparison(TypedDict):
    engine_contract_ref: Literal["mirrormind.local.retail_policy_test_double.v1"]
    engine_execution: Literal["worldkernel_not_invoked"]
    decision_status: Literal[
        "comparison_only_no_policy_selection_or_authorization"
    ]
    input_status: Literal["caller_supplied_assumptions_not_authenticated"]
    quantity_unit: Literal["item"]
    time_unit: Literal["day"]
    cost_unit: Literal["synthetic_cost_unit"]
    replications: int
    seed: int
    modeling_caveats: list[str]
    lead_time_sensitivity: list[_WorkflowScenario]


class _WorkflowReferenceParity(TypedDict):
    status: Literal["not_run"]


class _WorkflowSimulation(TypedDict):
    status: Literal["experimental_local_test_double_only"]
    selected_result_source: Literal["policy_test_double"]
    reference_parity: _WorkflowReferenceParity
    result: _WorkflowComparison


class _WorkflowForecast(TypedDict):
    model: Literal["seasonal_naive_lag7"]
    status: Literal[
        "experimental_synthetic_profile_not_empirically_validated"
    ]
    model_card_ref: str
    history_start: str
    history_end: str
    horizon_days: Literal[28]
    profile_units: list[int]


class _SyntheticWorkflowResult(TypedDict):
    """Static shape consumed from the existing M1F-02 workflow result."""

    schema_version: Literal["mirrormind.synthetic_retail_decision_workflow.v2"]
    status: Literal["synthetic_comparison_ready_experimental"]
    as_of: str
    source_status: Literal["fictional_fixture_not_authenticated_or_authorized"]
    decision_status: Literal[
        "comparison_only_no_policy_selection_or_authorization"
    ]
    forecast: _WorkflowForecast
    simulation: _WorkflowSimulation
    trace: object
    trace_sha256: str
    workflow_result_sha256: str
    human_review: Literal["not_requested"]
    action_authorized: Literal[False]
    writes_performed: Literal[False]


class _ToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class EvidenceSearchInput(_ToolModel):
    query: Annotated[StrictStr, StringConstraints(strip_whitespace=True, min_length=1, max_length=512)]
    top_k: StrictInt = Field(default=5, ge=1, le=10)

    @field_validator("query")
    @classmethod
    def reject_query_controls(cls, value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("query must not contain control characters")
        return value


class EvidenceSearchHit(_ToolModel):
    excerpt: Annotated[StrictStr, StringConstraints(min_length=1, max_length=480)]
    trust_label: Literal["untrusted_evidence"]
    citation: EvidenceCitation
    citation_ref: Annotated[StrictStr, StringConstraints(pattern=r"^[0-9a-f]{64}$")]

    @model_validator(mode="after")
    def match_citation_digest(self) -> EvidenceSearchHit:
        if self.citation_ref != _citation_ref(self.citation):
            raise ValueError("citation_ref must bind the exact typed citation")
        return self


class EvidenceSearchOutput(_ToolModel):
    schema_version: Literal["mirrormind.agent.evidence_search.v1"] = (
        "mirrormind.agent.evidence_search.v1"
    )
    status: Literal["results", "no_matches"]
    hits: tuple[EvidenceSearchHit, ...] = Field(max_length=10)

    @model_validator(mode="after")
    def match_status(self) -> EvidenceSearchOutput:
        if (self.status == "results") != bool(self.hits):
            raise ValueError("evidence status must match whether hits exist")
        return self


class SyntheticDecisionToolInput(_ToolModel):
    as_of: date
    replications: StrictInt = Field(default=1, ge=1, le=3)
    seed: StrictInt = Field(default=317, ge=0, le=(1 << 32) - 1 - 250)

    @field_validator("as_of")
    @classmethod
    def require_date(cls, value: date) -> date:
        if type(value) is not date:
            raise ValueError("as_of must be a calendar date")
        return value


class SyntheticForecastSummary(_ToolModel):
    model: Literal["seasonal_naive_lag7"]
    status: Literal["experimental_synthetic_profile_not_empirically_validated"]
    model_card_ref: Annotated[StrictStr, StringConstraints(min_length=1, max_length=160)]
    history_start: Annotated[StrictStr, StringConstraints(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")]
    history_end: Annotated[StrictStr, StringConstraints(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")]
    horizon_days: Literal[28]
    profile_units: tuple[StrictInt, ...] = Field(min_length=28, max_length=28)


class SyntheticPolicyMeanMetrics(_ToolModel):
    total_cost_units: StrictFloat
    stockout_days_per_replication: StrictFloat
    ending_on_hand_units: StrictFloat
    pending_order_units: StrictFloat
    order_count: StrictFloat
    fill_rate_basis_points: StrictInt | None

    @field_validator(
        "total_cost_units",
        "stockout_days_per_replication",
        "ending_on_hand_units",
        "pending_order_units",
        "order_count",
    )
    @classmethod
    def require_nonnegative_metric(cls, value: float) -> float:
        if value < 0:
            raise ValueError("synthetic policy metrics must be nonnegative")
        return value


class SyntheticPolicySummary(_ToolModel):
    policy_id: Literal[
        "fixed_cycle_quantity",
        "reorder_point_fixed_quantity",
        "forecast_aware_order_up_to",
    ]
    ranking_status: Literal["not_computed"]
    mean_metrics: SyntheticPolicyMeanMetrics


class SyntheticPolicyScenario(_ToolModel):
    lead_time_days: StrictInt = Field(ge=1, le=28)
    is_base_assumption: StrictBool
    demand_stream_sha256: tuple[Annotated[StrictStr, StringConstraints(pattern=r"^[0-9a-f]{64}$")], ...] = Field(min_length=1, max_length=3)
    policies: tuple[SyntheticPolicySummary, ...] = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def validate_pairing_and_policy_set(self) -> SyntheticPolicyScenario:
        if tuple(item.policy_id for item in self.policies) != _POLICY_IDS:
            raise ValueError("scenario must contain all fixed policies in source order")
        return self


class SyntheticSimulationSummary(_ToolModel):
    status: Literal["experimental_local_test_double_only"]
    selected_result_source: Literal["policy_test_double"]
    engine_contract_ref: Literal["mirrormind.local.retail_policy_test_double.v1"]
    engine_execution: Literal["worldkernel_not_invoked"]
    decision_status: Literal["comparison_only_no_policy_selection_or_authorization"]
    input_status: Literal["caller_supplied_assumptions_not_authenticated"]
    quantity_unit: Literal["item"]
    time_unit: Literal["day"]
    cost_unit: Literal["synthetic_cost_unit"]
    replications: StrictInt = Field(ge=1, le=3)
    seed: StrictInt = Field(ge=0, le=(1 << 32) - 1)
    reference_parity_status: Literal["not_run"]
    modeling_caveats: tuple[Annotated[StrictStr, StringConstraints(min_length=1, max_length=240)], ...] = Field(min_length=1, max_length=5)
    lead_time_sensitivity: tuple[SyntheticPolicyScenario, ...] = Field(min_length=1, max_length=3)


class SyntheticDecisionToolOutput(_ToolModel):
    schema_version: Literal["mirrormind.agent.synthetic_decision.v1"] = (
        "mirrormind.agent.synthetic_decision.v1"
    )
    workflow_schema_version: Literal["mirrormind.synthetic_retail_decision_workflow.v2"]
    status: Literal["synthetic_comparison_ready_experimental"]
    as_of: Annotated[StrictStr, StringConstraints(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")]
    source_status: Literal["fictional_fixture_not_authenticated_or_authorized"]
    decision_status: Literal["comparison_only_no_policy_selection_or_authorization"]
    forecast: SyntheticForecastSummary
    simulation: SyntheticSimulationSummary
    trace_sha256: Annotated[StrictStr, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
    workflow_result_sha256: Annotated[StrictStr, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
    human_review: Literal["not_requested"]
    action_authorized: Literal[False]
    writes_performed: Literal[False]


def _citation_ref(citation: EvidenceCitation) -> str:
    payload = json.dumps(
        citation.model_dump(mode="json"),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def _search_synthetic_evidence(request: EvidenceSearchInput) -> EvidenceSearchOutput:
    result = build_fictional_index().search(
        EvidenceQuery(text=request.query, top_k=request.top_k)
    )
    hits = tuple(
        EvidenceSearchHit(
            excerpt=hit.excerpt,
            trust_label=hit.trust_label,
            citation=hit.citation,
            citation_ref=_citation_ref(hit.citation),
        )
        for hit in result.hits
    )
    return EvidenceSearchOutput(status=result.status, hits=hits)


def _summarize_workflow(request: SyntheticDecisionToolInput) -> SyntheticDecisionToolOutput:
    workflow_request = SyntheticDecisionWorkflowRequest(
        as_of=request.as_of,
        replications=request.replications,
        seed=request.seed,
    )
    result = cast(
        _SyntheticWorkflowResult,
        run_synthetic_decision_workflow(workflow_request),
    )
    if result.get("status") != "synthetic_comparison_ready_experimental":
        raise ValueError("the fixed synthetic workflow did not produce a comparison")
    trace = DecisionTraceV2.model_validate(result["trace"])
    if trace.result_sha256 != result.get("trace_sha256"):
        raise ValueError("the fixed workflow trace digest does not match")

    source_simulation = result["simulation"]
    source_result = source_simulation["result"]
    scenarios: list[SyntheticPolicyScenario] = []
    for scenario in source_result["lead_time_sensitivity"]:
        policies = scenario["policies"]
        if len(policies) != len(_POLICY_IDS):
            raise ValueError("fixed simulation returned an unexpected policy count")
        digest_lists = tuple(
            tuple(row["demand_stream_sha256"] for row in policy["replication_results"])
            for policy in policies
        )
        if any(digests != digest_lists[0] for digests in digest_lists[1:]):
            raise ValueError("fixed simulation did not preserve paired demand streams")
        summaries = tuple(
            SyntheticPolicySummary(
                policy_id=policy["policy_id"],
                ranking_status=policy["ranking_status"],
                mean_metrics=SyntheticPolicyMeanMetrics.model_validate(
                    policy["mean_metrics_per_replication"], strict=True
                ),
            )
            for policy in policies
        )
        scenarios.append(
            SyntheticPolicyScenario(
                lead_time_days=scenario["lead_time_days"],
                is_base_assumption=scenario["is_base_assumption"],
                demand_stream_sha256=digest_lists[0],
                policies=summaries,
            )
        )

    return SyntheticDecisionToolOutput(
        workflow_schema_version=result["schema_version"],
        status=result["status"],
        as_of=result["as_of"],
        source_status=result["source_status"],
        decision_status=result["decision_status"],
        forecast=SyntheticForecastSummary.model_validate_json(
            json.dumps(
                {
                    "model": result["forecast"]["model"],
                    "status": result["forecast"]["status"],
                    "model_card_ref": result["forecast"]["model_card_ref"],
                    "history_start": result["forecast"]["history_start"],
                    "history_end": result["forecast"]["history_end"],
                    "horizon_days": result["forecast"]["horizon_days"],
                    "profile_units": result["forecast"]["profile_units"],
                },
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            strict=True,
        ),
        simulation=SyntheticSimulationSummary(
            status=source_simulation["status"],
            selected_result_source=source_simulation["selected_result_source"],
            engine_contract_ref=source_result["engine_contract_ref"],
            engine_execution=source_result["engine_execution"],
            decision_status=source_result["decision_status"],
            input_status=source_result["input_status"],
            quantity_unit=source_result["quantity_unit"],
            time_unit=source_result["time_unit"],
            cost_unit=source_result["cost_unit"],
            replications=source_result["replications"],
            seed=source_result["seed"],
            reference_parity_status=source_simulation["reference_parity"]["status"],
            modeling_caveats=tuple(source_result["modeling_caveats"]),
            lead_time_sensitivity=tuple(scenarios),
        ),
        trace_sha256=result["trace_sha256"],
        workflow_result_sha256=result["workflow_result_sha256"],
        human_review=result["human_review"],
        action_authorized=result["action_authorized"],
        writes_performed=result["writes_performed"],
    )


def build_synthetic_tool_registry() -> ToolRegistry:
    """Create only the fixed retrieval and composed M1 decision tools."""
    return ToolRegistry(
        (
            ToolDefinition(
                name="search_synthetic_evidence",
                description=(
                    "Search the fixed caller-scoped fictional method notes; "
                    "returned excerpts are untrusted evidence."
                ),
                input_model=EvidenceSearchInput,
                output_model=EvidenceSearchOutput,
                handler=_search_synthetic_evidence,
            ),
            ToolDefinition(
                name="run_synthetic_retail_decision",
                description=(
                    "Run the existing fixed M1F-02 fictional evidence, forecast "
                    "and policy comparison workflow; no writes or policy selection."
                ),
                input_model=SyntheticDecisionToolInput,
                output_model=SyntheticDecisionToolOutput,
                handler=_summarize_workflow,
            ),
        )
    )
