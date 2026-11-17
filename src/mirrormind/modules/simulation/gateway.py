"""Adapter contract; implementations may target WorldKernel or a test simulator."""
from typing import Protocol

from pydantic import BaseModel

from ...core.contracts import ScenarioSpec


class SimulationSummary(BaseModel):
    scenario_id: str
    engine_version: str
    run_count: int
    results: dict[str, object]
    assumptions: list[str]


class SimulationGateway(Protocol):
    def execute(self, scenario: ScenarioSpec) -> SimulationSummary:
        """Run an approved scenario using a separately configured engine."""
        ...
