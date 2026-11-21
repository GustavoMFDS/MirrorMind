# MM-M1b — local transactional review registry (experimental)

**This is not an approval service.** The [SQLite source](../../src/mirrormind/modules/evidence/sqlite_review_registry.py)
persists fictional, Ed25519-signed review decisions across interpreter and
process restarts. Unlike the [volatile registry](LOCAL_REVIEW_REGISTRY.md),
it provides a local transactional CAS and a recoverable signed history in a
single SQLite database. It still cannot certify source rights, reviewer
identity, an authenticated current registry head, publisher publication
vintages, or a permitted ingestion operation.

## Storage and update contract

`SQLiteReviewRegistry(absolute_db_path, trusted_reviewer_keys, create=True)`
creates a new database **only if the path does not already exist**.
`create=False` requires an existing schema version 1. The caller selects
a locally controlled directory; there is no path supplied by an HTTP user,
no file acquisition and no private signing key stored in the database.

The database stores metadata for at most **32 source packet manifests**
and **64 signed events per manifest**. Metadata includes the exact
manifest and snapshot SHA-256, declared source/use and dates, and opaque
review event/key reference IDs; these *are stored on disk* even though
receipts omit them. It never stores original CSV/XLSX rows, customer,
invoice, source evidence documents or private keys.

`snapshot(packet, checked_on=...)` reads the complete persisted
sequence, checks contiguous sequence numbers, the source packet
identity, the stored revision/head and the **entire** signed chain
with the provided public keys. It recalculates denial, expiry and
revocation at the requested date. Modified signatures, missing events
and forged packet metadata fail closed.

`append(packet, event, expected_revision=..., expected_head_sha256=...,
checked_on=...)` uses SQLite `BEGIN IMMEDIATE`. It checks the previous
revision/head, verifies the signed complete proposed history, and then
atomically inserts the signed event and updates the packet head. A
failed write rolls back all changes. A second concurrent interpreter
using the same stale revision must lose rather than overwrite the first.
No new events may follow a signed revocation of that packet.

The SQLite database runs with synchronous writes enabled. Normal
transaction recovery protects against interrupted *local* writes, but
it is not a backup, integrity-preserving hardware device, immutable
log or cross-device replication mechanism. Storage location, filesystem
permissions, disk protection, backup policy and operational identity
controls are outside this component.

## The rollback and independent authority gap

**An internally valid older database can still be restored by an actor
with local file access.** A trusted caller may supply
`externally_expected_head_sha256` when taking a snapshot, in which
case an older database whose head differs is rejected. This comparison
is effective against such rollback **only if** the latest hash comes
from a genuinely independent, fresh, trusted and non-rollbackable
source. This implementation **does not provide that source**.
Without it, a signed, older database can appear internally consistent.

The caller also supplies reviewer public keys, wall-clock date and
access to the database. Neither signature validity nor SQLite
transactionality establishes legal reviewer authority, privacy
clearance, source licensing or first-publication time. There are no
reviewer login/role checks, trusted clock, managed signing service,
key rotation/revocation, remote attestation, verified source
dataset card, or production endpoints in this feature. It is not
safe to treat a locally supplied head or public key as a trust root.

## No data usage grant

`SQLiteReviewRevision.receipt()` contains only revision, head,
review status and checked date. It always reports:

- `status = local_sqlite_signed_review_not_ingestion_authorization`
- `persistence_status = local_sqlite_transactional_not_tamper_proof`
- `head_trust_status = database_head_not_externally_attested`
- `ingestion_authorized = false`
- `forecast_eligible = false`

Even a correctly signed, unexpired approval does not authorize
M5/UCI ingestion or forecasting. This is explicitly a **separate
experimental capability**, and the parent `evidence_and_rag` and
`forecasting` capabilities remain planned.

## Deterministic regression evidence

[Unit tests](../../tests/unit/test_sqlite_review_registry.py) cover:

- Reopening the same database after a restart and preserving a signed
  approval plus an irrevocable same-packet revocation
- Two separate SQLite connections racing for the same CAS revision
- Two separate **Python interpreters** racing for that same revision
- An injected SQL trigger failure between event insertion and head
  update: both changes must roll back
- Corrupt or truncated event history, altered signatures, wrong
  public key, packet purpose mismatch, storage limits and expired dates
- Restoring an older valid copy of the database: undetected **without**
  a trusted external head, detected when the newer head is supplied

The tests use only invented, bounded rows and ephemeral signer keys.
No real data source, private key or external registry is accessed.

```bash
python -m pytest -q tests/unit/test_sqlite_review_registry.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```

Evidence claims `MM-DBREG-001` (restart/revocation),
`MM-DBREG-002` (independent-interpreter CAS), and `MM-DBREG-003`
(transaction rollback) refer to named tests above. None proves
third-party rights, independent monotonic log custody, hardware
durability, real-world process security or production readiness.
