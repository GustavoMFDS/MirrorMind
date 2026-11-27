"""Run bounded local retrieval over a generated fictional evidence corpus."""

from __future__ import annotations

import argparse
import json
import sys

from pydantic import ValidationError

from mirrormind.modules.retrieval.contracts import EvidenceQuery
from mirrormind.modules.retrieval.fictional_fixture import build_fictional_index


def main(argv: list[str] | None = None) -> int:
    """Print deterministic, cited fictional results without network or writes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="bounded local search text")
    parser.add_argument("--top-k", type=int, default=5)
    options = parser.parse_args(argv)
    try:
        query = EvidenceQuery(text=options.query, top_k=options.top_k)
        result = build_fictional_index().search(query)
    except (ValidationError, TypeError, ValueError):
        print("Error: invalid evidence retrieval request.", file=sys.stderr)
        return 2
    print(json.dumps(result.model_dump(mode="json"), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
