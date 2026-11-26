# Change request — M2-01 permission-filtered evidence retrieval

> Scope: a bounded, deterministic in-memory retrieval slice over fictional
> evidence. This request does not add real ingestion, authentication, an LLM,
> a persistent index or an agent.

## 1. Goal in plain language

**Current behavior:** `src/mirrormind/modules/evidence/snapshots.py` stages
caller-supplied bytes and `intake_review.py` prepares non-authorizing review
metadata. Neither module searches documents or maps retrieval hits to source
citations. The evidence package docstring explicitly limits it to staged
primitives. `GET /v1/capabilities` still reports `evidence_and_rag` as planned.

**Desired behavior:** provide strict typed document, access-context, query,
hit, citation and result contracts; build an immutable in-memory index from a
small fictional fixture; filter documents by the caller-provided principal
and collection scope **before** tokenization or ranking; then return stable
lexical hits with excerpt offsets and a content digest. Retrieved text is
always labeled untrusted evidence. A local CLI demonstrates the flow using a
fixed fictional principal and collection.

**Why:** M2-01 is the first grounded-evidence product slice and a dependency of
retrieval evaluation and later tool orchestration. A readable fictional
example lets engineers verify access filtering and citation integrity before
any external source, identity system or model provider is approved.

**Out of scope:** public retrieval API, user authentication, real-source
authorization, file/URL acquisition, persistence, vector embeddings, an LLM,
tool execution, document instruction interpretation or production guarantees.
The existing `evidence_and_rag` capability stays planned; a narrow
`local_fictional_evidence_retrieval` capability may be exposed as experimental.

## Capability status change

- Previous: `evidence_and_rag` is `planned` in
  [CAPABILITY_LEDGER](../CAPABILITY_LEDGER.json).
- Proposed: keep that broad capability `planned`; add
  `local_fictional_evidence_retrieval` as `experimental` after the local
  example and tests exist.
- Production behavior: no authenticated or externally served retrieval.
- Test selectors: added after implementation; they must prove permission
  filtering before ranking, exact citation spans, deterministic ranking,
  bounded query/index inputs, exact excerpt-digest validation after
  deserialization, and untrusted-content labeling.
- `GET /v1/capabilities`: add only the experimental local-library declaration;
  no retrieval route is proposed because the scaffold has no authentication.

## 2. Acceptance criteria

- [x] Strict immutable contracts reject unknown fields, coercion, blank or
  oversized text, invalid references, duplicate document IDs, and out-of-range
  `top_k` or corpus bounds.
- [x] Index construction retains only documents visible to the supplied
  principal and collection scope; filtering occurs before tokenization, query
  scoring and top-k selection. Results reveal no denied document names,
  counts, snippets or citations.
- [x] The fixed lexical algorithm is deterministic and returns citation
  offsets whose excerpt equals the exact source substring; every
  `RetrievedEvidence` validation recomputes SHA-256 over the exact UTF-8
  excerpt and rejects a mismatched citation digest, including deserialized
  results.
- [x] Every hit labels source text `untrusted_evidence`. Injection-like fixture
  text remains quoted evidence and creates no instruction, role, tool call,
  network access or write.
- [x] The CLI accepts only bounded query and top-k options and uses only a
  generated fictional fixture with a fixed local access context.
- [x] The capability ledger, live `/v1/capabilities` parity test, evidence map,
  atlas, symbol catalog, system map, API capability docs, debugging notes,
  learning exercise and source walkthrough describe the implemented boundary.
- [x] The exact integrated PR #54 + #60 correction state passes the full
  local quality gate. No real dataset or provider evidence is claimed.

