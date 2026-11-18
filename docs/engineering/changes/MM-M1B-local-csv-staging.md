# MM-M1b local CSV staging — strict offline structural adapter

## Goal, existing behavior and boundary

Prior code includes synthetic-only examples and versioned
`EvidenceRef` fields but **no reusable source-level parser**.
Implement one small, reusable evidence-module preflight
that accepts bounded CSV **bytes from a trusted caller**,
checks a caller-provided SHA-256 expectation, validates
per-series event and first-published dates, and returns
an immutable staged result with explicit **NOT AUTHORIZED**
status. Add a historical availability view.

This is not source acquisition, authorization, real M5
ingestion, forecast modeling, new HTTP endpoints or a
WorldKernel adapter. It is deliberately insufficient to
approve real customer data.

## Acceptance criteria

- [x] Strict 1 MiB maximum **provided bytes** and exact
  default 10,000-row cap, without network/filesystem I/O.
- [x] Exact CSV header and four columns; reject ambiguous
  duplicate per-series day, malformed dates, wrong
  publication ordering and invalid units.
- [x] Constant-time comparison of complete raw-byte
  SHA-256 to explicit lowercase expected digest;
  **do not** call this signer authentication.
- [x] Return frozen observations and a receipt explicitly
  labelled `local_structure_checked_not_authorized`.
- [x] At historical origin `t`, return only rows whose
  event date and first declared publication date are <= `t`.
- [x] No imputation, external fetch, persistence, customer
  permissions or unknown version acceptance.
- [x] Local unit tests including adverse cases and
  integration with invented versioned fixture.
- [ ] Python/API CI and documentation CI reviewed green
  before integration.

## Impact map

| Layer | Change | Trust boundary |
| --- | --- | --- |
| Production library | `src/mirrormind/modules/evidence/snapshots.py` | Structural parser and as-of selector only |
| Package | `src/mirrormind/modules/evidence/__init__.py` | No automatic source discovery |
| Test | `tests/unit/test_evidence_snapshots.py` | 30 unit checks locally run during development |
| Fixture/flow | `examples/staged-daily-observations.csv`; `tests/integration/test_local_snapshot_flow.py` | Fictional counts, not permitted third-party source |
| API capability status | Experimental `local_csv_snapshot_preflight` only | Existing real evidence/RAG remains planned |
| Docs/catalog | Generated symbol index, human atlas, claim map, source guide, data card | Structural links and selected test-backed semantics |
| WorldKernel | No changes | One-way dependency preserved |

## Unresolved risks

SHA-256 compared to a caller-owned digest checks byte
consistency but is not publisher authentication.
Local staging can read malicious or unauthorized bytes
**if an upstream caller ignores source rights**; that
caller must separately enforce permissions before
handling private data. No release-time proof,
publisher revisions, PII classification, compliance
retention or empirical model performance is provided.
The selector is a lower-level primitive; never expose
its raw observation tuple in a public API response.

## Reproduction

```bash
python -m pytest -q tests/unit/test_evidence_snapshots.py
python -m pytest -q tests/integration/test_local_snapshot_flow.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

This is a reproduction recipe, not a claim of CI
completion or real data permission.
