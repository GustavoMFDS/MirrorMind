"""Replay the fixed M2-03 flow using a local scripted provider double."""
from __future__ import annotations

import json
from datetime import date
from typing import Literal

from mirrormind.modules.agents.contracts import (
    AgentDraft,
    AgentRunRequest,
    AgentTurn,
    ProviderRequest,
    ToolCall,
)
from mirrormind.modules.agents.orchestrator import run_bounded_tool_orchestration
from mirrormind.modules.agents.synthetic_tools import (
    EvidenceSearchOutput,
    SyntheticDecisionToolOutput,
)


class ScriptedSyntheticProvider:
    """Deterministic teaching double; it does not call a model or network."""

    provider_mode: Literal["test_double"] = "test_double"

    def __init__(
        self,
        *,
        as_of: date = date(2011, 1, 26),
        replications: int = 1,
        seed: int = 17,
    ) -> None:
        self._turn_index = 0
        self._as_of = as_of
        self._replications = replications
        self._seed = seed

    def next_turn(self, request: ProviderRequest, /) -> AgentTurn:
        self._turn_index += 1
        if self._turn_index == 1:
            return AgentTurn(
                kind="tool_call",
                tool_call=ToolCall(
                    call_id="demo-search-1",
                    tool_name="search_synthetic_evidence",
                    arguments={"query": "seasonal naive baseline", "top_k": 2},
                ),
            )
        if self._turn_index == 2:
            return AgentTurn(
                kind="tool_call",
                tool_call=ToolCall(
                    call_id="demo-workflow-1",
                    tool_name="run_synthetic_retail_decision",
                    arguments={
                        "as_of": self._as_of.isoformat(),
                        "replications": self._replications,
                        "seed": self._seed,
                    },
                ),
            )

        observation = next(
            (
                item
                for item in request.observations
                if item.tool_name == "search_synthetic_evidence"
            ),
            None,
        )
        evidence = (
            EvidenceSearchOutput.model_validate_json(observation.output_json, strict=True)
            if observation is not None
            else None
        )
        workflow_observation = next(
            (
                item
                for item in request.observations
                if item.tool_name == "run_synthetic_retail_decision"
            ),
            None,
        )
        workflow = (
            SyntheticDecisionToolOutput.model_validate_json(
                workflow_observation.output_json, strict=True,
            )
            if workflow_observation is not None
            else None
        )
        if evidence is None or not evidence.hits or workflow is None:
            return AgentTurn(
                kind="final",
                final=AgentDraft(
                    status="insufficient_evidence",
                    summary="No visible fictional citation was available.",
                    citation_refs=(),
                ),
            )
        return AgentTurn(
            kind="final",
            final=AgentDraft(
                status="draft_for_human_review",
                summary=(
                    "The fictional workflow completed with result SHA-256 "
                    f"{workflow.workflow_result_sha256}. Review its trace and "
                    "cited method note before drawing a conclusion."
                ),
                citation_refs=(evidence.hits[0].citation_ref,),
            ),
        )


def main() -> int:
    """Print only the minimized deterministic orchestration receipt."""
    request = AgentRunRequest(
        question="Inspect this fictional retail decision workflow.",
    )
    report = run_bounded_tool_orchestration(request, ScriptedSyntheticProvider())
    print(
        json.dumps(
            report.model_dump(mode="json"),
            allow_nan=False,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0 if report.status == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
