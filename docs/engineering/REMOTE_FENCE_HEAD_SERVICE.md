# Experimental challenged current-head responder (G-01)

## Purpose and status

The existing
[remote head client](REMOTE_FENCE_HEAD_CLIENT.md) can request a signed,
nonce-bound report of a current integrated-fence head, but until G-01 the
repository had no code that could create that response. This guide documents a
minimal in-process responder and the read-only storage contract it consumes.

The implementation is **experimental and transport-neutral**. It is a
callable Python object, not a FastAPI route, socket listener, remote endpoint,
authenticated service, persistent store or independent authority. Tests use
generated Ed25519 keys, fictional digests and an in-memory store. No HTTP
server or live network is contacted. The responder does not authorize
publication, source ingestion, forecasting or decisions. The
[capability ledger](CAPABILITY_LEDGER.json) and `GET /v1/capabilities` remain
unchanged because this module is not externally exposed.

The scope is the
[G-01 change request](changes/G01_CURRENT_HEAD_SERVICE_RESPONSE.md). G-02's
authenticated persistent compare-and-swap, G-03's transport integration and
G-04's operational trust review remain separate work and acceptance gates.

## Architecture and data flow

```mermaid
sequenceDiagram
    participant C as Existing HTTPS client
    participant T as Future HTTP adapter (not implemented)
    participant R as RemoteFenceHeadResponder
    participant S as RemoteFenceHeadStore Protocol
    participant P as Shared canonical protocol

    C->>T: GET fixed path + fresh nonce + packet digest
    Note over T: No transport exists in this change
    T->>R: RemoteFenceHeadRequest
    R->>R: Validate method, path, Accept and exact query
    R->>S: read_current(packet_sha256)
    S-->>R: CurrentRemoteFenceHead or None
    R->>P: Build and validate SignedRemoteFenceHead
    P-->>R: Canonical signing bytes and compact JSON
    R-->>T: Status, headers and bytes
    T-->>C: HTTP response (future adapter responsibility)
    C->>P: Parse, verify signature, nonce, scope and expiry
    C->>C: Compare with signed local registry; no permission grant
```

The shared module
[`remote_fence_head_protocol.py`](../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py)
owns the existing wire record and canonical encoding. Both the client and
responder import the same functions, avoiding two independent signature
formats. The client still owns local-registry comparison; the responder only
signs the store's scoped claim.

| Component | Responsibility and boundary |
| --- | --- |
| [`RemoteFenceHeadStore`](../../src/mirrormind/modules/evidence/remote_fence_head_service.py) | Typed `read_current(packet_sha256)` boundary. It specifies a return shape, not persistence, transactions, caller authentication, trusted freshness or separate administration. |
| `CurrentRemoteFenceHead` | Immutable packet/snapshot digests, authority sequence and fence digest; no source rows or private material. |
| `RemoteFenceHeadRequest` / `RemoteFenceHeadResponse` | Minimal HTTP-shaped input and output records. An adapter would still have to map real HTTP headers, status handling, TLS and request limits. |
| `RemoteFenceHeadResponder` | Validates one fixed request, reads one matching scope, signs a short-lived response and returns bodyless errors. It has no listener or route registration. |
| [`remote_fence_head_protocol.py`](../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py) | Shared `SignedRemoteFenceHead`, endpoint rules, domain-separated canonical signing message, compact wire encoder and strict response parser. |
| [`remote_fence_head_client.py`](../../src/mirrormind/modules/evidence/remote_fence_head_client.py) | Existing outbound transport and verifier; checks the service signature and challenge, then compares against the local fully verified registry. |

## Source walkthrough

### Configuration and key separation

`RemoteFenceHeadResponder.__init__` requires a service ID, service key ID,
fixed endpoint, Ed25519 private signing key, non-service public-key roster,
store reader, UTC clock and lifetime. It refuses malformed IDs/endpoints,
non-Ed25519 keys, duplicate or malformed protected public keys, key-ID reuse
or public-key reuse, a missing store reader/clock, and a lifetime outside
1–120 seconds. The protected roster is copied into an immutable mapping so a
caller cannot mutate the checked configuration later.

