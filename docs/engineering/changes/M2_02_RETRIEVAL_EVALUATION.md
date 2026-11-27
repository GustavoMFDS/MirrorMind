# Change request — bounded fictional retrieval evaluation

## 1. Goal in plain language

**Current behavior:** M2-01 can rank at most 100 generated fictional
documents, filter caller-declared access before tokenization, and return
untrusted excerpts with exact citation metadata. Tests verify deterministic
examples and citation integrity, but there is no declared multi-query set or
aggregate report for retrieval relevance, abstention, access compliance and
document lineage. See [the retrieval walkthrough](../M2_EVIDENCE_RETRIEVAL.md),
`InMemoryEvidenceIndex.build`, and `tests/unit/test_evidence_retrieval.py`.

**Desired behavior:** Add a bounded, deterministic offline evaluator over
fictional `EvidenceDocument` values and an immutable, explicitly declared
query set. Report relevance recall/hit rate, correct and unexpected
abstentions, scope violations, source-lineage matches and excerpt support.
Expose no query text, excerpt content or out-of-scope identifiers in the
aggregate report.

**Why:** M2-02 in the [task backlog](../TASK_BACKLOG.md) depends on integrated
M2-01. A measured synthetic test set verifies that ranking, abstention,
citations and access filters compose as intended before any provider or
authorized real-source work is separately approved.

**Out of scope:** No real-source retrieval, authenticated identity, RAG/LLM,
route, persistent index, significance or calibration claim, source permission,
provider use, WorldKernel call, or capability promotion. A perfect score on
fictional fixtures is not empirical retrieval quality.

### Capability status

- `local_fictional_evidence_retrieval` stays **experimental**.
- `evidence_and_rag` stays **planned**; no endpoint or new public capability is
  added.
- Existing `/v1/capabilities` status is unchanged; its regression remains
  required after the ledger description is clarified.

## 2. Acceptance criteria

- [ ] Given a non-empty bounded corpus and unique non-empty case IDs, each
  declared query runs through the existing scope-first index deterministically.
- [ ] Given relevance labels, report recall@k and relevant-query hit rate with
  explicit denominators; return `null` when a denominator is zero.
- [ ] Given answerable and no-answer cases, report abstentions, correct
  abstentions, missed relevant queries and unexpected hits without claiming
  confidence calibration.
- [ ] Given each returned citation, independently verify collection/source/
  snapshot lineage, exact code-point excerpt span and UTF-8 digest. Report
  supported citations and rates; return only verified, in-scope citation refs.
- [ ] Given a scope-violating or unknown hit, count the violation without
  serializing its identifier, source ref, query or content.
- [ ] Given a relevance label for a missing or out-of-scope document, fail
  closed with a generic error that does not echo the label or hidden content.
- [ ] Bound corpus and cases; reject empty inputs, duplicate IDs, invalid
  labels, over-limit documents and unsupported document types before
  evaluation.
- [ ] Reject a retriever result that is not the exact versioned result
  contract or exceeds the case's declared `top_k`.
- [ ] Synthetic regressions cover full metric arithmetic, deterministic
  replay, correct abstention, lineage/citation failure, and access violations.
- [ ] Document equations, execution flow, reproduction, test meaning,
  limitations, debugging and learning exercises. Add evidence-map entries and
  atlas links for every new tracked path; regenerate the symbol catalog.
