# MM-M1b — bounded binary stream staging (offline only)

## Problem

The existing `stage_csv_snapshot(data: bytes)` rejects
oversized inputs **after** a caller has already supplied
an in-memory byte array. A future local source-specific
adapter needs a bounded reading primitive to avoid
using `Path.read_bytes()` on potentially large files.

## Accepted scope

- [x] A trusted caller supplies an already-open
  binary stream and an expected SHA-256.
- [x] Read in chunks no larger than 65,536 bytes;
  observe only a `MAX_BYTES + 1` sentinel, then
  refuse an oversized stream.
- [x] Treat short reads as partial data rather than EOF.
- [x] Reject nonbytes output, missing `read`, readers
  exceeding the requested size, and `OSError` without
  copying sensitive filesystem metadata into error text.
- [x] Delegate actual digest, strict CSV parsing and
  row cap to the existing source-backed parser.
- [x] Unit and fixture integration tests.
- [ ] Verify Python and documentation CI before merge.

## Impact map

| Area | Source | Security boundary |
| --- | --- | --- |
| Source library | `src/mirrormind/modules/evidence/snapshots.py:read_staged_csv` | Reads only caller-opened streams, no network/path open |
| Unit tests | `tests/unit/test_evidence_snapshots.py` | Partial/oversized, error/redaction, truncated hash and row cap |
| Integration | `tests/integration/test_local_snapshot_flow.py` | Existing invented CSV only |
| Documentation | AST index, evidence map, method guide, atlas, learning and roadmap | No claim of source rights or authenticated publication |
| API and WorldKernel | No changes | No new production evidence endpoint or simulation |

## Trust model and release condition

`read_staged_csv` cannot establish a dataset license,
user consent, tenant access, source authenticity,
signed manifest, publisher release date or approved
retention period. Only call it on data **already
selected and authorized by an independent trusted
source adapter and human-reviewed data policy**.
An input digest computed from the same untrusted
stream is not an authorization decision.

The generic error-handling test is local; app-wide
logging/telemetry must be reviewed separately.

## Reproduction

```bash
python -m pytest -q tests/unit/test_evidence_snapshots.py
python -m pytest -q tests/integration/test_local_snapshot_flow.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```
