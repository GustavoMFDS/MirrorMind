# MM-M1c — comparable eligible-value summaries (experimental)

## Scope and limits

[The source module](../../src/mirrormind/domains/retail/eligible_values.py)
compares the **mean and median of observed positive-invoice-line units**
for two disjoint adjacent windows. The input consists of fictional, bounded
UCI-shaped product-day projections and separate **unverified, caller-declared**
release dates. An eligible day must have a positive observation, seven
historically available feature days, and enough previously released
residuals for the [prequential envelope diagnostic](RETAIL_RESIDUAL_ENVELOPE.md).

Each window is evaluated with its own date cutoff. This prevents the
later cutoff from retroactively selecting newly published targets in
the earlier window. A later release may change subsequent availability,
but cannot make an earlier result historically visible.

**Eligibility is itself selective.** Missing observations (not zeros),
delayed releases, incomplete features and insufficient calibration remove
dates from the comparison. Means and medians therefore describe only
the *selected, eligible subsets*. They are neither complete sales totals,
unbiased population estimates, evidence of a genuine distribution shift
nor a selection-bias adjustment.

## Explicit gate and honest receipts

The comparator requires at least three eligible days per window by default
(two minimum when explicitly configured) and at least 80% of each window
eligible by default, using exact integer arithmetic without rounding.
If either window fails, it returns only eligibility/abstention counts;
**all means, medians and mean differences are None**.

Receipts contain only aggregate counts and conditional statistics,
without product, customer or invoice identifiers. They explicitly state
`distribution_shift_status=not_identified`,
`selection_bias_status=unknown_for_excluded_targets` and
`significance=None`. Source rights, publisher vintages and retail demand
meaning remain unauthenticated.

## Fictional examples and tests

[Regressions](../../tests/unit/test_retail_eligible_values.py) create
84 invented positive-line dates. With complete publication declarations,
days 71–77 have mean/median **74** and days 78–84 have mean/median **81**.
Their difference of **7** reflects the intentionally increasing fixture,
not evidence of any population trend.

The adversarial fixture delays publication of day 75 until day 84,
omits day 80 and publishes day 83 only after the final cutoff.
The default gate suppresses statistical output, preserves separate
denominators and abstention reasons, and never pads day 80 with zero.
Changing the unavailable earlier day-75 units leaves earlier-window
conditional values unchanged.

Claim **MM-EVALUE-001** maps to
`tests/unit/test_retail_eligible_values.py::test_sparse_observed_and_late_targets_refuse_conditional_difference`.

```bash
python -m pytest -q tests/unit/test_retail_eligible_values.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Review exercise and future acceptance

Compare the same delayed-release fixture under 80% with the three-origin default and 20% with an explicitly
lowered two-origin minimum. The latter can expose descriptive conditional values but
cannot repair missing data, identify excluded targets or establish
generalizable distribution change.

A real shift assessment requires independently authorized source rights,
authenticated historical publisher snapshots, stable product/exposure
calendars, predeclared distributional estimands, adequate samples and
independent validation. No forecasting, calibration or WorldKernel
capability is made operational by this module.
