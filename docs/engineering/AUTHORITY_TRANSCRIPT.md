# MM-M1b — offline witness-transcript contract (experimental)

**This is NOT an external checkpoint authority.** The
[offline verifier](../../src/mirrormind/modules/evidence/authority_transcript.py)
checks a bounded *supplied* sequence of signed witness receipts, including
key handoffs and a final [SQLite review head](SQLITE_REVIEW_REGISTRY.md)
comparison. It builds on the
[signed checkpoint format](SIGNED_HEAD_CHECKPOINTS.md) without hosting
keys, a public endpoint, a signed publisher, an append-only service,
live authentication, legal review or source ingestion.

## Two distinct signing responsibilities

An ordinary [signed checkpoint](SIGNED_HEAD_CHECKPOINTS.md) attests
to a particular review packet, intended use, event revision and head.
A `SignedAuthorityReceipt` adds a **witness** signature over the exact
checkpoint fingerprint, prior witness-receipt hash, witness key ID and
key epoch. It uses the separate domain
`mirrormind.review-head-witness.v1`. A witness key ID must not overlap
the checkpoint signer-key IDs. Different Ed25519 keys and delegated
roles are required; possessing the private key is not proof of legal
authority, reviewer identity or currentness.

A `WitnessKeyHandoff` names the old and new witness key IDs, previous
and next epochs, the exact previous witnessed hash and the effective
sequence. **Both** the departing and incoming keys must sign the
domain-separated handoff message
`mirrormind.review-head-witness-handoff.v1`.
A missing, mismatched, duplicate or forged handoff fails. This is an
offline format for a *proposed* rotation; it is not a key-provisioning,
revocation, incident-response or independently governed policy engine.

## Strict, bounded replay and recovery checks

`verify_authority_transcript(...)` requires a tuple of **1–32**
witnessed receipts and an optional bounded tuple of dual-signed
handoffs. It rejects missing publications, a gap, a duplicate sequence,
a bad predecessor digest, non-monotone issue dates, invalid signatures,
review revision regression, a changed head with unchanged revision,
an unchanged head with advanced revision, unannounced key changes,
epoch jumps, unconsumed handoffs and invalid current fences.

Each checkpoint must match the packet and carry a valid signer
signature. Earlier checkpoints are verified at their issue dates;
the *final* checkpoint must still be valid at `checked_on` and its
signature and review state must match one current SQLite snapshot.

The caller must supply **both** the starting fence (sequence, previous
receipt digest, witness identity and epoch) and exact expected ending
sequence/digest. These values and both signer trust maps must come from
an independent administrator, not the data requester, SQLite or a
self-signed payload. The program cannot verify the origin or freshness
of those caller-supplied values. Empty/missing receipts fail closed,
rather than returning a permissive previous result after an outage.
A changed, unavailable or truncated source requires the *complete
missing segment* and valid bridges before continuity can resume.

## Equivocation cannot be solved by a single supplied chain

If two different records for the **same sequence** are included in a
single transcript, the sequence check refuses them. But a hostile
witness can sign two forks and selectively present only one; a valid
single branch and a self-consistent, outdated pair of fences may still
pass. The verifier has no external witnesses, tamper-proof checkpoint
publisher or cross-reader gossip to prove global non-equivocation.

Similarly, a compromised old witness and new witness can both sign a
bogus handoff. This format has no custody, trusted root rotation,
key-compromise recovery or key-revocation mechanism. Those require a
real authority and independently governed current-state publication.
A locally replayed valid transcript with unchanged supplied start/end
fences still passes inside its validity window. These are deliberate
limitations, not success conditions.

The result `AuthorityTranscriptAssessment.receipt()` exposes only
count, final sequence and witness digest, review status and check date.
It always says:

- `status = supplied_authority_transcript_verified_not_live_authority`
- `freshness_status = caller_fences_not_independently_fetched`
- `equivocation_status = only_conflicts_in_supplied_chain_detectable`
- `ingestion_authorized = false`
- `forecast_eligible = false`

The verifier neither reads customer data nor writes a new registry or
makes network requests. Real M5 and UCI access, rights approval,
historical publisher vintages, privacy enforcement and forecasting
remain **NO-GO**.

## Deterministic evidence

[The unit regressions](../../tests/unit/test_authority_transcript.py)
use invented stage data and temporary keys only. They cover valid
witness chains, two-key handoff, revoked final review, missing/duplicate
events, gap and predecessor mismatches, tampering, wrong packet scope,
wrong end fences, expired checkpoints, fail-closed outages and replay
with stale caller-controlled fences.

`MM-AUTH-001` is supported narrowly by
`tests/unit/test_authority_transcript.py::test_contiguous_signed_authority_transcript_and_rotation_are_nonauthorizing`.

`MM-AUTH-002` is supported narrowly by
`tests/unit/test_authority_transcript.py::test_outage_empty_or_incomplete_recovery_transcript_fails_closed`.

`MM-AUTH-003` is supported narrowly by
`tests/unit/test_authority_transcript.py::test_valid_stale_transcript_with_caller_stale_fences_cannot_prove_freshness`.

None demonstrates an operating external authority, currentness,
third-party signature revocation, production authorization or absence
of unseen conflicting publications.

```bash
python -m pytest -q tests/unit/test_authority_transcript.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```

## Operational path deferred

A separately controlled service must administer witness/checkpoint
signers, protected private keys, identities and rotation/revocation;
publish current monotonic heads to independent readers with recovery
and gossip/consistency proofs; maintain a trusted clock and durable,
audited current state; and fail closed on outages. Build, model and
review those responsibilities in separate PRs before connecting any
real data source. A signed transcript is not a license.

## Experimental local publication journal

A separate [local checkpoint publisher](LOCAL_CHECKPOINT_PUBLISHER.md)
can retain externally pre-signed witness receipts and operator-signed
publication commands in a dedicated SQLite journal, with local
transactional CAS. That file is **not** an independent authority, live
witness or externally attested current head. The supplied operator
public keys are not real identity authentication and old coherent
publisher databases can still be restored without an independent
newer head.
