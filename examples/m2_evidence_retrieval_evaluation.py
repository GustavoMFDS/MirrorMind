"""Print a bounded retrieval evaluation over the generated fictional corpus."""

from __future__ import annotations

import json

from mirrormind.modules.retrieval.evaluation import run_retrieval_evaluation
from mirrormind.modules.retrieval.fictional_fixture import (
    fictional_documents,
    fictional_evaluation_cases,
)


def main() -> int:
    """Run the fixed synthetic protocol without network access or writes."""
    report = run_retrieval_evaluation(
        fictional_documents(), fictional_evaluation_cases()
    )
    print(json.dumps(report.model_dump(mode="json"), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
