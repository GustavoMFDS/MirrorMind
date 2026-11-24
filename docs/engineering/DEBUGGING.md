# Debugging and recovery playbook

This guide is a **method**, not an automated repair service.

## Evidence-first procedure
1. Define the observed symptom, expected behavior, runtime configuration and a safe reproducer. Preserve the failing input's schema, not private payloads or credentials.
2. Capture timestamp, version/commit, relevant feature flags, sanitized logs, a correlation/job ID if one exists, and stack trace.
3. Find the entrypoint in [SYSTEM_MAP](SYSTEM_MAP.md), then the symbol in the [generated catalog](generated/SYMBOLS.md). Follow callers, state mutations, contracts and related tests.
4. Generate competing root-cause hypotheses. Confirm or falsify with a focused test; never assume the AI-generated explanation is correct.
5. Fix the smallest relevant location, add a regression test for the observed failure, and run relevant broader tests.
6. Document the verified root cause, remediation, limitations, safe rollback and monitoring. Update the associated runbook in the PR.

## Incident note template
```text
Symptom:
Commit/version and environment:
How to reproduce (safe):
Observed / expected:
Relevant modules and stacktrace:
Evidence for root cause:
Mitigation / rollback:
Fix and regression test:
What is still unknown:
```

Never paste secrets, access tokens, user records, raw customer datasets or private prompt contents into agent context or public documentation.

## MirrorMind starting points
- Scenario-validation error: `api/routes/scenarios.py` → `core/contracts.py`; inspect `tests/unit/test_contracts.py`.
- Service/router mismatch: `api/app.py`, `api/routes/system.py`, `tests/integration/test_api.py`.
- Missing capability: check `GET /v1/capabilities` and [ROADMAP](../ROADMAP.md) before diagnosing a future feature as broken.
- Integrating WorldKernel: inspect `modules/simulation/gateway.py` and versioned contracts. An interface is not live execution.
- For planned evidence/agents, design permission-bound provenance, error handling and budget limits before implementing.
- For fictional UCI-shaped retail projection failures: trace [`domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py), [reviewed method guide](UCI_RETAIL_PROJECTION.md) and [unit regressions](../../tests/unit/test_uci_retail_projection.py). Do not copy customer IDs or invoice descriptions into bug reports.
- For bounded local XLSX input failures: inspect [`domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), [the workbook guide](UCI_WORKBOOK_READER.md) and [ZIP/schema tests](../../tests/unit/test_uci_workbook.py). Never paste original workbook bytes or customer fields in an issue.

- For missing or mismatched review packets: inspect [`modules/evidence/intake_review.py`](../../src/mirrormind/modules/evidence/intake_review.py), [the review guide](SOURCE_INTAKE_REVIEW.md) and [synthetic tests](../../tests/unit/test_source_intake_review.py). Share only sanitized refs/digests, never proof documents or raw rows in issues; references alone do not authorize use.

- For mismatched signed review chains: inspect [`review_decisions.py`](../../src/mirrormind/modules/evidence/review_decisions.py), [review security boundary](SIGNED_SOURCE_REVIEW.md) and [adversarial regressions](../../tests/unit/test_signed_source_review.py). Check key IDs, dates and independently anchored log heads without printing private keys, source IDs or reviewer evidence. A valid signature does not grant ingestion.

- For stale review writers in one process: inspect [`local_review_registry.py`](../../src/mirrormind/modules/evidence/local_review_registry.py), [the CAS limits](LOCAL_REVIEW_REGISTRY.md) and [concurrency tests](../../tests/unit/test_local_review_registry.py). Never assume a restart preserves the latest head, or infer permission from a local revision.

- For persistent review history failures: inspect [`sqlite_review_registry.py`](../../src/mirrormind/modules/evidence/sqlite_review_registry.py), [SQLite safety boundaries](SQLITE_REVIEW_REGISTRY.md) and [transaction regressions](../../tests/unit/test_sqlite_review_registry.py). Never expose raw SQLite databases containing review IDs; compare only sanitized revisions and independently provisioned heads. A correct local head is not an independent authority.

- If signed checkpoint verification refuses a restored SQLite database: inspect [`head_checkpoints.py`](../../src/mirrormind/modules/evidence/head_checkpoints.py), [checkpoint trust guide](SIGNED_HEAD_CHECKPOINTS.md) and [fictional replay tests](../../tests/unit/test_head_checkpoints.py). Do not use a checkpoint uploaded by the requester as a trusted freshness anchor, and never print private signing keys or source documents.

- For missing witness publications, rotation failures or stale head fences: inspect [`authority_transcript.py`](../../src/mirrormind/modules/evidence/authority_transcript.py), [witness protocol and limitations](AUTHORITY_TRANSCRIPT.md) and [fictional recovery tests](../../tests/unit/test_authority_transcript.py). Never assume a caller-supplied chain is current, or emit private key material/source IDs in issues.

