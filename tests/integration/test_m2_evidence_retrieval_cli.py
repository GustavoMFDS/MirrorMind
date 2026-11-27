"""CLI replay and failure contract for fictional evidence retrieval."""

from __future__ import annotations

import json

from examples.m2_evidence_retrieval import main


def test_evidence_retrieval_cli_replays_cited_results_and_rejects_oversized_query(
    capsys,
):
    args = ["--query", "availability publication cutoff", "--top-k", "3"]

    assert main(args) == 0
    first = capsys.readouterr().out
    assert main(args) == 0
    second = capsys.readouterr().out

    assert first == second
    result = json.loads(first)
    assert result["algorithm"] == "bm25_lexical_v1"
    assert result["status"] == "results"
    assert all(hit["trust_label"] == "untrusted_evidence" for hit in result["hits"])
    assert all("citation" in hit for hit in result["hits"])
    assert "availability publication cutoff" not in first

    secret_query = "private-query-marker-" + ("x" * 600)
    assert main(["--query", secret_query]) == 2
    failure = capsys.readouterr()
    assert failure.out == ""
    assert secret_query not in failure.err
    assert "invalid evidence retrieval request" in failure.err
