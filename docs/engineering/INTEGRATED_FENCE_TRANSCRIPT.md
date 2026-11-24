# MM-M1b — offline dual-witness integrated-fence continuity (experimental)

**No independent authority service, trusted latest-fence feed, protected key
custody, validated human identities or approved real-data ingestion.**

This [offline verifier](../../src/mirrormind/modules/evidence/integrated_fence_transcript.py)
extends [the PR #47 signed integrated-head fence](INTEGRATED_HEAD_FENCE.md).
It verifies a short caller-supplied chain between an **externally pinned
anchor** and an **externally pinned latest signed fence** for one
source-review packet. It does not store anything or modify the database.

## Signed contracts

A `SignedIntegratedFenceTransition` contains the existing
`SignedIntegratedHeadFence` (already signed by its authority), an
exact `previous_authority_sequence` and
`previous_fence_sha256`, a `witnessed_on` calendar day, two
**lexicographically ordered, distinct** witness key IDs and two
Ed25519 signatures. Every witness signs the same canonical JSON
message under the new domain
`mirrormind.integrated-fence-dual-witness.v1`:

| Canonical field | Meaning |
| --- | --- |
| `domain` | Prevent cross-protocol signature reuse |
| `previous_authority_sequence`, `previous_fence_sha256` | Exact predecessor |
| `authority_sequence`, `fence_sha256` | Exact next authority fence sequence and signed digest |
| `witnessed_on` | Signed declared date of witnessing, not a trusted timestamp |
| `witness_key_ids` | Exactly two separately configured witness signing roles |

The signed fence digest is SHA-256 of its canonical signed content
followed by its authority signature bytes, not just the unsigned
policy/publication head. The fence itself is separately signed by an
authorized key in the caller-provided authority public-key roster.
Witness public keys **and key IDs** must be distinct from authority
signing keys; reused witness keys and missing signature 2 fail.

The explicit caller inputs are `trusted_fence_keys`,
`trusted_witness_keys`, `anchor_authority_sequence`,
`anchor_fence_sha256`, `expected_current_authority_sequence`,
`expected_current_fence_sha256` and `checked_on`. These are
configuration/claims, **not** proof of protected external delivery.

## Bounded offline verification

`verify_integrated_fence_transcript(gate, packet, transitions, ...)`:

1. Requires a tuple of 1–32 links, independently configured signing
   roles and exact SHA-256 references, valid signatures and valid days.
2. Enforces each successor authority sequence equals predecessor + 1,
   exact predecessor hash and non-decreasing signed witness date.
3. Verifies each authority and **both** witness Ed25519 signatures,
   against the **same** source-review declaration/snapshot.
4. Rejects any regression of the signed policy revision or publication
   sequence. When a counter is unchanged, the corresponding signed
   head hash must also remain unchanged.
5. Compares the terminal signed fence sequence/digest to the caller's
   **exact** expected current fence values. Finally calls the PR #47
   [combined-head verifier](INTEGRATED_HEAD_FENCE.md), which compares
   policy and publication states against **one consistent local
   SQLite read transaction**. Intermediate states are not compared to
   historic SQLite snapshots.

Returning a local match **never authorizes** publication, source
ingestion or forecasting. The local result is not a capability token,
a consensus result or a safe separate pre-check for a future write.

## Observing a conflict does not resolve it

`classify_supplied_fence_fork(packet, first, second, ...)` verifies
two complete authority-and-dual-witness signed transitions and reports
a supplied **conflict** if they share the exact predecessor sequence,
predecessor digest and successor sequence for the same packet, but
differ in their signed successor fence digest. The result labels the
conflict as `observed_supplied_signed_fence_conflict_no_resolution`.
It intentionally does not select a valid branch, publish anything, or
decide who is trusted. Forged evidence or different predecessors are
not classified as a proven fork.

**Undetected conflicts remain possible:** a fork withheld from the
caller, a short supplied chain omitting history before its anchor,
colluding/compromised witness+authority keys, stale current/anchor
pins, false declared witness days, clock tampering and an adversary
with control over separate stores are not prevented. Honest independent
operations, durable append-only storage, remote timestamps and trusted
freshness still require dedicated services and operational review.
Rolling back both the local SQLite database **and all caller-supplied
pins and signed links** can still pass.

## Compatibility and reproducibility

- No changes to SQLite schemas or to signed v1/v2 publication formats.
- Existing `verify_integrated_head_fence` and standalone publisher
  remain usable; this is a **new optional offline proof format**.
- Tests use generated synthetic Ed25519 keys and fictional packet rows.
  No UCI/M5 source data or genuine permissions are accessed.
- `/v1/capabilities` reports only
  `local_dual_witness_integrated_fence_transcript` as `experimental`.
- [Scoped change record](changes/M1B_DUAL_WITNESS_FENCE_CONTINUITY.md)
  and [source](../../src/mirrormind/modules/evidence/integrated_fence_transcript.py).

## Regression evidence

The generated-key checks are in
[`test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py).

| Evidence | Function | Specific claim |
| --- | --- | --- |
| MM-FCHAIN-001 | `test_dual_witness_fence_chain_verified_against_integrated_local_snapshot` | Two links and final SQLite state match; no permissions |
| MM-FCHAIN-002 | `test_dual_fence_transcript_rejects_missing_hops_and_old_database_with_new_pin` | Conditional old-backup refusal; old pins can still replay |
| MM-FCHAIN-003 | `test_dual_fence_transcript_rejects_forged_signatures_and_role_reuse` | Both witness signatures and distinct roles required |
| MM-FCHAIN-004 | `test_two_valid_dual_witness_fence_successors_expose_unresolved_conflict` | Two verified conflicting successors can be classified, not resolved |
| MM-FCHAIN-005 | `test_dual_fence_transcript_rejects_regressing_counters_and_unchanged_revision_fork` | No signed counter regression or same-counter head change |
| MM-FCHAIN-006 | `test_dual_fence_transcript_bounded_dates_types_and_local_expiry` | Bounded, dated and valid terminal fence |

```bash
python -m pytest -q tests/unit/test_atomic_governed_publisher.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Opt-in local durable continuation

The [separate local signed-fence registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md)
stores and replays complete witnessed transitions and performs a
registry-file `BEGIN IMMEDIATE` CAS before appending one next signed
link. Its `compare_local` uses the registry's stored terminal head,
instead of trusting a newly supplied external latest pin. This is an
**additional local SQLite file**, not an externally independently
operated authority. Two-file rollback and a valid truncated suffix
remain undetectable without a separately protected latest digest.
