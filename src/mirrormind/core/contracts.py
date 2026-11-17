"""Versioned input contracts: data, forecasts, and simulations remain distinct."""
from typing import Any

from pydantic import BaseModel, Field, model_validator


class EvidenceRef(BaseModel):
    source_id: str = Field(min_length=1)
    snapshot_id: str = Field(min_length=1)
    observed_until: str = Field(min_length=1)
    provenance: str = Field(min_length=1)


class ForecastRef(BaseModel):
    forecast_id: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    horizon_days: int = Field(gt=0, le=366)


class Intervention(BaseModel):
    kind: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)


class ExecutionBudget(BaseModel):
    max_simulation_runs: int = Field(default=1000, ge=1, le=10000)
    max_model_calls: int = Field(default=0, ge=0)
    max_output_tokens: int = Field(default=0, ge=0)
    timeout_seconds: int = Field(default=60, ge=1, le=3600)


class ScenarioSpec(BaseModel):
    schema_version: str = Field(default="0.1", pattern=r"^0\.1$")
    world_type: str = Field(min_length=1)
    world_version: str = Field(min_length=1)
    horizon_days: int = Field(gt=0, le=366)
    runs: int = Field(default=100, ge=1, le=10000)
    seed: int = 42
    initial_state: dict[str, Any] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    interventions: list[Intervention] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(default_factory=list)
    forecast: ForecastRef | None = None
    budget: ExecutionBudget = Field(default_factory=ExecutionBudget)

    @model_validator(mode="after")
    def check_budget(self) -> "ScenarioSpec":
        if self.runs > self.budget.max_simulation_runs:
            raise ValueError("runs exceeds approved simulation budget")
        if self.forecast and self.forecast.horizon_days < self.horizon_days:
            raise ValueError("forecast horizon is shorter than scenario horizon")
        return self