- [ ] Do not change HTTP capabilities or existing M2-01 retrieval behavior.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m2_evidence_retrieval_evaluation.py` | Add local-only reproducible report command | Integration CLI test; no route or file/network input |
| Core implementation | `src/mirrormind/modules/retrieval/evaluation.py::run_retrieval_evaluation` | Add bounded harness over the existing index | Unit tests cover metric arithmetic, citation checks, scopes and failures |
| Existing retrieval | `contracts.py`, `index.py`, `fictional_fixture.py` | Add immutable evaluation case/output contracts and a declared synthetic set; do not alter ranking | Existing M2-01 regressions plus M2-02 tests |
| State / persistence / API | `/v1/capabilities`, storage, HTTP routes | No behavioral change | Existing capability parity test and capability guard |
| Calling components | `InMemoryEvidenceIndex.build`, `InMemoryEvidenceIndex.search` | Reused once per declared case | Evaluator unit tests and example CLI |
| Downstream consumers | None; report is offline evaluation output | No production consumer | Report omits query text and excerpts |
| External project/contracts | None | No change | No WorldKernel or external source calls |

## Data, modeling and decision review

- Dataset card: only existing generated fictional documents; no source bytes,
  customer data, or new license is involved.
- Forecast model card: not applicable; this evaluator measures lexical
  retrieval, not forecast skill.
- Decision trace: not applicable; report authorizes no action or decision.
- WorldKernel gateway: not used.
- Evidence boundary: metrics describe only the declared fictional cases and
  do not establish real-world relevance, source rights, authenticated
  authorization or security of a future service. The `fictional_fixture`
  source-status value is caller supplied and does not verify the data origin.

## 4. Constraints and risks

Keep corpus size at or below the existing 100-document bound and cap the
evaluation set at 100 cases. Rebuild a separately filtered in-memory index per
case so caller-declared scopes cannot contaminate document frequency or
ranking. Gold relevant-document labels must resolve to documents visible to
that case, including its query collection filter. Do not echo invalid labels
or scope-violating citation metadata. Rates must expose numerator counts and
denominator counts and be null when undefined. The `source_status` literal is
not an origin attestation; use only generated fixture data.

## 5. Implementation plan

1. Trace current access filtering, ranker and citation contracts; preserve
   `bm25_lexical_v1` behavior.
2. Add strict bounded evaluation contracts, fixed synthetic cases, the pure
   evaluator and a local example CLI.
3. Add redaction, relevance, abstention, scope and source-lineage regressions.
4. Update retrieval walkthrough, system map, semantic coverage, debugging,
   learning exercises, capability notes, evidence map and atlas; regenerate
   the source symbol catalog.
5. Run focused tests, Ruff, strict retrieval typing, all documentation guards
   and the exact-head local quality gate; verify official PR checks separately.

## 6. Evidence after implementation

- Commit / PR: pending publication after the clean exact-head gate.
- Modified symbols and files: `RetrievalEvaluationCase`,
  `RetrievalCaseOutcome`, `RetrievalEvaluationReport` and
  `run_retrieval_evaluation` in `src/mirrormind/modules/retrieval/evaluation.py`;
  fixed generated cases in `fictional_fixture.py`; local runner in
  `examples/m2_evidence_retrieval_evaluation.py`.
- Tests executed, result, environment: 22 focused M2-01/M2-02 unit and CLI
  tests passed. Ruff, catalog, atlas, evidence and capability checks passed.
  The full six-check local gate remains pending a clean committed head. Local
  `mypy` is not installed; official quality CI must validate strict retrieval
  typing on the published exact head.
- Claim IDs and test selectors: `MM-RETR-009` through `MM-RETR-016` in
  [EVIDENCE_MAP](../EVIDENCE_MAP.json), each bound to a top-level regression.
- Evidence provenance, cutoffs and uncertainty: generated fictional fixtures;
  no real-source values or temporal claims.
- Scope of human review and approval: M2-02 is an existing P1 backlog item;
  implementation is confined to offline fictional evaluation.
- New or changed contracts: bounded evaluation case and aggregate report
  contracts; existing retrieval request/result wire contracts unchanged.
- Docs updated: [retrieval walkthrough](../M2_EVIDENCE_RETRIEVAL.md),
  [system map](../SYSTEM_MAP.md), [debugging guide](../DEBUGGING.md),
  [learning path](../LEARNING.md), [semantic map](../SEMANTIC_COVERAGE.md),
  [capability ledger](../CAPABILITY_LEDGER.json),
  [repository atlas](../REPOSITORY_ATLAS.md), and current status/handoff.
- Known limitations / follow-up: fictional metrics cannot establish retrieval
  quality for a user corpus; no authentication, external provenance or real
  source access is provided.
- Independent explanation: the walkthrough documents the scope-first per-case
  execution, metric denominators, citation checks, privacy boundary, CLI replay,
  regressions, debugging steps and hands-on metric exercise.
