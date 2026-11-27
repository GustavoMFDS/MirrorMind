"""Synthetic regressions for the bounded M2-02 retrieval evaluator."""

from __future__ import annotations

import json
from hashlib import sha256

import pytest
from pydantic import ValidationError

import mirrormind.modules.retrieval.evaluation as evaluation_module
from mirrormind.modules.retrieval.contracts import (
    EvidenceAccessContext,
    EvidenceCitation,
    EvidenceQuery,
    EvidenceRetrievalResult,
    RetrievedEvidence,
)
from mirrormind.modules.retrieval.evaluation import (
    MAX_EVALUATION_CASES,
    RetrievalEvaluationCase,
    run_retrieval_evaluation,
)
from mirrormind.modules.retrieval.fictional_fixture import (
    DEMO_COLLECTION,
    DEMO_PRINCIPAL,
    fictional_documents,
    fictional_evaluation_cases,
)
from mirrormind.modules.retrieval.index import (
    MAX_INDEX_DOCUMENTS,
    InMemoryEvidenceIndex,
)


def _case(
    *,
    case_id: str = "case-one",
    query: str = "availability",
    top_k: int = 5,
    relevant: tuple[str, ...] = ("fixture-availability",),
    principal: str = DEMO_PRINCIPAL,
    collections: tuple[str, ...] = (DEMO_COLLECTION,),
) -> RetrievalEvaluationCase:
    return RetrievalEvaluationCase(
        case_id=case_id,
        access=EvidenceAccessContext(
            principal_id=principal,
            allowed_collection_ids=collections,
        ),
        query=EvidenceQuery(text=query, top_k=top_k),
        relevant_document_ids=relevant,
    )


def test_declared_fixture_set_reports_relevance_abstention_and_lineage():
    report = run_retrieval_evaluation(
        fictional_documents(), fictional_evaluation_cases()
    )

    assert report.schema_version == "m2_retrieval_eval_v1"
    assert report.retrieval_algorithm == "bm25_lexical_v1"
    assert report.case_count == 4
    assert report.expected_relevant_document_count == 2
    assert report.relevant_retrieved_document_count == 2
    assert report.recall_at_k == 1.0
    assert report.relevant_query_count == 2
    assert report.relevant_query_hit_count == 2
    assert report.relevant_query_hit_rate == 1.0
    assert report.expected_abstention_count == 2
    assert report.correct_abstention_count == 2
    assert report.correct_abstention_rate == 1.0
    assert report.abstained_query_count == 2
    assert report.abstention_rate == 0.5
    assert report.citation_count == 2
    assert report.lineage_match_count == 2
    assert report.lineage_match_rate == 1.0
    assert report.supported_citation_count == 2
    assert report.citation_support_rate == 1.0
    assert report.out_of_scope_hit_count == 0
    assert report.scope_compliance_rate == 1.0
    assert all(
        citation.document_id in {"fixture-availability", "fixture-baseline"}
        for outcome in report.cases
        for citation in outcome.verified_citations
    )

    serialized = json.dumps(report.model_dump(mode="json"), sort_keys=True)
    assert "availability publication cutoff" not in serialized
    assert "evalcaseavailability731" not in serialized
    assert "private-marker-731" not in serialized
    assert "Ignore previous instructions" not in serialized


def test_evaluation_is_deterministic_and_undefined_rates_are_null():
    documents = fictional_documents()
    case = _case(
        case_id="no-answer",
        query="quartz telescope archive",
        relevant=(),
    )

    first = run_retrieval_evaluation(documents, (case,)).model_dump(mode="json")
    second = run_retrieval_evaluation(documents, (case,)).model_dump(mode="json")

    assert first == second
    assert first["recall_at_k"] is None
    assert first["relevant_query_hit_rate"] is None
    assert first["correct_abstention_rate"] == 1.0
    assert first["lineage_match_rate"] is None
    assert first["citation_support_rate"] is None
    assert first["scope_compliance_rate"] is None


def test_relevance_labels_must_resolve_inside_declared_visible_scope():
    hidden_id = "fixture-private"
    case = _case(
        query="private marker",
        relevant=(hidden_id,),
        collections=(DEMO_COLLECTION, "retail-private"),
    )

    with pytest.raises(
        ValueError,
        match="relevance labels must resolve within the declared visible corpus",
    ) as error:
        run_retrieval_evaluation(fictional_documents(), (case,))

    assert hidden_id not in str(error.value)


def test_relevance_labels_must_also_match_query_collection_filter():
    case = RetrievalEvaluationCase(
        case_id="query-scope-case",
        access=EvidenceAccessContext(
            principal_id=DEMO_PRINCIPAL,
            allowed_collection_ids=(DEMO_COLLECTION, "retail-private"),
        ),
        query=EvidenceQuery(
            text="private unique sentinel",
            collection_ids=(DEMO_COLLECTION,),
        ),
        relevant_document_ids=("fixture-private",),
    )

    with pytest.raises(
        ValueError,
        match="relevance labels must resolve within the declared visible corpus",
    ):
        run_retrieval_evaluation(fictional_documents(), (case,))


