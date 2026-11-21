# M1b — signed, revocable source-review records (experimental)

**A valid signature is not legal permission to use a dataset.** The offline
[review-history verifier](../../src/mirrormind/modules/evidence/review_decisions.py)
adds a *different trust boundary* after the
[declaration-only intake packet](SOURCE_INTAKE_REVIEW.md).
An intake requester may submit packet fields and evidence pointers, but must
not be able to create a trusted reviewer signature or set the trusted log head.

## What is verified

A review event is a versioned Ed25519-signed record bound to the exact
review-packet manifest SHA-256, snapshot SHA-256, source format, requested
research/commercial use, reviewer key ID, decision date and expiry.
A review record has a unique opaque reference, strictly increasing sequence
number, and a SHA-256 of the preceding signed event. Supported actions:

| Signed action | Local result |
| --- | --- |
| `approve` with a bounded expiry date | Signature verified *as a record only*; ingestion stays blocked |
| `deny` | Review denied |
| `revoke` | Permanent veto of **this specific packet fingerprint** |
| Missing events | No approval assumed |
| Expired latest approval | Expired and blocked |

After a revocation, an attempted approval for the **same** packet
fingerprint remains blocked. Any new independent review would need a new
source/manifest identity and an independently approved workflow;
changing a hash alone does not create permission.

The verifier refuses missing/untrusted signatures, wrong keys, malformed
events, scope mismatches, reordering, gaps, incorrect previous heads,
invalid review chronology and mismatched supplied log head. The full
chain head binds the sequence of signed decisions, so a truncated history
is detected **only when** the expected head comes from a separately
trusted, current registry.

## Trust roots are outside this component

The verification caller must obtain two values **independently of the
intake request**:

1. A current set of previously vetted Ed25519 reviewer public keys,
   controlled by the review authority (not `source_record_ref`,
   requester input, a dataset card or an uploaded self-signed key).
2. The current trusted signed-history head SHA-256, maintained in a
   separately secured, append-only review registry and read freshly.
   A value from the same uploader as the review events is **not** an
   anti-replay control.

The actual trusted key registry, private-key custody, external signer,
append-only log, signature-key revocation, monotonic freshness control
and operator approval process **do not yet exist in MirrorMind**.
The code only verifies metadata against keys and a head supplied by its
trusted caller. It cannot tell if that caller used a forged trust root,
stale registry head or wrong clock. It is **not** a production permission
service, an OAuth/PKI identity provider, or a legally valid approval.

The optional runtime library is installed with `pip install -e '.[review]'`
(or with the project `dev` extra). Signing private keys **must never**
enter the application, git, fixtures, logs or review packets.
The unit tests create disposable fake private keys locally and provide
an example signature encoder in **test code only**.

## No automatic approval

Even when every signature is valid, the latest event is `approve`, the
expiry has not passed and the declared log head agrees:

- `status = signed_review_history_checked_not_ingestion_authorization`
- `review_status = signed_approval_record_verified_not_legal_permission`
- `log_freshness_status = supplied_head_not_independently_attested`
- `permission_status = independent_legal_permission_not_verified`
- `ingestion_authorized = false`
- `forecast_eligible = false`

Signed records do not authenticate historical publisher release dates.
They cannot repair unsupported M5 license terms or bypass UCI data
privacy/attribution review. No real file, API route, storage, external
reviewer identity or WorldKernel decision is accessed.

## Tests and reproduction

[The signed review regressions](../../tests/unit/test_signed_source_review.py)
exercise valid signatures, denial, permanent revocation, expiry, missing
review, tampered signatures, wrong public keys, source/use mismatch,
history truncation, reordering, replay protection conditional on a
trusted head, invalid dates, and identifier-minimized receipts.

```bash
python -m pytest -q tests/unit/test_signed_source_review.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

Claims **MM-REVIEW-001** and **MM-REVIEW-002** are respectively attached
to `test_valid_signature_is_review_metadata_not_permission_to_ingest`
and `test_signed_revocation_is_terminal_for_same_manifest_even_after_reapproval`
in the test file above.

The next separate milestone must establish a real independently
controlled signing/revocation/freshness service, review rights and human
signoff. Only then can a source-specific adapter be evaluated for
permission promotion in a separate PR, with actual evidence and a
reviewed dataset card. Until then M1b real ingestion remains **NO-GO**.

## Volatile local writer coordination

The [experimental process-local review registry](LOCAL_REVIEW_REGISTRY.md)
adds a bounded optimistic version/head check around appends and prevents
a second writer from overwriting a newer **in-process** review decision.
It does not create the independent trusted append-only log or stable
reviewer public-key authority described above. It loses freshness state
on process restart and never changes source-ingestion authorization.

## Transactional local persistence (experimental)

The [SQLite registry experiment](SQLITE_REVIEW_REGISTRY.md) retains signed
event histories across restarts and uses database transaction locks for
per-file writers. This is still an **offline local metadata mechanism**,
not an independently authenticated, append-only current-head service,
reviewer identity system or approval of dataset usage.

## Signed review-head witness protocol (experimental)

[Signed head checkpoints](SIGNED_HEAD_CHECKPOINTS.md) attest to a precise
SQLite review revision and packet with a domain-separated Ed25519 record.
Verification needs independently controlled signer keys and a **current**
monotonic sequence supplied externally. No such service exists in the
project and even a valid signature never grants ingestion or forecasting.
