# Synthetic Census vintage baseline evaluation

## Purpose and status

This guide explains the next executable slice of the aggregate Census/ALFRED
research lane: use only the release vintage visible at each declared origin,
compare two fixed monthly baselines at three horizons, and score only against
later first-estimate labels. The code is experimental and runs only on
caller-supplied normalized records. It does not fetch Census or FRED/ALFRED
data, parse a publisher file, authorize ingestion, or establish forecast skill.

The method is separate from the UCI event-time pilot. UCI InvoiceDate is a
transaction event date and cannot supply the publication dates required by
this evaluator. The owner-approved source sequence remains UCI first, then
aggregate Census/ALFRED; only the synthetic mechanics are runnable while
B-01/B-02 remain open.

## Architecture and data flow

<pre><code>
Synthetic records and fixed origins
    -> evaluate_census_vintage_backtest
    -> select_census_vintage_as_of for each issue date
    -> latest eligible revision per reference month
    -> first-estimate target matching and 12-month history gate
    -> lag-12 and trailing-12 predictions on matched targets
    -> per-horizon metrics plus sanitized lineage receipt
</code></pre>

| Component | Responsibility | Trust boundary |
| --- | --- | --- |
| CensusForecastOrigin | Freezes a reference month and date-only issue boundary | Caller-declared schedule; not an authenticated release calendar |
| select_census_vintage_as_of | Validates normalized records and chooses the newest eligible release per month | Digest syntax is checked; source bytes and rights are not |
| evaluate_census_vintage_backtest | Applies fixed horizons/baselines, target matching, abstention and receipt generation | No fitting, tuning, I/O, route, persistence or operational authority |
| examples/m1_census_vintage_evaluation.py | Builds an in-memory fictional series and exposes disjoint validation/holdout origin sets | No file or network source |
| tests/unit/test_census_vintage_evaluation.py | Reproduces temporal, metric, rejection and abstention behavior | Every value is invented |
| tests/integration/test_census_vintage_evaluation_cli.py | Runs the example twice and checks deterministic JSON, split separation and minimization | Does not validate a live source or publication schedule |

The evaluator reuses the selector rather than implementing another date filter.
At each origin, selected releases are fingerprinted; training never reads a
record whose reference month is after the declared origin. A future reference
month is allowed in the selected view only when it is one of the requested
targets and its first-estimate label is already published; that horizon
abstains instead of turning the observed target into a forecast.

## Contract and baseline semantics

The local function contract is:

<pre><code>
evaluate_census_vintage_backtest(
    records: tuple[CensusVintageRecord, ...],
    *,
    series_id: str,
    origins: tuple[CensusForecastOrigin, ...],
    split: Literal["validation", "holdout"],
) -> dict[str, object]
</code></pre>

Each immutable origin contains a first-of-month reference period and a
date-only issue boundary:

<pre><code>
@dataclass(frozen=True, slots=True)
class CensusForecastOrigin:
    reference_month: date
    issued_on: date
</code></pre>

Origins must be a bounded, nonempty tuple of at most 250 exact values. Their
reference months must be unique and chronological, and their issue dates must
increase. Each origin needs one first-estimate record published strictly
before issue. Each target month must have at most one first-estimate label.
Duplicate labels, mixed series, ambiguous (reference_month, published_on)
records, invalid release metadata and any release published on the issue date
are rejected or excluded by the selector.

For origin reference month o and horizon h in the fixed set {1, 3, 6}, the
target reference month is t = o + h calendar months. At issue time:

1. Select the newest release for each reference month where published_on is
   strictly before issued_on. Same-day vintages are unavailable because
   intraday order is not represented.
2. Require one first-estimate label for target month t, published after
   issued_on. A missing label or one already published by issue is an
   abstention; later monthly/annual revisions never replace the primary label.
3. Require all 12 consecutive months ending at o in the selected vintage.
   Missing periods remain absent; neither baseline inserts zero.
4. Forecast with two fixed, untuned heuristics:

   - seasonal_naive_lag12: the selected value for month t minus 12 months.
   - trailing_12_month_mean: arithmetic mean of the 12 selected months ending
     at o, held constant for that horizon.

