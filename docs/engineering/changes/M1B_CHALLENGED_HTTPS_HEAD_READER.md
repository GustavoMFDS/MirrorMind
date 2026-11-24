# Change request — MM-M1b challenged HTTPS current-head read (experimental)

## Goal and confirmed history
PR #49 added an **additional local SQLite file** storing bounded signed
dual-witness combined-state transitions, but no independent current-head
feed. Even two locally intact signed databases can be rolled back
together. PR #47 offers an offline verifier for separately pinned
current heads; PR #48 offers offline continuity and fork classification.

Implement a narrow opt-in **read-only HTTPS client** to request a fresh
signature over a current fence-head sequence and digest from a
configured external service endpoint. Verify a cryptographically
unpredictable client nonce, short UTC validity, distinct service Ed25519
public key and exact source-review packet. Compare the signed head
against the **separately stored signed registry**, which in turn
verifies the local governed publisher's signed state.

The client does NOT build, deploy, operate, register, authenticate or
attest an independent server. A malicious/compromised service can sign
an old head, so proof of operational independence still requires
separate custody, operators, audit and head-publication protocol.

## Acceptance and fail-closed boundaries
- Fixed `https://<fully-qualified-dns>/v1/integrated-fence/head`
  endpoint configured by trusted local code. No userinfo, IP literals,
  extra paths, redirects, insecure TLS, arbitrary query, secret headers
  or HTTP. Use system TLS certificate validation, bounded response bytes,
  explicit timeouts and JSON `application/json` content type.
- Generate a new 32-byte OS-random hex nonce per read. Send only
  `?nonce=<hex>&packet_sha256=<hex>`; the packet digest selects the
  source-specific remote head, without forwarding rows, private keys or tokens.
- Require canonical JSON without duplicate/unknown/missing fields:
  domain-separated Ed25519 signature covers service identity, key ID,
  nonce, packet/snapshot SHA-256, authority sequence, exact current
  fence digest, issued/expiry seconds in UTC, and the request endpoint
  identity. Strictly require a 1–120s validity interval, no expired or
  future-issued responses. A client-supplied clock is **not** an
  independent time authority; the network path uses the device UTC clock.
- Validate `service_id`, known service-key roster (1..8 entries),
  separate signing role from fence authority/witness keys by key ID
  **and key bytes**, packet scope and exact nonce equality.
- Refuse replayed response from a prior nonce, forged signature,
  stale signer key, future/expired time, wrong packet, wrong service,
  mismatched current signed fence, unavailable endpoint, redirect,
  invalid TLS/network response, oversized/duplicated JSON.
- Compare remote authenticated signed current state against
  `LocalIntegratedFenceRegistry.compare_local`: preserve its signature
  replay and local publisher comparison. Do not mutate stores or expose
  a network endpoint. Report `publication_authorized=false`,
  `ingestion_authorized=false`, `forecast_eligible=false`.
- Tests operate entirely on fictional data and generated Ed25519 keys,
  with a fake response transport. No actual external authority or
  network service is contacted or claimed deployed.
- Maintain existing signed command, SQLite, file and remote API paths.
  No automatic retries on mismatches or bypass during outages.

## Explicit non-goals and risks
The client authenticates a **specific response to its nonce**, not the
current world's one true head. A signer's compromised/colluding key,
wrong system clock, TLS/PKI or DNS control, stale signer service view,
unseen forks, external availability, server authz and operator identity
are not resolved. HTTPS alone does not prove separate hosting/ownership.
There is no remotely operated service or read-before-write admission;
a read-only check before a later local publish would be TOCTOU.
Do not claim real UCI/M5 ingestion rights, forecasts or production CI.

## Confirmed impact map
| Surface | Change |
| --- | --- |
| `src/mirrormind/modules/evidence/remote_fence_head_client.py` | New nonce-bound signed HTTPS reader and verifier |
| `tests/unit/test_atomic_governed_publisher.py` | Generated-key remote-fence tests using a fake response |
| `src/mirrormind/api/routes/system.py` | Experimental capability entry only, no HTTP execution |
| `docs/engineering/REMOTE_FENCE_HEAD_CLIENT.md` | Signature protocol, clock/transport and custody caveats |
| `docs/engineering/{SYSTEM_MAP,DEBUGGING,LEARNING,REPOSITORY_ATLAS}.md` | Data flow, runbooks, reviewed links |
| `docs/engineering/{EVIDENCE_MAP,CAPABILITY_LEDGER}.json` | Narrow test-backed truth status |
| `docs/engineering/generated/SYMBOLS.md` | Regenerate from code |
| `docs/ROADMAP.md`, `docs/engineering/README.md` | Incremental project state |

Rollback: remove new optional module and experimental capability;
no database or signed message migrations. Next step after this scope:
explicitly operated, independently administered current-head service.
