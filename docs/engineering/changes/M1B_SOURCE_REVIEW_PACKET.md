# Change request — M1b source review metadata binding

## 1. Goal

**Current:** `stage_csv_snapshot` and `read_uci_workbook` validate bounded
local byte structure and content digests, but do not provide a common
traceable review packet combining a declared source card, requested use,
rights/privacy evidence references and a staged result. The [M1 plan](../M1_EXECUTION_PLAN.md)
correctly blocks real ingestion until independent approval.

**Desired:** A minimal, offline and identifier-minimized packet that binds
one staged result to a reviewed manifest digest. **All** outputs must say
that authorization and historical availability remain unverified.

**Out of scope:** Actual rights checking, credentials, arbitrary files/URLs,
remote acquisition, M5 or UCI real-data ingestion, authorization tokens,
persistent audit storage, production forecasts and WorldKernel.

## 2. Capability truth

The local `local_source_intake_review_packet` primitive is
**experimental** and appears only under the API's `experimental` list.
`evidence_and_rag`, `forecasting` and other planned capabilities
remain planned. No existing route or staging signature changes.

## 3. Acceptance criteria

- Both existing synthetic staged formats can be fingerprint-bound to
  an exact declared content SHA-256.
- Missing/mismatched digests, unsafe review references, unexpected formats,
  false dates, impossible retention and unsupported uses refuse with
  sanitized errors.
- One changed reference, intended use or retention produces a different
  manifest digest. No reference or raw field is copied to the packet
  receipt.
- `ingestion_authorized` and `forecast_eligible` remain false, even
  with supplied references or publication-vintage assertions.
- Both fake fixture input types, adverse cases, live capabilities
  consistency and full local quality gate pass on the exact PR revision.

## 4. Impact map

| Layer | File or symbol | Change |
| --- | --- | --- |
| Existing CSV/XLSX parsing | `modules/evidence/snapshots.py`, `domains/retail/uci_workbook.py` | None |
| New local bridge | `modules/evidence/intake_review.py`: `SourceReviewDeclaration`, `prepare_source_review_packet` | Implement metadata-only result binding |
| Security/evidence | `tests/unit/test_source_intake_review.py` | Synthetic input, validation and privacy regressions |
| Advertised status | `api/routes/system.py` and `CAPABILITY_LEDGER.json` | Experimental only |
| Human review | `SOURCE_INTAKE_REVIEW.md`, dataset cards | Preserve mandatory independent authorization |
| Backend storage/transport | None | No persistent writes or API ingestion |
| Forecasting/simulation | None | No new operational permission |

## 5. Risks, rollback and independent review

User-supplied evidence references may point to nonexistent or false
documentation; cryptographic hashes bind declarations to staging but do
not authenticate publishers or grants. A caller is still responsible for
authorizing source acquisition *before* staging. No malicious payload
parsing or content sanitization beyond the upstream reader is claimed.
A rollback removes the bridge and its experimental capability label,
without changing previously staged data or stable API behavior.

Review [source guide](../SOURCE_INTAKE_REVIEW.md), [source rights](../datasets/M5_ACCESS_REVIEW.md)
and [dataset card template](../DATASET_CARD_TEMPLATE.md). Run the exact
SHA-bound local gate; official GitHub Actions must not be claimed to have
passed when unavailable. A real approved source adapter requires a
separate change request and independently reviewed evidence.
