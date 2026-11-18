# MM-M1b local XLSX reader — bounded, optional, unapproved sources stay blocked

## Existing behavior and accepted next step

The retail domain already has
[`project_uci_retail_rows`](../UCI_RETAIL_PROJECTION.md)
but it requires mappings supplied by a caller;
it cannot inspect the XLSX container that the
official UCI source uses.

Add an **opt-in** offline reader for a
**caller-opened, trusted binary stream**
conforming to a small UCI-shaped workbook
fixture. Never download files, resolve URLs,
open unknown paths, authorize data rights,
write user data, or declare the full UCI
dataset supported. The official data's
attribution, privacy and first-publication
history remain pending per
[UCI source review](../datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md).

## Accepted requirements

- [ ] `openpyxl` is an optional runtime dependency,
  enabled in CI/dev to test invented XLSX fixtures.
- [ ] Bounded compressed-byte reads, including
  short-read handling and a one-byte oversize
  sentinel, before parsing any workbook.
- [ ] Compare the complete bytes to a strict
  caller-provided lowercase SHA-256; do not
  treat this as independent provenance.
- [ ] Inspect ZIP entry count, entry sizes,
  total uncompressed metadata size and
  encrypted/external-link/macro payload markers
  before passing to openpyxl. No ZIP extraction.
- [ ] `read_only=True` / `keep_links=False`,
  fixed expected sheet/header, bounded rows.
  Only forward four needed transaction
  fields to the preexisting retail projection.
- [ ] Reject malformed/unsafe/corrupted
  workbooks without echoing customer values
  or filesystem paths into direct errors.
- [ ] Return digest-coupled immutable
  projection with `not_authorized` and
  **unknown publication time** statuses.
- [ ] Unit/integration tests create
  synthetic XLSX entirely in memory;
  reject forbidden schema/extra sheets,
  malformed source, wrong digest,
  oversized streams, row limits and
  illegal ZIP payload metadata.
- [ ] Update generated symbols, curated
  claims, capability API/ledger, atlas,
  guides, privacy and roadmap; merge
  only after Python + docs CI green.

## Impact and non-goals

| Surface | Change | Still unproved |
| --- | --- | --- |
| `src/mirrormind/domains/retail/uci_workbook.py` | Optional read-only bounded XLSX input stage | Full official workbook compatibility, permissions, hostile-file isolation |
| `src/mirrormind/domains/retail/uci_transactions.py` | Reused as-is | Cancellations, duplicates and business-day semantics need real-source review |
| `tests/unit/test_uci_workbook.py` | Purely fictional XLSX and malicious metadata cases | No actual customer data or external archive |
| `tests/integration/test_uci_workbook_flow.py` | Workbook -> privacy-minimized product/day fixture | No historical as-of or deployed forecast |
| `pyproject.toml` | Optional dependency and CI/dev extra | No added hard dependency for normal users |
| Generic evidence/forecasting/WorldKernel | Unchanged | No authorized ingest, prediction or simulations |

A later real-data PR requires reviewed rights,
attribution, privacy, identity of the exact
source snapshot, a bounded full-dataset strategy
and real historical availability policy.
This experimental reader must reject anything
outside its declared resource budget rather
than silently truncating the input.

## Reproduction

```bash
python -m pytest -q tests/unit/test_uci_workbook.py
python -m pytest -q tests/integration/test_uci_workbook_flow.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```
