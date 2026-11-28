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
    -> validate first-estimate/revision chronology and latest eligible vintage
    -> exclude/count revisions without a first-estimate anchor
    -> first-estimate target matching and 12-month history gate
    -> lag-12 and trailing-12 predictions on matched targets
    -> per-horizon metrics plus sanitized lineage receipt
</code></pre>

| Component | Responsibility | Trust boundary |
| --- | --- | --- |
| CensusForecastOrigin | Freezes a reference month and date-only issue boundary | Caller-declared schedule; not an authenticated release calendar |
| select_census_vintage_as_of | Validates normalized records, first-estimate uniqueness and revision chronology, then chooses the newest eligible release per month | Digest syntax is checked; source bytes and rights are not |
| evaluate_census_vintage_backtest | Applies fixed horizons/baselines, excludes and counts unanchored revisions, matches targets, abstains and emits receipts | No fitting, tuning, I/O, route, persistence or operational authority |
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
When an anchor exists for a month, each monthly or annual revision must be
published strictly after that first-estimate date. An earlier revision fails
chronology validation; a same-day collision fails the existing date-only
ambiguity rule. A revision with no first-estimate anchor is valid normalized
input, but is unanchored and cannot enter this evaluator's feature view.
Every release must also be published on or after the first day following its
reference month. This rejects a first estimate or revision dated inside the
period it describes. It is a calendar sanity bound, not authentication of the
actual release schedule; the Census Bureau describes MARTS estimates as being
released about ten business days after the reference month closes
([methodology](https://www.census.gov/retail/marts/how_surveys_are_collected.html)).
Duplicate labels, mixed series, ambiguous `(reference_month, published_on)`
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

Both forecasts use the same first-estimate labels. The trailing mean and the
additive metric aggregates use exact `Fraction` arithmetic constructed from
the input Decimals, so ambient Decimal precision and rounding mode cannot alter
the result. RMSE scales the exact mean-square by powers of two before converting
the bounded mantissa to float, applies the square root, then restores the
exponent with `ldexp`. This avoids an intermediate float underflow when the
final RMSE remains representable; final overflow and underflow still fail
closed. Per horizon, metrics are reported only with at least two matched
origins:

- MAE is mean absolute error.
- RMSE is the square root of mean squared error.
- WAPE is total absolute error divided by total actual value; it is null when
  the actual denominator is zero.
- Coverage is scored origins divided by requested origins. Abstentions retain
  distinct reasons.

The evaluator accepts at most 34 coefficient digits, Decimal exponents from
`-433` through `150`, nonzero adjusted exponents from `-400` through `150`,
and absolute input values up to `1e150`. These bounds limit rational-arithmetic
cost and keep squared errors representable; they are not a source-unit or
Census-series definition. Metric conversion rejects float overflow, non-finite
results and any nonzero exact result that would underflow to `0.0`. The public
call raises `ValueError` instead of returning infinity, NaN or a false zero.
This also rejects WAPE overflow such as errors near `1e150` divided by targets
near `1e-300`. The result reports no model winner and never returns
observation values or predictions.

## Result and replay receipt

The versioned result, `mirrormind.census.vintage_backtest.v2`, contains the
selected split, series, requested origin count, unanchored revision count,
fixed horizons, per-origin audit, per-horizon metrics, abstention counts and
false `ingestion_authorized`/`forecast_eligible` flags. V2 is required because
the explicit unanchored count changes the serialized result contract; the
v1 result is an unmerged experimental output with no other in-repository
consumer. Each origin audit records a compact selector receipt with the
selected-row count and a feature-vintage fingerprint; it does not repeat every
release ID and digest. Each target entry records its publication date, release
ID and caller-supplied source digest string. The top-level input fingerprint
binds all normalized records using canonical JSON, including unanchored
revisions; per-origin fingerprints include only eligible feature records.

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

The curated evidence-map claims are `MM-CEN-003` for fixed-horizon matched
metrics, `MM-CEN-004` for later-revision noninterference, `MM-CEN-005` for
missing-history abstention, and `MM-CEN-006` for deterministic split replay.
`MM-CEN-007` verifies independence from ambient Decimal context;
`MM-CEN-008` and `MM-CEN-009` cover anchored revision chronology and exclusion
of unanchored revisions; `MM-CEN-010` covers bounded decimal inputs;
`MM-CEN-011` and `MM-CEN-012` cover overflow and underflow rejection; and
`MM-CEN-014` verifies that the example CLI refuses non-finite JSON, and
`MM-CEN-015` protects RMSE square-root scaling from an intermediate float
underflow when the final metric remains representable. `MM-CEN-016` covers the
publication-after-period lower bound through both the selector and public
evaluator.
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
| tests/unit/test_census_vintage_evaluation.py::test_trailing_mean_and_metrics_ignore_ambient_decimal_context | Exact means and metrics replay identically under precision 2 with ROUND_DOWN and ROUND_UP | Tests two local Decimal contexts over generated values only |
| tests/unit/test_census_vintage_evaluation.py::test_revision_cannot_precede_or_match_known_first_estimate | Earlier revisions fail chronology and same-day collisions fail the date-only ambiguity rule | Does not authenticate a publisher calendar |
| tests/unit/test_census_vintage_evaluation.py::test_evaluator_rejects_first_estimates_published_before_reference_month_closes | The public evaluator rejects a synthetic release set that could otherwise score estimates published before their reference periods close | Generated dates prove the validation path only; the real Census schedule still needs independent verification |
| tests/unit/test_census_vintage_evaluation.py::test_unanchored_revisions_are_excluded_counted_and_cannot_fill_history | Missing first-estimate anchors remain missing, are counted and cannot become feature rows | One generated incomplete archive only |
| tests/unit/test_census_vintage_evaluation.py::test_decimal_precision_and_exponent_domain_is_bounded | Excess coefficient digits and out-of-range exponents fail before metric serialization | Numeric bounds are not Census source units |
| tests/unit/test_census_vintage_evaluation.py::test_non_finite_metric_overflow_is_rejected_by_public_evaluator | Public evaluation rejects WAPE overflow from finite extreme inputs | No claim about real source values or model performance |
| tests/unit/test_census_vintage_evaluation.py::test_positive_metric_underflow_is_rejected_by_public_evaluator | Public evaluation rejects a positive exact MAE that would serialize as zero | One synthetic tiny-value boundary case |
| tests/unit/test_census_vintage_evaluation.py::test_representable_rmse_does_not_underflow_while_scaling_mean_square | Exponent scaling preserves a representable RMSE even though its exact mean square is below float range | One synthetic tiny-value boundary case |
| tests/integration/test_census_vintage_evaluation_cli.py::test_synthetic_validation_and_holdout_cli_are_reproducible_and_disjoint | Example command output is deterministic and validation/holdout origins are disjoint | A generated split is not a locked empirical holdout |
| tests/integration/test_census_vintage_evaluation_cli.py::test_synthetic_census_cli_rejects_unknown_split | The command rejects an unreviewed split name without printing fixture values | No production CLI surface is added |
| tests/integration/test_census_vintage_evaluation_cli.py::test_synthetic_census_cli_refuses_non_finite_json | The CLI fails closed before writing an infinite metric as JSON | Exercises one injected non-finite synthetic result, not a production server |

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
7. Run the same records under precision 2 with `ROUND_DOWN` and `ROUND_UP`.
   Trace why the trailing mean uses `Fraction` and the output metrics remain
   identical. Add an earlier and same-day revision; distinguish chronology
   rejection from the date-only duplicate rule.
8. Remove a first estimate but retain a later revision for that month. Compare
   full-input and per-origin fingerprints, read `unanchored_revision_count`,
   and explain why missing history still abstains. Try `1e150` / `1e-300` and
   `1e-400`; explain why overflow and positive-metric underflow reject the
   whole public evaluation rather than emit invalid JSON.
9. Move an origin first estimate into its reference month and run the public
   chronology regression. Then move the release to the first day of the next
   month and explain why that satisfies only a lower bound, not a verified
   publication schedule.

## Diagnosis, maintenance and evolution

- origin_not_published_at_issue: move the issue boundary only when an
  independently reviewed release schedule supports it; never tune the date
  after seeing metrics.
- publication date must follow the reference month: inspect the observation
  period and normalized release date. Do not move dates to make an origin score;
  the lower bound does not verify the publisher's actual release calendar.
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

## Fingerprint formatting contract (review follow-up)

`_record_payload` serializes each bounded Decimal using explicit
`format(record.value, "G")`. Without a precision argument, the uppercase
general format retains the coefficient scale and signed zero while fixing
the exponent marker independently of `decimal.getcontext().capitals`.
The v2 uppercase-default input and as-of digests remain compatible;
prior lowercase-context digests for scientific notation are superseded.
This is a normalized-record replay fingerprint, not cross-language
canonicalization or publisher verification. Evidence claim `MM-CEN-017` uses the public regression
`test_scientific_notation_fingerprints_ignore_decimal_capitals` checks
the entire result and pins a historical uppercase-default digest.

## Opt-in descriptive paired losses (experimental, M1C-04)

The in-process function `evaluate_census_vintage_descriptive` calls the
same private evaluator as the v2 entrypoint; its optional collector runs
only when both baselines score the same first-estimate target. It returns
`mirrormind.census.descriptive.v1`, nesting the unchanged v2 result and one
row per scored origin/horizon. Rows include the origin month, issue date,
target month/release/snapshot digest, selected-vintage manifest digest,
absolute losses and their signed difference (seasonal naive minus trailing
mean). Rational strings preserve exact fractions; positive means larger
seasonal absolute loss in that observation only. Missing history or a
missing first estimate has no loss row; inspect the nested v2 audit.

The SHA-256 covers canonical JSON of the complete report excluding the
digest field itself: sorted keys, compact separators, ASCII escaping,
no nonfinite values. This binds the supplied manifest, split, full origin
schedule, v2 aggregate result and loss rows for local replay, not authenticity.
A caller-declared holdout label does not prove a locked split. Even when
loss rows exist, `inference_status=abstained`,
`confidence_interval=null`, `winner=null` and all authority flags are
false. No API/CLI change or new dependency. The previous v2 contract
still omits per-origin value-bearing losses by default.

Worked fictional example: seasonal prediction 100, trailing prediction
100 + 10/12 and first estimate 120 yield losses 20 and 115/6,
difference 5/6. The paired observations are not independent by definition.
Exploratory synthetic studies found that a nominal 95% 12-month moving
block percentile interval and a five-group t interval can undercover
under persistent or seasonal dependence; neither interval is implemented
or approved here. Do not use this result for real-source publication:
errors can disclose derived values and a hash is not anonymization.
B-01/B-02, locked split evidence and independent statistical review remain
required before any empirical or inferential promotion.

Proposed evidence MM-CEN-018:
`test_descriptive_receipt_exact_pairs_and_v2_compatibility` checks
arithmetic, original output, lineage and canonical digest.
`test_descriptive_only_scored_rows_and_split_binding` checks omission
and replay; `test_descriptive_reuses_rejection_and_abstention` checks
malformed ordering and missing history. Run
`python -m pytest -q tests/unit/test_census_vintage_evaluation.py tests/integration/test_census_vintage_evaluation_cli.py`.
See [change request](changes/M1C_04_CENSUS_DESCRIPTIVE.md). Independent
review pending.

## Predeclared chronological schedule (experimental follow-up)

`CensusOriginSchedule` in [census_split.py](../../src/mirrormind/domains/retail/census_split.py)
holds the series and 10–250 exact origins. The schedule fingerprint binds
all issue dates, reference months, the three fixed horizons and cumulative
floor boundaries at 60% and 80%. Partitioning uses declared origins, not
successful scores. Preserve missing months; a caller must predeclare any
gaps and cannot silently purge them after evaluation.

A strict embargo requires the latest possible six-month target of each
earlier split to precede the next split's first origin month. Then every
earlier split target must have a unique first estimate actually published
strictly before the next split's first issue date. Missing, same-day or
later labels reject the wrapper. This conservative rule is a proposed
experimental protocol, not a source-specific empirical acceptance.

`evaluate_frozen_census_split` verifies the caller-retained expected
schedule SHA-256 before scoring, checks the boundaries, and invokes the
descriptive evaluator for only the selected validation or holdout slice.
Its nested evaluation retains normalized input and as-of fingerprints.
The outer receipt hashes the complete returned report excluding its own
digest. It does not compare an independently registered dataset digest,
prove when the schedule was fixed, prevent a caller from recomputing the
expected hash, enforce one-time holdout access or attest source rights.
Both `registration_verified` and `holdout_lock_verified` remain false.
No winner or confidence interval, no API/CLI, no persistence or real data.

Worked example: 10 declared origins split into 6/2/2. If the last
development origin is June, its six-month target is December; the next
validation origin must be January or later, and the December first
estimate must be available strictly before validation issuance. Do not
move dates to make a failed run pass.

Proposed evidence MM-CEN-019:
`test_frozen_split_binds_schedule_and_preserves_abstention` checks split
sizes, replay and distinct result digests. The regressions
`test_frozen_split_rejects_schedule_mutation_before_scoring`,
`test_frozen_split_rejects_overlap_and_invalid_schedule` and
`test_frozen_split_rejects_late_same_day_and_missing_prior_labels`
exercise failure before scoring.
Run `python -m pytest -q tests/unit/test_census_split.py`.
See [change request](changes/M1C_04_CENSUS_FROZEN_SPLIT.md).
Independent review pending.

## Experimental identity and complete local replay

The pure [experiment contract](../../src/mirrormind/domains/retail/census_experiment.py)
uses the public `census_evaluation_manifest_sha256` helper in the evaluator.
It validates normalized records and numeric bounds, then uses the existing
v2 manifest serializer without altering the v2 output. Its cutoff parameter
validates the selection but the hash binds the complete input, not the
selected view. This helper alone does not establish evaluation eligibility.

`prepare_census_experiment` creates a frozen specification of schedule
digest, input manifest digest and caller-declared 40-character Git revision.
`census_experiment_sha256` binds these fields to the fixed protocol and
evaluation schemas. Retain the expected digest before executing. Execution
checks it, rederives the specification, calls the existing split wrapper
and compares the nested full-input manifest. The receipt contains the full
descriptive result and a SHA-256 over canonical JSON excluding its own digest.

`verify_census_experiment_receipt` accepts exact bytes of canonical JSON
(sorted keys, compact separators, ASCII escaping, finite numbers; maximum
4 MiB). It does not parse supplied JSON. It reruns the committed experiment
and compares the entire expected canonical bytes; changing a loss and
rehashing the result does not pass. The returned receipt digest is only
local reproduction evidence. No persistence or external attestation.
Recomputing a new commitment is possible; a caller-declared revision does
not authenticate the executing code. No trusted registration timestamp,
blind access, independent holdout lock or single-use evaluation. Receipts
contain derived values and are restricted to fictional use.

At the current 250-origin bound and cumulative floor 60/80 split, holdout
has at most 50 declared origins; the proposed 60-pair inference minimum is
unreachable. Do not enlarge limits, repartition or promote inference. No
confidence interval or winner is emitted. B-01/B-02 remain unresolved.

Proposed evidence MM-CEN-020:
`test_experiment_commitment_and_complete_replay` checks matched identity,
deterministic replay, distinct split receipts and false authority flags.
`test_experiment_rejects_changed_inputs_before_evaluation` and
`test_experiment_rejects_rehashed_forgery` cover changed commitment
and forged bytes. Run `python -m pytest -q tests/unit/test_census_experiment.py`.
See [change request](changes/M1C_04_CENSUS_EXPERIMENT.md).
Independent review pending.

## Local experiment metadata journal (experimental)

[CensusExperimentJournal](../../src/mirrormind/domains/retail/census_experiment_journal.py)
takes an explicit absolute caller-controlled filesystem path. Register
recomputes the commitment from normalized records and schedule before
inserting only the experiment ID, schedule/manifest digests and declared
revision. Admission invokes the pure replay verifier outside the write
transaction, then rechecks the stored commitment and inserts only the
verified digest for the requested split. Identical repeats are idempotent;
conflicting stored digests fail closed. At most 1000 experiments and two
split keys per experiment may be written through the adapter.

Each operation opens a short SQLite transaction (BEGIN IMMEDIATE, foreign
keys, three-second busy timeout), checks application ID, version and exact
noninternal schema objects, and rolls back on exception. The new schema
does not migrate unpublished prototype databases. An explicit
verify_stored replay checks the recorded digest; plain read returns
metadata with stored_receipts_verified_on_read=false. No submitted body,
values or losses are persisted. Do not point the adapter at an unrelated
or untrusted database. This is not hostile-file isolation, independent
registration, tamper-proof logging, trusted code attestation, a blind
holdout lock or a power-loss durability guarantee. B-01/B-02 remain open.

Proposed evidence MM-CEN-021:
`test_journal_reopen_and_replay` checks deterministic admissions, metadata
only and explicit replay after reopen.
`test_journal_external_digest_edit_requires_replay` documents the
difference between plain reads and verification.
`test_journal_abrupt_exit_and_recovery` checks an uncommitted child-process
write to a temporary database; not a physical storage failure test.
Run `python -m pytest -q tests/unit/test_census_experiment_journal.py`.
See [change request](changes/M1C_04_CENSUS_EXPERIMENT_JOURNAL.md).
Independent review pending.

## Runnable fictional research experiment

The [research runner](../../examples/m1_census_research_runner.py) composes
the pure experiment contract and local journal without a network or
arbitrary data input. Its fixed fixture generates 80 monthly records,
value 100 + 2*i + 3*(i mod 12), 50 origins partitioned 30/10/10 and
predeclared embargo gaps. All values and releases are invented.

From the repository root (REV is a declared 40-character Git SHA):

    python -m examples.m1_census_research_runner demo --revision REV --split both
    python -m examples.m1_census_research_runner prepare --revision REV
    python -m examples.m1_census_research_runner run --revision REV --expected DIGEST --journal ABSOLUTE_PATH

Demo computes its own commitment and uses a temporary journal.
Prepare prints the commitment without scoring or opening a database.
Run requires the retained digest and caller-owned absolute path.
Validation is default; holdout or both require explicit selection.
Each split registers, evaluates, admits, reopens and explicitly replays.
Summary JSON includes actual per-horizon MAE/RMSE/WAPE, coverage,
abstentions, receipt digests and provenance; no paired loss rows.
The summary fingerprint excludes its own field. A later split failure
does not undo an earlier committed receipt; digest mismatch before
journal construction cannot create the journal. No independent
registration, blind holdout, code attestation, inference or authority.

Proposed evidence MM-CEN-022:
`test_runner_demo_replays_both_splits_and_reports_actual_metrics`
checks deterministic CLI replay, actual fictional metrics and false
authority flags. Run
`python -m pytest -q tests/integration/test_census_research_runner.py`.
See [change request](changes/M1C_04_CENSUS_RESEARCH_RUNNER.md).
Independent review pending.

## Local fictional Research Observatory
The [HTML generator](../../examples/m1_census_research_observatory.py)
runs the fixed fictional demo through the existing runner and temporary
journal. From the repository root:

    python -m examples.m1_census_research_observatory --revision REV --split both --output ABSOLUTE_HTML_PATH

The output is created exclusively; existing files are not overwritten.
Validation is the default. The report includes descriptive MAE/RMSE/WAPE,
coverage, abstention counts and provenance for each selected split.
Missing metrics are explicitly unavailable, not zero. No arbitrary
report ingestion, JavaScript, remote resources or server. Dynamic text
is escaped; native details and tables provide local inspection.
A matching local report is not independent attestation or calibrated
inference. The displayed revision is caller-declared. Temporary journal
is not durable history; the file is a report, not a registry.
No real data or source rights, no winner or action authority.

Proposed evidence MM-CEN-023:
`test_observatory_offline_reproducible_report` checks repeatable HTML,
metric rendering and offline markup. Other integration regressions cover
missing metrics, escaping and exclusive output. Run
`python -m pytest -q tests/integration/test_census_research_observatory.py`.
See [change request](changes/M1C_04_CENSUS_RESEARCH_OBSERVATORY.md).
Independent review pending; markup tests are not a browser accessibility audit.

## Closed fictional scenario catalog
The [runner](../../examples/m1_census_research_runner.py) and
[observatory](../../examples/m1_census_research_observatory.py) accept
`--scenario`. The default trend-seasonal fixture is unchanged, including
its commitment and report fingerprints for the same declared revision.
The catalog fixes 80 months and the same 30/10/10 origin schedule:
- fictional-trend-seasonal-v1: 100 + 2*i + 3*(i mod 12).
- fictional-flat-v1: 150.
- fictional-volatile-v1: 150 + ((37*i*i + 17*i + 11) mod 101) - 50.
- fictional-regime-shift-v1: 100 + 3*(i mod 12) + 80 when i >= 68
  (otherwise no additional 80).

These are deterministic illustrations, not sampled distributions or
independent replications. Each normalized input manifest and experiment
identity is distinct; the schedule digest is shared. Reusing a commitment
with another scenario fails before journal creation. Use the same scenario
on prepare and run. Example:

    python -m examples.m1_census_research_runner demo --revision REV --scenario fictional-regime-shift-v1 --split both

The observatory labels its scenario. Do not pool errors, select winners,
or treat evaluation coverage as confidence interval calibration. All
inference remains abstained. No real data, source authorization or
independent holdout lock.

Proposed evidence MM-CEN-024:
`test_scenario_full_replay_and_expected_metrics` covers the four fixtures,
both splits, exact replay and expected descriptive errors.
`test_scenario_catalog_preserves_default_and_separates_commitments` and
`test_scenario_cross_commitment_rejected_before_journal` verify identity
and failure before storage. Run
`python -m pytest -q tests/integration/test_census_research_scenarios.py`.
See [change request](changes/M1C_04_CENSUS_RESEARCH_SCENARIOS.md).
Independent review pending.

## Comparative fictional Research Observatory
Use the explicit all-scenarios mode of the
[local observatory](../../examples/m1_census_research_observatory.py):

    python -m examples.m1_census_research_observatory --revision REV --scenario all --split both --output ABSOLUTE_HTML_PATH

All four scenario commitments are prepared before scoring. The existing
runner independently admits and replays each selected split in a shared
temporary metadata journal. Comparison tables separate validation and
holdout and display MAE, RMSE, WAPE and scored/requested counts. Each
scenario retains its own provenance, coverage and abstention details.
There is no pooling or ranking; four designed sequences are not random
independent samples. The default single-scenario mode remains available.
Output is deterministic, exclusively created, offline HTML; no scripts,
external resources, imported report files or persistent history. All
commitments are self-generated demo identities, not independent registration.

Proposed evidence MM-CEN-025:
`test_comparative_observatory_replays_all_scenarios_and_unique_anchors`
checks eight split receipts, distinct experiment identities, anchors and
deterministic markup. Separate tests cover prepare-before-score order
and failed generation without output. Run
`python -m pytest -q tests/integration/test_census_research_observatory.py`.
See [change request](changes/M1C_04_CENSUS_COMPARATIVE_OBSERVATORY.md).
Independent review pending; no accessibility certification.

## Local fictional experiment history
The [history example](../../examples/m1_census_research_history.py)
uses `read_census_journal_snapshot` in the existing journal module.
It opens an existing absolute caller-owned path in SQLite read-only mode,
sets query_only and reads a consistent transaction, checking schema,
identity and digest syntax. Maximum 1000 commitments and 2000 receipts.
No migration, initialization, or admission. Unknown fixtures remain
unknown; known names match both schedule and manifest to the current
closed catalog. Plain snapshots do not score or verify receipt content.

    python -m examples.m1_census_research_history --journal ABSOLUTE_DB --output ABSOLUTE_HTML
    python -m examples.m1_census_research_history --journal ABSOLUTE_DB --output ANOTHER_HTML --replay-experiment DIGEST --split validation

Explicit replay of one recorded split regenerates the known fictional
fixture, checks the commitment and compares the current result digest
against the snapshot. It never writes a receipt or executes an unselected
split. Holdout requires explicit selection. The report distinguishes stored
metadata from explicit replay. The revision is declared, not historical code
attestation; current code may not reproduce old results. Unknown fixture,
missing split or conflicting digest rejects replay. No chronology or
execution counts: there are no timestamps and repeated runs are idempotent.
Snapshot SHA-256 is a local fingerprint, not a trusted timestamp or seal.
Existing output is never overwritten. No real data, inference or new trust.

Proposed evidence MM-CEN-026:
`test_history_snapshot_replay_does_not_write` checks deterministic metadata,
explicit replay and unchanged journal bytes. Other regressions cover
capacity, missing/foreign files, schema identity, tampered receipts and
exclusive output. Run
`python -m pytest -q tests/integration/test_census_research_history.py`.
See [change request](changes/M1C_04_CENSUS_RESEARCH_HISTORY.md).
Independent review pending. Read-only SQLite is not hostile-file isolation.

## One-factor fictional sensitivity grid
The [sensitivity example](../../examples/m1_census_research_sensitivity.py)
uses a shared base 200 + 3*(i mod 12), the existing 80-month fixture's
release timing and 30/10/10 schedule. Its fixed axes add:
- trend: level*i, levels 0, 1, 2, 4, 8;
- volatility: level*(((37*i*i + 17*i + 11) mod 101) - 50),
  levels 0, 1, 2, 3, 4;
- shift: level for i >= 68, levels 0, 20, 40, 80, 120.

The generated month/value marker is a fictional snapshot identifier,
not an external source digest. Prepare all 15 cells before scoring;
the three zero cells share one experiment and receipt, so there are
13 unique commitments. For one explicitly selected split, admit and
replay each distinct result through a temporary journal. Per-horizon
summaries include MAE for both fixed baselines, matched count, evaluation
coverage and exact rational mean paired loss difference (seasonal minus
trailing). The report has separate manifest, schedule and receipt
digests for every cell. No pooling, optimization, inference or ranking.
These designed sequences are not independent random samples. Different
factor scales preclude a universal ranking of their effects.

    python -m examples.m1_census_research_sensitivity --revision REV
    python -m examples.m1_census_research_sensitivity --revision REV --split holdout --output ABSOLUTE_HTML

Validation is default; holdout is explicitly selected. JSON stdout or
exclusive static HTML. No input-file or external source access. Current
history recognizes only the original four fixtures, not sensitivity cells;
the temporary journal is not persistent history. All code revisions are
caller-declared, not attested. B-01/B-02 remain open.

Proposed evidence MM-CEN-027:
`test_sensitivity_grid_replays_unique_cells_and_preserves_reference`
checks exact paired summaries, shared baseline and distinct replay.
Separate tests cover factor isolation, closed grid, prepare-before-score
and exclusive HTML output. Run
`python -m pytest -q tests/integration/test_census_research_sensitivity.py`.
See [change request](changes/M1C_04_CENSUS_RESEARCH_SENSITIVITY.md).
Independent review pending.

## Experimental five-model validation protocol

The [model library](../../src/mirrormind/domains/retail/census_models.py)
has a separate protocol identity. It binds the existing experiment spec,
five method identifiers, 13-month history requirement, fixed horizons
and validation-only split. Prepare the retained comparison digest before
scoring. The two-model evaluator and journal remain unchanged; this
receipt is not admitted to that journal.

On each legacy-scored pair, use 13 consecutive visible months ending at
the origin. The original seasonal and trailing mean losses must agree
exactly with the legacy receipt. Persistence uses the last value.
Seasonal drift adds current minus current lag-12 to the target lag-12
value; OLS uses the last 12 observations, intercept and slope estimated
with exact rational arithmetic, extrapolated h months. Both extrapolated
models floor negative predictions at zero. No training across origins,
parameter selection or target-dependent fitting. All five share the
extra-history eligibility restriction. Fewer than two common observations
gives unavailable MAE and differences. The difference is model absolute
loss minus seasonal absolute loss, averaged on matched pairs.

The full receipt binds target and visible-vintage lineage, exact
forecasts and losses. Explicit replay compares complete canonical bytes
(up to 4 MiB), not just a caller-provided digest. No independent
registration, code attestation, empirical claims, confidence interval
or winner. Value-bearing receipts are fictional-use only.

The [fixed example](../../examples/m1_census_model_comparison.py)
prepares five commitments before scoring and reproduces each report:

    python -m examples.m1_census_model_comparison --revision REV

The added validation-break fixture has level 150 before index 53 and
230 from index 53 onward, within the validation origins 48..57.
The original regime-shift fixture changes only at index 68, after all
validation targets. Its validation results are pre-break only.
The five deterministic fixtures are not independent samples. Holdout is
not executed or used for selection by this protocol.

Proposed evidence MM-CEN-028:
`test_validation_break_catalog_and_replay` checks five distinct commitments,
exact pre-break forecasts and known errors. `test_model_commitment_and_receipt_replay`
rejects a rehashed forgery. The model suite also checks exact linear oracles,
legacy parity, late revisions and shared extra-history abstention.
Run `python -m pytest -q tests/unit/test_census_models.py`.
See [change request](changes/M1C_04_CENSUS_FIVE_MODELS.md).
Independent review pending.

## Bounded exact discrete probability primitives

The experimental [probability module](../../src/mirrormind/domains/retail/census_probability.py)
uses sorted distinct integer support and positive integer weights reduced
by their greatest common divisor. Inputs are bounded: support -144..144,
total mass at most 1024 bits, up to six increments in -24..24, increment
law mass at most 64 bits, and Markov chains with at most nine closed
states and 65535 canonical weight per transition row. Explicit
canonical_pmf normalization is required for noncanonical weights.
There is no general continuous or unbounded distribution interface.

convolve_increments sums independent increment laws. propagate_markov
conditions on the supplied last state, scales rows by their common
denominator, propagates integer weights and checks mass conservation.
discrete_quantile uses the inverse CDF (zero maps to minimum support).
score_discrete_pmf returns exact CRPS, mean pinball at 0.1/0.5/0.9,
median absolute error, inclusive interval coverage and width.
reference_interval_coverage measures interval mass under the supplied
reference distribution; it does not authenticate that law. Discrete
central intervals may exceed nominal coverage. A point mass CRPS is
absolute error. These are mathematical primitives, not a predictive
model, calibration certificate or new receipt protocol.

Proposed evidence MM-CEN-029:
`test_crps_against_direct_pair_and_cdf_oracles` checks both independent
exact CRPS formulations. Other tests enumerate independent sums and
Markov paths at horizons 1..6, including distinct row denominators,
and reject invalid types, supports, masses, horizons and transition
closures. Run `python -m pytest -q tests/unit/test_census_probability.py`.
See [change request](changes/M1C_04_CENSUS_PROBABILITY.md).
No new dependencies, API, journal schema, learned model, empirical
forecasting claim or inference. Independent review pending.

## Fixed fictional probabilistic study protocol

The [probability study example](../../examples/m1_census_probability_study.py)
uses the bounded discrete probability core. It binds the complete fixed
design and caller-declared Git revision before scoring. Two groups of
32 paths, 64 monthly increments including initial zero, origins 48..57,
horizons 1/3/6. Deterministic SHA-256 counter draws from ASCII
seed:path:index, first byte modulo four selects -1,0,0,1. Seeds 61001
and 61002; amplitude four, with amplitude twelve from transition index
53 in the second scenario. These deterministic fixtures are not a
cryptographic random or independent statistical sample claim.

Methods: point persistence, narrow fixed iid increments (amplitude two),
fixed iid increments (amplitude four), iid empirical last 24 increments
and privileged true-law oracle. The non-oracle methods receive only
historical increments. The oracle knows the future law, not realized
increments. Exact rational group means cover CRPS, pinball, median MAE,
inclusive 10/90 coverage, width and reference coverage. Each group
includes a streaming digest of all evaluated PMFs, observations and
scores in fixed path/origin/horizon/model order. No raw paths are
published. The receipt binds the design, group summaries and transcript
digests. The digest is not a signed registration or runtime attestation.

    python -m examples.m1_census_probability_study prepare --revision REV
    python -m examples.m1_census_probability_study run --revision REV --expected STUDY_SHA256
    python -m examples.m1_census_probability_study demo --revision REV

Prepare never scores; run requires a caller-retained commitment; demo
generates its own. Both execution modes explicitly reproduce the
complete canonical report before printing. verify_study compares full
canonical bytes, at most 1 MiB, not just a supplied report hash. The
canonical bytes exclude the stdout newline. No arbitrary inputs,
journal admission, holdout, statistical winner, calibration, real data
or authority. Overlapping origins and horizons are not independent
replications. The earlier adaptive prototypes remain separate.

Proposed evidence MM-CEN-030:
`test_study_identity_and_complete_replay` checks fixed digests, complete
replay and stationary oracle parity. Other tests reject rehashed
metric forgery and mismatched commitments before scoring, verify
causal inputs and prepare-only behavior. Run
`python -m pytest -q tests/integration/test_census_probability_study.py`.
See [change request](changes/M1C_04_CENSUS_PROBABILITY_STUDY.md).
Independent review pending.

## Fictional probabilistic observatory
The [probabilistic observatory](../../examples/m1_census_probability_observatory.py)
generates a standalone offline HTML report from a freshly executed and
fully replayed fixed probability study.

    python -m examples.m1_census_probability_observatory --revision REV --output ABSOLUTE_HTML

It shows separate per-group/horizon CRPS, mean pinball, median MAE,
observed coverage, reference coverage and interval width, with exact
rational scores available in expandable details. Reference coverage
uses the supplied simulator law; observed coverage is the fraction of
simulated outcomes inside the inclusive interval. Neither is an
operational calibration certificate. The fixed example is path 0,
origin 52, horizon six in each group, with all five PMFs regenerated
from the same design, their quantiles, realized displacement and CRPS.
The example is not an independent experiment or cherry-picked result.
The oracle is a privileged reference. The study and report digests,
declared revision and per-group event transcript digests are displayed.
No arbitrary imported report, scripts, network, server, persistence or
output overwrite. Self-generated demo commitment only.

Proposed evidence MM-CEN-031:
`test_probability_observatory_replayed_metrics_and_examples` checks
reproducible markup, actual report metrics, provenance and internal
navigation. Other tests check point-mass display, exclusive output and
replay failure without output. Run
`python -m pytest -q tests/integration/test_census_probability_observatory.py`.
See [change request](changes/M1C_04_CENSUS_PROBABILITY_OBSERVATORY.md).
Independent review pending; markup tests are not accessibility certification.

## Bounded exact bivariate probability core
The experimental [bivariate module](../../src/mirrormind/domains/retail/census_bivariate.py)
represents sorted unique integer pairs with positive canonical integer
weights. Each axis supports displacement -24..24, at most 2401 cells,
and total mass at most 512 bits. Convolution accepts up to six
independent-in-time joint increment laws with each axis in -4..4 and
mass at most 64 bits per law. It preserves within-step dependence but
does not model serial dependence. Joint marginal projection reuses the
univariate canonical PMF contract. The independent projection preserves
both marginals exactly and rejects results exceeding the mass bound.

Exact covariance, simultaneous-positive event probability, multiclass
joint Brier (sum of squared probability-vector errors, range 0..2)
and expected Brier excess under an explicitly supplied reference are
available. Expected excess equals squared probability-vector distance;
the reference is not authenticated. Identical marginal distributions
do not establish correct joint behavior. No fitted model, causal
effect, dependence detector, confidence interval or calibration claim.

Proposed evidence MM-CEN-032:
`test_joint_brier_exact_proper_score_identity` verifies the identity
by enumerating outcomes. Additional tests check joint convolution by
path enumeration at horizons one through six, marginal preservation,
covariance and invalid input rejection. Run
`python -m pytest -q tests/unit/test_census_bivariate.py`.
See [change request](changes/M1C_04_CENSUS_BIVARIATE.md).
Independent review pending. No API, journal or univariate changes.

## Fixed fictional bivariate study protocol
The [bivariate study](../../examples/m1_census_bivariate_study.py)
commits the fixed design and declared Git revision before scoring.
Four scenarios (positive, independent, negative and positive-to-negative
shift at increment 53), seeds 111001..111004, 16 paths each, origins
48..57, horizons 1/3/6. Counter-hash fixtures use first SHA-256 byte
modulo eight; paired increments are independent over time with each
axis +/-4. Compare fixed independent, smoothed joint last24 (one
pseudocount per cell), its matched independent projection and a
privileged true-law reference. All use identical observed targets.
The joint and matched product forecasts have identical marginals.
Exact group means include multiclass Brier, reference excess, marginal
CRPS on each axis, simultaneous-positive event Brier and probability,
observed event rate and covariance. Each group has a streaming event
transcript digest. No inference or operational calibration claim.

    python -m examples.m1_census_bivariate_study prepare --revision REV
    python -m examples.m1_census_bivariate_study run --revision REV --expected STUDY_SHA256
    python -m examples.m1_census_bivariate_study demo --revision REV

Prepare does not score. Run requires a caller-retained commitment;
demo self-generates one. Both execution modes replay the whole report.
verify_study compares canonical bytes at most 1 MiB, excluding stdout
newline. No imported records, journal, holdout, winner, independent
registration, runtime attestation, causal effect or temporal
autocorrelation. These are deterministic fixtures, not independent
statistical samples; origins and horizons overlap.

Proposed evidence MM-CEN-033:
`test_bivariate_study_exact_replay_and_matched_marginals` verifies
fixed digests, complete replay and exact matched marginal score parity.
Other tests reject rehashed forgery and mismatched commitment before
scoring, and test future invariance and invalid inputs.
See [change request](changes/M1C_04_CENSUS_BIVARIATE_STUDY.md).
Independent review pending.

Run `python -m pytest -q tests/integration/test_census_bivariate_study.py`.

## Offline multivariate research observatory
The [bivariate observatory](../../examples/m1_census_bivariate_observatory.py)
renders a freshly executed and fully replayed fixed bivariate study.

    python -m examples.m1_census_bivariate_observatory --revision REV --output ABSOLUTE_HTML

Separate scenario and horizon tables include exact rational joint Brier,
reference excess, both marginal CRPS scores, event Brier, predicted and
observed simultaneous-positive event rates and covariance. Fixed examples
(path 0, origin 52, horizon six) show joint matrices with explicit axes
and numeric probability labels, exact cell fractions in titles, and
marginal tables with visible exact fractions. A common probability
intensity scale is used across all matrices. The examples do not add
independent observations. The oracle is privileged. Provenance includes
study, report and group transcript digests, and declared revision.
Self-generated demo commitment only; no imported records, network,
scripts, storage, overwrite or operational authority.

Proposed evidence MM-CEN-034:
`test_bivariate_observatory_replayed_report_and_matrices` checks
actual replayed metrics, matrix counts, provenance and internal links.
Other tests verify exact cell mass, exclusive output and no output
after a replay mismatch.
Run `python -m pytest -q tests/integration/test_census_bivariate_observatory.py`.
See [change request](changes/M1C_04_CENSUS_BIVARIATE_OBSERVATORY.md).
Independent review pending; markup checks are not accessibility certification.

## Bounded joint Markov propagation
The [joint Markov engine](../../src/mirrormind/domains/retail/census_joint_markov.py)
propagates a paired sign process on ordered states (-4,-4), (-4,4),
(4,-4), (4,4). A supplied schedule contains one through six immutable
4-by-4 transition matrices; rows and columns follow state order.
Each row contains exact integer weights 0..1024 and positive total,
normalized independently. Zero transitions and deterministic rows are
permitted. The output is the canonical joint PMF of cumulative future
states, excluding the supplied start. The algorithm tracks integer
mass by cumulative pair and current state, scales row denominators
by their least common multiple, reduces common factors and checks
mass conservation before projection. No approximation or cache.
All nested inputs are checked before propagation. Schedules may
vary by step, but the engine neither estimates nor authenticates them.
Four states only; this is not a general dynamic network, fitted model,
intervention, causal effect or empirical calibration.

Proposed evidence MM-CEN-035:
`test_joint_markov_enumeration` checks exact equality to direct
Fraction path enumeration for every start state and horizon 1..6.
Other tests cover time-varying schedules, unequal row totals,
deterministic/zero transitions, row scaling, maximum weights and
invalid nested types. Run
`python -m pytest -q tests/unit/test_census_joint_markov.py`.
See [change request](changes/M1C_04_CENSUS_JOINT_MARKOV.md).
Independent review pending.

## Fixed paired-state temporal estimators
The [temporal estimators](../../src/mirrormind/domains/retail/census_temporal_models.py)
fit four fixed candidate matrices from exactly 24 observed paired
sign states. IID counts all 24 observations; own-axis and cross-axis
models estimate separately smoothed binary conditional distributions
and multiply them within each row; full estimates the four-outcome
conditional law given the previous pair. Conditional models use 23
consecutive transitions. One pseudocount per outcome gives uniform
unseen contexts. Weights are reduced by their common divisor; the
candidate order is fixed. Forecasting propagates each fitted stationary
matrix from the last observed state at horizons 1/3/6 using the joint
Markov engine. No target, future observations, scenario identifier,
adaptive selection or public cache. The history is supplied by the
caller; the module does not authenticate dates or availability.

Proposed evidence MM-CEN-036:
`test_temporal_estimators_direct_counting` compares all candidate rows
against an independent rational counting oracle. Additional tests
check cross-axis orientation, missing contexts, forecast propagation,
future invariance, fresh mappings and rejection of invalid histories.
Run `python -m pytest -q tests/unit/test_census_temporal_models.py`.
See [change request](changes/M1C_04_CENSUS_TEMPORAL_MODELS.md).
No empirical model, calibration, causal identification or authority.
Independent review pending.

## Fixed fictional temporal study
The [temporal study](../../examples/m1_census_temporal_study.py)
commits a fixed paired-sign study and declared revision before scoring.
Four designs: independent, own-state persistence, cross-axis persistence
and cross-to-own switch at transition 53. Counter-hash seeds
131001..131004; 16 paths each, 64 states, origins 48..57, horizons
1/3/6. The two axes update simultaneously from the preceding state;
copy probability 3/4, independent signs probability 1/2.
The four fixed fitted candidates use only the last 24 observed states.
The oracle alone knows the future transition schedule, not realizations.
All methods share observed cumulative future signed targets.
Exact group means include joint Brier, reference excess, both marginal
CRPS scores, event Brier and probability, observed event rate and
covariance. Each group has a streaming event transcript digest.

    python -m examples.m1_census_temporal_study prepare --revision REV
    python -m examples.m1_census_temporal_study run --revision REV --expected STUDY_SHA256
    python -m examples.m1_census_temporal_study demo --revision REV

Prepare does not score. Run requires a retained commitment; demo
self-generates one. Both execution modes replay the report. The
verifier compares canonical bytes at most 1 MiB, excluding stdout
newline. Fixed fixtures and overlapping targets are not independent
statistical samples. No causal effect, authenticated temporal
availability, independent registration, attestation, empirical data,
holdout, selection, calibration, confidence interval or winner.

Proposed evidence MM-CEN-037:
`test_temporal_study_exact_replay` verifies fixed report and study
digests, complete replay, expected row counts and oracle excess.
Additional tests reject rehashed forgery, validate commitment before
scoring, check future invariance and the exact transition boundary.
Run `python -m pytest -q tests/integration/test_census_temporal_study.py`.
See [change request](changes/M1C_04_CENSUS_TEMPORAL_STUDY.md).
Independent review pending.

## Offline dynamic network observatory
The [temporal observatory](../../examples/m1_census_temporal_observatory.py)
renders a fresh fixed temporal study only after full local replay.

    python -m examples.m1_census_temporal_observatory --revision REV --output ABSOLUTE_HTML

Separate descriptive scenario/horizon tables expose exact joint and
marginal scores, event probabilities, covariance, and reference excess.
Fixed examples (path 0, origin 52, horizon six) show previous/next
state transition matrices with percentages and exact fractions,
conditional cumulative joint distributions and marginals. Each fitted
candidate uses one stationary estimated matrix; the oracle displays
each of its six privileged future matrices. No additional sample,
statistical winner, empirical calibration, causal effect, imported
record, network, script or operational authority. Report includes
declared revision, study, report and group transcript digests.

Proposed evidence MM-CEN-038:
`test_temporal_observatory_replay_and_matrices` checks replayed metrics,
provenance, table counts and internal links. Other tests verify exact
row mass, exclusive output and no output after replay mismatch.
Run `python -m pytest -q tests/integration/test_census_temporal_observatory.py`.
See [change request](changes/M1C_04_CENSUS_TEMPORAL_OBSERVATORY.md).
Independent review pending; markup tests are not accessibility certification.

## Exact bounded three-axis propagation
The [network3 engine](../../src/mirrormind/domains/retail/census_network3.py)
supports three binary sign axes (-1,+1), eight lexicographically ordered
states and one through six future steps. The full joint engine accepts
immutable 8-by-8 matrices with integer weights 0..15625 and nonempty
rows. Row denominators are independently normalized via LCM scaling.
The lineage engine accepts one bijective parent mapping per step and
three binary conditional laws (integer weights 0..25, nonempty rows);
each child has one unique parent and innovations are conditionally
independent. Given a fixed initial state, the three lineages are
independent and their cumulative-vector laws can be convolved exactly.
factor_matrix expands the same validated law into a joint matrix.
Both engines conserve integer mass, reduce common factors and return
sorted immutable tuples of (cumulative triple, positive canonical weight).
At most 343 cells and 1024 total-mass bits. Start state excluded.
No cache or automatic algorithm selection. Shared parents, arbitrary
graphs and correlated innovations are outside the lineage contract;
the general joint engine supports any admissible supplied joint matrix.
No fitted model, authenticated data, causal claim or operational authority.

Proposed evidence MM-CEN-039:
`test_network3_lineage_parity` compares canonical outputs from both
engines for all starts and horizons 1..6 under heterogeneous schedules.
Direct rational path enumeration, deterministic transitions, maximum
support and nested invalid inputs are covered by additional tests.
Run `python -m pytest -q tests/unit/test_census_network3.py`.
See [change request](changes/M1C_04_CENSUS_NETWORK3.md).
Independent review pending. Performance depends on schedule and
implementation; no general speed or scalability guarantee.

## Bounded local parent learning
The [structure estimators](../../src/mirrormind/domains/retail/census_network_structure.py)
accept exactly eight or 24 observed binary triples. Each child has
four candidate parent labels (none, 0, 1, 2) with equal prior.
Independent Beta(1,1) context priors yield exact integrated
Bernoulli likelihoods, normalized per child. MAP uses fixed tie
order; conservative accepts a parent only if its evidence exceeds
twice no-parent evidence and every alternative strictly. This
threshold is a fixed exploratory rule, not calibrated confidence.
Explicit graph fitting uses one pseudocount per binary outcome and
returns a canonical row-weight joint matrix; shared parents allowed.
One-step posterior averaging integrates the local parent/parameter
posterior under independent priors and the supplied history.
Uniform parent averaging is a separate control. Both return exact
immutable integer PMFs; no multistep Bayesian integration, causal
identification, authenticated observations, empirical calibration
or automatic candidate promotion. No public cache.

Proposed evidence MM-CEN-040:
`test_parent_average_complete_graph_mixture` compares exact
one-step local averaging to explicit enumeration of all 64 graphs
for both history lengths and weighting modes. Sequential evidence,
ties, shared parents and invalid input boundaries have additional
tests. Run `python -m pytest -q tests/unit/test_census_network_structure.py`.
See [change request](changes/M1C_04_CENSUS_NETWORK_STRUCTURE.md).
Independent review pending.

## Persistent Bayesian prediction
The [persistent engine](../../src/mirrormind/domains/retail/census_network_bayes.py)
integrates a fixed uncertain local graph and fixed uncertain binary
parameters under the local independent priors above. Each hypothetical
prefix updates its own posterior predictive law; no actual future
observation is used. The frozen control holds issuance-time posterior
mean rows constant. Equivalent for one step, generally not for longer
horizons. Eight or 24 observations, one to three steps, at most 512
future paths and 64 cumulative cells. Both return bounded canonical
integer PMFs. No dynamic graph posterior, causal effect or scalability claim.

The [fixed study](../../examples/m1_census_network_bayes_study.py)
reuses four exploratory scenarios (seeds 161001..4, four paths each,
origins 48/52/56, windows 8/24, horizons 1/2/3, ring-to-own at
transition 53). Integrated, frozen, MAP and privileged schedule oracle
share 288 window-specific targets, 1152 scores, and 144 distinct
path/origin/horizon events. Exact separate group means and transcript
digests. Oracle knows future schedule, not outcomes. Reference excess
is squared distance to generating law. No winner, inference, holdout,
independent registration, runtime attestation, calibration or authority.
Fixtures are not independent confirmation.

    python -m examples.m1_census_network_bayes_study prepare --revision REV
    python -m examples.m1_census_network_bayes_study run --revision REV --expected STUDY_SHA256
    python -m examples.m1_census_network_bayes_study demo --revision REV

Prepare does not score; run requires caller-retained commitment.
Demo self-generates it. Execution modes replay canonical bytes.
Verifier bounds receipt to 1 MiB, excluding stdout newline.

Proposed MM-CEN-041: `test_persistent_bayes_graph_oracle` enumerates
64 persistent graphs and two-step paths, integrating parameters
sequentially. Run `python -m pytest -q tests/unit/test_census_network_bayes.py`.
Proposed MM-CEN-042: `test_persistent_study_exact_replay` checks fixed
digests, replay, group coverage and oracle excess. Additional tests
reject rehashed forgery and scoring before commitment.
Run `python -m pytest -q tests/integration/test_census_network_bayes_study.py`.
See [change request](changes/M1C_04_CENSUS_NETWORK_BAYES.md).
Independent review pending.

## Bounded modular exact network queries
The [modular engine](../../src/mirrormind/domains/retail/census_modular.py)
accepts 24 or 48 immutable observed binary states over 2..12 axes,
a complete disjoint partition into modules of 1..6 axes, and at
most 24 directed cross-module candidate ports. Each child may
choose zero, one or two lag-one parents from its own module and
incoming port sources. Uniform subset prior by default; balanced
mode allocates equal mass to available parent-set sizes. Context
parameters have independent Beta(1,1) priors. The graph and
parameters persist through each hypothetical trajectory.

The public query returns the exact sorted rational PMF of
cumulative future states (excluding the observed start) on 1..4
ordered distinct axes, plus the enumerated first-step axes.
At horizon two the first-step scope is the union of queried axes
and their allowed parents; other first-step outcomes can be
integrated out exactly because local predictive laws factor given
the observed history. Hypothetical updates for queried children
preserve graph/parameter uncertainty. Local candidate scopes and
first-step closure are each limited to eight axes. Larger requests
fail closed, not approximately. Horizon 1..2 only. The result is
an in-process Fraction contract, not a wire or decimal encoding.

Proposed MM-CEN-043: `test_modular_graph_oracle` independently
enumerates sixteen graphs and two-step trajectories with sequential
Beta-Bernoulli evidence, both priors and both history lengths.
Additional checks cover projection, disconnected products, port
orientation, twelve-axis scope, singleton priors and malformed
inputs. Run `python -m pytest -q tests/unit/test_census_modular.py`.
See [change request](changes/M1C_04_CENSUS_MODULAR.md).

Candidate ports are supplied, not learned or causal. No empirical
skill, calibration, scalability beyond bounds, deployment or
authority. Independent review pending.
