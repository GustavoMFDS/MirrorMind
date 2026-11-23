# Change request — M1b policy-bound signed publication command

## Observed gap

The experimental atomic single-database publisher validates the current
dual-admin policy under the same SQLite transaction as a publication.
However, the operator's v1 signature covers the receipt and publication
predecessor only. The **caller**, not the signed command, supplies the
expected policy revision/head. A command therefore has no cryptographic
declaration of which local policy epoch the operator believed it was
authorizing. This is a narrower defect than the already-resolved local
revocation TOCTOU race.

## Goal and acceptance

- Add optional policy revision/head fields to the canonical
  `SignedPublicationCommand`; both present and strictly validated or
  both absent for legacy v1 history.
- Sign bound commands under a new domain-separated v2 message covering
  exact policy revision, SHA-256 policy head, source receipt and existing
  publication predecessor. Reusing a valid v1 signature for v2 fails.
- New `AtomicGovernedPublisher.publish` writes require a v2 command
  whose signed binding equals the current policy read under
  `BEGIN IMMEDIATE`. An unrelated policy enrollment/change also
  requires a newly signed command, even without operator revocation.
- Keep standalone v1 serializations **byte-for-byte compatible**.
  Integrated database schema stays v1, with no automatic migration.
  Reopening old integrated histories must still verify v1 events;
  fresh integrated writes must reject unbound v1 commands.
- Reject v2 commands from the standalone static-roster publisher,
  which cannot evaluate current operator policy.
- Synthetic regressions cover replay, domain separation, incomplete
  or wrong binding, policy evolution, tampered stored history, v1
  persistence compatibility, standalone refusal, and happy-path v2.
  Preserve existing revocation/concurrent-writer tests.

## Affected surfaces

| Surface | Change |
| --- | --- |
| `src/mirrormind/modules/evidence/local_checkpoint_publisher.py` | Optional v2 signed fields; legacy canonical encoding and explicit standalone refusal |
| `src/mirrormind/modules/evidence/atomic_governed_publisher.py` | Require signed policy revision/head matching transaction-local policy |
| `tests/unit/test_atomic_governed_publisher.py` | Fictional generated-key compatibility and adversarial regressions |
| `docs/engineering/ATOMIC_GOVERNED_PUBLISHER.md` | Precise v1/v2 signature and trust boundary |
| Capability/evidence map, atlas, roadmap, symbol catalog | Trace bounded experimental claim to code and test |

## Non-goals and rollback

No real administrator identities, role authorizer, private-key service,
external currentness/witness quorum, cross-host non-equivocation, source
legal/privacy approval, live M5/UCI ingestion, RAG, or forecasts. A
coherent old integrated SQLite backup plus old signed command remains
locally valid absent an independently trusted newer head. The v2
binding addresses the **operator's signed intent in one policy epoch**,
not global trust.

Rollback can preserve old v1 data and standalone API; new integrated
v2 history requires retaining the v2 verifier. Any downgrade must
refuse opening v2-bearing data rather than silently dropping fields.
No database file or real source record should be bundled with this PR.
