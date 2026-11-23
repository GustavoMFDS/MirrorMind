# M1b — local operator-signed checkpoint publisher (experimental)

**No external checkpoint authority is deployed.** The
[publication registry](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py)
is a local, operator-key-gated SQLite journal *separate from* the
[review decision registry](SQLITE_REVIEW_REGISTRY.md). It extends
the [witness transcript contract](AUTHORITY_TRANSCRIPT.md) by storing
publication records in a local transaction, but it is **not** an
independently administered identity service, source permission or
trustworthy monotonic witness.

## Three separate signatures

A publication request contains:
1. The existing Ed25519-signed [source-review checkpoint](SIGNED_HEAD_CHECKPOINTS.md)
   for one exact manifest, source digest, intended use, review head,
   revision and numbered publication.
2. The existing witness signature over the checkpoint fingerprint,
   predecessor publication digest and witness key epoch. When changing
   witness keys, a handoff must bear **both** the old and new signatures.
3. A **different authorized publishing operator's signature** over a
   canonical domain-separated record
   (`mirrormind.local-checkpoint-publication.v1`) binding the entire
   signed witness receipt, any signed handoff, the operator key ID, and
   the expected previous sequence and digest.

All three Ed25519 *public* key maps are supplied separately at startup.
Their key IDs must not overlap. The library never creates or accepts
private signing keys in its runtime API and cannot determine whether
the supplied operator key belongs to a human or trustworthy service.
The "operator role" is just membership in a caller-configured public
key map, not remote authentication, two-factor login or real-world
permission to publish legal decisions.

## Transactions, restarts and recovery

`LocalCheckpointPublisher(absolute_path, checkpoint_keys=...,
witness_keys=..., operator_keys=..., initial_witness_key_id=...,
create=True)` creates a new dedicated SQLite schema-v1 journal only
if the path is unoccupied. `create=False` reopens an existing
schema; the bootstrap witness ID cannot silently change.

`publish(packet, signed_command, expected_sequence=...,
expected_receipt_sha256=..., checked_on=...)` uses SQLite
`BEGIN IMMEDIATE`, fully re-verifies the stored publication chain,
compares caller version/head, checks all signatures and role membership,
then atomically commits the new signed publication and head. Two
writers contending for the same version in one local database yield
one winner; the losing writer receives a stale-state error.

It refuses missing predecessors, duplicate sequence, non-forward
review revision/head pairs, malformed metadata, incorrect witness
handoffs, altered operator signatures, signature changes on disk,
missing publication rows and change to source identity. Readers
`snapshot(...)` fully replay the persisted signed chain and expose
whether the **latest** checkpoint is expired for the caller's date.
At most 16 packet histories and 32 publications per history are
accepted. An injected SQL update abort rolls back both row and head.

The database **contains** signed metadata, opaque key IDs,
authorization records and declared source identifiers — although the
public revision receipt exposes none of these. Filesystem ACLs,
encryption at rest, review access policies, backup retention and
incident response are not implemented in this module.

## What remains untrusted

This is **local, single-database transactionality**, not a globally
monotonic or externally witnessed current head. Replacing the
database with an older coherent copy can restore a valid earlier
publication. The optional `externally_expected_head_sha256` snapshot
comparison catches this **only if** supplied by an independently
trusted, newer source; this module does not provide one.

A compromised operator with authorized signing keys, a compromised
witness, a malicious local filesystem administrator, or dishonest
issuance on different hosts can still create forks. No independent
identity, secure signing/key rotation, revocation, quorum, witness
gossip, trusted time, production endpoint, durable cross-host
anti-equivocation or source legal approval exists. The review database
is **not** automatically synchronized with this journal. No source
acquisition or real M5/UCI ingestion is attempted.

All `LocalPublicationRevision.receipt()` values continue to say:

- `status = local_operator_signed_publication_not_external_authority`
- `freshness_status = local_database_not_independently_attested`
- `operator_status = supplied_public_key_role_only_not_real_identity`
- `ingestion_authorized = false`
- `forecast_eligible = false`

These do not certify trusted provenance, verified reviewer identity,
compliant licensing/privacy, historical publication vintages or an
operational Evidence Engine.

## Unit reproduction

The [fictional publisher tests](../../tests/unit/test_local_checkpoint_publisher.py)
use disposable signing keys and synthetic data to cover:
signed admission and restart, explicit dual-signed witness rotation,
two concurrent SQLite connections, stale/altered operator or checkpoint
signatures, wrong scopes, injected mid-transaction failure, truncated
and tampered stored records, restored old SQLite, changed key maps
and bounds.

Evidence `MM-PUBLISH-001`:
`tests/unit/test_local_checkpoint_publisher.py::test_publisher_reopens_verified_signed_head_and_never_grants_ingestion`.

Evidence `MM-PUBLISH-002`:
`tests/unit/test_local_checkpoint_publisher.py::test_competing_independent_connections_yield_only_one_winner`.

Evidence `MM-PUBLISH-003`:
`tests/unit/test_local_checkpoint_publisher.py::test_old_coherent_publisher_db_is_not_independently_fresh`.

The tests verify a **local fictional protocol**, not a real
identity provider, globally witnessed append-only service, independent
head custody or legally authorized dataset use.

```bash
python -m pytest -q tests/unit/test_local_checkpoint_publisher.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```

## Separate experimental operator-key governance — not enforced here

The [dual-admin key-policy registry](OPERATOR_GOVERNANCE.md) can store
fictional signed operator enrollment, expiry, revocation and new-key
replacement in a **different** SQLite database. The publisher's
preexisting static `operator_keys` map has **not** been connected to
that policy. A policy check followed by a separate publisher transaction
would introduce a time-of-check/time-of-use race. No effective
publication admission or revocation protection is claimed; a future
single-transaction and independently governed design is required.

## Optional integrated single-database gate (experimental)

The [atomic policy-gated publication experiment](ATOMIC_GOVERNED_PUBLISHER.md)
uses a **new combined SQLite file** to place current dual-admin operator
policy validation and the signed publication write under one transaction.
This standalone publisher intentionally **rejects the combined marker**:
its static-key path cannot be used to bypass governed admission in
that database. Old separate publisher databases remain compatible and
are not automatically governed. This is still local-only, not external
operator identity, fresh witness currentness or licensed-source access.