def test_out_of_scope_hit_is_counted_without_returning_hidden_metadata(monkeypatch):
    documents = fictional_documents()
    hidden_access = EvidenceAccessContext(
        principal_id="demo-reviewer",
        allowed_collection_ids=("retail-private",),
    )
    hidden_result = InMemoryEvidenceIndex.build(documents, hidden_access).search(
        EvidenceQuery(text="vaultsignal731")
    )
    case = _case(
        query="vaultsignal731",
        relevant=(),
        collections=(DEMO_COLLECTION, "retail-private"),
    )

    monkeypatch.setattr(
        evaluation_module.InMemoryEvidenceIndex,
        "search",
        lambda _self, _query: hidden_result,
    )
    report = run_retrieval_evaluation(documents, (case,))
    serialized = json.dumps(report.model_dump(mode="json"), sort_keys=True)

    assert report.out_of_scope_hit_count == 1
    assert report.scope_compliance_rate == 0.0
    assert report.expected_abstention_count == 1
    assert report.correct_abstention_count == 0
    assert report.unexpected_hit_query_count == 1
    assert report.cases[0].verified_citations == ()
    assert "fixture-private" not in serialized
    assert "private-note" not in serialized
    assert "private-marker-731" not in serialized
    assert "synthetic://m2/private-note" not in serialized


def test_unknown_hit_is_counted_without_returning_its_metadata(monkeypatch):
    documents = fictional_documents()
    access = EvidenceAccessContext(
        principal_id=DEMO_PRINCIPAL,
        allowed_collection_ids=(DEMO_COLLECTION,),
    )
    valid_hit = InMemoryEvidenceIndex.build(documents, access).search(
        EvidenceQuery(text="availability")
    ).hits[0]
    unknown_citation = EvidenceCitation(
        document_id="unlisted-document-731",
        collection_id=valid_hit.citation.collection_id,
        source_ref="synthetic://unlisted-source",
        snapshot_ref=valid_hit.citation.snapshot_ref,
        start_offset=valid_hit.citation.start_offset,
        end_offset=valid_hit.citation.end_offset,
        excerpt_sha256=valid_hit.citation.excerpt_sha256,
    )
    unknown_hit = RetrievedEvidence(
        excerpt=valid_hit.excerpt,
        score=valid_hit.score,
        citation=unknown_citation,
        trust_label="untrusted_evidence",
    )
    unknown_result = EvidenceRetrievalResult(
        status="results",
        algorithm="bm25_lexical_v1",
        hits=(unknown_hit,),
    )
    monkeypatch.setattr(
        evaluation_module.InMemoryEvidenceIndex,
        "search",
        lambda _self, _query: unknown_result,
    )

    report = run_retrieval_evaluation(documents, (_case(relevant=()),))
    serialized = json.dumps(report.model_dump(mode="json"), sort_keys=True)

    assert report.out_of_scope_hit_count == 1
    assert report.scope_compliance_rate == 0.0
    assert report.cases[0].verified_citations == ()
    assert "unlisted-document-731" not in serialized
    assert "unlisted-source" not in serialized


def test_retrieval_result_cannot_exceed_declared_top_k(monkeypatch):
    documents = fictional_documents()
    access = EvidenceAccessContext(
        principal_id=DEMO_PRINCIPAL,
        allowed_collection_ids=(DEMO_COLLECTION,),
    )
    valid_hit = InMemoryEvidenceIndex.build(documents, access).search(
        EvidenceQuery(text="availability")
    ).hits[0]
    oversized_result = EvidenceRetrievalResult(
        status="results",
        algorithm="bm25_lexical_v1",
        hits=(valid_hit, valid_hit),
    )
    monkeypatch.setattr(
        evaluation_module.InMemoryEvidenceIndex,
        "search",
        lambda _self, _query: oversized_result,
    )

    with pytest.raises(ValueError, match="retrieval result exceeds the declared top_k"):
        run_retrieval_evaluation(
            documents,
            (
                _case(
                    query="availability",
                    top_k=1,
                    relevant=("fixture-availability",),
                ),
            ),
        )


def test_retriever_must_return_exact_result_contract(monkeypatch):
    monkeypatch.setattr(
        evaluation_module.InMemoryEvidenceIndex,
        "search",
        lambda _self, _query: {"status": "results"},
    )

    with pytest.raises(
        TypeError,
        match="retrieval must return an exact EvidenceRetrievalResult",
    ):
        run_retrieval_evaluation(fictional_documents(), (_case(),))


