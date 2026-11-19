# MM-M1c — adjacent-window eligibility drift audit (experimental)

## What is actually measured

[Source](../../src/mirrormind/domains/retail/eligibility_drift.py)
compares **two disjoint, consecutive holdout windows** using the
[prequential residual envelope diagnostic](RETAIL_RESIDUAL_ENVELOPE.md)
and its exact abstention reasons. The earlier window is evaluated at its
**own earlier cutoff**, not using the later evaluation date. Therefore
publisher releases declared after that earlier cutoff cannot retroactively
turn unavailable history or targets into earlier-window evidence.

Each window contains 2–30 daily origins. The immutable receipt provides
separate denominators, evaluated-origin numerators and missing-target,
unpublished-target, feature-history and calibration-insufficiency counts.
Each group must sum to its own requested-origin count. Only the **change
in eligible origin counts** is reported. A mismatch is a warning that
the evaluated subset may differ materially between the windows.

**This does not identify selection bias, estimate a correction for it, or
measure changes in the distribution of true demand.** Values for excluded
targets are unknown, so conditional scores and retrospective interval-hit
rates cannot tell us the performance on excluded dates. The receipt
explicitly states `selection_bias_status=not_identifiable_from_eligible_only_targets`
and `distribution_shift_status=not_measured`. It provides no statistical
significance value, no calibrated intervals and no future performance claim.

The data remain invented positive invoice-line proxies with independent,
caller-asserted and **unauthenticated** release dates, not authorized
retail ingestions, complete store calendars or empirical forecast outcomes.

## Fictional cases and adversarial review

[Unit regressions](../../tests/unit/test_retail_eligibility_drift.py)
use a complete synthetic 84-day positive-line history and demonstrate
**7/7 eligible days in each holdout window** (days 71–77 and 78–84).
A second fixture removes day 80 (not zero), delays release of day 75 and
leaves day 82 unpublished by the later cutoff. Both windows then have
excluded origins, with separate causes rather than false model ranks.

A negative control moves the release of day 75 from day 84 to day 85.
The earlier window's entire eligibility summary must be unchanged:
both declarations are after its own day-77 cutoff. Other tests require
complete exact release declarations and bounded, unambiguous date inputs.

Claim **MM-EDRIFT-001** maps to
`tests/unit/test_retail_eligibility_drift.py::test_future_release_change_cannot_rewrite_earlier_eligibility`.

```bash
python -m pytest -q tests/unit/test_retail_eligibility_drift.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Review exercise and future acceptance criteria

Move a target release from after to before the **earlier window's cutoff**
and observe which eligibility counts change. Distinguish this bookkeeping
effect from a shift in the true underlying sales-generating process.

A genuine distribution-shift assessment requires approved, verified
revisions and publisher vintages, complete exposure/collection calendars,
known denominator definitions, adequate effective sample sizes and
predeclared methods. Historical authorization, identifiable selection
mechanisms, model calibration, production forecasting and WorldKernel
decisions remain separate uncompleted gates.
