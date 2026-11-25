# G-01 — in-process signed current-head response

## 1. Goal in plain language

**Current behavior:** The outbound-only
[`remote_fence_head_client.py`](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py)
requests a nonce-bound signed current head, but the repository has no
service-side response implementation. PR #50 established the fixed wire
format, canonical signing domain, key separation and client verifier.

**Desired behavior:** Add a bounded, in-process responder that validates the
client's fixed `GET /v1/integrated-fence/head` request, reads one packet-scoped
current-head record through a typed storage protocol, and signs the exact
existing response format. Keep it callable without an HTTP server so tests can
exercise the complete service-to-client contract using generated keys and a
fake store.

**Why:** The accepted G-01 backlog item is the smallest next executable step
toward a server-side response. It allows negative request, scope, nonce and key
separation checks before any later persistence or deployment work.

**Out of scope:** HTTP routing/listening, authentication or ACLs, nonce
consumption, persistent or independently operated storage, atomic head
advancement, governance writes, remote deployment, capability promotion,
source permissions, publication/ingestion authorization and any WorldKernel
change. The current-head store is an interface only; tests use a fictional
in-memory implementation.

### Capability status

- Previous/proposed ledger status: no service-side capability is declared;
  this work will not add or promote an externally visible capability.
- The responder is an experimental in-process contract, not a deployed service
  or independently trusted authority.
- The existing client continues to verify canonical bytes, signature,
  configured signer, nonce, packet/snapshot scope and validity window before
  comparing the signed local registry. Service tests will call that verifier.
- `GET /v1/capabilities` remains unchanged because no route or user-visible
  runtime behavior is added.

## 2. Acceptance criteria

- [x] A shared protocol module owns the existing response type, canonical
  signing message and wire serialization; the client keeps its current import
  surface and behavior.
- [x] A typed store contract reads a current record for one packet digest; no
  database or server implementation is added.
- [x] A pure responder accepts only the fixed method, path, media type and
  canonical two-field query; malformed/duplicate/extra/encoded fields fail
  closed without echoing request data.
- [x] Valid fictional records produce a canonical response within 4096 bytes,
  signed with the existing domain and a distinct configured Ed25519 service
  key, with a caller-supplied clock and a 1–120 second lifetime.
- [x] Missing scope, store outage, corrupt/mismatched records, key reuse,
  invalid configuration, malformed request, wrong nonce and wrong packet or
  snapshot scope have regression coverage. Service failure bodies do not leak
  store exceptions or request contents.
- [x] Expected operational clock and store adapter failures have explicit
  typed error contracts and return the same generic bodyless 503; unrelated
  programming exceptions continue to propagate to the in-process caller.
- [x] The existing client verifies a response produced by the responder, and
  its resulting receipt still grants no publication, ingestion or forecast
  permission.
- [x] Update the source walkthrough, system map, debugging, learning, atlas,
  symbol catalog, evidence map, hub and task/status record; preserve the
  capability ledger/API parity because the responder is not externally
  exposed.
- [x] Focused tests and the repository's exact-head local quality gate pass;
  official CI is reported separately.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | New `RemoteFenceHeadResponder.respond` in the service module | Add an in-process call only | `test_remote_head_service_*` selectors in `tests/unit/test_atomic_governed_publisher.py` |
| Protocol | [`remote_fence_head_protocol.py`](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py); existing client exports | Extract canonical type/helpers without changing bytes | Existing `test_remote_*` client tests and service/client round-trip |
| Core implementation | New immutable head record, storage `Protocol`, typed clock/store operational errors, request/response contracts | Add; no persistent store | Normal, malformed, typed outage and scope regressions; unrelated runtime errors remain visible |
| Local generated-artifact hygiene | [`.gitignore`](../../../.gitignore) | Ignore local Graphify products so generated caches remain local and do not enter tracked-file coverage | Atlas/catalog/evidence/capability checks |
| State / persistence / API | None | No change | Capability parity remains unchanged |
| Calling components | Current outbound client | Preserve | Existing client tests and service-produced response verification |
| Downstream consumers | None | No change | No route or authorization consumer exists |
| External project/contracts | PR #50 wire format and domain | Reuse as-is | Existing verifier and canonical protocol tests |

