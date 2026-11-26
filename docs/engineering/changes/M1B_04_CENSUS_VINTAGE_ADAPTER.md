# Change request — prepare a synthetic aggregate vintage selector

## 1. Goal in plain language

**Current behavior:** The repository contains the owner-approved Census/ALFRED
research protocol, but no Census vintage adapter in `src/` or tests. The UCI
pilot in `uci_event_time.py` deliberately uses event dates and cannot model
publication-time revisions.

**Desired behavior:** Add a pure, bounded local adapter over normalized
aggregate vintage records. Given one series and an exclusive target-release
date, select the latest record for each reference month published strictly
before that date. Preserve the source release ID, release kind and snapshot
digest for replay. Same-day ambiguity, duplicate records and invalid metadata
must fail closed. Empty history remains empty; it is never zero-filled.

**Why:** The second approved research lane needs a testable point-in-time
selection rule before any Census/ALFRED bytes are reviewed or acquired. A
synthetic adapter can prove the date and revision contract without making a
source-rights, completeness or forecasting claim.

**Out of scope:** Network requests, Census or FRED/ALFRED file/API parsing,
credentials, real-data access, rights authorization, forecast scoring,
baseline comparison, HTTP exposure, capability promotion and WorldKernel.

## Capability status change

- Previous and proposed status: no public capability is added or promoted.
- Production behavior versus interface/experiment-only: pure local
  experimental selection over caller-supplied synthetic records only.
- Tests: `tests/unit/test_census_vintages.py` covers the exclusive cutoff,
  revisions, abstention, duplicate/conflicting metadata and receipt limits.
- `GET /v1/capabilities` remains unchanged; no route or public capability is
  added.

## 2. Acceptance criteria

- [x] Immutable versioned records represent one aggregate series, a month
  reference period, published date, release kind/ID, Decimal value and
  64-digit source snapshot digest.
- [x] The selector uses only `published_on < target_release_on`; a same-day
  observation is not treated as available when timestamp precision is only a
  date.
- [x] The latest eligible revision is selected independently for each
  reference month, with its release ID/kind/digest preserved.
- [x] Missing months remain missing; no zeros or synthetic releases are
  invented.
- [x] Invalid values, unsupported release kinds, ambiguous duplicate period
  dates, conflicting release metadata, mixed series and over-limit inputs are
  rejected.
- [x] The result marks source provenance unverified and both
  `ingestion_authorized` and `forecast_eligible` false.
- [x] Automated tests use only generated records; the adapter performs no
  filesystem/network access and does not read a credential.
- [x] Technical/learning docs, synthetic fixture card, architecture and atlas
  links explain the exact behavior, limitations and reproduction steps.
- [x] The six-check exact-head local gate passes with the optional reviewed
  WorldKernel pin installed; no test is skipped.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | None | No | No CLI/API surface |
| Core implementation | `domains/retail/census_vintages.py::select_census_vintage_as_of` | Yes | Pure unit regressions in `tests/unit/test_census_vintages.py` |
| State / persistence / API | None | No | No writes, route, file read or network client |
| Calling components | Future aggregate evaluation only | No caller yet | Current tests invoke the function directly |
| Downstream consumers | Synthetic research protocol and backlog | Docs only | No forecast consumer or capability promotion |
| External project/contracts | Census/ALFRED source formats | No | Normalized MirrorMind contract only; source-specific parser remains gated |

## Data, modeling and decision review

- Dataset card: added synthetic Census-vintage fixture card; it contains only
  invented values. Real source bytes, rights and retention are not reviewed.
- Forecast model card: not applicable; this change selects vintages and does
  not forecast or score outcomes.
- Decision trace: no recommendation or operational action is produced.
- WorldKernel compatibility gate: not applicable.
- Temporal leakage: same-day and after-cutoff publications are excluded;
  records carry publication date separately from reference month. Tests mutate
  the release order and preserve later revisions as unavailable.

## 4. Constraints and risks

The input is a normalized in-memory contract, not an official Census or ALFRED
parser. A 64-character digest is syntax-checked but source bytes are not
available to verify it. Date-only publication metadata cannot order two
releases on the same day, so ambiguous entries reject instead of guessing.
The returned source state is caller-supplied and remains explicitly
unverified; this is not an authorization boundary. Only synthetic fixtures
are used until B-01/B-02 approvals and the exact source archive are reviewed.

## 5. Implementation plan

1. Trace the Census protocol, UCI event-time adapter, retail release contracts
   and existing test conventions.
2. Add failing tests for same-day leakage, revision selection, missing history
   and invalid/ambiguous metadata.
3. Implement the smallest pure bounded selector and immutable result type.
4. Add a synthetic dataset card and source walkthrough with sequence diagram,
   typed contract, examples, tests, privacy boundary, diagnostics and exercises.
5. Update system map, learning, debugging, task backlog, evidence map and
   repository atlas; regenerate the symbol catalog from source.
6. Run the focused suite and exact-clean-head six-check local gate with the
   reviewed WorldKernel pin installed. Report local evidence separately from
   GitHub Actions.

## 6. Historical initial implementation evidence

- Commit / PR: local branch `codex/m1-census-vintage-adapter`, stacked on
  reviewed PR #62 head `777c2d2`; source/docs commit `97fb0ff046a13fa0364324adf5936504f7b15cb1` is not pushed and has no PR.
