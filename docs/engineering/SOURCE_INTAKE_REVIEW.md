# M1b — metadata-only source review packet (experimental)

**No real data source has been approved or ingested by this feature.** The
[preflight source](../../src/mirrormind/modules/evidence/intake_review.py)
joins one already structurally staged local result to a caller-declared
review manifest. It is strictly **in-memory** and does not open paths,
fetch external data, persist contents, invoke models or issue permissions.

## Supported preflight inputs

The two existing source-specific parsers remain responsible for format,
byte ceilings and digest checks:

- [Local daily CSV preflight](../../src/mirrormind/modules/evidence/snapshots.py):
  `StagedSnapshot`, format `daily_csv`, at most 1 MiB / 10,000 rows.
- [Optional UCI-shaped XLSX preflight](../../src/mirrormind/domains/retail/uci_workbook.py):
  `UciWorkbookReadResult`, format `uci_xlsx`, at most 32 MiB compressed
  and 10,000 input transaction rows.

The caller must **already be permitted** to open and stage the local
source before using either parser. The review packet cannot create that
permission after the fact.

`SourceReviewDeclaration` requires an explicit exact lowercase SHA-256
digest of the staged bytes, a sanitized source-card reference, references
to license evidence, use permissions and privacy review, the **intended
usage** (`research_evaluation` or `commercial_product`), a declared
retention period of 1–3,650 days and the capture date. An optional
historical-availability evidence reference may also be supplied.

The separate `inspected_on` date cannot precede capture. Review
references accept only compact uppercase letters, numbers, underscores
and hyphens, **not arbitrary URLs, file paths, credentials or personal
descriptions**. They are deliberately *opaque pointers*, whose actual
evidence must be reviewed **outside the software**.

A SHA mismatch, format mismatch, missing/invalid reference, impossible
date or invalid scope is rejected before the packet can be returned.
The packet hashes a canonical, versioned manifest of declared metadata;
changing any bound reference or permission scope changes the fingerprint.
This fingerprint proves neither that the declared evidence exists nor
that it is authentic, signed, approved, legally sufficient or current.

## Output and trust boundary

`prepare_source_review_packet(...).receipt()` reports the snapshot
digest, manifest fingerprint, kind, intended use, capture/inspection
dates, declared retention, row count and explicit pending-review flags.
It deliberately omits product/customer/invoice identifiers, all evidence
reference strings, raw observations and workbook details.

**Always**, even when every evidence reference is populated:

- `status = source_intake_requires_independent_human_review`
- `permission_status = not_verified_no_ingestion`
- `privacy_status = not_verified`
- `historical_availability_status = not_verified_no_asof_claim`
- `ingestion_authorized = false`
- `forecast_eligible = false`

The packet is not an access-control or legal-permission engine. It
cannot certify historical publication times from invoice event dates.
It does not promote the M5 or UCI sources to authorized status, enable
an Evidence Engine, establish a real backtest or release a model.

## Independent review remains a human go/no-go

Before a **separate, future** real-data adapter can proceed, a human
reviewer must verify the original grant for the intended use, provider
attribution, account/use terms, applicable privacy and retention rules,
exact byte identity from a trusted source, and any independent
publication-vintage evidence. The reviewer must maintain an approved
[dataset card](DATASET_CARD_TEMPLATE.md) outside the payload and follow
the [M5](datasets/M5_ACCESS_REVIEW.md) or
[UCI](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) review as appropriate.
Absence or ambiguity remains **NO-GO**.

## Tests and reproduction

[Unit tests](../../tests/unit/test_source_intake_review.py) cover both
synthetic staging types, digest mismatch, wrong-format rejections,
malformed/sensitive reference refusal, declared-purpose changes, exact
dates, immutable packets, confidentiality of identifiers and a
non-authorizing result even with every evidence pointer supplied.

```bash
python -m pytest -q tests/unit/test_source_intake_review.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

The narrow reviewed claim `MM-INTAKE-001` is tied to
`tests/unit/test_source_intake_review.py::test_staged_csv_packet_is_digest_bound_but_never_permission_approval`.
That test verifies metadata binding and refusal **only**, not external
rights, source accuracy or effective security against malicious callers.