## 3. Impact map (confirmed before implementation)

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m2_evidence_retrieval.py` | New local demonstration; no HTTP route | New deterministic CLI integration test |
| Core implementation | `src/mirrormind/modules/retrieval/contracts.py::RetrievedEvidence.require_excerpt_integrity`, `index.py`, `fictional_fixture.py` | Revalidate exact span length and SHA-256 of the exact UTF-8 excerpt for every constructed or deserialized result | Regression tests reject same-length excerpt tampering and a different well-formed 64-character digest |
| State / persistence / API | `src/mirrormind/api/routes/system.py`; no database or retrieval route | Add one experimental capability string; no identity, storage or public retrieval | Existing API capability parity test plus capability checker |
| Calling components | No current retrieval callers; CLI will call the local retrieval service | New CLI caller only | CLI replay and error tests |
| Downstream consumers | Future M2-02 retrieval evaluation and M2-03 tool registry | No consumer changes in this slice | Contracts expose evidence/citation refs; no agent consumes them yet |
| Existing evidence staging | `src/mirrormind/modules/evidence/snapshots.py`, `intake_review.py` | No change; these remain separate, non-authorizing input/review primitives | Existing staging and review tests remain applicable |
| External projects/contracts | None | No change | No cross-repository dependency |

Confirmed links come from the current source imports and Graphify traversal:
the existing evidence modules stage/review local bytes; retail evaluation
consumes domain-specific records; capability reporting is a separate route.
No current source path calls a retriever. Future identity integration and
consumer wiring are hypotheses for M2-03/M3, not part of this change.

## Data, modeling and decision review

- Dataset card: not applicable to generated fictional text; any real-source
  adapter requires a reviewed dataset card and permission evidence first.
- Forecast model card: not applicable; this slice makes no forecast.
- Decision trace: no decision outcome or recommendation is produced.
- WorldKernel: not used.
- Temporal leakage: no time-based scoring or forecast is performed.

## 4. Constraints and risks

Access context is a trusted-caller input, not authenticated identity. The CLI
uses a hard-coded fictional scope only. No API exposes arbitrary caller scopes,
and this capability must not be treated as production access control. The
lexical score supports reproducible lookup only; it is not relevance
validation, calibrated confidence or retrieval quality evidence. Result text
is untrusted input and must not receive instruction or tool authority in a
future agent. Corpus, query, token and result sizes need explicit bounds.

## 5. Implementation plan

1. Inspect M1F-01 trace contracts, existing evidence staging and capability
   reporting; preserve those contracts.
2. Add strict contracts and an immutable in-memory index with pre-search scope
   filtering, deterministic lexical ranking and exact citation spans.
3. Add generated fixture and bounded local CLI; keep retrieval off the
   unauthenticated HTTP surface.
4. Add normal, denied-scope, adversarial-content, citation, bounds and replay
   tests.
5. Update walkthrough, system/semantic maps, atlas, catalog, evidence and
   capability records; run all required guards and the exact local gate.

## 6. Evidence after implementation

- Commit / PR: implementation commit
  `e151f9d9925d83d2b3e27fb88683672a93b48c30`; draft [PR #60](https://github.com/GustavoMFDS/MirrorMind/pull/60)
  targets the PR #54 branch. The PR remains unmerged and awaits review.
- Modified symbols and files: `EvidenceDocument`, `EvidenceAccessContext`,
  `EvidenceQuery`, `EvidenceCitation`, `RetrievedEvidence`,
  `EvidenceRetrievalResult`, `InMemoryEvidenceIndex.build/search`, the fixed
  fictional corpus, local CLI and capability declaration.
- Tests executed, result, environment: canonical
  `scripts/local_quality_gate.py --expected-head
  e151f9d9925d83d2b3e27fb88683672a93b48c30` passed on Python 3.13.5 at
  `2026-11-24T19:18:35.552346+00:00`: 720 tests passed, followed by Ruff,
  symbol catalog, atlas coverage, evidence map and capability ledger checks.
  The HTTP capability-parity test ran within that suite. One existing
  Starlette/httpx `TestClient` deprecation warning was emitted. An earlier
  focused attempt in the restricted sandbox stalled and was interrupted;
  the later full gate used the approved execution environment and passed.
- Claim IDs and cited test path/function: `MM-RETR-001` through `MM-RETR-006`
  in `docs/engineering/EVIDENCE_MAP.json`, covering permission filtering,
  citation spans, untrusted text, CLI replay, duplicate IDs and strict model
  validation.
- Evidence/provenance/cutoff and uncertainty: fictional fixture only; no
  empirical source or forecast claim.
- Scope of human review and approval: none requested or represented; a local
  fixture access context does not represent identity or source approval.
- New or changed contracts: strict frozen Pydantic models with bounded IDs,
  content, ACL lists, query size/top-k, excerpt size, citation offsets and
  SHA-256 digest; index size is bounded to 100 documents.
- Docs updated: M2 walkthrough, system map, semantic coverage, API walkthrough,
  security guide, debugging guide, learning exercise, capability ledger,
  evidence map, atlas, backlog, roadmap, blocker register and generated symbol
  catalog.
- Known limitations / follow-up: real identity and source authorization,
  durable index, retrieval evaluation and agent/tool consumers remain open.
  Historical PR #60 head `6374f0bb9a981271cb9340a190dcdebec6263cc9` failed
  before repository steps; check-run metadata records one annotation per
  check, but its text was not recovered and logs were unavailable. Do not call
  this head unannotated or infer a cause from another revision. Human review
  and integration remain pending.
- Independent explanation: the learning exercise traces scope filtering before
  tokenization, verifies excerpt offsets and digest bytes, and distinguishes
  the fixed demo scope from authentication. Independent human review remains
  pending with PR #60.

## Independent review correction — excerpt digest binding

- Finding: the original `RetrievedEvidence` validator compared excerpt length
  with the citation span but accepted any syntactically valid 64-character
  digest. `_make_hit` created correct digests, but a deserialized envelope
  bypassed that producer and could carry altered text with the old digest.
- Reproduction: both new tests failed before the fix with `DID NOT RAISE`:
  `test_contract_rejects_same_length_excerpt_tampering` and
  `test_contract_rejects_wrong_well_formed_excerpt_digest`.
- Resolution: `RetrievedEvidence.require_excerpt_integrity` checks span length,
  then recomputes SHA-256 over the exact UTF-8 excerpt bytes on every model
  validation. This detects excerpt/digest mismatch, not source authenticity or
  absolute-offset correctness without source bytes. Scope remains caller-
  declared rather than authenticated RBAC; duplicate IDs remain a trusted
  build-time invariant.
- Focused verification after the fix: `tests/unit/test_evidence_retrieval.py`
  passed all 9 tests.
- Integrated verification: merge commit `708171f` brought the latest PR #54
  corrections into this branch without cherry-picking duplicates. Exact
  integrated implementation/documentation SHA
  `73c191050865b0865e582f31a78859cc24262efb` passed
  `scripts/local_quality_gate.py --expected-head` at
  `2026-11-25T02:31:16.177471+00:00`: 738 pytest tests, Ruff, catalog, atlas,
  evidence and capability checks all passed. The sole warning is the existing
  Starlette/httpx `TestClient` deprecation. The sandboxed attempt stalled
  without test output and was interrupted; the same unchanged gate then passed
  in the approved execution environment. This is local evidence, not official
  GitHub Actions CI. Later documentation head `cad28d8c1e38dfd1cf8007c1b50853132d719ee3`
  also passed the exact six-stage local gate at `2026-11-25T02:37:37.528550+00:00`
  with 738 tests and the same existing deprecation warning.
- Official checks for integrated/docs SHA `cd9542156d8ab3cec2876ab07f3aa1c22dd00c37`
  were `test` run `45534005860` and `symbol-catalog` run `45534005856`.
  Both failed before any step and logs were unavailable (`BlobNotFound`). The
  check-run API reports one annotation per check, but its text was not
  recovered for that historical head; do not call it unannotated or infer its
  cause from another revision.
- Exact diagnostics for final published head
  `cad28d8c1e38dfd1cf8007c1b50853132d719ee3` show test runs `45534347123` and
  `45534341307`, plus `symbol-catalog` runs `45534347132` and `45534341412`.
  All four annotations state that the job was not started because recent
  account payments failed or the spending limit needs to be increased, and
  direct the account owner to Billing & plans. This confirms a pre-job
  account-level gate for this exact head but does not identify which condition
  applies. No repository steps ran and the latest pair's logs were unavailable;
  these are not remote test results.
- Follow-up docs head `cb4745635be7d57994d8766b59b40312a6b1702e` passed the exact
  local six-stage gate at `2026-11-25T03:11:16.792135+00:00`: 738 tests, Ruff,
  catalog, atlas, evidence and capabilities, with one existing
  Starlette/httpx `TestClient` deprecation warning. Its four Actions runs are
  `45538255051`/`45538248713` (`test`) and
  `45538255077`/`45538248727` (`symbol-catalog`). Exact check diagnostics
  return the same payment-or-spending-limit pre-job message for all four;
  repository steps did not run and logs were unavailable. This is not remote
  test evidence.
- New evidence selectors: `MM-RETR-007` and `MM-RETR-008` in
  `docs/engineering/EVIDENCE_MAP.json` identify the regressions and limitations.

## Main synchronization and integrated gate — 2026-11-26

- PR #60 remains a separate change. Its branch was ancestry-preservingly
  synchronized with PR #62's merged main at `a456034` by merge commit
  `a5186a680b307c4ecd9d56321321a5b27048731d`; the first parent is the PR #60
  head and the second parent is the exact new main. The resolved tree retains
  the same-length excerpt-tampering and wrong-digest regressions, while also
  including the merged M1 contracts and documentation. No duplicate commits
  were cherry-picked.
- On exact sync commit `a5186a680b307c4ecd9d56321321a5b27048731d`,
  `scripts/local_quality_gate.py --expected-head ...` passed at
  `2026-11-26T03:43:45.974393+00:00`: 845 tests, zero skips, Ruff, source
  catalog, repository atlas, evidence and capability checks. The existing
  TestClient deprecation warning remains. WorldKernel was installed from
  reviewed source revision `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
  Receipt: `results/local-quality-gate-a5186a680b307c4ecd9d56321321a5b27048731d.json`.
  Status is `local_gate_passed_not_official_ci`; Actions were not checked by
  this script. This receipt does not cover later documentation edits.
- A separate scoped `ruff check examples` found five findings in unchanged
  example files: I001 in `m1_asof_rolling_backtest.py`,
  `m1_observation_preflight.py` and `m1_temporal_backtest.py`; RUF007 in
  `m1_asof_rolling_backtest.py`; and F401 in `m1_temporal_backtest.py`.
  RUF007 is marked unsafe to auto-fix. These pre-existing findings are tracked
  as ENG-02 maintenance, outside this PR and outside the `src`/`tests` Ruff
  gate. No example code or verifier was changed to obtain the gate result.
- Before publication/review, rerun the complete six-check gate on the exact
  documentation-inclusive head and attach that receipt separately. Local
  checks do not replace official Actions or change required protections.