## 4. Data, modeling and decision review

- Dataset card: not applicable; tests use only fictional digests and generated
  keys.
- Forecast model card: not applicable.
- Decision trace: no decision result or recommendation is produced.
- WorldKernel gate: not applicable; no cross-project adapter is changed.
- Temporal/data integrity: the service signs a store-supplied current-head
  claim and a short issuance interval. It does not establish that the store is
  independent, current, honest or durable.

## 5. Constraints and risks

The wire contract is compatibility-sensitive: domain, field set, canonical
JSON encoding, endpoint, request query, status, content type, byte limit and
validity window must match PR #50. The responder must not create a second
canonicalization implementation. Signing keys and protected non-service key
rosters are injected, copied at configuration time and checked for ID/public
key overlap. A responder clock is a test seam, not a trusted timestamp.

The typed store boundary is the only source of the claimed current head. A
later adapter must define transactional consistency and independent
administration; this change cannot provide either. Client nonce binding makes
an old response unusable for a fresh challenge, but the responder does not
consume nonces or prevent a dishonest store from freshly signing a stale head.

## 6. Implementation plan

1. Extract the existing canonical response primitives without changing the
   client-visible symbols or wire bytes.
2. Add the request/response, current-head and read-only store contracts plus a
   pure fail-closed responder.
3. Add generated-key/fake-store tests for valid client verification, request
   rejection, scope/nonce mismatch, signer separation, typed store/clock
   failures and propagation of unrelated programming errors.
4. Document the call flow, exact contracts, reproduction, limits, debugging
   and a learner exercise; update references and evidence selectors.
5. Run focused tests, Ruff and all local documentation checks, then the
   repository exact-head quality gate. Record official CI independently.

## 7. Evidence after implementation

- Baseline: merged main `e4f05a152aefcf68fa8ec22f3baa3b61adb8519d`; the
  starting working branch was clean at PR #60 head, and that branch remains
  preserved locally as `codex/g01-current-head-service-stacked`.
