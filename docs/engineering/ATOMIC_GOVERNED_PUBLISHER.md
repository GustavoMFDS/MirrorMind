# M1b — atomic local operator-policy gated checkpoint publication (experimental)

**This is not a real authorization, identity or independently witnessed
checkpoint authority.** The [single-database gate](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py)
combines the prior [dual-admin operator policy](OPERATOR_GOVERNANCE.md)
with the [signed checkpoint publisher](LOCAL_CHECKPOINT_PUBLISHER.md)
in a newly created **single local SQLite database**. The implementation
addresses a *specific* local time-of-check/time-of-use (TOCTOU) race:
the policy check and publication commit share **one**
`BEGIN IMMEDIATE` writer transaction.

## Deployment model: opt-in new database only

`AtomicGovernedPublisher(absolute_path, administrator_public_keys=...,
checkpoint_keys=..., witness_keys=..., initial_witness_key_id=...,
create=True)` creates an isolated schema v1. It contains both the
existing signed governance tables and publication tables, plus an
`atomic_governed_schema` marker binding the independently configured
admin, checkpoint and witness public-key rosters and bootstrap witness.
All initial schema tables are created in **one local transaction**.

No existing governance or publisher database is automatically migrated
or treated as governed. Existing standalone callers keep their previous
behavior for their previous databases. The **standalone**
`LocalCheckpointPublisher` rejects an integrated database with the
marker, instead of taking its static-key route and silently bypassing
the new policy checks. The gate uses a verification-only internal
helper to replay the prior publication signature/chain format; that
helper cannot submit an independent publication.

The integrated database stores signed policy/publication metadata,
opaque operator/source IDs and public keys, not raw CSV/XLSX rows,
customer/invoice payloads or signer private keys. The code cannot
protect the database from malicious filesystem owners, independently
authenticate key ownership or guarantee key custody.

## Policy changes and atomic admission

`append_policy(signed_event, expected_policy_revision=...,
expected_policy_head_sha256=..., checked_on=...)` performs the same
two-administrator signed enrollment/revocation checks as before,
inside the integrated database's SQLite write transaction. An
operator cannot be enrolled under an administrator, checkpoint or
witness key ID **or exact public-key material**. Revoked key IDs
and key material remain unusable for new enrollment.

`publish(packet, signed_command, expected_policy_revision=...,
expected_policy_head_sha256=...,
expected_publication_sequence=...,
expected_publication_head_sha256=..., checked_on=...)`
begins **one `BEGIN IMMEDIATE` transaction**, then:

1. Re-verifies the entire dual-signed operator policy chain and
   its current revision/head, refusing stale policy expectations.
2. Checks that the command's exact operator ID is enrolled,
   not revoked and not expired at `checked_on`. Unknown or
   role-conflicting public keys fail closed.
3. Re-verifies *historical* signed publication records using the
   exact keys originally enrolled, even when those keys are
   currently revoked. Old legitimate signatures do not disappear.
4. Rechecks the expected publication sequence/head, checkpoint,
   witness signature, operator signature, signed source/use scope,
   predecessor links and checkpoint expiry.
5. Commits the new signed publication record and head **atomically**,
   or rolls back everything on any error.

If revocation commits **first**, publication sees a changed policy
version or a revoked record and refuses. If publication commits
**first**, that publication is ordered *before* revocation and
may legitimately complete; any later publication by the revoked key
is denied. This is the correct scope of serialization. It is not
a promise to erase previously committed publications.

`snapshot(packet, checked_on=...)` re-verifies both histories in
one SQLite read transaction, returning sanitized policy and
publication heads and revisions. Optional independently supplied
policy/publication heads may reveal rollback when they really
are maintained by a separate, trusted current authority.

## Limits and unimplemented trust boundaries

This is an **experimental local-only** SQL atomicity guarantee.
Existing standalone publishers using **other databases** still
operate under their old static-key policy. The integrated API is
the only local code path in this PR that promises to check current
policy inside the publishing transaction. Direct external modification
of SQLite files, unpublished forks, maliciously provided keys, and
restoring an older **coherent combined database** can defeat
current-state freshness. The code does not supply an authenticated
current monotonic head, real administrator identity, secure private
key custody, admin rotation or cross-host witness consensus.

The operator-signed existing command is bound to the publication
sequence and predecessor receipt hash. The integrated **call**
supplies the expected policy revision and head, which are checked
atomically but **not separately part of that signature**; the policy
revocation itself is enforced from the current stored policy state.
A more complete production authority may require a separately
policy-bound command and reviewed identity/role governance.

Most importantly: no actual M5 or UCI source access, data-rights
review, source vintage, privacy approval, product forecasting or
ingestion has been implemented. `AtomicGovernedRevision.receipt()`
always includes:

- `status = single_database_policy_publication_not_external_authority`
- `atomicity_status = one_local_sqlite_begin_immediate_transaction`
- `external_freshness_status = not_independently_attested`
- `operator_identity_status = signed_keys_only_no_real_identity`
- `publication_authorized = false`
- `ingestion_authorized = false`
- `forecast_eligible = false`

These fields deliberately distinguish experimental *local policy
admission for signed metadata* from real-world authorization.

## Regression evidence and reproduction

[The synthetic tests](../../tests/unit/test_atomic_governed_publisher.py)
cover current signed enrollment, accurate historical verification
after revocation, denial after revocation, **a real two-thread race**
between revocation and publication, concurrent publication conflicts,
standalone bypass refusal on the guarded DB, role/signature forgery,
expiry, SQLite injected failure rollback for both kinds of writes,
reopen and corrupted policy, and an older **internally coherent**
restored database that remains acceptable absent an independently
newer policy head.

- `MM-ATOMIC-001`:
  `tests/unit/test_atomic_governed_publisher.py::test_revocation_before_publication_is_terminal_and_history_still_verifies`
- `MM-ATOMIC-002`:
  `tests/unit/test_atomic_governed_publisher.py::test_publication_and_revocation_race_only_admits_if_publication_commits_first`
- `MM-ATOMIC-003`:
  `tests/unit/test_atomic_governed_publisher.py::test_standalone_static_roster_publisher_cannot_open_guarded_schema`
- `MM-ATOMIC-004`:
  `tests/unit/test_atomic_governed_publisher.py::test_restored_valid_old_integrated_db_needs_independent_head_for_rollback`

No test proves production authentication, independent currentness,
legal source permissions, tamper-resistant storage or real-world
ingestion. The existing separate review-source SQLite is also **not**
atomically tied to publication: even the integrated policy+publisher
does not grant source or forecast rights.

```bash
python -m pytest -q tests/unit/test_atomic_governed_publisher.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```
