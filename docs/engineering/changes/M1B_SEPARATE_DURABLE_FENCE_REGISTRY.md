# Change request — MM-M1b separately persisted signed current-fence registry

## Goal
Replace caller-only *in-memory/passed* current-fence pins with a **separate,
opt-in local SQLite durable registry** of signed, dual-witness integrated
fence transitions for **one** source-review packet. Compare that registry's
verified current head against a separately stored governed publication DB.
This detects restoration of the publisher DB alone if the registry remains
intact. It does not magically provide operationally independent storage.

## Confirmed starting point
- PR #45 local atomic operator governance/publishing remains one SQLite DB.
- PR #47 supplied signed combined policy+publication head equality compares
  exactly one verified local read transaction.
- PR #48 validates a bounded dual-witness signed forward transcript *supplied
  entirely by the caller* with exactly pinned anchor/current hashes.
- No persistent current signed-head registry exists in the repository.
  A maliciously restored caller-supplied old transcript/pin may pass.

## Scope and acceptance
- Implement `LocalIntegratedFenceRegistry` with an absolute **different**
  SQLite file from the governed publication DB, explicit `create=True`
  initialization, exact configured signing public-key roster/packet marker
  and no ability to accept unsigned or single-witness transitions.
- Persist **canonical full signed transitions** and compare-and-swap heads.
  Bootstrap sequence 0 and all-zero anchor are local conventions only.
  Signed head progresses one sequential link per append, with 1..32 events.
- Every append must take one registry-local `BEGIN IMMEDIATE` writer lock,
  fully replay persisted signatures/continuity, check expected
  sequence/digest, validate new signatures and current publisher local
  snapshot, and commit only valid next links. No lost updates or partial
  writes when rejected. Hashes and dates must not be silently dropped.
- Every read replays stored signatures+continuity and rejects altered
  signatures, malformed records or an interior missing link. A deleted
  **valid terminal suffix** cannot be detected without a separately
  pinned latest head. Also support comparison with the local publisher head
  using the *registry's stored* latest signature/pin, rather than a
  caller-supplied arbitrary latest digest.
- Recovery/reopen preserve the head. Registry loss/unavailable, missing
  link, key roster/packet changes and malformed event data fail closed.
  A publisher-only old backup is rejected while the separate registry
  is intact. Rollback **both** files remains undetectable absent an
  independent third-party pinned latest digest.
- Do not wire registry into publication admission or legal ingestion.
  There is NO two-file transaction. Explicitly document the possibility
  of divergence if a publish commits between the registry's local
  comparison and registry commit. No service, identity, real key custody,
  secure clock, external storage/network or self-proclaimed consensus.
- Synthetic tests: persistence/reopen, CAS/replay, concurrent same-head
  attempts, signature/payload tampering, corrupted schema/key roster,
  publisher-only restore and paired restores, no-source permissions,
  deliberate separate-store offline/missing file failure, expiry.

## Impact map
| Layer | File | Planned change |
| --- | --- | --- |
| Source | `src/mirrormind/modules/evidence/local_integrated_fence_registry.py` | New independent-file local registry, verification and CAS |
| Existing | `integrated_fence_transcript.py`, `integrated_head_fence.py`, `atomic_governed_publisher.py` | Reuse tested signature/transcript/snapshot contracts; unchanged |
| Tests | `tests/unit/test_atomic_governed_publisher.py` | Synthetic cross-file/rollback/concurrency regressions |
| API truth | `src/mirrormind/api/routes/system.py` | Experimental-only capability ID, no REST endpoint |
| Guides | `docs/engineering/LOCAL_INTEGRATED_FENCE_REGISTRY.md`, system/debug/learning/roadmap | Detailed trust/dataflow/limits |
| Traceability | `EVIDENCE_MAP.json`, `CAPABILITY_LEDGER.json`, `REPOSITORY_ATLAS.md`, `generated/SYMBOLS.md` | Test claims, links, generated index |

## Safety/roll-back plan
No migration of existing DBs, no overwrite of existing files; choose a
new registry path and require explicit creation. Removing new module
and experimental capability requires no legacy database changes. Do not
claim anti-rollback if attacker can restore both files. Receipt must
report `publication_authorized=false`,
`ingestion_authorized=false`, `forecast_eligible=false`.
Real-source permission reviews and model cards remain independent gates.
