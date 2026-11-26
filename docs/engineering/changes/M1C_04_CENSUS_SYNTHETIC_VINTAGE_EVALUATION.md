# Change request — evaluate fixed forecasts on synthetic Census vintages

## 1. Goal in plain language

**Current behavior:** The local Census lane can choose an as-of vintage from
normalized records, but it cannot form a forecast input or compare that input
with a later first estimate. The selector is covered by
`tests/unit/test_census_vintages.py`.

**Desired behavior:** Add a pure, bounded evaluator that takes an explicit,
chronological set of synthetic forecast origins. At each origin it selects the
latest monthly vintage strictly before issuance, then compares fixed lag-12
seasonal-naive and trailing-12-month-mean forecasts at horizons 1, 3 and 6
against the target month's first estimate. Require complete 12-month history;
keep missing history and missing/future targets as abstentions. Report
privacy-limited per-origin lineage and matched MAE, RMSE and zero-safe WAPE.

**Why:** The approved second pilot is about publication-time knowledge and
revisions, not transaction event time. A synthetic evaluator can exercise the
chronological mechanics while retaining the boundary that its invented
releases do not establish source rights, archive coverage or real forecast
quality.

**Out of scope:** Census/FRED/ALFRED parsers, network access, credentials,
real data, rights decisions, model fitting/tuning, uncertainty calibration,
capability promotion, HTTP/API exposure and operational decisions.

## Capability status change

- No public capability is added or promoted.
- The evaluator is a local experimental utility over fictional normalized
  records; it is not a production forecast endpoint.
- Curated claims MM-CEN-003 through MM-CEN-006 are recorded in the evidence
  map; they establish only synthetic as-of selection, fixed-baseline arithmetic
  and abstention behavior.
- `GET /v1/capabilities` remains unchanged.

## 2. Acceptance criteria

- [x] Immutable origin contracts bind a first-estimate reference month to an
  exact date-only issuance cutoff; origins are unique, ordered and bounded.
- [x] Only the fixed horizons 1, 3 and 6 months are evaluated.
- [x] Every origin uses records with `published_on < issued_on`; any selected
  reference month after the origin is rejected as contradictory future input.
- [x] Forecast labels are the unique first-estimate record for each target
  month; missing labels and labels already published at issuance abstain.
- [x] Seasonal naive reads the target's lag-12 month from the selected vintage;
  trailing mean uses 12 consecutive reference months ending at the origin.
- [x] Both baselines score on identical target origins; incomplete monthly
  history is never filled with zero. Fewer than two matched origins yields
  null metrics rather than a winner or score claim.
- [x] MAE, RMSE and WAPE are computed on matched first-estimate labels; WAPE is
  null when the actual-value denominator is zero.
- [x] Results omit values and forecasts, preserve target release lineage, and
  bind the normalized input and each as-of view to deterministic SHA-256
  fingerprints that do not imply byte verification or source authenticity.
- [x] Generated records alone cover normal behavior, later-revision
  noninterference, same-day exclusion, missing history, target abstention,
  ambiguity and metric edge cases.
- [x] A source walkthrough, synthetic model card, dataset card, architecture,
  learning/debugging notes, atlas and evidence map explain the code and limits.
- [x] The six-check exact-head local gate passes with the reviewed WorldKernel
  pin installed and no skipped tests; official Actions remain separate.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | examples/m1_census_vintage_evaluation.py | Example only | Integration tests run deterministic synthetic validation and holdout commands |
| Core implementation | `domains/retail/census_evaluation.py::evaluate_census_vintage_backtest` | Yes | Unit tests compare fixed synthetic monthly origins |
| State / persistence / API | None | No | No filesystem, network, database or API access |
| Calling components | `census_vintages.py::select_census_vintage_as_of` | Reuse only | Existing selector tests plus evaluation regressions |
| Downstream consumers | Aggregate Census research protocol | Docs only | No consumer outside the offline evaluator |
| External project/contracts | Census, FRED and ALFRED | No | Existing normalized MirrorMind contract only |

## Data, modeling and decision review

- Dataset card: generated monthly values only; source-rights and retention gates
  remain unresolved.
- Forecast model card: fixed lag-12 and trailing-12 heuristics; synthetic
  temporal origins only; no empirical or uncertainty claim.
