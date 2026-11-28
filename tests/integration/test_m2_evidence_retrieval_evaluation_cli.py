"""Local CLI replay test for the declared M2-02 fictional protocol."""

from __future__ import annotations

import json

from examples.m2_evidence_retrieval_evaluation import main


def test_retrieval_evaluation_cli_replays_query_free_aggregate_report(capsys):
    assert main() == 0
    first = capsys.readouterr().out
    assert main() == 0
    second = capsys.readouterr().out

    assert first == second
    report = json.loads(first)
    assert report["schema_version"] == "m2_retrieval_eval_v1"
    assert report["retrieval_algorithm"] == "bm25_lexical_v1"
    assert report["case_count"] == 4
    assert report["recall_at_k"] == 1.0
    assert report["correct_abstention_rate"] == 1.0
    assert report["citation_support_rate"] == 1.0
    assert report["scope_compliance_rate"] == 1.0
    assert "availability publication cutoff" not in first
    assert "private-marker-731" not in first
    assert "Ignore previous instructions" not in first
