# Retail excluded-target sensitivity sweep — experimental

[Source](../../src/mirrormind/domains/retail/sensitivity_sweep.py) compares
a limited set of **2–8 strictly increasing caller-selected hypotheses** about
the possible units on dates that the [single-ceiling sensitivity
diagnostic](RETAIL_SELECTION_SENSITIVITY.md) could not evaluate.

Each hypothesis is an independent invocation of the existing as-of
eligibility and hypothetical-mean arithmetic. Results carry the same
earlier/later denominators, eligible counts, difference floor and ceiling,
and explicitly conditional direction. Widening a declared ceiling can
only decrease the difference floor and increase the difference ceiling;
the eligible observations remain unchanged. If either window has fewer
than two eligible observations, **every** scenario abstains.

The caller must provide an exact tuple of 2–8 unique strictly increasing
integer ceilings, each 0–1,000,000. The budget prevents unbounded repeated
evaluation. Receipts include only per-scenario aggregate diagnostics and
declare missing selection-bias identification and statistical guarantees.
No result is a real value bound, demand distribution-shift detector,
calibrated forecasting interval, or source authorization.

[Invented regressions](../../tests/unit/test_retail_sensitivity_sweep.py)
show 7/7 complete positive-line history producing the same synthetic
+7 difference for any ceiling; delayed and absent lines demonstrate
widening differences and direction ambiguity under larger assumptions.
A hidden earlier value altered from 75 to 999,999 leaves all earlier
scenarios unchanged. Single-eligible-day windows abstain for all ceilings.
A strict cap/shape/type validation and incomplete release rejection are
also tested.

Claim **MM-SWEEP-001** maps to
`tests/unit/test_retail_sensitivity_sweep.py::test_incomplete_windows_can_lose_direction_robustness_as_ceiling_increases`.

Review checklist: inspect time-of-publication assumptions, verify no
excluded value is consulted by the underlying diagnostic, test the same
inputs at ceiling 0 and 1,000,000, check no private invoice/stock/customer
identifiers in receipts, and confirm that no population, bias or forecast
accuracy claim is inferred. A real retail diagnostic still requires
approved sources, authenticated vintages, proper exposure calendars,
independent evaluation and production governance.
