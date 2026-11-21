# Change request — M1b external signed head checkpoint verifier

## Problem and objective

The SQLite signed review registry ([technical guide](../SQLITE_REVIEW_REGISTRY.md))
persists history and can compare its head with a caller-supplied expected
hash, but cannot prove that the supplied hash is independently held or
current. A valid old SQLite copy can look internally consistent.

Add an **optional, offline verifier** for a separately signed,
versioned, packet-scoped head checkpoint and a caller-supplied
monotonic minimum sequence. Compare the signed head and revision
against one validated SQLite review snapshot without exposing source
identifiers or enabling ingestion.

## Acceptance criteria

- A correctly signed domain-separated Ed25519 checkpoint binds the exact
  source manifest and snapshot, intended use, review revision/head,
  issuing signer, sequence and bounded expiry.
- Reject invalid authority keys, unknown key IDs, tampered payload,
  wrong manifest or purpose, invalid dates, old sequence relative to a
  **supplied** high-water, and a mismatch with the SQLite head or version.
- Test restored old SQLite state with newer signed checkpoint and
  reject; also demonstrate old valid checkpoint + old valid SQLite
  **cannot be detected** when high-water is stale.
- Test no-event genesis, signed revocation status, key separation,
  expiry, nonauthorizing sanitized receipts.
- Add no keys, identities, network calls, OAuth, rights evaluation,
  signed checkpoint issuing authority or shared storage.
- All six checks pass in an exact-head clean isolated local gate.

## Impact map

| Area | Change |
| --- | --- |
| `modules/evidence/head_checkpoints.py` | New offline signed checkpoint integrity and SQLite equality checker |
| `modules/evidence/sqlite_review_registry.py` | Reused existing snapshot API and externally expected head; unchanged |
| `modules/evidence/review_decisions.py` | Signature protocol remains separate, unchanged |
| `tests/unit/test_head_checkpoints.py` | Fictional signing, rollback/replay, dates, scope, key and permission tests |
| `api/routes/system.py`, capabilities and evidence | New **experimental** verifier only |
| `SIGNED_HEAD_CHECKPOINTS.md`, atlas, maps, roadmap, debugging, learning | Trust boundary and explicit replay counterexample |
| Signing authority, external monotonic counter, key custody, real data rights | **Not implemented** |

## Risks, rollback and next gate

Cryptographic validity is not freshness. A requester-controlled
public key or `minimum_anchor_sequence` allows old signed checkpoints
to appear acceptable. Even trusted keys need rotation/revocation and
protection against equivocation and dishonest signing.
The application has no independently administered authority to
supply current keys, minimum sequence and head. The caller-supplied
`checked_on` is not a trusted wall clock.

The receipt **always** states `ingestion_authorized=false` and
`forecast_eligible=false`, including on a verified signed approval.
No user or provider rights are inferred. This is an experimental
check, not an operational permission service or producer of new
source evidence.

Rollback removes the isolated verifier, tests and experimental
capability name; the SQLite schema and existing APIs are unchanged.
