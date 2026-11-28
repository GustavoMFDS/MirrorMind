"""Optional local WorldKernel executor for the exact synthetic policy contract."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from pydantic import ValidationError

from ...domains.retail.policy_simulation import (
    HORIZON_DAYS,
    POLICY_IDS,
    RetailPolicyAssumptions,
    RetailPolicyComparisonRequest,
    _build_demand_streams,
    _DemandStream,
    _lead_time_scenarios,
    compare_synthetic_retail_policies,
    finalize_retail_policy_metrics,
    summarize_retail_policy_runs,
)
from ...domains.retail.worldkernel_policy_world import (
    POLICY_TEST_DOUBLE_CONTRACT_REF,
    POLICY_WORLD_ENGINE_CONTRACT_REF,
    POLICY_WORLD_STATE_SCHEMA,
)
from .worldkernel_mapping import WorldKernelMappingError, WorldKernelOperatorLimits
from .worldkernel_policy_mapping import build_worldkernel_policy_exchange_request
from .worldkernel_runner import (
    WORLDKERNEL_PACKAGE_VERSION,
    WORLDKERNEL_SOURCE_COMMIT,
    WorldKernelRunnerError,
    WorldKernelRuntimeConfig,
    execute_mapped_worldkernel_request,
)

_FINAL_STATE_FIELDS = frozenset(
    {"schema_version", "day_index", "demand_units", "policy_states"}
)
_SAMPLED_DEMAND_MAX = 1_250


@dataclass(frozen=True, slots=True)
class LocalWorldKernelRetailPolicyGateway:
    """Execute only the code-owned retail policy world in a local worker."""

    operator_limits: WorldKernelOperatorLimits
    runtime: WorldKernelRuntimeConfig = field(default_factory=WorldKernelRuntimeConfig)

    def compare(self, request: RetailPolicyComparisonRequest) -> dict[str, object]:
        """Run engine transitions, then reject any drift from the reviewed model."""
        mapped = build_worldkernel_policy_exchange_request(
            request,
            operator_limits=self.operator_limits,
        )
        try:
            request = RetailPolicyComparisonRequest.model_validate(
                request.model_dump(mode="python")
            )
        except ValidationError as exc:
            raise WorldKernelMappingError(
                "policy comparison failed execution-boundary revalidation"
            ) from exc
        result, raw_result = execute_mapped_worldkernel_request(
            mapped,
            runtime=self.runtime,
        )
        assumptions = request.assumptions
        expected_streams = _build_demand_streams(request)
        final_states = result["final_states"]
        if type(final_states) is not list or len(final_states) != request.replications:
            raise WorldKernelRunnerError("WorldKernel policy run count mismatch")

        for index, (state, expected_stream) in enumerate(
            zip(final_states, expected_streams, strict=True)
        ):
            _validate_policy_world_state(state, assumptions)
            if tuple(state["demand_units"]) != expected_stream["demand_units"]:
                raise WorldKernelRunnerError(
                    "WorldKernel policy demand stream differs from the paired seed"
                )
            if expected_stream["replication"] != index:
                raise WorldKernelRunnerError("WorldKernel replication order mismatch")

        reference = compare_synthetic_retail_policies(request)
        engine_scenarios = _summarize_engine_runs(
            final_states=final_states,
            request=request,
            expected_streams=expected_streams,
        )
        if engine_scenarios != reference["lead_time_sensitivity"]:
            raise WorldKernelRunnerError(
                "WorldKernel policy outcomes differ from the reviewed reference rules"
            )
        selected_result_sha256 = _canonical_json_sha256(engine_scenarios)

        return {
            **reference,
            "simulation_status": "experimental_local_worldkernel_policy_world",
            "engine_execution": "worldkernel_invoked",
            "selected_result_source": "worldkernel_policy_world",
            "engine_contract_ref": POLICY_WORLD_ENGINE_CONTRACT_REF,
            "lead_time_sensitivity": engine_scenarios,
            "reference_parity": {
                "reference_simulator_invoked": True,
                "reference_engine_contract_ref": POLICY_TEST_DOUBLE_CONTRACT_REF,
                "status": "exact_match",
                "result_sha256": _canonical_json_sha256(
                    reference["lead_time_sensitivity"]
                ),
            },
            "worldkernel_execution": {
                "package_version": WORLDKERNEL_PACKAGE_VERSION,
                "source_commit": WORLDKERNEL_SOURCE_COMMIT,
                "result_schema": result["schema_version"],
                "world": result["world"],
                "registered_world_version": result["registered_world_version"],
                "result_sha256": hashlib.sha256(raw_result).hexdigest(),
                "selected_result_sha256": selected_result_sha256,
            },
        }


def _canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_policy_world_state(
    state: Any,
    assumptions: RetailPolicyAssumptions,
) -> None:
    if type(state) is not dict or set(state) != _FINAL_STATE_FIELDS:
        raise WorldKernelRunnerError("WorldKernel policy final-state fields are invalid")
    stream = state.get("demand_units")
    lead_times = _lead_time_scenarios(assumptions.lead_time_days)
    policy_states = state.get("policy_states")
    expected_policy_keys = {str(value) for value in lead_times}
    if (
        state.get("schema_version") != POLICY_WORLD_STATE_SCHEMA
        or type(state.get("day_index")) is not int
        or state["day_index"] != HORIZON_DAYS
        or type(stream) is not list
        or len(stream) != HORIZON_DAYS
        or any(
            type(value) is not int or not 0 <= value <= _SAMPLED_DEMAND_MAX
            for value in stream
        )
        or type(policy_states) is not dict
        or set(policy_states) != expected_policy_keys
    ):
        raise WorldKernelRunnerError("WorldKernel policy final-state envelope is invalid")
    for lead_time in lead_times:
        policies = policy_states[str(lead_time)]
        if type(policies) is not dict or set(policies) != set(POLICY_IDS):
            raise WorldKernelRunnerError("WorldKernel policy set is invalid")
        for policy_id in POLICY_IDS:
            policy_state = policies[policy_id]
            try:
                metrics = finalize_retail_policy_metrics(policy_state, assumptions)
            except (TypeError, ValueError) as exc:
                raise WorldKernelRunnerError(
                    "WorldKernel policy inventory state is invalid"
                ) from exc
            if metrics["total_demand_units"] != sum(stream):
                raise WorldKernelRunnerError(
                    "WorldKernel policy demand and inventory totals do not match"
                )


def _summarize_engine_runs(
    *,
    final_states: list[dict[str, Any]],
    request: RetailPolicyComparisonRequest,
    expected_streams: tuple[_DemandStream, ...],
) -> list[dict[str, object]]:
    scenarios: list[dict[str, object]] = []
    for lead_time in _lead_time_scenarios(request.assumptions.lead_time_days):
        policies = []
        for policy_id in POLICY_IDS:
            replication_results: list[dict[str, object]] = []
            for state, stream in zip(final_states, expected_streams, strict=True):
                metrics = finalize_retail_policy_metrics(
                    state["policy_states"][str(lead_time)][policy_id],
                    request.assumptions,
                )
                replication_results.append(
                    {
                        "replication": stream["replication"],
                        "seed": stream["seed"],
                        "demand_stream_sha256": stream["demand_stream_sha256"],
                        "metrics": metrics,
                    }
                )
            policies.append(
                summarize_retail_policy_runs(policy_id, replication_results)
            )
        scenarios.append(
            {
                "lead_time_days": lead_time,
                "is_base_assumption": lead_time
                == request.assumptions.lead_time_days,
                "policies": policies,
            }
        )
    return scenarios