- Decision trace: not applicable; no recommendation or operational action.
- WorldKernel compatibility gate: not applicable; this is an aggregate
  statistical baseline evaluator, not a simulation request.
- Temporal leakage controls: strict publication cutoff, origin reference-month
  ceiling, first-estimate labels, later-revision noninterference and explicit
  missing-history abstention.

## 4. Constraints and risks

The issue schedule and monthly values are caller assertions. Input and
as-of-view digests fingerprint normalized records only; they do not verify the
source snapshot digest strings or authenticate a publisher. The evaluator
requires complete consecutive monthly history and can abstain heavily on a
real archive. Real evaluation still requires the B-01/B-02 reviews, approved
source artifacts, frozen chronological origins and external first-release
cross-checks. Metrics on fictional values are arithmetic demonstrations only.

## 5. Implementation plan

1. Reuse the normalized vintage selector and inspect existing baseline metric
   semantics; do not reimplement data acquisition.
2. Add failing tests for fixed horizons, as-of vintage selection, revision
   noninterference, target lineage, missing history, target leakage and
   zero-safe metrics.
3. Implement the smallest pure bounded evaluator and immutable origin type.
4. Add an explanatory guide/model card and update the protocol, dataset card,
   system map, atlas, debugging, learning, semantic coverage and evidence map.
5. Regenerate the symbol catalog and run the focused suite plus the complete
   exact-head local gate with WorldKernel installed.

## 6. Evidence after implementation

- Commit / PR: implementation commit
  `ce446496616d20a782e0ebcb7e7b0f42cec49e83` on local-only branch
  `codex/m1-census-vintage-adapter`, based on consolidated PR #62 review head
  `777c2d2e3598f1eb06e2ae3b972428adfc7e718e`; no push or separate PR while the
  consolidated candidate awaits review.
- Modified symbols: `CensusForecastOrigin`,
  `evaluate_census_vintage_backtest`, `_month_offset`, `_record_payload`,
  `_manifest_sha256`, `_selection_receipt`, `_metric_values`, `_metrics`,
  `build_synthetic_records` and `run_synthetic_evaluation`.
- Tests executed, result, environment: focused evaluator, selector and CLI
  suite — 28 passed on Python 3.13.5. Exact-head local gate on the clean
  implementation commit passed at 2026-11-25 23:16:44 UTC: 860 passed, no
  skipped tests, and pytest, Ruff, catalog, atlas, evidence and capability
  checks all passed. One existing Starlette/httpx TestClient deprecation
  warning appeared. WorldKernel was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
  `results/local-quality-gate-ce446496616d20a782e0ebcb7e7b0f42cec49e83.json`.
  This is local evidence, not official GitHub Actions.
- Claim IDs and cited test path/function:
  - MM-CEN-003 —
    `tests/unit/test_census_vintage_evaluation.py::test_fixed_horizons_use_asof_vintages_and_matched_first_estimates`.
  - MM-CEN-004 —
    `tests/unit/test_census_vintage_evaluation.py::test_later_revision_does_not_change_any_prior_origin_score`.
  - MM-CEN-005 —
    `tests/unit/test_census_vintage_evaluation.py::test_incomplete_trailing_history_abstains_without_filling_months`.
  - MM-CEN-006 —
    `tests/integration/test_census_vintage_evaluation_cli.py::test_synthetic_validation_and_holdout_cli_are_reproducible_and_disjoint`.
- Evidence/provenance/cutoff and uncertainty: fictional values and declared
  release dates only; no empirical claim.
- Scope of human review and approval: owner-approved synthetic pilot
  preparation; real source access/processing remains unauthorized.
- New or changed contracts: local result schema
  `mirrormind.census.vintage_backtest.v1`; immutable date-only forecast origin;
  no public API or capability change.
- Docs updated: Census vintage adapter/protocol, source walkthrough, synthetic
  dataset and model cards, system/semantic maps, learning/debugging guides,
  atlas, evidence map, backlog, project status and handoff.
- Known limitations / follow-up: Census/ALFRED parsing, rights, coverage,
  real release verification, retention and empirical review remain blocked;
  GitHub Actions remains unavailable under B-08.
