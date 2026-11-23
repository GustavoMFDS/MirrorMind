# MM-M1b — signed external review-head checkpoints (experimental)

A signed checkpoint can bind a source review packet to a precise SQLite
review-history revision and signed head **without itself proving freshness,
reviewer identity, legal rights or source ingestion permission**. The
[offline verifier](../../src/mirrormind/modules/evidence/head_checkpoints.py)
is a narrowly scoped experiment building on the [SQLite review store](SQLITE_REVIEW_REGISTRY.md).
It neither contacts nor implements any external authority.

## Checkpoint signer and fields

`SignedReviewHeadCheckpoint` contains an opaque `anchor_key_id`, exact
packet-manifest and staged-source SHA-256 hashes, format and intended use,
review-history revision and hash, a positive `anchor_sequence`, an
`issued_on` date, an `expires_on` date no more than 30 days later,
and a hex-encoded Ed25519 signature.

The signed message is canonical JSON with domain string
`mirrormind.review-head-checkpoint.v1`. Its key is a **different role**
from the signer of ordinary review decisions. Private signing keys are
never generated, persisted or used in production code; tests use
disposable private keys in memory only.

The verification caller must obtain the signed checkpoint, a trusted
anchor-public-key registry and a monotonic **minimum anchor sequence**
from independently governed sources. These values cannot safely come
from the intake requester, the SQLite database, a self-signed payload,
or a stale cache. This project does not yet implement the authority,
its key custody, authenticated signer identity, monotonic sequence
publication or the transport needed to fetch an authoritative current
checkpoint.

## Exact verification behavior

`verify_signed_head_checkpoint(...)` refuses invalid key metadata,
unknown keys, signature forgery, changed packet, source kind or intended
use, revision/head mismatch at genesis, invalid date ranges, expiry,
and a signed checkpoint whose sequence is below the **caller-provided**
minimum. The signature is domain-separated from the ordinary signed
review event format.

`compare_sqlite_to_signed_checkpoint(...)` then invokes the existing
SQLite snapshot verification with the exact *signed* head and additionally
compares the signed revision. A local history that has been truncated,
modified or restored to an older head is rejected **when** a genuinely
current signed checkpoint is supplied.

The `minimum_anchor_sequence` is a *caller assertion*, not a live
monotonic counter maintained here. A valid older signature presented
with a stale minimum **still passes** when the SQLite database also
matches that older version. Expiry alone is a bounded lifetime, not
proof of the newest checkpoint or defense against same-period replay.
It is still possible for a dishonest or compromised authority to sign
two conflicting heads with the same sequence; only independent
sequencing, access control and externally retained current state can
address that.

## Security limitations and output

`CheckpointComparison.receipt()` reports local review revision,
head and status, signed anchor sequence and evaluation date. It does
not expose source/customer/reviewer identifiers or trusted key strings.
Every receipt unconditionally reports:

- `status = signed_checkpoint_matches_local_review_not_authorization`
- `signature_status = valid_against_supplied_anchor_key_not_identity_proof`
- `freshness_status = caller_supplied_high_water_not_independently_checked`
- `ingestion_authorized = false`
- `forecast_eligible = false`

A valid checkpoint can correspond to a signed revocation, denial or
expired approval. Checkpoint verification does not promote any of
those states to permission. It does not authenticate real source
ownership, licensing, privacy status, publisher historical availability,
keys, clocks or reviewer legal authority.

This feature intentionally **does not** implement a second persistent
local file that pretends to be an independent trust root. The
next operational milestone requires a separately administered,
monotonically advancing and externally readable authority with
authenticated credentials, protected signing keys, key-revocation
and anti-equivocation policies, and witnessed current-head values.
Only after separate lawful-source review could real-source ingestion
be reconsidered in a future change request.

## Verification and evidence

[The synthetic test module](../../tests/unit/test_head_checkpoints.py)
covers exact signatures, source/use binding, signed revocation status,
reverted SQLite file, stale minimum replay, wrong key, altered
signature, domain separation, expiry, and zero-event genesis.

- `MM-ANCHOR-001`:
  `tests/unit/test_head_checkpoints.py::test_restored_older_sqlite_is_rejected_against_newer_independent_signed_head`.
- `MM-ANCHOR-002`:
  `tests/unit/test_head_checkpoints.py::test_older_valid_checkpoint_replay_is_not_prevented_if_high_water_is_stale`.

These demonstrate a *conditional local property* of signatures and
SQLite equality checks only. No live independent key service, head
freshness guarantee, real customer data or authorized ingest is
tested or implied.

```bash
python -m pytest -q tests/unit/test_head_checkpoints.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```

## Optional witnessed succession (experimental)

The [offline authority transcript](AUTHORITY_TRANSCRIPT.md) checks
multiple signed checkpoints carried in a hash-linked witness chain,
with explicit old/new witness-key signatures on rotations. This
validates only a *supplied* chain between caller-provided fences; it
does not supply trusted currentness, an independent publisher, protection
against unseen forks or data-use permissions.
