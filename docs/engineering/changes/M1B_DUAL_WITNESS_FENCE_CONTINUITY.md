# MM-M1b — dual-witness signed integrated-fence continuity

## Current behavior and desired outcome
PR #47 added an offline signed exact-head comparison
[`integrated_head_fence.py`](../../../src/mirrormind/modules/evidence/integrated_head_fence.py),
but a single independently supplied fence does not show how its sequence
continues from a previously pinned fence, or expose a pair of competing
signed successors when both are handed to the verifier.

Implement **bounded offline dual-witness transition verification**
linking authority-signed combined policy/publication fences. Each signed
transition names an explicit predecessor sequence+digest and has two
different configured witness keys sign the transition in a new domain.
Provide optional **conflict evidence classification** when TWO fully
valid, same-predecessor successors have different signed fence hashes.

## Scope, non-goals and capability
New experimental capability `local_dual_witness_integrated_fence_transcript`
and truthful `/v1/capabilities` entry. No service, live external
authority, identity enrollment, key custody, trusted clock, network,
cross-database transaction, write admission, dynamic key rotation,
automatic fork discovery, authorized source ingestion or forecasting.

Do not alter the v1 offline fence, legacy publication signatures or
SQLite DB schema. Existing consumers remain compatible.

## Acceptance criteria
- Explicit tuple of 1–32 transitions; exact caller-supplied anchor
  sequence + digest and expected current sequence + digest.
- Transitions bind a previously Ed25519-signed source-specific combined
  fence to exact predecessor, next sequence, witness day and a pair of
  alphabetically ordered independent witness IDs. Both witness signatures
  cover an explicitly domain-separated canonical message.
- Validate each authority fence signature, both distinct witness
  signatures, key role separation, packet identity, date boundaries,
  monotonic policy and publication counts, and unchanged hashes when
  the corresponding count is unchanged. No silent gaps, duplicates,
  reverse order, missing head or stale pin acceptance.
- Only the terminal signed fence is compared with the local
  transaction-consistent SQLite snapshot through the PR #47 verifier.
  Older intermediate state equality to old DB snapshots is not claimed.
- Valid old signed chain + stale independently supplied pins can still
  be replayed. Require explicit external current pins; receipt never
  reports any authorization.
- A separately supplied conflicting valid successor is reported as
  **observed conflict, not resolved authority**. No automatic discovery
  or consensus / global non-equivocation assertion.
- Tests exercise good continuity, missing/duplicate/reordered and stale
  anchors, one forged signer/witness, role reuse, date/status invariants,
  fork evidence and non-conflicts, and receipt privacy.

## Confirmed impact map
| Layer | Files | Result |
| --- | --- | --- |
| Core | `src/mirrormind/modules/evidence/integrated_fence_transcript.py` | New offline pure transcript verifier + conflict classifier |
| Existing verifier | `src/mirrormind/modules/evidence/integrated_head_fence.py` | Read-only final fence equality, **unchanged** |
| Local publisher | `src/mirrormind/modules/evidence/atomic_governed_publisher.py` | Existing snapshot only, **unchanged** |
| Tests | `tests/unit/test_atomic_governed_publisher.py` | Generated-key synthetic transcript and tamper/fork cases |
| Public status | `src/mirrormind/api/routes/system.py` | Experimental capability ID only |
| Catalogues | `docs/engineering/CAPABILITY_LEDGER.json`, `EVIDENCE_MAP.json`, `REPOSITORY_ATLAS.md`, generated `SYMBOLS.md` | Explicit claim boundaries |
| Guides | `docs/engineering/INTEGRATED_FENCE_TRANSCRIPT.md`, hub, roadmap, system/debugging/learning, existing fence guide | Trust contract, change and runbook |

## Threat model, risks and rollback
The caller supplies both immutable trust rosters and exact current/anchor
pins. Witness key custody, independent operating parties, external
pin freshness, trusted clock and later snapshots are **not** established.
A colluding authority and witnesses can sign forks; if both are supplied,
the verifier can classify conflict, but it cannot find unseen forks or
select an authentic current branch. A malicious caller could present an
older complete chain and its old pins. The verifier never gates later
writes (separate offline preflight would be TOCTOU). Removing the new
module and status ID needs no SQLite migration. Source permission
reviews and real forecast model cards remain outside scope.