The responder can prove only that its signing key differs from the public
keys supplied to it. It cannot prove that the supplied roster is complete or
that the service key has separate custody, operators or infrastructure.

### Request validation and store read

`respond` accepts only the exact `RemoteFenceHeadRequest` type. It requires
`GET`, path `/v1/integrated-fence/head`, `Accept: application/json`, and a raw
query string in this exact order and spelling:

```text
nonce=<64 lowercase hex>&packet_sha256=<64 lowercase hex>
```

Percent escapes, reordered values, duplicate keys, unknown fields, blank
values and extra query bytes are refused before the store is called. This
mirrors the current client's fixed request. A 405 response includes `Allow:
GET`; 400, 404, 405, 406 and 503 responses have an empty body, `Content-Length:
0` and `Cache-Control: no-store`.

After validation, the responder calls
`RemoteFenceHeadStore.read_current(packet_sha256)`. `None` means no record and
returns 404. A record for another packet violates the store contract and also
returns 404 to avoid revealing scope. A
`RemoteFenceHeadStoreError`, `RemoteFenceHeadClockError`, malformed head, or
invalid returned clock fails with a generic bodyless 503. Store and clock
adapters must translate expected operational failures into their respective
typed errors; unrelated programming exceptions propagate so this in-process
boundary does not conceal defects. A future HTTP adapter must preserve these
typed outcomes while mapping its own unexpected failures to a generic
transport-level 5xx response.

### Canonical response and client verification

For a valid record, `respond` takes one injected timezone-aware UTC instant,
truncates sub-second precision and adds the configured lifetime. It creates a
`SignedRemoteFenceHead` with the request nonce, exact packet and snapshot
digests, authority sequence, fence digest, fixed endpoint and service identity.
`_canonical_remote_message` validates every signed field and encodes the
existing domain `mirrormind.remote-fence-head-challenge.v1` with sorted compact
JSON. The service signs those bytes with its Ed25519 key. `_signed_wire` then
encodes the complete record as sorted compact JSON. The response includes
`Content-Type: application/json`, `Cache-Control: no-store` and the exact
content length, and is refused if it would exceed the client's 4096-byte
limit.

The existing
`verify_challenged_remote_head` in the client parses the same bytes, checks the
trusted signer, nonce, endpoint, packet and snapshot, signature and validity
interval, then compares the claimed sequence/digest with its local signed
registry. A good response proves only a configured signer signed this
challenge-bound claim. A fresh nonce does not prove the store is honest or
independent, and the local equality check does not grant authority.

## Contracts and failure behavior

| Input/output | Contract |
| --- | --- |
| Request method/path | Exact `GET` and `/v1/integrated-fence/head` |
| Accept | Exact `application/json`; otherwise 406 |
| Query | Exactly `nonce` then `packet_sha256`, each 64 lowercase hex characters |
| Store lookup | `read_current(packet_sha256) -> CurrentRemoteFenceHead \| None`; translate expected unavailable/unsafe reads to `RemoteFenceHeadStoreError` |
| Sequence/digests | Sequence is an integer 1–1,000,000,000; digests are lowercase SHA-256 strings; booleans are not accepted as integers |
| Time | Injected aware UTC clock; translate expected clock-service failures to `RemoteFenceHeadClockError`; output uses exact `YYYY-MM-DDTHH:MM:SSZ` seconds |
| Lifetime | Integer 1–120 seconds; the default is 60 seconds |
| Success response | 200, canonical JSON, no-store, maximum 4096 bytes |
| Failure response | 400 malformed input, 404 unknown path/scope, 405 wrong method, 406 wrong media type, 503 typed store/clock failure, malformed stored record or invalid returned clock; empty body |
| Authorization | None. Receipt flags from the client remain false for publication, ingestion and forecast eligibility. |

Compatibility-sensitive fields and signatures are owned by the shared
protocol module and predate this responder. Do not add, rename, normalize or
reorder fields without a separately reviewed protocol migration and client
compatibility tests.

## Reproducible fictional example

This sample constructs only an in-memory fake store and generated keys. The
host is illustrative; no connection is made:

```python
from datetime import UTC, datetime

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.remote_fence_head_service import (
    CurrentRemoteFenceHead,
    RemoteFenceHeadRequest,
    RemoteFenceHeadResponder,
)