- Independent explanation: trace `evaluate_census_vintage_backtest` from
  normalized-record validation through each origin's strict as-of view, target
  matching, abstention and aggregate metrics; reproduce both splits with the
  linked CLI commands in the source walkthrough.

## 7. Independent review follow-up — numeric determinism and release chronology

**Reproduced review findings:** On the same synthetic inputs and origin
schedule, changing the ambient Decimal precision from its default to precision
2 changes the trailing-mean metric despite an identical normalized-input
fingerprint. A monthly revision whose publication date precedes the known
first-estimate publication is currently accepted into the historical feature
view. Finite values at extreme magnitudes can also make float metrics overflow
to infinity or underflow a positive result to zero.

Before the fix, `python -m pytest tests/unit/test_census_vintage_evaluation.py
-q` reproduced 10 failures against 15 passing tests: context-dependent metrics,
both invalid revision dates, missing unanchored-revision accounting, three
unsupported numeric domains, WAPE overflow and positive-metric underflow. The
selector also returned the pre-first-estimate revision as the newest vintage.

**Correction scope:** Keep all Census changes on the local descendant branch,
separate from consolidated PR #62. Use context-independent exact arithmetic
for fixed means and aggregate metrics; bound Decimal coefficient precision and
exponents; reject metric conversions that are non-finite or underflow a
nonzero exact result. If a month has a first-estimate record, require each
revision date to be strictly later because timestamps are date-only. If the
first-estimate release is absent, treat that month's revisions as unanchored:
exclude them from the evaluator's feature vintage, count the excluded records
in the result and allow the resulting history gate to abstain. This does not
authenticate an archive or assert that an incomplete source has no earlier
publication. Because the new count changes the result envelope, advance the
experimental result contract to
`mirrormind.census.vintage_backtest.v2`; repository search found no other
consumer of the unmerged v1 result. No external v1 compatibility is inferred.

### Follow-up acceptance criteria

- [x] Replaying identical records and origins under low precision and alternate
  Decimal rounding modes returns identical fingerprints and metrics.
- [x] A revision earlier than, or on the same date as, a known first estimate
  is rejected; a later revision remains eligible under the date-only contract.
- [x] Revisions without a first-estimate anchor are excluded from forecast
  features, counted in the result, and cannot prevent missing-history
  abstention.
- [x] Public evaluator calls reject unsupported coefficient/exponent domains,
  non-finite metric conversions and positive exact metrics that would underflow
  to zero; output contains no `Infinity`, `NaN` or fabricated zero.
- [x] RMSE scales the exact mean-square before float conversion, so an
  intermediate underflow does not reject a representable final result; true
  final underflow still fails closed.
- [x] Public evaluation regressions reproduce the reviewed `1e150` / `1e-300`
  WAPE overflow and tiny-positive metric underflow cases.
- [x] A public regression confirms RMSE near `1e-200` stays representable while
  its exact mean-square lies below float range.
- [x] The result uses `mirrormind.census.vintage_backtest.v2` and reports the
  count without changing the M1 API or capability ledger.
- [x] The Census guide, model card, learning exercise, debugging notes, system
  map, atlas and evidence map explain the revised arithmetic and archival
  boundaries.
- [ ] Full exact-head local gate passes on the descendant with WorldKernel
  pinned and no skipped tests; no official Actions claim is made.

| Layer | Follow-up impact | Evidence |
| --- | --- | --- |
| Evaluator | Exact rational mean/metrics, numeric-domain validation, scaled RMSE conversion and v2 result with unanchored count | `tests/unit/test_census_vintage_evaluation.py` public-call regressions |
| Vintage selection for evaluator | Validate first-estimate/revision chronology and omit unanchored revisions from the feature view | `test_revision_before_known_first_estimate_is_rejected`, evaluator chronology and incomplete-anchor abstention tests |
| CLI / serialized result | Add explicit unanchored-revision count; preserve schema safety and synthetic-only flags | CLI replay, v2/count assertions and non-finite JSON rejection |
| API / capability ledger / source access | No change | Existing API and capability checks; no file/network or source ingestion |
| Documentation | Explain exact arithmetic, numeric bounds, revision chronology, abstention and reproduction | Census source walkthrough, model card, learning/debugging, system/semantic maps and evidence selectors |
