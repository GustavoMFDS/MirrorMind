# Change request — MM-M1b supplied signed integrated-state fence

## Confirmed gap
The atomic governed publisher replays both local histories in one read
transaction, and operator commands bind their signed intent to the
transaction-local policy epoch. A coherent older SQLite backup remains
cryptographically self-consistent. The existing optional caller-supplied
policy/publication head comparisons carry no signature or trustworthy
latest-sequence proof of their own.

## Goal
Add a bounded, **offline verification-only** signed state fence covering
the exact operator-policy revision/head **and** signed publication
sequence/head for one source-review packet. Compare it to a single
transactional SQLite snapshot. Require the caller to provide the exact
currently expected fence sequence and digest separately from the SQLite
file. A genuinely independent trusted current fence could reveal a
coherent old DB restore; the code does not itself obtain that fence.

## Acceptance
- Domain-separated Ed25519 canonical message binds source declaration
  and snapshot SHA-256, authority signing-key ID, authority sequence,
  both policy and publication counters/heads, issuance and expiry.
- Strict bounded values, distinct supplied trusted public-key material,
  exact expected current sequence and signed-record digest; refuse
  unknown keys, forged signatures, missing or stale fences, expired or
  future-issued attestations, malformed hashes and packet substitution.
- Read policy and publication within one consistent
  `AtomicGovernedPublisher.snapshot` transaction; never write to it.
  Compare **both revisions and heads**, not just latest policy head.
- Test an old coherent combined backup against newer signed fence:
  refuse mismatch; demonstrate that a matching old signed fence with
  a matching old caller-supplied expectation remains locally acceptable.
- The receipt includes only minimal technical metadata and permanently
  reports `publication_authorized=false`,
  `ingestion_authorized=false`, `forecast_eligible=false`.
- Do not connect this offline verifier to live publisher admission,
  ingestion or forecast APIs, or imply source permission approval.
- Keep existing SQLite schema and signed publication formats unchanged.
  Preserve v1/v2 historical replay and all previous tests.

## Impact map
| Surface | Role |
| --- | --- |
| `modules/evidence/integrated_head_fence.py` | New bounded signed offline consistency verifier |
| `api/routes/system.py` | Disclose experimental-only capability ID; no new execution endpoint |
| `tests/unit/test_atomic_governed_publisher.py` | Generated-key signed-fence failure, restore and forgery regressions alongside the integrated publisher fixtures |
| `docs/engineering/INTEGRATED_HEAD_FENCE.md` | Trust model, signed fields, offline usage, limits |
| `docs/engineering/ATOMIC_GOVERNED_PUBLISHER.md` | Reference the opt-in verification boundary |
| `docs/engineering/REPOSITORY_ATLAS.md` | Source, test, guide and change-map link |
| `docs/engineering/EVIDENCE_MAP.json` | Curated test claims/limitations |
| `docs/engineering/CAPABILITY_LEDGER.json` | Experimental-only capability |
| `docs/ROADMAP.md`, docs hub, system/debug/learning | Progress and operational assumptions |
| `docs/engineering/generated/SYMBOLS.md` | Regenerated syntax index |

## Non-goals, risks and rollback
No external signer service, identity attestation, protected custody,
independently fetched latest digest/sequence, secure clock,
anti-equivocation consensus, cross-host locks, legally approved
source use, ingestion, forecasting, or production authorization.
Caller-provided stale trusted keys and current fences can be replayed.
An offline read-only checker cannot atomically gate a later write and
must not be wired into publication as a time-of-check admission.
Removing this module does not migrate or rewrite any existing database.
