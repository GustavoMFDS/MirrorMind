# M1c-local — rolling-origin baselines over structurally staged observations

**Status: experimental, offline and source-unverified.**
This is the first reusable baseline evaluator inside
[`src/mirrormind/modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py).
It consumes an immutable
[`StagedSnapshot`](M1_LOCAL_CSV_STAGING.md), not a real
approved dataset or a production forecast API.

See [synthetic weekly staged data](datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md),
[the evaluated model card](model_cards/STAGED_WEEKLY_BASELINES.md),
[M1 delivery plan](M1_EXECUTION_PLAN.md) and
[model evaluation requirements](FORECAST_MODEL_CARD_TEMPLATE.md).

## Source and dependency path

```text
Trusted local caller (not an HTTP endpoint)
  -> stage_csv_snapshot(bytes, expected_sha256) [structural preflight ONLY]
      -> immutable staged Observations, declared availability timestamps
  -> backtest_staged_snapshot(staged, series_id, evaluation_on)
      -> historical target day, prediction origin is the prior day
      -> available_as_of(staged, series_id, origin)
      -> require exactly seven preceding consecutive published days
      -> _predict(history): seasonal naive lag7 / trailing mean lag7
      -> _score on the exact same scored targets for both models
      -> one report with metrics or explicit null + abstention counts
```

**No source authorization happens anywhere in this path.**
A SHA-256 compared with the digest generated from the
same unverified data is not provenance authentication.
Future approved-source ingestion and secure permissions
must remain separate from statistical evaluation.

## Method-by-method reviewed contracts

| Symbol | Inputs / output | Critical failure and statistical boundary |
| --- | --- | --- |
| `_day(value)` | Canonical ISO calendar cutoff -> `date` | Reject invalid/ambiguous/non-string cutoffs; this is not a verified publication timestamp |
| `_predict(seven)` | Exactly seven nonnegative integer past observations -> two one-step estimates | Reject insufficient history; no fit, intervals or future-target access |
| `_score(forecasts, actuals)` | Aligned predictions and held-out actuals -> MAE, RMSE, signed bias, WAPE | Reject mismatched/empty arrays; WAPE `null` for zero observed sum |
| `backtest_staged_snapshot(staged, series_id, evaluation_on, holdout_days=7, min_history_days=14)` | Fixed last `holdout_days` calendar dates ending at the declared evaluation cutoff; returns counts, optional metrics and snapshot hash | Reject non-staged input, bad bounds, unknown series and insufficient event-span; abstain when a target was not published by final cutoff or the lag-7 input wasn't published by its own origin |

Each candidate target date is **fixed from the cutoff**,
not chosen because a convenient observation exists.
For day `t`, the forecast is formed at `t-1`
using only `t-7 ... t-1` **if every value was published
by that origin**. The code calls the shared staged
snapshot's `available_as_of`, never substitutes a
missing value with zero, and does not silently change
the comparison set for one model only.

The final evaluation may use target outcomes that were
published by the evaluation cutoff. It cannot claim a
true untouched or independently pre-registered holdout:
the fixture is explicitly generated to favor a seasonal
pattern. Real sources may have revisions, blackout
windows, backfilled labels and reporting timestamps
that this module cannot authenticate.

## Deterministic example: four of seven origins scored

The invented CSV has **35 consecutive January 1–February 4,
2025** dates repeating `[2,4,6,8,10,12,14]`, with
January 27 declared published only on January 31.

- Origins January 28, 29 and 30 cannot see January 27
  and abstain.
- The February 1–4 targets have complete seven-day
  published windows. Their synthetic actuals are
  `[8,10,12,14]`, and the last-seven mean is 8.
- Both models are evaluated on these **same four days**.

| Metric | Lag-7 seasonal naive | Trailing 7-day mean |
| --- | ---: | ---: |
| MAE (synthetic units/day) | 0 | 3 |
| RMSE | 0 | sqrt(14) ≈ 3.7417 |
| Signed bias (forecast minus observed) | 0 | -3 |
| WAPE ratio | 0 | 3/11 ≈ 0.2727 |
| Scored / requested origins | 4/7 | 4/7 |

The report separates `abstained_missing_history`
from `abstained_target_unavailable`. If fewer than two
origins are scored, it emits **null metrics and null winner**
instead of inventing a model ranking. A repeated-week
synthetic pattern yielding zero errors does not show
real predictive accuracy, improved retailer inventory
or causal benefit. Coverage selection itself can
bias the measured error.

## Reproduce using only invented local observations

```python
from hashlib import sha256
from pathlib import Path
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.forecasting.baselines import backtest_staged_snapshot

raw = Path("examples/staged-weekly-availability.csv").read_bytes()
staged = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
report = backtest_staged_snapshot(
    staged, series_id="item-A", evaluation_on="2025-02-04"
)
assert report["scored_origins"] == 4
assert report["abstained_missing_history"] == 3
assert report["source_status"] == "not_authorized_or_authenticated"
```

Again, this recipe hashes the same generated fixture:
**it demonstrates parser behavior, not actual source
or licensing proof**. The core functions do not open
files or issue network requests on their own.

## Curated regressions and explicit limitations

| Claim | Test selector | What this does not prove |
| --- | --- | --- |
| **MM-BL-001** | `tests/unit/test_staged_rolling_baselines.py::test_staged_rolling_baselines_score_four_of_seven_after_late_publication` | Scores are on invented seasonality and do not generalize to genuine demand |
| **MM-BL-002** | `tests/unit/test_staged_rolling_baselines.py::test_all_forecast_inputs_precede_origin_and_have_available_seven_day_window` | Explicit window selection does not authenticate actual publication dates or hidden features |
| **MM-BL-003** | `tests/unit/test_staged_rolling_baselines.py::test_all_origins_can_abstain_with_null_metrics_not_fake_winner` | Abstention prevents fabricated scores, but is not an uncertainty/calibration assessment |
| **MM-BL-004** | `tests/integration/test_staged_rolling_flow.py::test_staged_csv_to_matched_rolling_backtest_without_runtime_io` | Local fixture integration does not provide permission, production execution or versioned model serving |

Other tests cover observed zero versus missing target,
late publication, bad horizon/date, insufficient
prehistory and undefined WAPE at an all-zero denominator.

```bash
python -m pytest -q tests/unit/test_staged_rolling_baselines.py
python -m pytest -q tests/integration/test_staged_rolling_flow.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These are reproduction instructions, not claims that
real observations or authorized sources have been tested.

## Independent exercise and next acceptance gate

Change January 27's claimed `available_on` to
January 27 and predict why all **7/7** origins become
scorable. Then postpone January 28 publication until
March and identify why even the last origin must abstain.
Explain how a 4/7 result can conceal selection bias
against a model evaluated on all seven days, and why
a good WAPE on deliberately repeated invented data
cannot justify purchasing inventory.

Before calling a real forecasting feature
`implemented`, obtain a separately approved dataset,
first-availability and revision evidence, source rights,
locked temporal holdouts, a second measured baseline,
uncertainty evaluation, versioned inference output,
access controls, model-card review and actual replay.
**The existing `forecasting` capability remains planned.**


## 6. Auditable origin disposition (M1c local improvement)

A single MAE can conceal **which days were excluded** from
evaluation. `backtest_staged_snapshot` therefore includes
`origin_audit`, a deterministic, one-row-per-requested-origin
list of day-level **nonvalue** metadata:

| Field | Meaning |
| --- | --- |
| `target_on` | The calendar day for which one-step comparison was requested |
| `origin_on` | The immediately preceding prediction origin |
| `status` | One of `scored`, `required_history_unavailable`, `target_missing`, or `target_not_published_by_cutoff` |

The fixture produces three
`required_history_unavailable` days (Jan 29–31) and
four `scored` days (Feb 1–4). `scored_origins`,
`abstained_missing_history` and
`abstained_target_unavailable` remain intact for
compatibility. The new counters
`abstained_target_missing` and
`abstained_target_not_published` partition the
existing target-unavailable counter. Thus:

```text
requested_origins =
    scored_origins +
    abstained_missing_history +
    abstained_target_unavailable

abstained_target_unavailable =
    abstained_target_missing +
    abstained_target_not_published
```

The list deliberately contains no original units,
raw data payload, individual forecast values or model
prompts. It **is not safe to expose indiscriminately**:
calendar dates, series IDs and a snapshot hash can still
be sensitive metadata for real sources. This is an
internal review artifact, not an authenticated audit
event store, tamper-proof signature or authorization
token. The original snapshot remains unverified.

### Additional claim IDs and independent regressions

| Claim | Direct test | Limitation |
| --- | --- | --- |
| **MM-AUD-001** | `tests/unit/test_staged_rolling_baselines.py::test_every_requested_origin_has_one_reproducible_nonvalue_audit_record` | Deterministic status per synthetic date does not certify actual publisher timing or legal data rights |
| **MM-AUD-002** | `tests/unit/test_staged_rolling_baselines.py::test_missing_target_is_not_conflated_with_unpublished_target` | Distinguishing two missingness reasons does not recover missing records or establish model quality |
| **MM-AUD-003** | `tests/unit/test_staged_rolling_baselines.py::test_all_abstained_audit_has_no_fabricated_scores` | A complete abstention record is not a forecast, decision or calibrated uncertainty estimate |

**Exercise:** remove the Feb 4 row from the invented
CSV and recalculate its digest, then restore the row
but declare first publication on Feb 5. Predict the
two distinct statuses and counters. Explain why a
reviewer should consider the excluded dates before
claiming one model is superior, and why merely
printing an audit list does not make it authentic.


## 7. Minimum history counts rows, not calendar age

Earlier code tested the **oldest** staged observation
against `min_history_days`. One ancient row could
therefore satisfy an apparent 14-day history requirement
even when fewer than 14 observations existed before
the first target. The accepted rule is now:

```text
observed_rows_with_event_date_before_first_holdout
    >= min_history_days
```

This is a **count of unique staged observation dates for
the selected series**, not elapsed calendar time or a claim
that all these dates were independently published. The
snapshot parser already rejects duplicate series/date
records. Actual seven-day rolling history still requires
a **contiguous, published** window for each target; when
one is missing, the corresponding origin abstains.
The minimum-history preflight does **not** fill holes,
train a model or bypass that per-origin availability check.

The evaluator now also rejects a holdout whose start
would precede the earliest supported ISO calendar day
with a deliberate `ValueError`, rather than leaking
a `datetime.OverflowError`.

| Claim | Negative or boundary test | Limitation |
| --- | --- | --- |
| **MM-HIST-001** | `tests/unit/test_staged_rolling_baselines.py::test_min_history_counts_observations_not_one_ancient_row` | Actual row counts do not establish real publisher provenance or statistical representativeness |
| **MM-HIST-002** | `tests/unit/test_staged_rolling_baselines.py::test_earliest_supported_calendar_cutoff_fails_cleanly_not_overflow` | Clean calendar failure does not prove safe real-data ingestion or permission checking |
| **MM-HIST-003** | `tests/unit/test_staged_rolling_baselines.py::test_custom_history_minimum_is_an_observation_count` | The threshold checks record count only; missing/late series remain subject to other gates |

**Independent exercise:** keep January 1 and only
January 22–February 4 of the synthetic fixture.
Predict why a 14-observation prehistory fails even
though the oldest event is four weeks before the
holdout. Lower the count threshold to seven and
explain why the three late-publication abstentions
still apply. Do not infer source permission or
generalized forecasting accuracy from either result.
