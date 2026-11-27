# MM-M1b — nonce-challenged signed HTTPS current-head reader (experimental)

**This is an opt-in outbound HTTPS read client, not an installed or
deployed external authority, signer or server.** Its code can authenticate
a *particular signer response* to a fresh challenge. It cannot prove
that the signer independently controls its own data, is reporting the
globally latest state, or has custody or separate administrators.

The [client module](../../src/mirrormind/modules/evidence/remote_fence_head_client.py)
builds on the [separate local registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md).
For every opt-in call it receives the registry, a trusted fixed HTTPS
endpoint, an expected service identifier and an independently configured
Ed25519 **service public-key** roster.

## Fixed wire request and response

Only the following fixed-path endpoint is supported:

`https://head-authority.example.org/v1/integrated-fence/head`

`head-authority.example.org` is a **fictional illustrative host**, not
an active deployment or endorsed authority. A deployment supplies
its own trusted fully qualified DNS name; IP-literal hosts, localhost,
userinfo, alternate ports, arbitrary paths, HTTP, URL fragments,
preexisting query strings and redirects are rejected.

For a given request the client generates a **new 32-byte random nonce**
using the OS secure randomness API and issues:

```text
GET /v1/integrated-fence/head?nonce=<64-lowercase-hex>&packet_sha256=<64-lowercase-hex>
Accept: application/json
```

The source packet digest selects one remotely reported source head
but may be correlatable across reads; it is not a private dataset row.
**No customer records, source payloads, private keys or bearer tokens**
are sent. The caller must configure outbound DNS/firewall permissions
appropriately; DNS ownership, route segregation and actual remote-host
administrative independence are outside the implementation.

The response is **canonical compact JSON with lexicographically sorted
keys**, content type `application/json`, HTTP 200 and at most 4096
bytes. It uses `SignedRemoteFenceHead`:

| Signed field | Bound purpose |
| --- | --- |
| `service_id`, `service_key_id` | Expected signer role, both checked against the caller's trusted roster |
| `endpoint` | Exact configured HTTPS URL (without query) |
| `nonce_hex` | Echoes the 64-hex client-generated unpredictable challenge |
| `packet_sha256`, `snapshot_sha256` | Exact source review declaration/snapshot scope |
| `authority_sequence`, `fence_sha256` | Claimed exact latest **fully signed** integrated-fence sequence and digest |
| `issued_at_utc`, `expires_at_utc` | Exact UTC-second timestamps `YYYY-MM-DDTHH:MM:SSZ`, lifetime 1–120 seconds |
| `signature_hex` | Ed25519 signature over all fields above with the domain below |

Signing message is canonical JSON of **every field except
`signature_hex`**, plus
`"domain":"mirrormind.remote-fence-head-challenge.v1"`.
The signature MUST use a distinct **remote service signing key**.
Neither key IDs nor public-key material may be reused from the
integrated fence authority or its dual witnesses. Configured public
keys must be explicitly provided; the client never auto-enrolls or
downloads trust roots.

## Fail-closed steps

`fetch_and_compare_remote_head(registry, endpoint=..., service_id=...,
trusted_service_keys=...)`:

1. Validates the fixed HTTPS service URL and trusted public-key roster
   **before** network access; generates a fresh random 32-byte nonce.
2. Performs a single outbound **HTTPS GET**, standard system CA and
   hostname checks, no insecure context override, redirects or proxy
   environment use. Request timeout: 3 seconds. Body: max 4096 bytes.
   Non-200 or incorrect content-type, malformed JSON, extra/missing or
   duplicate fields, noncanonical encoding and outage fail closed.
3. Uses the device UTC clock **after** response retrieval. Checks the
   service identity, endpoint, packet/snapshot, nonce, Ed25519 signature,
   key separation and short signed validity interval.
4. Calls `LocalIntegratedFenceRegistry.compare_local`, which itself
   replays all stored dual-witness signatures and checks the final
   signed policy+publication state against the local governed SQLite
   database. Requires **exact equality** of remote claimed authority
   sequence and signed fence digest to that locally verified current
   state. Behind, ahead, forged and unknown heads **all fail**.
5. Returns a sanitized metadata-only receipt, always
   `publication_authorized=false`,
   `ingestion_authorized=false`,
   `forecast_eligible=false` and
   `independent_authority_status=not_established_by_this_client`.

The separate
`verify_challenged_remote_head(registry, raw_response, ...,
checked_at=...)` accepts a **caller-supplied clock only for offline
verification/test use**. The network helper chooses its own local
UTC clock. Neither is a secure independent timestamp.

The experimental [G-01 in-process responder](REMOTE_FENCE_HEAD_SERVICE.md)
uses the same canonical protocol helpers and a read-only storage `Protocol`.
It is not wired to this client's HTTPS transport, and no route, listener,
persistent store or deployment exists. A generated-key test passes its bytes
through this existing verifier to check wire compatibility.

## What this changes and what it cannot guarantee

The client can reject a **replayed previous HTTP reply** because the
old response lacks the *new* nonce and will not match a new request.
When a separately operated and honest signer still advertises a
newer signed head, even **paired rollback of both local databases**
can be detected by sequence/digest mismatch. This is a **conditional
cross-domain comparison**. There is no deployed signer, server, remote
head publication path, ACL system, key custody, HSM, consensus or
durable remote feed to validate that scenario in real operations.

**A malicious, stale or colluding service can freshly sign an old
head using the new nonce.** If both local databases were also rolled
back to that head, the check can still pass. The code cannot discover
hidden forks, establish correct public keys, prove honest independent
operations, or keep the remote service online. System clock/CA trust,
DNS transport, remote endpoint ownership and response issuance require
deployment review. HTTPS authenticates a configured DNS endpoint but
alone does not prove administrator independence.

This reader is **never called from `publish`**. Adding a separate
read-before-write permission check would introduce another TOCTOU
race rather than a cross-domain transactional authorization protocol.
The read result is not a source-use entitlement, publication token,
release approval or proof of numeric forecasting readiness.

## Reproducible synthetic verification

All tests use fictional packets, temporary SQLite databases, generated
Ed25519 signing keys and fake in-memory HTTPS responses. **No live
network endpoint or external authority service was contacted**;
real TLS interoperability, trust operations and remote recovery
remain unverified.

- `MM-RHEAD-001`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_challenged_head_matches_signed_local_heads_without_permissions`
- `MM-RHEAD-002`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_response_replay_wrong_nonce_and_signature_tampering_fail`
- `MM-RHEAD-003`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_response_clock_interval_missing_fields_and_canonical_json`
- `MM-RHEAD-004`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_head_distinct_service_keys_and_fixed_https_path_required`
- `MM-RHEAD-005`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_signed_head_detects_two_file_restore_with_newer_remote_reply`
- `MM-RHEAD-006`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_https_fetch_uses_fresh_nonce_and_never_calls_real_network`
- `MM-RHEAD-007`:
  `tests/unit/test_atomic_governed_publisher.py::test_remote_https_transport_enforces_timeout_mime_bytes_and_no_redirects`

```bash
python -m pytest -q tests/unit/test_atomic_governed_publisher.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

[Scoped change request](changes/M1B_CHALLENGED_HTTPS_HEAD_READER.md).
