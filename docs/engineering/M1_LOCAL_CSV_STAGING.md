# M1b — bounded local CSV snapshot staging (unverified, not authorized)

**What now exists:** a real, reusable, deterministic module under
[`src/mirrormind/modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py)
for **local in-memory structural inspection** of a daily observation CSV.
It performs **no file opening, network request, persistence, account
permission check, source acquisition, model inference or business action**.

**What it is not:** an approved source connector, licensed M5 ingestion,
a real Evidence Engine, authenticated provenance, a temporal model or a
WorldKernel integration. A passing receipt is labelled
`local_structure_checked_not_authorized`.

Read the [dataset approval requirements](DATASET_CARD_TEMPLATE.md),
[security boundary](../SECURITY.md),
[local synthetic fixture card](datasets/LOCAL_CSV_STAGING_FIXTURE.md),
[capability status](CAPABILITY_LEDGER.json), and
[M1 milestones](M1_EXECUTION_PLAN.md).

## Exact source contracts

| Symbol | Inputs / output | Rejection and trust boundary |
| --- | --- | --- |
| `Observation` | Frozen row: series ID, observed calendar day, first declared publication day, nonnegative integer units | Carries **unverified** source content; no claim about true demand |
| `StagedSnapshot` | Immutable tuple of observations and SHA-256 of supplied bytes | Immutable Python fields do **not** make source provenance authentic |
| `StagedSnapshot.receipt()` | Only row count, series count, digest and `not_authorized` status | No raw rows returned; counts and digest alone are not permission proof |
| `_day(text)` | Strict canonical `YYYY-MM-DD` calendar date | Rejects ambiguous/invalid dates; assumes declared dates reflect real time |
| `stage_csv_snapshot(data, expected_sha256, max_rows)` | Bytes -> staged immutable observations after hash, UTF-8, exact schema and row checks | 1 MiB and 10,000-row default caps, no duplicate observation day **within a series**, no negative/bool/float counts, no publication before event |
| `available_as_of(snapshot, series_id, origin_on)` | Returns only existing rows for one series with **both** observed and declared available dates at or before origin | Returns empty when no rows eligible (not fabricated zeros); **raw internal data** must not be exposed to unauthorized users |

The strict CSV header is:

```text
series_id,observed_on,available_on,units
```

The rows are **not** automatically joined, imputed,
resampled, modified, uploaded or retained. Different
series can share a calendar day; the same series/day
cannot be duplicated, even if two records claim different
publication dates. Legitimate historical corrections
must therefore be handled by a separately reviewed
versioned revision mechanism, not silently overwritten.

### SHA-256 is an integrity comparison, not an authorization system

`stage_csv_snapshot` compares bytes against a **caller-supplied**
lowercase hex digest. If that digest was obtained from a separately
verified source or reviewed manifest, it can help detect altered
bytes. If somebody hashes the same untrusted input and submits the
digest with it, **the two matching values establish no external
authenticity**. The module does not verify signatures, dataset cards,
source contracts, licenses or human approval. Do not pass a receipt
directly to a production workflow as an authorized dataset.

The data cap applies to the supplied in-memory bytes; a future
file reader must itself read a bounded amount from a trusted,
permission-approved location rather than unconditionally loading
a huge file before calling this validator.

## Independent local reproduction (invented values only)

This example intentionally computes a digest from the same
**synthetic** fixture merely to exercise the parser; it is
not a source attestation:

```python
from pathlib import Path
from hashlib import sha256
from mirrormind.modules.evidence.snapshots import (
    stage_csv_snapshot, available_as_of,
)

raw = Path("examples/staged-daily-observations.csv").read_bytes()
staged = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
assert staged.receipt()["status"] == "local_structure_checked_not_authorized"
assert staged.receipt()["record_count"] == 4

past = available_as_of(staged, series_id="item-A", origin_on="2025-01-03")
assert [(x.observed_on.isoformat(), x.units) for x in past] == [
    ("2025-01-01", 2),
    ("2025-01-03", 0),
]
```

The January 2 event (4 units) is withheld on January 3
because its stated first publication is January 5.
The January 3 zero remains a *recorded zero*; an
unavailable or missing row would remain **absent**.
The internal return value includes raw observations:
do not render it in public HTTP output or model prompts.

## Reviewed evidence and independent negative paths

| Claim ID | Test selector | What the test cannot prove |
| --- | --- | --- |
| **MM-SNAP-001** | `tests/unit/test_evidence_snapshots.py::test_snapshot_content_hash_and_receipt_are_immutable_and_unverified` | Field immutability and digest equality do not prove source legitimacy or confidentiality |
| **MM-SNAP-002** | `tests/unit/test_evidence_snapshots.py::test_asof_excludes_late_publication_but_keeps_real_zero` | Declared `available_on` may be false or revised by a real publisher |
| **MM-SNAP-003** | `tests/unit/test_evidence_snapshots.py::test_digest_mismatch_fails_before_interpreting_unverified_bytes` | A caller-controlled hash is not an independent trust anchor |
| **MM-SNAP-004** | `tests/integration/test_local_snapshot_flow.py::test_local_example_receipt_and_historical_view_remain_unverified` | A local example does not enforce customer data permissions, retention or tenant isolation |

Additional unit cases reject duplicates, future/invalid
calendars, publication-before-observation, malformed headers,
unknown columns, invalid counts, oversize bytes and row limits.
No test involves real customer data.

```bash
python -m pytest -q tests/unit/test_evidence_snapshots.py
python -m pytest -q tests/integration/test_local_snapshot_flow.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

The commands are reproducibility instructions; CI results
must be inspected before merge. A passing test is not a
licensed dataset approval or a deployed ingestion flow.

## Remaining MM-M1b acceptance work

1. Choose a source and verify its terms, legal permissions,
   collection scope, privacy and deletion/retention review
   **outside a user-provided label**.
2. Record an immutable, trusted dataset manifest plus
   publisher release/availability and revision history;
   reject contradictory claims or missing approval.
3. Add source-specific mapping and a bounded local/remote
   reader with access controls, no credentials in logs.
4. Test as-of availability for each forecast origin and
   reproduce an independently locked empirical holdout.
5. Only then promote the narrowly implemented capability
   from experimental staging to actual authorized ingestion.

**Independent exercise:** reproduce the January 3 view,
change only the January 2 publication to January 2, and
explain the difference. Then alter the bytes while reusing
the old digest: why does the integrity comparison reject?
What if you also replace the expected digest? Explain why
that is still not proof of a real producer's permission or
the observation's accuracy.


## 6. Bounded stream reader (MM-M1b local extension)

A future source-specific adapter should not call
`Path.read_bytes()` on an unbounded file and rely
solely on `stage_csv_snapshot` to reject it
*after the full file has already been loaded*.
The new
[`read_staged_csv`](../../src/mirrormind/modules/evidence/snapshots.py)
accepts a **caller-opened binary stream**, reads at most
`MAX_BYTES + 1` bytes in chunks of at most 65,536 bytes,
then hands the **complete** bytes to the existing parser.

```python
from hashlib import sha256
from pathlib import Path
from mirrormind.modules.evidence.snapshots import read_staged_csv

example = Path("examples/staged-daily-observations.csv")
# Demo only: the hash comes from the same invented fixture.
expected = sha256(example.read_bytes()).hexdigest()
with example.open("rb") as stream:
    staged = read_staged_csv(stream, expected_sha256=expected)
assert staged.receipt()["status"] == "local_structure_checked_not_authorized"
```

The `read_bytes()` call above is **only for the
small, checked-in synthetic fixture used in this
example**. For actual sources, obtain the expected
digest from a separately trusted, reviewed manifest;
never compute it from untrusted bytes and treat
the match as provenance or permission evidence.

### Reader behavior and boundaries

| Input | Result |
| --- | --- |
| A normal short local binary fixture | Same digest and `StagedSnapshot` as the bytes-only parser |
| A cooperative stream returning partial chunks | Continue until genuine EOF; do not mistake a short read for the complete file |
| More than 1 MiB available | Stop after observing the `MAX_BYTES+1` sentinel and refuse before loading the remainder |
| Stream yielding text, non-bytes, or more than the requested chunk | Reject without interpreting content |
| Stream raising `OSError` | Raise a generic `ValueError` without including sensitive path/credential text |
| Valid stream but wrong digest, bad CSV rows or `max_rows` too low | Preserve existing fail-closed parser behavior |

This is **not a file opener**, secure network connector,
sandbox, rate limiter, customer-data authorization system,
or guarantee against arbitrary/malicious Python objects
that violate the stream contract. The caller owns
source selection, file permissions, transport and
lifecycle. The function does not log, persist or
send data to an LLM, WorldKernel or third party.
It is a bounded structural reader, **not a new
implemented Evidence Engine**.

### Additional curated claims

| Claim | Exact test | Limit of evidence |
| --- | --- | --- |
| **MM-STRM-001** | `tests/unit/test_evidence_snapshots.py::test_partial_stream_reads_continue_until_eof_and_do_not_accept_prefix_hash` | Prevents accepting partial bytes as complete from a cooperative stream, but does not authenticate the source |
| **MM-STRM-002** | `tests/unit/test_evidence_snapshots.py::test_bounded_reader_rejects_oversized_stream_before_full_read` | Enforces a local byte ceiling; a custom reader could still allocate outside this function |
| **MM-STRM-003** | `tests/unit/test_evidence_snapshots.py::test_bounded_reader_sanitizes_read_failures` | A generic exception message does not establish an application-wide logging/redaction guarantee |
| **MM-STRM-004** | `tests/integration/test_local_snapshot_flow.py::test_bounded_file_stream_stages_exactly_same_invented_fixture` | Local fixture ingestion has no approved real-data grant, real publication proof or deployed connector |

**Independent exercise:** make a mock stream return
two bytes at a time and confirm the final SHA-256
covers the whole fixture. Then append untrusted
bytes while reusing the original digest, and
predict the mismatch. Finally, explain why these
checks would be insufficient to authorize reading
a customer's file or a Kaggle dataset whose
terms have not been reviewed.