- For publication CAS conflicts, missing operator role or local rollback: inspect [`local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py), [the local publisher trust guide](LOCAL_CHECKPOINT_PUBLISHER.md) and [synthetic transactional tests](../../tests/unit/test_local_checkpoint_publisher.py). Never log private signing keys or copy a publisher SQLite database with metadata into issues. The journal cannot attest to its own globally current head.

- For operator policy enrollment or revocation incidents: inspect [`operator_governance.py`](../../src/mirrormind/modules/evidence/operator_governance.py), [its trust and TOCTOU limits](OPERATOR_GOVERNANCE.md) and [synthetic regressions](../../tests/unit/test_operator_governance.py). Do not mistake an active policy record for effective publisher authorization or log private key material; the databases are not atomically coupled.

- For the **integrated** publisher refusing an operator after a revocation or reporting stale policy heads: inspect [`atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py), [same-file transaction contract](ATOMIC_GOVERNED_PUBLISHER.md) and [concurrent revocation tests](../../tests/unit/test_atomic_governed_publisher.py). The legacy publisher intentionally refuses integrated files. Keep original source IDs and signed keys out of debug logs; local transactions do not prove external freshness.

Useful local checks:
```bash
python -m pytest -q
python -m ruff check src tests
```
Do not assert connectors, agents, forecasts or simulations are operational without implementation and tests.
## Supplied signed integrated-fence mismatch or rollback suspicion

Inspect [the fence contract](INTEGRATED_HEAD_FENCE.md), the
[verifier source](../../src/mirrormind/modules/evidence/integrated_head_fence.py)
and the [fictional rollback test](../../tests/unit/test_atomic_governed_publisher.py).
Record whether the separately pinned expected current sequence/digest
came from a genuinely independent trusted process. An old coherent
database may pass if those external values are stale. Never log
private signing keys, source-row payloads or customer identifiers.
A passing fence comparison cannot authorize a later publish.

## Dual-witness combined-fence continuity or conflict error

Follow the [transcript guide](INTEGRATED_FENCE_TRANSCRIPT.md)
and [generated-key fixture regressions](../../tests/unit/test_atomic_governed_publisher.py).
Check that anchor digest/sequence and exact expected latest digest
were obtained **separately** from the local publisher, that each link
signs the previous digest, and that both witness key IDs/public keys
are distinct from the authority key and each other. If two fully
signed same-predecessor successors conflict, preserve both original
records as evidence; do not silently choose a branch. Failure to
receive a competing record is **not** evidence that none exists.
Do not treat a successful offline chain check as live publication
admission or ingest permission.

## Separate signed-fence registry mismatch / disaster recovery

Use the [registry guide](LOCAL_INTEGRATED_FENCE_REGISTRY.md)
and [synthetic rollback tests](../../tests/unit/test_atomic_governed_publisher.py).
Check the identity marker (one packet and configured Ed25519 signing
rosters), signed event ordering, both witness signatures, CAS head and
actual publisher snapshot. Preserve original signed transition JSON
and both DB files for forensic comparison. If the governed DB alone
was restored, the intact separate journal can detect its older
policy/publication heads. If the registry was also restored or its
last valid event was removed, **do not claim** independent freshness.
Never repair by silently inserting unsigned records or granting
publish/ingestion permission. A publisher write may race a registry
comparison because there is no two-file transaction.

## Challenged HTTPS current-head read fails or remote signer disagrees

Inspect the [protocol and threat model](REMOTE_FENCE_HEAD_CLIENT.md)
and [generated-key/fake HTTPS regressions](../../tests/unit/test_atomic_governed_publisher.py).
Require an explicit trusted HTTPS domain with its fixed path;
validate outbound CA/hostname and firewall separately, without
disabling TLS checks or enabling redirects. A signed response must
echo **the current random request nonce**, the correct source-review
hash, the exact endpoint/service key and a 1–120-second UTC
validity interval. A remote/local sequence or digest mismatch is
not automatically evidence of attack: the remote service can be
ahead, behind, stale or falsely signing a head. Preserve minimal
hash evidence and verify each side with independent operators.
Never log signer private keys or source rows, retry with stale
pins, bypass on outage or use read receipt to authorize publishing.
No live authority is deployed in the project.

## Local retail evidence-flow failures

For a failed M1 composite preflight, reproduce with
[`tests/integration/test_retail_evidence_flow.py`](../../tests/integration/test_retail_evidence_flow.py)
and read the [flow contract](M1_SYNTHETIC_EVIDENCE_FLOW.md). Confirm the
caller-opened stream is binary and bounded, calculate its SHA-256 locally,
and compare it to both the expected digest and `SourceReviewDeclaration`.
Then isolate the format helper: CSV uses strict schema/two-date rules;
XLSX uses the optional workbook parser, caller calendar and explicit release
tuple. A missing CSV slice is a normal abstention. A workbook calendar gap or
missing release is invalid input, not evidence of zero sales. Do not dump raw
rows, references or workbook XML while diagnosing. Matching hashes and
synthetic release declarations never prove rights or real publisher
availability.
