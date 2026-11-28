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

B-01/B-02 remain open. The current proposal prefers original Census MARTS
release artifacts, subject to exact artifact rights, attribution, official
archive completeness, publication schedule/timezone, privacy scope, local
storage, retention/deletion and output review. FRED Services terms apply to
ALFRED and prohibit storage/cache/archive; API terms also prohibit
software/AI-development use, so FRED/ALFRED is currently NO-GO for this
development/archive route absent St. Louis Fed written authorization or
changed terms, plus separate source-owner rights clearance. Before any Census
source access, verify original bytes and first-estimate releases, pre-register
chronological fit/validation/locked-holdout origins, compare with fixed
baselines, and obtain independent source/model review. Preserve later annual
revisions as a separate sensitivity analysis. A passing test or local quality
gate cannot resolve these reviews or establish official CI.

See the source walkthrough (../CENSUS_VINTAGE_EVALUATION.md), vintage selector
guide (../CENSUS_VINTAGE_ADAPTER.md), aggregate-vintage protocol
(../CENSUS_ALFRED_VINTAGE_PROTOCOL.md) and synthetic fixture card
(../datasets/SYNTHETIC_CENSUS_VINTAGES.md).

### Experimental descriptive companion

The optional local descriptive result includes exact paired absolute losses
for fictional scored origins; the default v2 output remains minimized.
It explicitly abstains from inferential comparison and winner selection.
A caller-supplied split does not prove cross-split disjointness or a frozen
holdout. No uncertainty calibration or empirical performance is claimed.
See [paired loss walkthrough](../CENSUS_VINTAGE_EVALUATION.md).

The experimental predeclared schedule wrapper uses cumulative 60/80%
floor cuts and rejects cross-split target reach or late/missing prior
labels. This is local caller-retained digest matching only. It neither
verifies an independent holdout lock nor authorizes empirical evaluation.

The local experiment contract binds caller-retained normalized manifest,
schedule and declared code revision. Replay compares complete canonical
receipt bytes; no empirical source or independent code attestation.
The current schedule permits at most 50 holdout origins, below the
proposed 60 matched-pair minimum; inference remains abstained.

The experimental journal persists only the local experiment identity and
replayed result digest. It does not establish independent preregistration,
blind access or empirical performance. All inference remains abstained.

The separate fictional runner fixture has 80 invented records,
deterministic trend and seasonality, and 30/10/10 declared origins with
embargo gaps. Metrics are descriptive only; inference remains abstained.

The local observatory displays the fixed synthetic runner's descriptive
metrics and receipt provenance. It does not provide inference, independent
holdout protection or empirical claims.

The experimental catalog adds flat, deterministic volatile and abrupt
level-shift fixtures to the original trend-seasonal example. These fixed
designed sequences share the origin schedule but have distinct manifests.
They are not independent random draws, a calibration study or evidence
of empirical forecasting skill.

The comparative observatory retains separate results and identities for
the four deterministic fictional scenarios, with no pooled metric,
ranking, inference or empirical model selection.

The experimental history view displays stored commitment metadata without
scoring by default. Explicit replay checks one recorded digest using current
code and the known fictional catalog. No chronology, independent attestation,
empirical validation or inference is claimed.

The one-factor sensitivity example uses 15 fixed cells, 13 unique
commitments and a shared zero baseline. Exact paired differences are
descriptive, not inferential. No stochastic replication, model selection,
empirical validation or independent holdout claim.

The separate five-model experimental protocol adds persistence, seasonal
drift and OLS trend with a 13-month common history requirement. It uses
validation only, checks legacy losses exactly and reproduces complete
receipts. No model promotion, holdout execution, inference or empirical
skill is asserted. A designed validation break is distinct from the
original post-validation break fixture.

The separate experimental probability core provides exact finite
discrete mathematical operations. It has no fitted model or predictive
calibration evidence, does not modify the deterministic protocols and
does not authorize empirical uncertainty or forecasting claims.

The separate fixed probability study evaluates five methods (including
a privileged reference) under two deterministic synthetic designs.
Exact scores and local receipt replay do not establish calibration,
empirical skill, independent registration or a statistical winner.

The local probability observatory renders a freshly replayed fixed
fictional study and one preselected example per group. Reference-law
coverage, observed coverage and CRPS do not establish empirical
calibration or a statistical winner.

The separate experimental bivariate core adds bounded joint mathematical
operations, not a fitted predictor. Equal marginal scores do not
establish accurate dependence; joint Brier excess is reference-relative.
No empirical calibration or causal effect is established.

The fixed fictional bivariate study estimates contemporaneous dependence
from observed pairs and compares matched independent forecasts. It uses
independent-in-time increments and a privileged reference; no causal
effects, empirical calibration, holdout or statistical winner.

The bivariate observatory visualizes a freshly replayed fixed study and
preselected joint examples, not an operational model or independent
calibration or causal evidence.

The experimental joint Markov engine adds exact conditional propagation
for four paired sign states under bounded caller-supplied schedules.
It does not establish learned dynamics, authentic transitions,
causal effects, empirical calibration or operational forecasts.

Experimental temporal estimators learn fixed transition rows from
24 supplied paired sign states, then propagate conditional joint PMFs.
No authenticated temporal availability, model selection, empirical
calibration, causal effects or operational forecasts.
