# MM-M1c — excluded-target counterfactual sensitivity (experimental)

## Why this diagnostic exists

[The eligible-value comparator](RETAIL_ELIGIBLE_VALUES.md) reports only
positive-line proxy dates that passed historic as-of evaluation. Large
differences between eligible means cannot tell us what happened on
**excluded** dates. This diagnostic makes that limitation visible with
explicit, caller-chosen **counterfactual assumptions** rather than
silently converting missing or unpublished observations to zero.

[Source](../../src/mirrormind/domains/retail/selection_sensitivity.py)
reuses the prequential eligibility audit independently for two disjoint,
adjacent windows, each evaluated at its **own** date cutoff.
It never retrieves excluded values, including values present in a later
snapshot but not declared published by that earlier cutoff.

## Mathematical scenario, not a data inference

A caller **must** supply an exact nonnegative integer upper bound
`excluded_value_ceiling` (0–1,000,000) for a hypothetical
per-excluded-date value. This is **not validated against true demand**.
Let S be the sum over eligible proxy values, N the number of requested
dates and E the number eligible. For each window, the scenario computes:

- Hypothetical mean floor: `S/N`.
- Hypothetical mean ceiling: `(S + (N-E)*ceiling)/N`.
- Difference floor: later floor minus earlier ceiling.
- Difference ceiling: later ceiling minus earlier floor.

This is interval arithmetic under an expressly stated scenario
`0 <= unknown excluded value <= ceiling`, **not an imputation or
assertion that the excluded dates actually have those values**.
For both windows with at least two eligible values, the scenario reports
the sign only if both extremes agree; otherwise direction is marked
nonrobust. If either window has fewer than two eligible references, all numeric
bounds are omitted and the function abstains.

The receipt reports counts, assumptions and the status flags
`selection_bias_status=not_identified` and
`population_shift_status=not_identified`. It reveals no customer,
invoice, product identifier, unavailable unit value, individual forecast
or target. Neither real demand nor even complete positive-line exposure
has been established; the scenario is purely hypothetical.

## Fictitious experiment and negative controls

[Tests](../../tests/unit/test_retail_selection_sensitivity.py)
use 84 invented positive-line days. With no missing data, both windows
have 7/7 eligible dates, exact proxy means 74 and 81 and the
hypothetical difference interval collapses to +7.

An adversarial version removes day 82, declares day 75 released only on
day 78 and leaves day 83 unpublished by the evaluation cutoff. With a
hypothetical excluded-value ceiling of 1,000, the difference interval
spans negative and positive values, so the direction is **not robust**.

A further privacy regression refuses mean bounds with only one eligible
record in either window, preventing reconstruction of an individual
positive-line total from the aggregate receipt. Zero eligible days
also force abstention. Changing the hidden earlier day-75 value from 75 to 999,999 cannot
change any earlier-window scenario bound. Widening the caller ceiling
cannot narrow the hypothetical difference interval. Invalid ceilings,
missing publication declarations and ambiguous dates fail closed.

Evidence claim **MM-SEL-001** maps to
`tests/unit/test_retail_selection_sensitivity.py::test_incomplete_windows_show_unknown_days_can_reverse_apparent_difference`.

```bash
python -m pytest -q tests/unit/test_retail_selection_sensitivity.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Remaining acceptance gates

The ceiling is a sensitivity assumption rather than a proven bound on
any real target. A positive sign conditional on it is not statistical
evidence of drift or forecast skill. Authorized ingestion, publisher
snapshot verification, exposure calendars, valid estimands for demand,
external holdouts, bias mechanisms, model calibration and WorldKernel
execution all remain outstanding. No production inference capability
is introduced.
