# Change request — M1b volatile, revision-checked review history

## Goal, existing state and why

The [signed review verifier](../SIGNED_SOURCE_REVIEW.md) verifies a
complete chain of Ed25519 review records **when** a caller provides an
independently trusted current head. It does not maintain a history.
Two independent writers may otherwise race with an older local head.

Add an opt-in, **process-local** signed review registry that atomically
appends only when both the expected version and head match. Reject
stale writers and any append after a signed revocation. This teaches
safe compare-and-swap semantics but does not create the missing
external authority, durable historical integrity or ingest access.

## Capability truth

Introduce `local_volatile_review_registry` under **experimental** only.
Leave `evidence_and_rag` and `forecasting` planned, do not add any
API route or promote rights to authorized. An in-process object can
be replaced or restarted and hence cannot establish historical log
freshness independently. There is no automatic `true` permission field.

## Acceptance

- A valid signed event appends exactly once to its matching review
  packet and yields version 1 / a signed head, with no data identifiers
  in its receipt and both permissions false.
- A stale version, stale head, concurrent writer with the same version,
  wrong source or purpose, bad signature or packet metadata collision
  fails without a partial mutation.
- Signed revocation blocks all later writes for the same packet,
  including a later otherwise valid signed approval. Expired approvals
  are recomputed on read, not permanently cached.
- A new object starts empty, proving **rollback after restart remains
  unsolved**. Limit packets and events. Copy supplied public keys.
- Real source rights, source acquisition, reviewer authentication,
  private-key custody, durable clock and append-only persistence
  remain out of scope.

## Impact map

| Surface | Change |
| --- | --- |
| `src/mirrormind/modules/evidence/local_review_registry.py` | New bounded synchronized in-memory append/snapshot |
| `src/mirrormind/modules/evidence/review_decisions.py` | Reused signed-event verification; no changes |
| `src/mirrormind/modules/evidence/intake_review.py` | Reused source packet identity; no changes |
| `tests/unit/test_local_review_registry.py` | Concurrency, tampering, expiry, revocation and restart regressions |
| `api/routes/system.py`, capability ledger and evidence map | Report **experimental** claim only |
| `LOCAL_REVIEW_REGISTRY.md`, system map, atlas, roadmap and learning | Document local trust boundary and missing durable service |
| Persistent storage, signing, credentials, external projects | **No changes** |

## Security, rollback and future milestones

The local RLock serializes only threads within one process; it cannot
coordinate multiple workers, guarantee a trusted time, defend after
process loss, or stop a malicious caller from replacing an entire
registry. A real implementation requires transactional durable storage,
protected reviewer identity and keys, key rotation/revocation, independent
log head publishing with freshness, documented privacy/retention
reviews and independent legal/rights decisions. Reusing a local head
after restart **cannot** be represented as a valid trust anchor.

Rollback is removal of the isolated in-memory module, its test and
experimental API capability name, with zero migration for existing
formats and no persisted state. A clean exact-SHA gate is required
before merging under the owner's temporary CI exception.
