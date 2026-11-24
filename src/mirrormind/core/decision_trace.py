"""Versioned, non-authorizing decision result contract for M1 review flows."""

import hashlib
import json
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal, TypeAlias

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StrictBool,
    StrictInt,
    StrictStr,
    StringConstraints,
    field_validator,
    model_validator,
)

RecordId = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$",
    ),
]
Reference = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)]
Label = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=96,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9 ./_:-]{0,95}$",
    ),
]
ScalarValue: TypeAlias = StrictStr | StrictInt | FiniteFloat | StrictBool
NumericValue: TypeAlias = StrictInt | FiniteFloat
Sha256Digest = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]


class _TraceModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


def _require_timezone(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value


def _require_optional_timezone(value: datetime | None) -> datetime | None:
    return _require_timezone(value) if value is not None else None


class EvidenceReference(_TraceModel):
    """Opaque pointer supplied by a caller; not an authenticated source record."""

    evidence_id: RecordId
    source_ref: Reference
    snapshot_ref: Reference
    provenance_ref: Reference
    available_at: datetime

    _aware_available_at = field_validator("available_at")(_require_timezone)


class ObservedFact(_TraceModel):
    """One scalar observation, separate from estimates and modeled outcomes."""

    fact_id: RecordId
    value: ScalarValue
    unit: Label
    observed_at: datetime
    evidence_refs: tuple[RecordId, ...] = Field(min_length=1)

    _aware_observed_at = field_validator("observed_at")(_require_timezone)


class ForecastEstimate(_TraceModel):
    forecast_id: RecordId
    target_ref: Reference
    value: ScalarValue
    unit: Label
    model_card_ref: Reference
    fact_refs: tuple[RecordId, ...] = Field(min_length=1)


class ModelingAssumption(_TraceModel):
    assumption_id: RecordId
    statement: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=512)]


class OutcomeMetric(_TraceModel):
    name: Label
    value: NumericValue
    unit: Label


class ConditionalOutcome(_TraceModel):
    """A declared conditional result; the reference does not prove execution."""

    outcome_id: RecordId
    alternative_ref: Reference
    engine_contract_ref: Reference
    forecast_refs: tuple[RecordId, ...] = Field(min_length=1)
    assumption_refs: tuple[RecordId, ...] = Field(min_length=1)
    metrics: tuple[OutcomeMetric, ...] = Field(min_length=1)
    seed: int = Field(ge=0, le=2**63 - 1)
    runs: int = Field(ge=1, le=10_000)


class MissingEvidence(_TraceModel):
    gap_id: RecordId
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=512)]
    blocks_refs: tuple[RecordId, ...] = Field(min_length=1)


class CostMeasurement(_TraceModel):
    cost_id: RecordId
    category: Label
    amount: Decimal | None = Field(default=None, ge=0, max_digits=24, decimal_places=8)
    unit: Label
    status: Literal["metered", "declared", "unavailable"]
    source_ref: Reference | None = None

    @model_validator(mode="after")
    def check_measurement(self) -> "CostMeasurement":
        if self.status == "unavailable":
            if self.amount is not None or self.source_ref is not None:
                raise ValueError("unavailable cost must omit amount and source_ref")
        elif self.amount is None or self.source_ref is None:
            raise ValueError(f"{self.status} cost requires amount and source_ref")
        return self


class HumanReview(_TraceModel):
    status: Literal["not_requested", "pending", "approved", "rejected"] = "not_requested"
    reviewer_ref: Reference | None = None
    decided_at: datetime | None = None
    reviewed_result_sha256: Sha256Digest | None = None

    _aware_decided_at = field_validator("decided_at")(_require_optional_timezone)

    @model_validator(mode="after")
    def check_decision_fields(self) -> "HumanReview":
        if self.status in {"not_requested", "pending"}:
            if self.decided_at is not None or self.reviewed_result_sha256 is not None:
                raise ValueError("pending review cannot contain a decision time or result digest")
            if self.status == "not_requested" and self.reviewer_ref is not None:
                raise ValueError("not-requested review cannot name a reviewer")
        elif (
            self.reviewer_ref is None
            or self.decided_at is None
            or self.reviewed_result_sha256 is None
        ):
            raise ValueError("approved review requires reviewer, decision time and result digest")
        return self


