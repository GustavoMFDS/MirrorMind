# Change request — MM-M1b durable local SQLite review store

## 1. Intent and current boundary

The [in-process registry](../LOCAL_REVIEW_REGISTRY.md) validates
signed review sequences and serializes competing threads with a
revision/head compare-and-swap, but loses every review decision on
restart. The [offline verifier](../SIGNED_SOURCE_REVIEW.md) requires
an independently trusted current head it does not produce.

Add a **local, versioned SQLite transaction store** for the same
signed reviewer metadata and packet identities. It must persist
approval, denial and terminal revocation after restart, coordinate
different interpreter processes using atomic transactions, and
fail closed on partial writes and corrupt histories. **It must not**
enable real ingestion or mistake local persistence for independent
trusted history freshness.

## 2. Acceptance and security

- Explicit new-path creation and schema 1; never silently replace
  an existing database or repair a malformed schema.
- Persist only bounded source manifest metadata, signed review events,
  and head/version; never original source rows or signing private keys.
- On every read, validate packet binding, signed chain, sequence
  continuity, expected internal head and expiry/revocation.
- On append, atomically check expected version and head under SQLite
  `BEGIN IMMEDIATE`; verify the entire proposed signed chain and
  commit event plus head **together**.
- Competing SQLite connections and two different Python interpreters
  must yield exactly one winning same-revision writer.
- A simulated write failure after event insertion must leave neither
  packet/head nor event persisted (transaction rollback).
- Demonstrate that a restored older but valid database is detectable
  **only when** independently retained new head is supplied.
- Every receipt must keep `ingestion_authorized=false` and
  `forecast_eligible=false`, without source/reviewer identifiers.

## 3. Impact map

| Layer | Change |
| --- | --- |
| `modules/evidence/sqlite_review_registry.py` | New bounded SQLite schema v1, read validation and transactional signed CAS |
| `modules/evidence/review_decisions.py` | Reused signature/chain verifier; unchanged |
| `modules/evidence/intake_review.py` | Reused manifest binding; unchanged |
| `tests/unit/test_sqlite_review_registry.py` | Reopen/revoke, corrupt history, rollback, multi-process/connection races |
| `api/routes/system.py` and `CAPABILITY_LEDGER.json` | **Experimental** local persistent registry name only |
| `SQLITE_REVIEW_REGISTRY.md`, atlas, maps, roadmap, learning | State current claims and missing independent trust |
| External authority, real source connectors and authorization routes | **No implementation and no promotion** |

## 4. Risks, migration and rollback

Local SQLite transactions do not prevent a system owner from restoring
an older coherent database. Independently published monotonic current
head and protected reviewer identity and key custody, key revocation,
recovery policy, privacy/rights review and approved dataset cards are
required before any real usage. The caller must control DB location
and access; this module does not provide OS-level credentials, process
isolation, trusted time or tamper-resistant storage.

The new schema is isolated and opt-in: existing local volatile
registry and CSV/XLSX staging APIs are unchanged. Rollback removes
this experimental module and capability from the API; no production
state migration is implied. A clean exact-head local QA gate is
required before merge (temporary owner-approved Actions alternative).