- Commit / PR: implementation commit `23bc97337d3691c5ec930c11086b45e3e2b3a940`;
  draft [PR #61](https://github.com/GustavoMFDS/MirrorMind/pull/61) targets
  `main`. The exact-head local gate passed on `9897a76d955233c35fe89d87e2df574d6e6659ce`.
- Modified symbols: `SignedRemoteFenceHead`, `_canonical_remote_message`,
  `_signed_wire`, `_parse_signed_response`, `RemoteFenceHeadStore`,
  `RemoteFenceHeadStoreError`, `RemoteFenceHeadClockError`,
  `CurrentRemoteFenceHead`, `RemoteFenceHeadRequest`,
  `RemoteFenceHeadResponse`, `RemoteFenceHeadResponder.__init__` and
  `RemoteFenceHeadResponder.respond`.
- Tests executed: the repository exact-head local quality gate passed on
  `9897a76d955233c35fe89d87e2df574d6e6659ce` at 2026-11-24 21:15 UTC:
  695 pytest tests, Ruff, symbol catalog, repository atlas, evidence map and
  capability ledger checks all passed. Pytest emitted one existing
  Starlette/httpx TestClient deprecation warning. The local receipt is kept
  under ignored `graphify-out/`; the script explicitly reports that this is
  not official GitHub Actions. The focused service/client selector had also
  passed 11 tests on the original implementation commit before rebase.
- Evidence claim IDs: MM-RHEAD-008 through MM-RHEAD-013, backed by the
  `test_remote_head_service_*` selectors in
  `tests/unit/test_atomic_governed_publisher.py`.
- Contract change: new in-process responder and storage read protocol; existing
  client wire/signature contract preserved.
- Docs: `REMOTE_FENCE_HEAD_SERVICE.md`, client guide cross-reference, system
  map, debugging, learning exercise, semantic map, repository atlas, evidence
  map, roadmap, backlog/status and generated symbol catalog.
- Known limitations: no live server, persistence, authentication, independent
  custody, nonce ledger, external integration or operational acceptance.
- Official Actions: no PR-triggered workflow run was returned when PR #61
  was inspected at creation. This is not a CI pass or failure.
- Reproduction: `.venv\Scripts\python.exe scripts/local_quality_gate.py
  --expected-head 9897a76d955233c35fe89d87e2df574d6e6659ce --receipt
  graphify-out\docs-engineering-refresh-20261124\g01-pr-quality.json`.

## Independent review correction — typed clock failure boundary

- Finding: `respond` caught `RemoteFenceHeadStoreError`, but invoked the clock
  outside a typed adapter-failure boundary. A clock outage therefore escaped
  instead of producing the documented generic response. Store adapters also
  needed an explicit rule that only expected operational failures are
  translated; broad exception catches would hide programming defects.
- Reproduction: after defining `RemoteFenceHeadClockError` and adding
  `test_remote_head_service_translates_typed_clock_failure_without_leaking`,
  the focused regression failed before the handler fix because the exception
  escaped from `respond`.
- Resolution: the injected clock contract uses `RemoteFenceHeadClockError`;
  expected store outages use the existing `RemoteFenceHeadStoreError`. Both
  return the generic bodyless 503. Other clock/store `RuntimeError`s propagate,
  as verified by `test_remote_head_service_propagates_unexpected_adapter_programming_errors`.
- Focused verification after the fix: all six `test_remote_head_service_*`
  tests passed.
- Exact integrated verification: commit
  `1847e8102a47a5ab7b0d1c66c9aa6512b7cdbf54` passed
  `scripts/local_quality_gate.py --expected-head` at
  `2026-11-25T02:50:34.876565+00:00`: 697 pytest tests, Ruff, catalog, atlas,
  evidence and capability checks all passed. The only warning is the existing
  Starlette/httpx `TestClient` deprecation. This is local evidence, not
  official Actions CI.
- Exact documented head `4931e049dcf03a7b3843bb4c12a54ea4d26b533a` also passed
  the full gate at `2026-11-25T02:52:00.508060+00:00`: 697 tests and all six
  stages. Corrected-head Actions runs `45536001576` (`test`) and
  `45536001585` (`symbol-catalog`) failed before steps; both had empty step
  lists and logs returned `BlobNotFound`. Check-run metadata records one
  annotation per check, but its text was not recovered. Do not call this head
  unannotated or infer a cause from another revision.
- The documentation snapshot `411546a9915ef82e81a5ed6723ce7292d85c3a57`
  passed the exact local gate at `2026-11-25T02:54:32.328327+00:00` with 697
  tests and all six stages. Its test run `45536284392` and symbol-catalog run
  `45536284438` failed before steps; both step lists were empty and logs
  returned `BlobNotFound`. Check-run metadata records one annotation per
  check, but its text was not recovered. No cause is inferred.
- Previously published review head `b9a8151269287b7264dc1eed0da7ed02a50202f2` passed the
  exact local gate at `2026-11-25T02:58:12.913401+00:00`: 697 tests, Ruff,
  catalog, atlas, evidence and capabilities. Receipt:
  `%TEMP%\mirrormind-pr61-final-b9a8151-quality.json`. The four Actions runs
  are `45536692432`/`45536687429` (`test`) and
  `45536692334`/`45536687419` (`symbol-catalog`). Exact annotations state
  that jobs were not started because recent account payments failed or the
  spending limit needed to be increased. This confirms the account-level
  pre-job gate on this exact head but not which condition applies; no
  repository steps ran, logs were unavailable, and no remote test result is
  claimed.
- Scope: no HTTP adapter, persistence, CAS, authentication, nonce tracking or
  independent custody was added. A future transport must map exceptions at
  its own boundary without changing the typed responder contract.
- New evidence selectors: `MM-RHEAD-012` and `MM-RHEAD-013` in
  `docs/engineering/EVIDENCE_MAP.json`.
