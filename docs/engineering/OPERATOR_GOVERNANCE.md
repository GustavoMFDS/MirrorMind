# M1b — local operator-key governance (experimental)

**No live operator identity service or source-use authorization is implemented.**
The [local policy registry](../../src/mirrormind/modules/evidence/operator_governance.py)
tracks signed **metadata** for publishing-operator key enrollment,
expiry, revocation and replacement. It does **not** automatically change
the configured allowed keys in the
[existing checkpoint publisher](LOCAL_CHECKPOINT_PUBLISHER.md).

## Dual administrative control

Every `SignedOperatorPolicyEvent` is a canonical, domain-separated
Ed25519 record with an action (`enroll` or `revoke`), opaque operator
key ID, exact 32-byte public-key hex, policy sequence, predecessor
head SHA-256, issuance date, optional enrollment expiry and **two
distinct administrator key IDs with two distinct signatures**.

The signing domain is `mirrormind.operator-policy.v1`. The registry is
created with a separately supplied map of 2–8 administrator **public**
keys. Both keys and IDs must be distinct; their canonical roster
fingerprint is bound to SQLite schema version 1 so a reopened local
database cannot silently adopt a different admin roster. This is
an intentionally static *experimental* roster, not admin-key rotation.

The public-key map, dates and database file are all **supplied by the
caller**. Verifying two signatures proves only possession of matching
private keys, not the operator's identity, the administrators' actual
independence, a real authorized role or the origin of the source data.
Neither private keys nor login credentials are handled or persisted
by this code. Public-key *syntax* does not prove a new operator
controls the matching private key.

## Enrollment, revocation and key compromise recovery

`LocalOperatorGovernance(absolute_path, administrator_public_keys=...,
create=True)` creates a dedicated local SQLite database **only at an
unused absolute path**, and `create=False` reopens the same schema
and trusted administrative public-key roster.

`append(signed_event, expected_revision=..., expected_head_sha256=...,
checked_on=...)` uses SQLite `BEGIN IMMEDIATE` to validate the complete
stored policy history and atomically append the signed event plus
updated head. Two writers using the same revision/head cannot both
win. Failed signature checks, replay, duplicate or wrong predecessor,
invalid date, revocation mismatch and SQL failure do not partially
commit.

Enrollment allows at most **32 distinct operator IDs**, each with
a previously unused 32-byte public-key value and an expiry within
365 days. A revocation must refer to a previously enrolled,
not-yet-revoked exact ID/key pairing. Revocation is a permanent local
tombstone: re-enrolling the **same ID or public-key material** is
refused, even with a new ID. The only modeled compromise recovery
is a *new, different operator ID and a newly generated public key*
attested by two administrators. This is not a full real-world
key-compromise, audit or incident-response procedure.

`snapshot(checked_on=...)` reports local revision, head and total
historically registered key count. `assess_operator(key_id, public_key,
checked_on=...)` can report a locally registered, expired, revoked,
unknown or mismatched record. It is **not an admission token**.
A policy database has at most 64 signed events and re-verifies
both administrator signatures for every event on every read.

## The publisher is deliberately NOT connected

The current publication journal accepts a *static* public-key map
supplied when it is instantiated. Reading this policy database before
calling the publisher would be a **time-of-check/time-of-use race**:
the policy could be revoked in one SQLite file while a publication is
committed in another. Separate SQLite transactions provide **no
atomic admission** across these stores.

As a result, an operator record can be revoked *here* while the old
publisher configuration still accepts signatures from that key. The
source code makes no promise of real-time revocation enforcement.
Do not wire the policy to publication without a separate design and
transaction/security review, ideally under an independently
governed authority with a jointly atomic policy + publication state.

## Historical freshness and external rights remain unknown

An internally coherent old SQLite policy backup, including an older
non-revoked enrollment, can be restored and will pass local signature
verification. `externally_expected_head_sha256` can detect that
rollback **only when obtained from a trusted independently current
authority**; none is implemented here. The supplied `checked_on`
is not a secure clock. No multi-host consistency, real key custody,
admin-key replacement, witnessed current head, rights review, privacy
clearance, M5/UCI actual ingestion or forecasting is added.

All `OperatorPolicyRevision.receipt()` and
`OperatorPolicyAssessment.receipt()` results explicitly report
`publication_authorized = false`,
`ingestion_authorized = false`, and `forecast_eligible = false`.
Receipts omit operator/admin IDs, public keys, signed payloads and
original data rows.

## Tests, evidence and reproduction

[Synthetic unit tests](../../tests/unit/test_operator_governance.py)
cover dual-admin enrollment, reopen, revocation tombstones, fresh-key
replacement, expiry, malformed/forged signatures, administrator
overlap, concurrent SQLite connections, injected SQL rollback,
truncated/tampered records and a valid older backup accepted unless
a **newer independently retained head** is supplied.

- `MM-GOV-001`:
  `tests/unit/test_operator_governance.py::test_dual_admin_enrollment_survives_restart_but_never_authorizes`
- `MM-GOV-002`:
  `tests/unit/test_operator_governance.py::test_revocation_is_terminal_and_replacement_needs_fresh_key_and_id`
- `MM-GOV-003`:
  `tests/unit/test_operator_governance.py::test_coherent_old_backup_needs_independent_head_to_detect_revocation_rollback`

These test a bounded **local experimental policy model**, not
trusted identity, live independent administrative controls, legally
authorized ingestion, complete key compromise response, or an
operationally enforced publication policy.

```bash
python -m pytest -q tests/unit/test_operator_governance.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```
