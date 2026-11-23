# M1b — supplied signed integrated-head fence (offline, experimental)

**No independent latest-state authority is operated by MirrorMind.**
The [offline verifier](../../src/mirrormind/modules/evidence/integrated_head_fence.py)
checks a caller-supplied Ed25519-signed fence for an
[atomic governed SQLite database](ATOMIC_GOVERNED_PUBLISHER.md).
It provides a *conditional* backup-rollback diagnostic when the signer
public keys and **exact latest fence sequence and digest** truly arrive
from an independently trustworthy source. It cannot itself fetch,
operate or certify that source.

## What exactly is signed?

A `SignedIntegratedHeadFence` uses the distinct canonical JSON
signing domain `mirrormind.integrated-head-fence.v1` and covers:

| Field | Bound meaning |
| --- | --- |
| `authority_key_id`, `authority_sequence` | Claimed signing role and monotonic fence number (1..1e9) |
| `packet_sha256`, `snapshot_sha256` | Specific source-review declaration and staged snapshot |
| `policy_revision`, `policy_head_sha256` | Signed local dual-admin operator-policy state |
| `publication_sequence`, `publication_head_sha256` | Signed checkpoint-publication state for the same packet |
| `issued_on`, `expires_on` | Caller-reported signing dates; validity at most 30 calendar days |

The Ed25519 signature covers every field above. The fence digest is
SHA-256 of the canonical signing message **followed by signature bytes**,
so independently issued signed forks with the same sequence can have
different pinned digests.

The independent reference is **not** the database's own
`governance_head`, its SQLite file, or a caller-computed digest of an
arbitrary fence. The verifier **requires**:
`trusted_fence_keys` (1–8 well-formed distinct public keys),
`expected_current_authority_sequence`,
`expected_current_fence_sha256`, and `checked_on`.
For a meaningful rollback check, these must be pinned by a separate
currently trusted process, not derived from the local database or
provided exclusively by the database owner.

## Verification behavior

`verify_integrated_head_fence(gate, packet, fence, ...)`:

1. Rejects malformed, missing, expired, not-yet-valid or oversized
   attestations, missing/mismatched keys and incorrect source packet.
2. Requires **exact** equality with the caller-provided current fence
   sequence and signed fence digest. A minimum sequence alone is not
   considered evidence of the current/latest digest.
3. Verifies the signing key against the supplied Ed25519 public roster.
4. Replays and compares both policy and packet-publication histories
   inside `AtomicGovernedPublisher.snapshot`'s **single SQLite read
   transaction**, including both counts and head hashes.
5. Returns identifier-minimized local equality metadata and
   `publication_authorized=false`,
   `ingestion_authorized=false`, `forecast_eligible=false`.

A valid old backup of a signed integrated DB **fails** if the supplied
current fence reflects a later signed policy or publication change.
If an attacker supplies an older signed fence **and** its old
`expected_current_*` values, the same old backup may still pass:
cryptographic verification does not independently establish freshness.
A malicious signer, clock, trusted-key map or current-fence service may
also undermine the assumption. The verifier cannot discover hidden
forks or guarantee signer independence or key custody.

## Not a write permission, service, or legal approval

This is an **offline, read-only** diagnostic. It is not wired into
`AtomicGovernedPublisher.publish`, a network API or data ingestion.
Calling it before a write would introduce a new TOCTOU gap unless a
separate reviewed transactional authority protocol were designed.
Do not use a passing receipt to authorize publishing, data access,
source ingestion, customer processing or forecasts.

The existing publisher/dual-admin schema and v1/v2 publication signing
formats are unchanged. No M5 or UCI rows are downloaded, bundled or
evaluated. The signature and external pins are synthetic in tests;
there is no managed independent signing service.

## Regression evidence

- `MM-FENCE-001`:
  `tests/unit/test_atomic_governed_publisher.py::test_signed_integrated_fence_matches_verified_heads_without_authorizing`
- `MM-FENCE-002`:
  `tests/unit/test_atomic_governed_publisher.py::test_signed_fence_detects_coherent_old_database_only_given_new_current_fence`
- `MM-FENCE-003`:
  `tests/unit/test_atomic_governed_publisher.py::test_signed_fence_checks_publication_head_even_without_policy_change`
- `MM-FENCE-004`:
  `tests/unit/test_atomic_governed_publisher.py::test_signed_fence_wrong_scope_signer_tampering_and_equivocation_fail`
- `MM-FENCE-005`:
  `tests/unit/test_atomic_governed_publisher.py::test_signed_fence_bounds_expiry_bad_keys_and_type_confusion_fail`

Run the fictional generated-key checks locally:

```bash
python -m pytest -q tests/unit/test_atomic_governed_publisher.py
python scripts/local_quality_gate.py --expected-head $(git rev-parse HEAD)
```

## Optional forward continuity proof

The [dual-witness integrated-fence transcript](INTEGRATED_FENCE_TRANSCRIPT.md)
is a *separate, opt-in* offline verifier: it checks up to 32 signed
forward transitions against caller-supplied anchor/current pins, requires
two distinct configured witness signatures per transition, and checks
its terminal fence against the same local SQLite snapshot contract.
It can classify two supplied conflicting successors but cannot find
hidden forks or independently establish the latest sequence. Existing
single-fence callers remain unchanged.