service_key = Ed25519PrivateKey.generate()
protected_key = Ed25519PrivateKey.generate().public_key().public_bytes(
    Encoding.Raw, PublicFormat.Raw
)
record = CurrentRemoteFenceHead(
    packet_sha256="a" * 64,
    snapshot_sha256="b" * 64,
    authority_sequence=1,
    fence_sha256="c" * 64,
)

class FictionalStore:
    def read_current(self, packet_sha256):
        return record if packet_sha256 == record.packet_sha256 else None

responder = RemoteFenceHeadResponder(
    service_id="EXAMPLE_AUTHORITY_001",
    service_key_id="EXAMPLE_SERVICE_KEY_001",
    endpoint="https://head-authority.example.org/v1/integrated-fence/head",
    signing_key=service_key,
    non_service_public_keys={"EXAMPLE_FENCE_KEY_001": protected_key},
    store=FictionalStore(),
    clock=lambda: datetime(2026, 11, 24, 12, 0, tzinfo=UTC),
)
response = responder.respond(RemoteFenceHeadRequest(
    method="GET",
    path="/v1/integrated-fence/head",
    query_string=f"nonce={'d' * 64}&packet_sha256={'a' * 64}",
    accept="application/json",
))
assert response.status_code == 200
assert len(response.body) <= 4096
```

The response signature varies because the example generates a new private
key. The expected observable result is a 200 response containing compact
JSON. The sample does not provide a real signed registry for the client to
compare, a deployment, independently held keys or a trusted current head.
The integrated generated-key round trip is verified by the tests below.

## Safety, limitations and recovery

- The service does not authenticate a caller, consume a nonce, store history,
  advance a head, rate-limit, listen on a port or provide TLS. A future
  transport must define these controls and its own request-size/error policy.
- Replaying a response against a different client challenge fails because the
  nonce is signed. Reusing the same challenge is not prevented server-side.
- A fresh response may still describe a stale head if the configured store
  returns stale data. The client only detects this when its verified local
  state differs.
- An invalid store record returns an empty 503 without including record or
  exception contents. A missing/mismatched packet scope returns empty 404.
- A clock callback that returns a naive/non-UTC value returns empty 503. An
  expected operational clock failure must be translated to
  `RemoteFenceHeadClockError`, which the responder maps to the same empty 503
  as `RemoteFenceHeadStoreError`. Unexpected callback, store or signing
  programming errors propagate to the in-process caller; a future HTTP
  adapter must map them to a generic server error without logging key or
  source material.
- The protected key roster, clock and store are caller-configured. Tests do
  not establish production key custody, clock quality, DNS ownership, source
  rights, persistence durability or operational independence.
- Recovery is read-only in G-01: correct configuration/store state and retry
  with a fresh nonce. Do not repair or advance state through this responder.

## Tests and evidence

All service tests use generated Ed25519 keys, a temporary fictional registry
where client verification is needed, and an in-memory store. They make no live
network call.

| Claim / test selector | What it demonstrates | Limitation |
| --- | --- | --- |
| MM-RHEAD-008 — `tests/unit/test_atomic_governed_publisher.py::test_remote_head_service_response_round_trips_through_existing_client` | Service response uses bytes accepted by the existing verifier, stays within the size bound and retains false authorization flags. | The store and keys are process-local fixtures; no HTTP transport, persistent storage or independent authority is tested. |
| MM-RHEAD-009 — `tests/unit/test_atomic_governed_publisher.py::test_remote_head_service_rejects_bad_wire_scope_and_store_failure` | Malformed query/method/path/Accept, wrong packet, missing/corrupt record and typed store outage fail closed with empty bodies. | Does not exercise request parsing in a web framework or a production database adapter. |
| MM-RHEAD-010 — `tests/unit/test_atomic_governed_publisher.py::test_remote_head_service_binds_nonce_and_snapshot_scope` | A response for a different nonce or snapshot is rejected by the existing client verifier. | A malicious service with a fresh challenge can still sign a stale claim; independent freshness is not proven. |
| MM-RHEAD-011 — `tests/unit/test_atomic_governed_publisher.py::test_remote_head_service_enforces_distinct_keys_and_bounded_clock` | Service signer cannot reuse a configured non-service ID/key; lifetime and invalid clock return/refuse bounded values. | Only the supplied key roster is checked; custody, completeness and clock trust are not established. |
| MM-RHEAD-012 — `tests/unit/test_atomic_governed_publisher.py::test_remote_head_service_translates_typed_clock_failure_without_leaking` | A typed operational clock-adapter failure returns the same empty 503 as the typed store failure, without exposing adapter details. | Uses an injected in-process fake clock; does not test a real clock service, HTTP mapping or trusted time. |
| MM-RHEAD-013 — `tests/unit/test_atomic_governed_publisher.py::test_remote_head_service_propagates_unexpected_adapter_programming_errors` | Unexpected clock/store `RuntimeError`s still propagate, preventing a broad catch from masking programming defects. | In-process exception behavior only; no future transport or production adapter is present. |

Reproduce the focused tests and existing client regressions:

```powershell
python -m pytest -q tests/unit/test_atomic_governed_publisher.py -k "remote_head_service_ or remote_challenged_head or remote_response or remote_head_distinct or remote_signed_head or remote_https_"
```

Run the exact-head local gate before review; see
[local quality gate](LOCAL_QUALITY_GATE.md). A passing test proves behavior
only for the executed local environment and the named fixtures. It is not
official CI, TLS interoperability, a live service or deployment evidence.

Run all six `test_remote_head_service_*` tests after changing the adapter error
contract. The typed clock and store tests must return empty 503 responses;
unexpected Python programming exceptions must still propagate from this
in-process boundary.

## Learning exercise

1. Read `RemoteFenceHeadResponder.respond` and predict which status is returned
   for an extra query key, a missing record and a store exception.
2. Change the nonce in `test_remote_head_service_binds_nonce_and_snapshot_scope`
   while leaving the verifier's expected nonce unchanged. Identify which
   signed field causes the client to reject the response.
3. Add the service public key to `non_service_public_keys` and predict why
   construction fails. Then remove it and explain why passing construction
   still does not prove the roster is complete.
4. Trace `_canonical_remote_message` into `_signed_wire` and compare it with
   the client parser. Which test would fail if field order or whitespace
   changed?

Expected observations: malformed wire is rejected before store access; a
store outage produces bodyless 503; the verifier checks challenge and source
scope before returning a metadata-only, non-authorizing comparison.

## Debugging and evolution

For a 400/405/406 result, inspect the exact request method, path, `Accept` and
raw query order; do not log the nonce or packet contents into shared systems.
For 404, check whether the store has a record for the requested packet and
whether it returned that same packet digest. For 503, inspect only sanitized
store availability and record schema, then reproduce with the focused test;
do not include private storage details or source rows in the response. If the
client rejects a 200 response, preserve the non-sensitive status/field names
and check configured service key, nonce, packet/snapshot digests, UTC interval
and signature against the existing client tests.

To change this service contract, start from the linked G-01 change request and
map the exact callers, verifier and tests. A future persistent implementation
must separately specify authentication, replay resistance, atomic predecessor
checks, concurrency, restart recovery and audit history (G-02/G-03). A real
deployment requires the operational review in G-04 and owner approval; this
guide is not a deployment grant.
