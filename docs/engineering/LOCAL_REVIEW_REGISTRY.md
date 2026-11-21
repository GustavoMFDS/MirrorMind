# M1b — local compare-and-swap review registry (experimental)

The [in-memory registry](../../src/mirrormind/modules/evidence/local_review_registry.py)
holds a bounded, per-packet signed decision history for the duration of one
Python process. It extends [the offline signed history verifier](SIGNED_SOURCE_REVIEW.md)
without providing source authorization, durable storage, independent trust
anchors, a protected key registry, a reviewer identity service or legal approval.
**Never treat its history snapshots as production permission tokens.**

## Review writer contract

`LocalReviewRegistry(trusted_reviewer_keys)` copies a caller-provisioned
mapping of Ed25519 public keys. Those keys **must** come from the review
authority, not the intake requester. The registry does not authenticate
the caller's identity, verify the authority behind the keys, or guarantee
the keys were independently provisioned.

`snapshot(packet, checked_on=...)` returns an immutable revision, signed
log head, review status and explicit refusal to grant ingestion. With no
events, the version is `0`, the head is 64 zeroes and the status is
`missing_review_record`.

`append(packet, signed_event, expected_revision=..., expected_head_sha256=...,
checked_on=...)` acquires a per-process lock and **atomically** checks the
expected previous revision and head. It rejects a stale writer, wrong
packet/use/snapshot, invalid signature, duplicate/invalid signed sequence,
events exceeding the budget or an attempt to append anything after a
revocation. It verifies the entire proposed event chain before committing
the next local version. A failed append must not alter any state.

The registry permits at most **32 packet histories**, each with at most
**64 signed events**. Histories are isolated by their declared manifest
fingerprint, and a collision on that digest with different packet metadata
fails closed. The values are deliberately not serialized to disk or sent
over the network.

A signed approval may be followed by an independent signed denial,
and the registry evaluates expiration at each new read. Revocations of a
packet are terminal in this in-memory registry; attempts to reapprove or
append after one are rejected.

## What rollback protection actually means

The CAS rule protects one **live** registry instance against two writers
racing with the same old revision. It is **not** durability, a
tamper-resistant append-only log, anti-replay after a restart, multi-worker
coordination, or a monotonic externally attested head. A new instance
starts from `0` and has no way to prove which old signed events existed
in a previous instance. A malicious or incorrectly configured caller
controlling the trusted public keys and head can still spoof a history.
The host-supplied `checked_on` clock is not a trusted timestamp.

A future real registry needs protected durable storage with atomic
transactions, independent reviewer authentication and key custody,
key-revocation/rotation, a separately published monotonic head, recovery
and rollback tests across process crashes and machines, privacy
clearance, and human approval before a source-specific adapter is ever
enabled. The current M1b real-data gate remains **NO-GO**.

## Privacy, source rights and receipts

The returned `LocalReviewRevision.receipt()` contains **only** revision,
head, status and review date, without raw rows or source/reviewer IDs.
Every outcome unconditionally includes:

- `ingestion_authorized = false`
- `forecast_eligible = false`
- `head_trust_status = local_not_independently_attested`
- `persistence_status = process_memory_only_lost_on_restart`

A valid signature does not authenticate licensing, publisher vintage,
source provenance, reviewer authority, retention compliance or safe
use of personal data. Only fictional inputs and disposable test keys
are included.

## Tests

[Unit regressions](../../tests/unit/test_local_review_registry.py)
cover signed optimistic concurrency, a real two-writer race, stale
head/version rejection, exact packet and requested-use binding, forged
signatures without partial writes, revocation, expiry, separate packet
histories, bounded storage, caller key mutation and **loss of local
history after restart**.

Run:

```bash
python -m pytest -q tests/unit/test_local_review_registry.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```

Evidence **MM-REGISTRY-001**:
`tests/unit/test_local_review_registry.py::test_revocation_is_terminal_and_old_head_cannot_rewrite_current_state`.
Evidence **MM-REGISTRY-002**:
`tests/unit/test_local_review_registry.py::test_second_same_revision_writer_loses_atomic_compare_and_swap`.
Neither test establishes a durable review authority, an actual legal
permission grant or historical data availability.
