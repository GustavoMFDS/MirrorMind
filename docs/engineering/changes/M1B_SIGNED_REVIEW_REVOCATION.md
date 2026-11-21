# Change request — M1b signed review records and revocation

## 1. Goal

**Current behavior:** The offline [intake packet](../SOURCE_INTAKE_REVIEW.md)
binds staged CSV/XLSX bytes to declarations but cannot distinguish
what a requester asserted from what an independent reviewer attested.

**Desired behavior:** Verify independently signed, versioned and
scope-bound review events (approval/denial/revocation), including
expiry, order, chain head and a fail-closed veto after revocation.
A signed review remains **metadata only**, not data-use permission.

**Out of scope:** signing keys, authentication of reviewer employment
or legal authority, tamper-proof registry, currentness guarantee,
actual legal/license review, real data ingestion, source connectors,
new HTTP routes, publisher vintages, forecasting, or WorldKernel.

## 2. Capability status

`local_signed_source_review_history`: **experimental only**.
`evidence_and_rag` stays **planned**; no data rights or ingestion
capability is promoted. Existing CSV/XLSX and packet contracts are
unchanged; this verifier is an optional `review` dependency.

## 3. Acceptance tests

- Verify a signature against independently provisioned Ed25519 public
  key and exactly match the source packet, snapshot, format and use.
- Deny invalid and unknown keys, signature tampering, changed manifest,
  expired approval, reordered events, gaps and mismatched trusted head.
- Revoke remains terminal for the same packet, even after a subsequent
  syntactically valid signed approval.
- Missing decisions are denied. Verification requires a supplied
  `checked_on`, cannot verify freshness independently, and **never**
  returns `ingestion_authorized=true` or `forecast_eligible=true`.
- Receipts omit raw source/customer/reviewer IDs, signed event refs,
  public/private keys and credentials. All errors are generic.
- Exact-head local quality gate validates the implementation, catalog,
  atlas, evidence map, ledger and live API list consistency.

## 4. Impact map

| Layer | Implementation and effect |
| --- | --- |
| Declaration/preflight | `modules/evidence/intake_review.py`: consumed but not modified |
| New verification | `modules/evidence/review_decisions.py`: offline signatures, hash chain, revocation |
| Optional dependency | `pyproject.toml`: `[review]` Ed25519 verifier and dev tests |
| Regression evidence | `tests/unit/test_signed_source_review.py`: signed synthetic event histories |
| Capability truth | `api/routes/system.py`, `CAPABILITY_LEDGER.json`: experimental only |
| Documentation | `SIGNED_SOURCE_REVIEW.md`, system map, debugging, learning, atlas, roadmap |
| Network/identity/keys | No integration or managed trust store |
| Data/model/business | No actual ingestion, source rights, predictions or writes |

## 5. Trust risks, rollback and next gate

If the caller supplies its own signing public keys **and** current head,
it can forge an entirely valid-looking history. Therefore public-key
authorization and the current append-only head must be supplied
by a separately operated trust system. The software has no such service:
a cryptographic signature proves only possession of the matching private
key, **not** original dataset rights, legal competence, reviewer authority
or freshness. Keep `ingestion_authorized=false` even with valid events.

A future governed approval flow needs protected keys, reviewer-role
and dual-control process, key rotation/revocation, append-only
versioned registry with monotonic head publication, audited decisions,
retention enforcement and independent privacy/legal review before
actual source use. This PR does not build or assume these.

Rollback: remove the optional verifier and its experimental claim;
the prior source packet, workbook/CSV parsing and API validation remain
compatible. Run the full local gate on exact PR HEAD, and record whether
GitHub Actions actually ran (do not call an owner-approved local gate CI).