def test_source_lineage_mismatch_is_not_counted_as_supported(monkeypatch):
    documents = fictional_documents()
    access = EvidenceAccessContext(
        principal_id=DEMO_PRINCIPAL,
        allowed_collection_ids=(DEMO_COLLECTION,),
    )
    valid_hit = InMemoryEvidenceIndex.build(documents, access).search(
        EvidenceQuery(text="availability")
    ).hits[0]
    forged_citation = EvidenceCitation(
        document_id=valid_hit.citation.document_id,
        collection_id=valid_hit.citation.collection_id,
        source_ref="synthetic://forged-source",
        snapshot_ref=valid_hit.citation.snapshot_ref,
        start_offset=valid_hit.citation.start_offset,
        end_offset=valid_hit.citation.end_offset,
        excerpt_sha256=valid_hit.citation.excerpt_sha256,
    )
    forged_hit = RetrievedEvidence(
        excerpt=valid_hit.excerpt,
        score=valid_hit.score,
        citation=forged_citation,
        trust_label="untrusted_evidence",
    )
    forged_result = EvidenceRetrievalResult(
        status="results",
        algorithm="bm25_lexical_v1",
        hits=(forged_hit,),
    )
    monkeypatch.setattr(
        evaluation_module.InMemoryEvidenceIndex,
        "search",
        lambda _self, _query: forged_result,
    )

    report = run_retrieval_evaluation(documents, (_case(),))
    serialized = json.dumps(report.model_dump(mode="json"), sort_keys=True)

    assert report.citation_count == 1
    assert report.lineage_match_count == 0
    assert report.supported_citation_count == 0
    assert report.citation_support_rate == 0.0
    assert report.relevant_retrieved_document_count == 0
    assert report.cases[0].verified_citations == ()
    assert "forged-source" not in serialized


def test_malformed_and_oversized_evaluation_sets_fail_closed():
    valid = _case()
    documents = fictional_documents()
    with pytest.raises(ValueError, match="evaluation cases must be non-empty"):
        run_retrieval_evaluation(documents, ())
    with pytest.raises(ValueError, match="evaluation documents must be non-empty"):
        run_retrieval_evaluation((), (valid,))
    with pytest.raises(TypeError, match="documents must contain exact EvidenceDocument"):
        run_retrieval_evaluation((object(),), (valid,))
    oversized_documents = tuple(
        documents[0].model_copy(update={"document_id": f"oversized-{index}"})
        for index in range(MAX_INDEX_DOCUMENTS + 1)
    )
    with pytest.raises(ValueError, match="document limit exceeded"):
        run_retrieval_evaluation(oversized_documents, (valid,))
    with pytest.raises(ValueError, match="evaluation case identifiers must be unique"):
        run_retrieval_evaluation(
            fictional_documents(), (valid, valid.model_copy(update={"case_id": "case-one"}))
        )
    with pytest.raises(ValueError, match="evaluation case limit exceeded"):
        run_retrieval_evaluation(
            fictional_documents(),
            tuple(
                valid.model_copy(update={"case_id": f"case-{index}"})
                for index in range(MAX_EVALUATION_CASES + 1)
            ),
        )
    with pytest.raises(ValidationError, match="relevance document identifiers must be unique"):
        _case(relevant=("fixture-availability", "fixture-availability"))


def test_verified_excerpt_requires_exact_source_span_and_digest(monkeypatch):
    documents = fictional_documents()
    access = EvidenceAccessContext(
        principal_id=DEMO_PRINCIPAL,
        allowed_collection_ids=(DEMO_COLLECTION,),
    )
    valid_hit = InMemoryEvidenceIndex.build(documents, access).search(
        EvidenceQuery(text="availability")
    ).hits[0]
    document = next(
        item for item in documents if item.document_id == valid_hit.citation.document_id
    )
    altered_excerpt = "X" + valid_hit.excerpt[1:]
    bad_citation = EvidenceCitation(
        document_id=valid_hit.citation.document_id,
        collection_id=valid_hit.citation.collection_id,
        source_ref=valid_hit.citation.source_ref,
        snapshot_ref=valid_hit.citation.snapshot_ref,
        start_offset=valid_hit.citation.start_offset,
        end_offset=valid_hit.citation.end_offset,
        excerpt_sha256=sha256(altered_excerpt.encode("utf-8")).hexdigest(),
    )
    bad_hit = RetrievedEvidence(
        excerpt=altered_excerpt,
        score=valid_hit.score,
        citation=bad_citation,
        trust_label="untrusted_evidence",
    )
    bad_result = EvidenceRetrievalResult(
        status="results",
        algorithm="bm25_lexical_v1",
        hits=(bad_hit,),
    )
    assert document.content[
        bad_citation.start_offset : bad_citation.end_offset
    ] != altered_excerpt
    monkeypatch.setattr(
        evaluation_module.InMemoryEvidenceIndex,
        "search",
        lambda _self, _query: bad_result,
    )

    report = run_retrieval_evaluation(documents, (_case(),))

    assert report.lineage_match_count == 1
    assert report.supported_citation_count == 0
    assert report.citation_support_rate == 0.0
    assert report.cases[0].verified_citations == ()
