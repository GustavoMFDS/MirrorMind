# MM-M1b — source-unverified aggregated snapshot quality review

## Problem and narrow goal

The local CSV staging parser already refuses
ambiguous rows and the rolling evaluator reports
when historical forecasts must abstain. A reviewer
still lacks a reusable, low-data-exposure
summary of basic record coverage, explicitly
recorded zeros and declared publication delays
*before* trying any statistical model.

Add `snapshot_quality_summary(StagedSnapshot)`
to the existing evidence module. It takes
only structurally staged in-memory rows and
returns counts/dates, **not** raw records,
product IDs, customer fields, business demand
or a source permission certificate.

## Acceptance

- [x] Count rows/series and per-series **internal**
  calendar gaps between recorded first/last dates.
- [x] Count explicitly recorded zero-unit
  observations separately from absent dates.
- [x] Count rows with declared publication
  dates after the event date.
- [x] Reject unstaged/empty snapshots and
  directly constructed duplicate records.
- [x] Return only summary counts, overall date
  boundaries, hash and explicit non-authorized status.
- [x] Unit and bounded-reader integration
  regressions using invented data.
- [ ] Python and docs CI checked green before merge.

## Impact map

| Source | Change | Limitation |
| --- | --- | --- |
| `src/mirrormind/modules/evidence/snapshots.py` | Pure bounded aggregate quality function | No external source verification |
| `tests/unit/test_evidence_quality.py` | Missing-vs-zero, delays, invalid snapshots and output minimization | Synthetic data only |
| `tests/integration/test_local_snapshot_flow.py` | File-stream staging to quality summary | No authorized customer ingest |
| Method guide, evidence map, symbol catalog, atlas, roadmap | Source-backed learning and navigation | Structural guards are not data accuracy tests |
| WorldKernel and API | Unchanged | No runtime simulation, connector or forecasting release |

## Risks and independent review

A missing calendar date can be closed business,
no purchase, a filtered return or an absent report;
it is **not automatically zero demand**.
The summary does not know expected coverage
before the first or after the last observed date.
Dates and SHA-256 remain potentially sensitive
metadata, not an authenticated audit signature.
Source rights, customer privacy, retention,
and publication-time provenance remain
external prerequisites.

## Reproduce

```bash
python -m pytest -q tests/unit/test_evidence_quality.py
python -m pytest -q tests/integration/test_local_snapshot_flow.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```