class DecisionTrace(_TraceModel):
    """Immutable v1 result shape; approval records review but grants no action."""

    schema_version: Literal["mirrormind.decision_trace.v1"] = "mirrormind.decision_trace.v1"
    trace_id: RecordId
    decision_ref: Reference
    revision: int = Field(ge=1, le=2**31 - 1)
    question: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=512)]
    cutoff_at: datetime
    created_at: datetime
    evidence: tuple[EvidenceReference, ...] = ()
    observations: tuple[ObservedFact, ...] = ()
    forecasts: tuple[ForecastEstimate, ...] = ()
    assumptions: tuple[ModelingAssumption, ...] = ()
    outcomes: tuple[ConditionalOutcome, ...] = ()
    missing_evidence: tuple[MissingEvidence, ...] = ()
    costs: tuple[CostMeasurement, ...] = ()
    human_review: HumanReview = Field(default_factory=HumanReview)

    _aware_trace_times = field_validator("cutoff_at", "created_at")(_require_timezone)

    @property
    def result_sha256(self) -> str:
        """Hash canonical result fields, excluding review to avoid circularity."""
        payload = self.model_dump(mode="python", exclude={"human_review"})

        def encode(value: object) -> str:
            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, Decimal):
                return format(value.normalize(), "f")
            raise TypeError(f"unsupported canonical result value: {type(value).__name__}")

        canonical = json.dumps(
            payload,
            default=encode,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @model_validator(mode="after")
    def check_trace_references_and_cutoff(self) -> "DecisionTrace":
        if self.created_at < self.cutoff_at:
            raise ValueError("trace creation cannot precede the declared cutoff")

        evidence_ids = {item.evidence_id for item in self.evidence}
        fact_ids = {item.fact_id for item in self.observations}
        forecast_ids = {item.forecast_id for item in self.forecasts}
        assumption_ids = {item.assumption_id for item in self.assumptions}
        outcome_ids = {item.outcome_id for item in self.outcomes}
        blocked_target_ids = fact_ids | forecast_ids | outcome_ids

        record_ids = [
            self.trace_id,
            *(item.evidence_id for item in self.evidence),
            *(item.fact_id for item in self.observations),
            *(item.forecast_id for item in self.forecasts),
            *(item.assumption_id for item in self.assumptions),
            *(item.outcome_id for item in self.outcomes),
            *(item.gap_id for item in self.missing_evidence),
            *(item.cost_id for item in self.costs),
        ]
        if len(record_ids) != len(set(record_ids)):
            raise ValueError("duplicate record identifier in decision trace")

        for evidence in self.evidence:
            if evidence.available_at > self.cutoff_at:
                raise ValueError("evidence available after the trace cutoff")

        for fact in self.observations:
            if fact.observed_at > self.cutoff_at:
                raise ValueError("observation occurs after the trace cutoff")
            unknown = set(fact.evidence_refs) - evidence_ids
            if unknown:
                raise ValueError(f"unknown evidence reference: {min(unknown)}")
            for evidence_ref in fact.evidence_refs:
                evidence = next(item for item in self.evidence if item.evidence_id == evidence_ref)
                if evidence.available_at < fact.observed_at:
                    raise ValueError("evidence availability precedes its observation")

        for forecast in self.forecasts:
            unknown = set(forecast.fact_refs) - fact_ids
            if unknown:
                raise ValueError(f"unknown fact reference: {min(unknown)}")

        for outcome in self.outcomes:
            unknown_forecasts = set(outcome.forecast_refs) - forecast_ids
            if unknown_forecasts:
                raise ValueError(f"unknown forecast reference: {min(unknown_forecasts)}")
            unknown_assumptions = set(outcome.assumption_refs) - assumption_ids
            if unknown_assumptions:
                raise ValueError(f"unknown assumption reference: {min(unknown_assumptions)}")

        for gap in self.missing_evidence:
            unknown = set(gap.blocks_refs) - blocked_target_ids
            if unknown:
                raise ValueError(f"unknown blocked record reference: {min(unknown)}")

        if (
            self.human_review.status in {"approved", "rejected"}
            and self.human_review.reviewed_result_sha256 != self.result_sha256
        ):
            raise ValueError("human review digest does not match result digest")
        return self
