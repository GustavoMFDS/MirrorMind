# Change request — M1b local operator-key governance ledger

## Context and goal

The [local checkpoint publisher](../LOCAL_CHECKPOINT_PUBLISHER.md)
accepts signatures based on a **static, caller-provided operator public-key
map**. It cannot model separate administrative enrollment, revocation,
or replacement after a compromised operator key. Its local publication
database is not an independently anchored current-head authority.

Add a **separate** offline, SQLite-backed, bounded governance **experiment**:
two distinct administrator keys must sign any operator enrollment or
revocation, with optimistic version/head concurrency, full-chain
revalidation after restart, irreversible key tombstones and dated
operator enrollment. Maintain the experimental boundary, without
pretending that a database file identifies legal humans or controls
the publisher automatically.

## Scope, acceptance, and threat model

- A domain-separated versioned `SignedOperatorPolicyEvent` binds
  action, operator ID, exact Ed25519 public key, policy sequence,
  predecessor digest, issued date, optional expiry, two distinct
  administrator IDs and both signatures.
- Enrollment requires a previously unseen ID **and** never-before-used
  key material, an expiry no more than one year after enrollment,
  and both admin signatures. Revocation binds the exact enrolled key
  and becomes permanent; replacement requires a **fresh** ID and key.
- A wrong admin, missing second signature, identical admin identity
  or signing key, wrong previous head, old version, duplicate event,
  bad dates or tampered stored chain must fail closed. A failed
  transaction must not partially commit, including on injected SQL
  failure. Cross-connection concurrent writes must produce one winner.
- The schema and configured administrator public-key roster are bound
  on initial creation; opening an existing file cannot change them
  silently. Explicit creation must refuse overwrite. No private
  signing keys or original data rows may be stored.
- `assess_operator` reports only a locally registered/revoked/
  expired/unknown **record status**. It never returns a permission
  token or `publication_authorized=true`.
- Deliberately test a coherent old SQLite backup: local integrity
  alone still permits revocation rollback unless an independently
  trusted newer head is supplied. This module cannot solve key
  compromise of *administrators* or independently verify identity.
- Do NOT wire governance to the existing publisher yet: cross-file
  policy-check + publication writes are **not atomic** and a revoked
  key could race or be replayed. A future single-transaction
  integration or independently authoritative service is required.

## Impact map

| Surface | Change |
| --- | --- |
| `src/mirrormind/modules/evidence/operator_governance.py` | New bounded local policy events, dual-admin verification and SQLite CAS |
| `tests/unit/test_operator_governance.py` | Synthetic enrollment, expiry, revocation, replacement, replay, signatures, concurrent writes and crash rollback |
| `docs/engineering/OPERATOR_GOVERNANCE.md` | Precise local security and missing integration boundary |
| `src/mirrormind/modules/evidence/local_checkpoint_publisher.py` | **No code changes**; static key admission remains a separate experiment |
| `src/mirrormind/api/routes/system.py`, capability ledger and evidence | Experimental label only; not production authorization |
| Atlas, system map, learning, debugging, roadmap and change guide | Links, trust boundaries, limitations |

## Rollback and next decision

Remove the standalone policy ledger and experimental claim; no migration
to the existing review or publisher SQLite schema. Before an
operational integration, independently reviewed controls must address
trusted admin identities, secure key custody, quorum governance,
admin-key rotation/revocation, real-time independent monotonic heads,
cross-database policy/publication atomicity, legal source rights,
privacy approval, publisher timestamps, and actual source permissions.
A source-use grant is always **NO-GO** in this experiment.
