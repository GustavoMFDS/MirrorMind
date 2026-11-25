# Proposed aggregate Census release-vintage evaluation protocol

**Status:** method prepared; no Census/ALFRED data, vintage archive, API key
or credential acquired. This protocol supports a temporal-method pilot only.
It cannot validate SKU demand, retailer inventory, supplier lead times or
replenishment policies.

## Objective and source candidate

Evaluate whether MirrorMind's temporal controls can reproduce a forecast using
only aggregate values that were published by each historical origin. Prefer
free official archived Census Bureau releases. Candidate products are
Monthly Retail Trade Survey (MARTS) advance and subsequent monthly estimates;
their reference month, release timestamp and revision status are distinct
fields. The [Census release schedule](https://www.census.gov/retail/release_schedule.html)
and [MARTS methodology](https://www.census.gov/retail/marts/how_surveys_are_collected.html)
are background sources, not a retained vintage archive.

ALFRED may be considered only when access is free and authorized, the selected
series terms permit the exact use, and archived realtime values are adequate
to establish the information set available at each origin. No paid credential
or service is assumed. If a historical vintage cannot be verified, exclude
that origin or stop the pilot; never reconstruct it from a currently revised
series.

## Decision-ready protocol

1. Before retrieving values, select one aggregate series, geography, units,
   release product, target semantics (first release or revised-final), one
   to three monthly horizons, and the intended research-only use.
2. Identify an immutable archive for every value. Record the source URL,
   retained bytes, SHA-256, reference month, first release time and time zone,
   retrieval time, vintage/revision identifier, series definition and
   transformation. A schedule date alone is not evidence that a particular
   value is first-release data.
3. Reserve a chronological final holdout of the latest 12–24 eligible months,
   subject to archive completeness, before model tuning. Use expanding origins
   strictly before the holdout; never shuffle timestamps.
4. At each origin, expose only feature vintages with a documented release
   timestamp at or before that origin. Keep reference month separate from
   availability time. Missing target vintages abstain; never fill missing
   values with zero.
5. Compare matched seasonal-naive lag-12 and trailing-three-month-mean
   baselines on identical eligible origins. Report MAE, RMSE, MASE when its
   denominator is defined, coverage, abstentions/excluded origins, target
   vintage, and uncertainty separately.
6. Freeze split and baselines before tuning. Do not infer product-level
   demand, stockouts, inventory accuracy or policy quality from aggregate
   sales.

## Dataset card and privacy controls

Before acquisition, create a source-specific dataset card and immutable
private manifest. Record exact terms and attribution, authorized research
purpose, series/geography, snapshot and vintage SHA-256 values, retrieval
times, minimum required fields, local access controls, retention deadline and
deletion check. Propose local processing only; keep source bytes and rows out
of Git, CI, logs, prompts and external services. Retain only aggregate
metrics and provenance fields permitted by the approved terms. The owner
selected this method lane but has not approved a particular series, data
retrieval, ALFRED access or source-specific processing.

All tests and examples remain synthetic. A generated fixture can exercise
release-time filtering, revision choice, missing-vintage abstention, exact
holdout boundaries and metric denominators; it cannot establish real archive
availability, rights or forecasting quality. M5 remains NO-GO. B-01 and B-02
remain open until the specific source evidence and review exist.

## Verification and learning

When implemented, add regressions proving that (a) a value released after an
origin cannot enter the feature set, (b) a later revision does not rewrite an
earlier origin, (c) an absent target vintage abstains, (d) both baselines use
the same eligible origin/target pairs and (e) locked holdout labels are never
used for tuning. Link each claim to the top-level test function in the
evidence map and record the source-specific limitation.

To investigate a proposed run, trace the archive manifest into the vintage
selector, draw reference-month and publication-time axes separately, then
recompute one matched-origin metric by hand. Explain which actual bytes prove
the value's vintage and which conclusions aggregate Census data cannot
support. Do not treat a passing fixture or an official release calendar as a
retained first-release value.

See the related [UCI source review](UCI_ONLINE_RETAIL_SOURCE_REVIEW.md),
[dataset card template](../DATASET_CARD_TEMPLATE.md), and the owner direction
and evidence in [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818).