- Modified symbols and files: `CensusVintageRecord`, `CensusVintageView`,
  `_validate_record` and `select_census_vintage_as_of` in
  `src/mirrormind/domains/retail/census_vintages.py`.
- Tests executed, result, environment: focused suite passed (11 tests), then
  the complete exact-head gate passed on `97fb0ff046a13fa0364324adf5936504f7b15cb1`
  with Python 3.13.5 and WorldKernel `0.0.1` installed from source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`: 843 passed, zero skipped;
  Ruff, catalog, atlas, evidence and capability checks passed. One existing
  Starlette/httpx TestClient deprecation warning appeared. Receipt:
  `results/local-quality-gate-97fb0ff046a13fa0364324adf5936504f7b15cb1.json`.
  GitHub Actions was not checked by the local gate.
- Claim IDs and cited test path/function: `MM-CEN-001` cites
  `tests/unit/test_census_vintages.py::test_selects_latest_revision_per_month_strictly_before_target_release`;
  `MM-CEN-002` cites
  `tests/unit/test_census_vintages.py::test_same_day_first_estimate_is_excluded_and_receipt_is_unverified`.
- Evidence/provenance/cutoff and uncertainty: synthetic records only;
  publication dates are day-granular and source bytes are unavailable.
- Scope of human review and approval: synthetic pilot preparation only; no
  real source acquisition/processing permission.
- New or changed contracts: `mirrormind.census.aggregate_vintage_view.v1`.
- Docs updated: adapter guide, synthetic dataset card, change request,
  protocol, system map, debugging, learning, evidence map, semantic map,
  repository atlas, backlog, project status and handoff.
- Known limitations / follow-up: source-specific adapter, rights, privacy,
  retention, historical archive completeness, target cross-checks and temporal
  evaluation remain gated by B-01/B-02.
- Independent explanation: the tests prove local selection and rejection
  semantics for normalized generated records. They do not prove a source parser,
  source-byte digest, rights, completeness or forecast quality.
- Final documentation follow-up: the validation result above is bound to the
  exact source/docs commit shown. A later documentation-only evidence update
  requires its own exact-head receipt; the receipt itself is keyed by the tested
  SHA so the tested tree is not edited after validation.

## Current main synchronization — 2026-11-26

The candidate is now on `codex/m1-census-vintage-adapter`, descended from the
merged PR #62 baseline. Merge commit
`55e91f7d73c67867edaf1aa790242f6cdbc611b9` has the previous Census head
`da540a2ba48c90107ba846da582a6561946abe9c` as first parent and exact main
`a456034c55ed7634ad4768b26788fec09dab1d08` as second parent. This preserves
both histories and does not cherry-pick duplicate work.

The exact merged candidate passed the full local six-check gate at
`2026-11-26T03:58:32.075461+00:00`: 877 tests, zero skips, Ruff, symbol
catalog, atlas, evidence and capability checks. WorldKernel `0.0.1` was
installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-55e91f7d73c67867edaf1aa790242f6cdbc611b9.json`.
This is synthetic local evidence; Actions were not checked, and no source
parser, real bytes, credential or permission is added. The current
documentation-inclusive follow-up needs its own exact-head gate before a
separate PR is published.

## Independent review follow-up — publication cannot precede period close

The normalized selector checks revision chronology against a known first
estimate, but accepts a first-estimate publication dated inside its own
reference month. A public evaluator reproduction scored such records as
available observations. That is impossible for the approved Advance Monthly
Retail Trade Series: the Census Bureau says its advance estimates are released
about ten business days after the reference month closes. The selector must
enforce the weaker, source-neutral calendar invariant that every normalized
release date is on or after the first day following its reference month. It
does not infer or authenticate the actual scheduled release day.

### Acceptance criteria

- [x] Reject first estimates and revisions with `published_on` before the
  reference month closes; accept a release dated on the first day of the next
  month as the lower-bound boundary case.
- [x] Reproduce the false-scoring case through the public Census evaluator and
  prove it fails through the shared selector validation.
- [x] Keep the selector pure, bounded, date-only and synthetic; do not add
  source calendars, file/network reads, authorization or empirical claims.
- [x] Explain the invariant, its source-specific motivation, the exact tests,
  and the limit that valid chronology does not authenticate a publisher.
- [x] Regenerate the catalog and pass the exact six-check local gate on the
  final clean PR head with the reviewed optional WorldKernel pin.

### Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Core contract | `domains/retail/census_vintages.py::_validate_record` | Yes | Selector regressions reject in-month releases and accept next-month boundary |
| Consumer | `domains/retail/census_evaluation.py::evaluate_census_vintage_backtest` | No algorithm change | Public evaluator regression reproduces prior false scoring and now rejects |
| API, persistence, source access | None | No | No route, I/O, credential or authorization surface |
| Documentation | Census adapter/evaluation/protocol, system map, debugging, learning and evidence map | Yes | Source guide and exact top-level pytest selector linked in the evidence ledger |
| Compatibility | `mirrormind.census.aggregate_vintage_view.v1` | Validation tightened; result shape unchanged | The only in-repository consumers are the synthetic evaluator and tests; invalid pre-period records now fail closed |

The Census methodology is linked in the protocol and guide as the reason for
the invariant. The implementation accepts any date after the reference month
as a valid normalized lower bound; the real MARTS schedule, release identity,
source bytes and rights still require separate review.
