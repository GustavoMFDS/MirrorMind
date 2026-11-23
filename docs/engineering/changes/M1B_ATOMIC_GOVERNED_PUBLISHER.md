# Change request — M1b atomic local operator-policy gated publication

## Existing behavior and safety gap

The experimental [operator governance](../OPERATOR_GOVERNANCE.md)
and [checkpoint publisher](../LOCAL_CHECKPOINT_PUBLISHER.md) are in
**separate SQLite databases**. Querying policy before committing a
publication permits a key to be revoked between checking and writing.
The old publisher also uses its own caller-supplied static operator roster.

## Goal

Introduce a separate **opt-in, integrated local SQLite database** holding
both the existing signed governance events and signed publication events.
Validate *both histories* and the operator's current enrollment and
expiry within **one BEGIN IMMEDIATE transaction**, then commit a
publication as a single SQLite transaction. Revocation and publication
must have a consistent linearizable order within that database.

The standalone publisher must reject opening this integrated database
so its static-key admission cannot bypass the gated flow. Existing
standalone databases and callers remain unchanged. The feature is
**experimental**, and any receipt's authorization flags remain false.

## Acceptance criteria

- Explicit empty-path creation initializes policy, publication and
  a versioned integration marker atomically; refuse overwrites,
  malformed/mixed schemas, wrong administrator/checkpoint/witness
  public-key rosters or unknown bootstrap witness on reopen.
- Use the existing signed administrator event format for enroll/revoke,
  including two administrator signatures and permanent reused-key/ID
  tombstones. Refuse enrollment of public keys already used for
  administrator, checkpoint or witness roles.
- Reuse the existing signed publication commands/checkpoints/witness
  verifier. Historical signatures remain valid under historical
  operator key material even after operator revocation; **future**
  admissions refuse revoked, expired, mismatched or absent keys.
- Both administrative mutations and publications acquire the same
  SQLite write lock and validate current policy state inside their
  own transaction. A stale expected policy head/revision is rejected.
  Two publication writers with the same expected head cannot both win.
- Tests include deliberately ordered revocation-before-publication,
  parallel race (only serially valid outcomes), revoked writer after
  restart, valid historical read after revocation, rollback on injected
  DB error, key role overlap, corrupted stored history, old coherent
  DB restore and the standalone publisher bypass attempt.
- No live external identity provider, key custody, trusted current
  monotonic head, global anti-equivocation, real source/legal/privacy
  approval, or ingestion. A restored old coherent **integrated**
  database remains undetectable without a trusted independent head.

## Impact map

| Surface | Behavior |
| --- | --- |
| `modules/evidence/atomic_governed_publisher.py` | New single-DB combined schema, writer transactions and guarded admission |
| `modules/evidence/local_checkpoint_publisher.py` | Reject legacy standalone publisher on a guarded integrated DB |
| `modules/evidence/operator_governance.py` | Reuse private local signature/history checks without changing standalone semantics |
| `tests/unit/test_atomic_governed_publisher.py` | Concurrent revocation vs publish, rollback, reopen, overlap, corruption and bypass regressions |
| `docs/engineering/ATOMIC_GOVERNED_PUBLISHER.md` | Threat model, SQL consistency scope, separate external authority |
| API capability ledger, source atlas, evidence, maps, learning, debugging, roadmap | Experimental claims and links only |

## Compatibility and rollback

The existing publisher/review/governance SQLite schemas keep their
format and remain usable in standalone mode, but a new integrated DB
cannot be opened by the legacy standalone publisher: this is an
intentional *fail-closed* boundary. The integrated feature does not
migrate existing databases; integration of real source permissions,
network services or trusted keys is explicitly deferred.

Rollback removes the new opt-in integrated database helper and marker
rejection, leaving existing database users on their unchanged format.
Do not claim local SQLite locking prevents cross-host forks or a
malicious process with file access; source ingestion stays blocked.
