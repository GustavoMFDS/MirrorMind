# Change request — M1b witness-continuity and key-handoff contract

## Current behavior, goal and boundaries

The existing [checkpoint verifier](../SIGNED_HEAD_CHECKPOINTS.md)
checks one signed review head and a caller-supplied minimum sequence;
the [SQLite store](../SQLITE_REVIEW_REGISTRY.md) retains the locally
signed decisions. Neither checks a transcript across several
checkpoint publications, source outages or witness signing-key
rotations.

Introduce an **offline bounded verification contract** for supplied,
independently signed witness receipts chained across monotonically
numbered checkpoints and a dual-signed witness-key handoff. The final
receipt must match one validated SQLite review head. This is a
protocol test tool, not a live checkpoint publisher.

## Acceptance and trust assumptions

- Refuse an absent transcript, missing or duplicated sequence,
  incorrect previous hash, malformed metadata, forged signature,
  inconsistent review revision/head and non-monotone issue date.
- Check both review-checkpoint signer and separate witness signer.
  Refuse a silent witness key change or key-epoch jump. A rotation
  requires explicit dual signatures by old and new witness keys
  over the same handoff domain, prior hash and effective sequence.
- Require exact caller-provided starting and ending fences; refuse
  stale/replayed branches **when** independent current fences are
  correctly supplied. Explicitly test that self-consistent old
  transcripts may still pass under old caller-provided fences.
- Refuse missing history segments after outages; don't use the last
  good signature as an automatic approval.
- Recheck the final checkpoint at the supplied evaluation date and
  compare it against a validated SQLite signed review snapshot.
- Keep all receipts identifier-minimized and permission flags false.
  No external signer, protected key store, trust root, authority
  transport, monotonic counter, trusted time, witnessed gossip or
  authorized data use is introduced.

## Impact map and compatibility

| Layer | Change |
| --- | --- |
| `modules/evidence/authority_transcript.py` | New offline bounded witness transcript and dual-key handoff verifier |
| `modules/evidence/head_checkpoints.py` | Reuse exact signed checkpoint verifier and SQLite comparator; no format change |
| `modules/evidence/sqlite_review_registry.py` | Existing local transactional storage, read only; no schema migration |
| `tests/unit/test_authority_transcript.py` | Synthetic full chain, missing event, adversarial signatures, rotation, expiry and replay tests |
| `api/routes/system.py`, capability ledger, evidence map | Experimental method only, with truthful limits |
| `AUTHORITY_TRANSCRIPT.md`, maps, atlas, roadmap, learning, debugging | Explicit protocol semantics and incomplete external authority |
| External network, secrets, private keys, real sources/ingestion | No changes |

## Known risks, rollback and future governance

A signature proves control of a paired private key, not legal authority.
Caller-provided keys and start/end fences cannot certify freshness or
global non-equivocation. A witness may fork the history and hide one
branch; compromised old/new keys may sign an apparently valid handoff.
An unavailable independent authority means fresh permission cannot
be established, so all ingestion and forecast flags stay false.

Rollback removes this standalone component, its tests and
experimental capability claim; no existing source or database contract
changes. Validate all six local quality checks on the exact PR head.
A future separately administered authority must address authenticated
roles, protected key custody and revocation, independent current
publication/gossip, durable monotonic storage, recovery, audit,
source licensing and privacy *before* any operational source use.
