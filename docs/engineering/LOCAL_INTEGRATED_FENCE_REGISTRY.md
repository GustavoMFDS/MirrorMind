# MM-M1b — separate local signed integrated-fence registry (experimental)

**This is a separate SQLite file, not an independent external authority.**
The [bounded implementation](../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py)
stores an Ed25519 authority-signed, **dual-witness signed**
[combined-state transition chain](INTEGRATED_FENCE_TRANSCRIPT.md)
for **one** [source-review packet](SOURCE_INTAKE_REVIEW.md). The
[governed publication database](ATOMIC_GOVERNED_PUBLISHER.md) remains
untouched; no existing SQLite schema is migrated.

## Local deployment / separation model

Construct `LocalIntegratedFenceRegistry(absolute_path, gate, packet,
trusted_fence_keys=..., trusted_witness_keys=..., create=True)` for an
explicit new **different** absolute local file. It refuses the
publisher's path, unsafe/missing parent, symbolic-link registry path,
re-creation of a present file and unrecognized signing key roles.
Reopen with the same packet, exact trusted public-key roster and
`create=False`. The on-disk version/packet/snapshot/roster marker is
strictly checked on open and during every operation.

This does **not** prove the files reside on separate hardware, under
separate administrators, on independently protected backup infrastructure
or with custody of private signing keys. Both paths may be on the same
host, disk and Windows user account; the independent failure-domain
assumption is an **operational requirement**, not a software claim.
Never bundle real signer private keys with the registry or the project.

The schema uses `signed_transitions(seq, signed_json)` and a
`registry_identity` marker. At most 32 fully signed, canonical,
bounded JSON links are accepted per instance. Each stored link contains
the complete authority-signed combined fence, two witness signatures,
source packet hashes, exact predecessor and declared date; **not**
customer rows. Bootstrap uses authority sequence 0 and all-zero digest
as local conventions, not a signed global genesis.

## Operation contracts and evidence

- `head(checked_on=...)` replays and verifies **every stored**
  authority signature, two distinct witness signatures, source packet
  digests, monotonic policy/publication revisions, identical state heads
  for unchanged revisions, chronological witnesses and exact hash links,
  inside one registry SQLite read transaction. A head receipt reports
  `publication_authorized=false`,
  `ingestion_authorized=false`, `forecast_eligible=false`.
- `append(link, expected_authority_sequence=...,
  expected_fence_sha256=..., checked_on=...)` holds a
  **registry-local** `BEGIN IMMEDIATE` lock, fully replays history,
  checks exact expected current head (CAS), checks the candidate link
  and compares the final signed fence with the **current local
  governed publisher snapshot**. Only then is the complete canonical
  signed record inserted and committed. A duplicate or conflicting
  same-predecessor append is rejected without modifying the journal.
- `compare_local(checked_on=...)` verifies the stored sequence under
  one registry SQLite read transaction and compares its **own**
  signed terminal fence with the signed policy+publication heads in the
  governed publisher's independent SQLite read transaction. Absence of
  a registry head, untrusted signature, expired terminal fence, damaged
  history, unavailable file and head mismatch fail closed.

The two SQLite transactions **do not form one transaction**. If a
publisher commits between the comparison and the registry commit,
`append` can commit a valid but now-behind snapshot; a later
`compare_local` rejects the divergence until a new signed
checkpoint is appended. The registry is never wired into
`publish` as a separate advisory authorization preflight.

## Conditional rollback evidence

A **coherent older copy of the governed publication database alone**
does not match the more recent signed head retained in a separately
intact registry; `compare_local` rejects it. This is a useful
*conditional* local rollback signal, not a guarantee of global
anti-rollback or source-use authority.

Restoring **both** the governed database **and** the separate registry
to compatible signed earlier copies **still passes**. Deleting
the terminal signed link can also reveal only a cryptographically
valid earlier prefix; without a separately preserved latest pin,
local cryptography cannot distinguish intentional truncation from
an older committed head. Replaying valid signed history cannot
establish currentness by itself.

To progress toward trustworthy external currentness, a different
service must protect its own storage, latest head receipt, signer
identity/keys, access control, freshness and forks under a distinct
administrative failure domain and published protocol. None is
implemented here. Absence of live network reads must never be
described as verified independent external authority.

## Regression evidence

Synthetic generated-key cases live in
[`tests/unit/test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py):

| ID | Verified case | Limitation |
| --- | --- | --- |
| MM-FREG-001 | `test_separate_signed_fence_registry_persists_verifiable_heads_after_reopen` | Locally persistent, not separately operated |
| MM-FREG-002 | `test_separate_registry_detects_publisher_only_rollback_but_not_both` | Paired rollback escapes |
| MM-FREG-003 | `test_registry_atomic_cas_refuses_replay_stale_and_bad_predecessor` | CAS is registry-local only |
| MM-FREG-004 | `test_registry_concurrent_same_head_only_one_signed_successor_commits` | Locks cover just the registry file |
| MM-FREG-005 | `test_separate_registry_replay_catches_corruption_missing_link_and_bad_roster` | Old valid prefix still possible |
| MM-FREG-006 | `test_separate_registry_rejects_missing_recreate_alias_and_expiry` | No remote high availability or protected clock |
| MM-FREG-007 | `test_separate_registry_rejects_missed_publisher_update_until_refenced` | A later publish can race a registry comparison |

The module is `experimental` in `GET /v1/capabilities`.
No UCI/M5 rows, real provenance/license approvals, user identities,
private production keys or numeric forecast results are supplied.

```bash
python -m pytest -q tests/unit/test_atomic_governed_publisher.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

[Change request](changes/M1B_SEPARATE_DURABLE_FENCE_REGISTRY.md)
documents scope, acceptance, non-goals and rollback path.