Both forecasts use the same first-estimate labels. Per horizon, metrics are
reported only with at least two matched origins:

- MAE is mean absolute error.
- RMSE is the square root of mean squared error.
- WAPE is total absolute error divided by total actual value; it is null when
  the actual denominator is zero.
- Coverage is scored origins divided by requested origins. Abstentions retain
  distinct reasons.

Metric output converts Decimal amounts to finite floats and rejects absolute
values above 1e150 so squared errors remain representable. This is a numerical
safety bound, not a source-unit or Census-series definition. The result reports
no model winner and never returns observation values or predictions.

## Result and replay receipt

The versioned result, mirrormind.census.vintage_backtest.v1, contains the
selected split, series, requested origin count, fixed horizons, per-origin
audit, per-horizon metrics, abstention counts and false
ingestion_authorized/forecast_eligible flags. Each origin audit records a
compact selector receipt with the selected-row count and an as-of vintage
fingerprint; it does not repeat every release ID and digest. Each target entry
records its publication date, release ID and caller-supplied source digest
string. The top-level input fingerprint binds all normalized records using
canonical JSON.

These fingerprints bind supplied normalized rows for deterministic replay.
They do not hash or verify official source bytes, establish a legal grant,
prove archive completeness, make low-entropy data anonymous or replace an
approved manifest. Release identifiers and digest strings are still metadata;
review before logging or publishing any future real-source receipt. The
example includes only fictional IDs and values.

## Reproducible example

From the repository root, run:

<pre><code>
.\.venv\Scripts\python.exe -m examples.m1_census_vintage_evaluation --split validation
.\.venv\Scripts\python.exe -m examples.m1_census_vintage_evaluation --split holdout
.\.venv\Scripts\python.exe -m pytest -q tests/unit/test_census_vintage_evaluation.py tests/integration/test_census_vintage_evaluation_cli.py
</code></pre>

The example constructs 21 monthly first estimates and one fictional November
revision entirely in memory. Validation origins are December 2020 and January
2021; holdout origins are February and March 2021. The two origin sets do not
overlap. A generated monthly release occurs on the 15th of the following
month, and the forecast issue date is after the origin's first estimate. These
dates are demonstration fixtures, not Census dates. Each split emits two
matched origins for horizons 1, 3 and 6, so the result contains arithmetic
metrics. Repeated validation execution emits identical JSON.

The observed metrics are computed from invented values and are not a result
about RSAFS, Census publications, retail demand or real forecast accuracy.
The tests assert exact behavior and boundary conditions; the example does not
authorize, download, store or submit any real source values.

## Regression evidence

The curated evidence-map claims are MM-CEN-003 for fixed-horizon matched
metrics, MM-CEN-004 for later-revision noninterference, MM-CEN-005 for
missing-history abstention and MM-CEN-006 for deterministic split replay.
Each claim cites the real top-level test selector and states what the fixture
cannot establish.

