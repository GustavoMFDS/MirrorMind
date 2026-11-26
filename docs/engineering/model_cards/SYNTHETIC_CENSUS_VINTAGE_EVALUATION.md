# Model card — synthetic aggregate Census vintage baselines

## Status and intended use

This card describes two fixed, untuned heuristics implemented by
evaluate_census_vintage_backtest. They demonstrate date-aware data selection,
matched-origin scoring and abstention on fictional aggregate records. They are
not fitted forecasting models, empirical performance claims, causal estimates,
inventory recommendations or decision support.

## Data and temporal protocol

The only runnable data are generated in memory by
examples/m1_census_vintage_evaluation.py and the unit-test fixtures. The
example creates 21 fictional monthly records from January 2020 through
September 2021, one later revision, and fixed validation/holdout origin sets.
Validation reference months are December 2020 and January 2021; holdout months
are February and March 2021. Their issue dates are date-only and are strictly
after the origin first-estimate publication dates. These are arbitrary test
dates, not observed Census release dates.

At every origin, only the latest normalized vintage with
published_on < issued_on can become history. First estimates are the primary
labels at reference months one, three and six months ahead. The method requires
12 consecutive visible monthly observations and never pads a gap. A later
revision published after an origin cannot rewrite its inputs or score. The
split labels and origin dates are fixed in the example, but all values and
source identities are public synthetic fixtures; this is not a blind or locked
empirical holdout.

When a first-estimate publication is present for a reference month, monthly
and annual revisions must be published on a strictly later date. Earlier
revisions are rejected and same-day collisions remain ambiguous because the
contract has no intraday ordering. If an archive fragment contains a revision
but no first-estimate anchor for its month, the evaluator excludes that row
from all feature vintages, increments `unanchored_revision_count`, and leaves
the missing month absent. The full input manifest still binds the excluded
row; origin feature manifests do not.

## Baselines and metrics

- seasonal_naive_lag12: use the selected vintage value for the target month
  minus 12 months.
- trailing_12_month_mean: average the 12 consecutive visible months ending at
  the origin; hold that estimate constant across the requested horizon.
- MAE: average absolute difference over matched target/origin pairs.
- RMSE: square root of average squared error on the same pairs.
- WAPE: total absolute error divided by total first-estimate values; null when
  the denominator is zero.
- Coverage: scored origins divided by requested origins for each horizon.

The trailing mean and additive error aggregates use exact `Fraction`
arithmetic, so local Decimal precision and rounding settings cannot alter a
score. The supported Decimal inputs contain at most 34 coefficient digits,
raw exponent `-433..150`, nonzero adjusted exponent `-400..150`, and magnitude
no greater than `1e150`. Metrics that overflow float range, become non-finite,
or underflow a positive exact result to zero raise `ValueError`; output never
substitutes infinity, NaN or a false zero. RMSE applies square root after
scaling the exact mean-square's power-of-two exponent: only its bounded
mantissa is converted to float, then `ldexp` restores the square-root exponent.
This avoids rejecting a representable RMSE because its intermediate square is
below float range. The final result still fails closed if it overflows or
underflows. These are computational bounds, not source-unit limits.

Metrics are withheld for a horizon with fewer than two matched origins. The
evaluator does not select a winner, tune parameters or calculate uncertainty.
Its result schema is `mirrormind.census.vintage_backtest.v2`, which reports the
unanchored-revision count. The earlier v1 output was only on an unmerged
experimental branch and no in-repository consumer remains on it.

## Results and uncertainty

The example emits numerical results only for its fictional fixture. Those
numbers are deterministic arithmetic checks and must not be quoted as Census,
ALFRED, retail-demand or forecast-accuracy evidence. There are no empirical
observations, confidence intervals, calibration results, statistical tests or
source completeness evidence. Target entries expose their publication date,
release ID and digest string; origin summaries expose a count and selected
vintage fingerprint, without values or forecasts. The normalized-input
fingerprint does not authenticate source bytes or make low-entropy aggregates
anonymous.

## Review gates before real use

B-01/B-02 remain open. Before any source access, review the exact Census table
or ALFRED series rights, attribution, official archive and release schedule,
privacy scope, local storage, retention/deletion and output handling. Verify
original bytes and first-estimate releases, pre-register chronological
fit/validation/locked-holdout origins, compare with the fixed baselines, and
obtain independent source/model review. Preserve later annual revisions as a
separate sensitivity analysis. A passing test or local quality gate cannot
resolve these reviews or establish official CI.

See the source walkthrough (../CENSUS_VINTAGE_EVALUATION.md), vintage selector
guide (../CENSUS_VINTAGE_ADAPTER.md), aggregate-vintage protocol
(../CENSUS_ALFRED_VINTAGE_PROTOCOL.md) and synthetic fixture card
(../datasets/SYNTHETIC_CENSUS_VINTAGES.md).
