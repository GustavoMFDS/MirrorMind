# MM-M1b-exp — as-of time preflight for generated daily records

**Scope:** standalone synthetic example. This does **not**
complete MM-M1b authorized observation ingestion.

## Why

The existing M1a date-only preflight rejects observations
whose calendar date is after a cutoff but cannot distinguish
an event from a value published late. Future M1 evaluation
requires that separation to avoid direct data leakage.

## Narrow implementation and acceptance

- [x] Fixed v1 synthetic schema with `observed_on` and
  `available_on` per record and explicit `as_of_date`.
- [x] Accept a value into the aggregate only when both
  dates are on/before cutoff; classify future events and
  late publication separately.
- [x] Reject malformed/missing fields, non-canonical dates,
  booleans/negative counts, impossible publication ordering
  and duplicate observation days.
- [x] Refuse empty eligible sets; keep holes missing
  instead of treating missing as zero.
- [x] Fail safely with a bounded 1 MiB local CLI input,
  duplicate JSON key rejection and generic errors.
- [x] Unit and subprocess regressions on the invented fixture.
- [ ] Verify all CI workflows conclude success before merge.

## Impact map

| File or contract | Effect |
| --- | --- |
| `examples/m1_availability_preflight.py` | Pure teaching implementation; no external connector |
| `examples/synthetic-asof-sales.json` | Generated dates and counts only |
| `tests/unit/test_m1_availability_preflight.py` | As-of filtering and late-publication prevention |
| `tests/integration/test_m1_availability_preflight_cli.py` | Safe CLI outputs and adverse paths |
| `src/mirrormind/api/routes/system.py` | Add **experimental** status, keep Evidence Engine planned |
| Capability ledger, evidence map, guide and dataset card | Reproducible narrow claims and explicit limitations |
| WorldKernel | Not modified; no simulation invoked |

## What remains unknown

A claimed `available_on` is text, not proof of the
original source's publication schedule or legal permission.
Actual ingestion requires real license/consent scope,
publisher availability metadata, immutable snapshot and
revision evidence, privacy controls and data retention
approval. The synthetic filter is not a fact checker
or deployable evidence pipeline.

## Reproduce

```bash
python -m examples.m1_availability_preflight examples/synthetic-asof-sales.json
python -m pytest -q tests/unit/test_m1_availability_preflight.py
python -m pytest -q tests/integration/test_m1_availability_preflight_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

Do not treat these instructions as executed results.