| Selector | What it demonstrates | Limitation |
| --- | --- | --- |
| tests/unit/test_census_vintage_evaluation.py::test_fixed_horizons_use_asof_vintages_and_matched_first_estimates | Fixed horizons, visible-vintage selection, paired metrics, output minimization and release lineage | The series and dates are generated, not an authentic archive |
| tests/unit/test_census_vintage_evaluation.py::test_revision_published_before_origin_changes_only_that_asof_vintage | A revision before the second origin changes that origin's vintage fingerprint and matched scores, not the earlier origin | Does not authenticate publication timestamps |
| tests/unit/test_census_vintage_evaluation.py::test_later_revision_does_not_change_any_prior_origin_score | A later historical revision cannot rewrite earlier as-of metrics or receipts | One fixed synthetic schedule only |
| tests/unit/test_census_vintage_evaluation.py::test_same_day_revision_is_excluded_from_date_only_origin | Same-day publication is excluded from the issue cutoff | No intraday ordering is available |
| tests/unit/test_census_vintage_evaluation.py::test_incomplete_trailing_history_abstains_without_filling_months | A missing month yields abstention rather than imputed zero | Does not prove a real archive is complete |
| tests/unit/test_census_vintage_evaluation.py::test_missing_first_estimate_target_abstains_and_minimum_count_is_two | Missing target and fewer than two paired origins produce null metrics | No statistical significance or winner selection |
| tests/unit/test_census_vintage_evaluation.py::test_zero_actual_denominator_produces_null_wape | WAPE is undefined when total first-estimate actuals are zero | Fixture-only arithmetic |
| tests/unit/test_census_vintage_evaluation.py::test_target_already_published_at_issue_is_not_scored | Earlier or same-day target releases are not scored as future outcomes | Date-only boundary cannot order events within a day |
| tests/unit/test_census_vintage_evaluation.py::test_future_reference_rows_outside_requested_targets_fail_closed | An unrelated future reference period in an as-of vintage is rejected | Does not validate source-specific revision rules |
| tests/unit/test_census_vintage_evaluation.py::test_origins_must_be_unique_chronological_and_split_is_explicit | Duplicate/out-of-order origins and undeclared split labels fail | The caller still chooses the frozen schedule |
| tests/unit/test_census_vintage_evaluation.py::test_origin_count_budget_is_enforced_before_evaluation | Evaluation origin work is bounded before processing | Does not benchmark runtime |
| tests/unit/test_census_vintage_evaluation.py::test_metric_range_rejects_values_that_cannot_be_scored_safely | Non-finite metric conversions are rejected | The numeric bound is not a source-unit contract |
| tests/integration/test_census_vintage_evaluation_cli.py::test_synthetic_validation_and_holdout_cli_are_reproducible_and_disjoint | Example command output is deterministic and validation/holdout origins are disjoint | A generated split is not a locked empirical holdout |
| tests/integration/test_census_vintage_evaluation_cli.py::test_synthetic_census_cli_rejects_unknown_split | The command rejects an unreviewed split name without printing fixture values | No production CLI surface is added |

The focused selectors above are run by the repository's full pytest gate. The
exact-head local receipt also includes Ruff, generated symbol catalog,
repository-atlas coverage, evidence-map and capability-ledger checks. It is
local evidence, not GitHub Actions or independent scientific review.

## Learning exercises

1. Move the November revision from February 1 to February 16. Predict why the
   January-origin fingerprint and its metrics remain unchanged, then run the
   same-day regression.
2. Change the first-estimate value for one target month while keeping its
   source digest string. Explain which metrics change and why the evaluator
   cannot detect that the supplied digest does not match source bytes.
3. Remove one month from the origin's trailing history. Find the abstention
   reason and explain why inserting zero would confuse missing coverage with
   an observed zero.
4. Make the target first estimate available on the issue date. Explain why the
   target is not a future outcome even though the date-only selector excludes
   same-day observations.
5. Compare the origin reference month, issue date and target release date.
   Identify why UCI InvoiceDate cannot replace any of these publication
   fields.
6. Add a third fixed origin to only one split. Predict the coverage denominator
   and why a per-horizon score still requires two matched outcomes.

## Diagnosis, maintenance and evolution

- origin_not_published_at_issue: move the issue boundary only when an
  independently reviewed release schedule supports it; never tune the date
  after seeing metrics.
- target_not_future_at_origin: separate the already-observed release from the
  forecast target set; do not score the same public label as future.
- required_monthly_history_unavailable: inspect the selected vintage receipt
  and archive gap; do not fill missing months.
- future reference month rejection: inspect source normalization and release
  dates; a future period outside requested targets is contradictory to origin.
- input_manifest_sha256: compare normalized input snapshots for replay. It is
  not a publisher-byte digest and cannot prove source authenticity.
- Missing scores: preserve reason-specific abstention counts. Do not change
  horizon, origin dates, holdout, baseline or target definition based on the
  observed result.

Before empirical use, resolve B-01/B-02, review exact source terms and
retention, preserve original release bytes outside Git, verify digests and
publication boundaries, cross-check first estimates, freeze real chronological
origins and model-card assumptions, and obtain independent source/model review.
Keep later annual revisions as a separate sensitivity analysis. Do not merge
their scores with first-estimate targets or treat ALFRED as automatic rights
evidence.
