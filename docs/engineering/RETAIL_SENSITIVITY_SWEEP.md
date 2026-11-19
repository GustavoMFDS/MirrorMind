# Retail excluded-target sensitivity sweep — experimental

[Source](../../src/mirrormind/domains/retail/sensitivity_sweep.py) compares
a limited set of **2–8 strictly increasing caller-selected hypotheses** about
the possible units on dates that the [single-ceiling sensitivity
diagnostic](RETAIL_SELECTION_SENSITIVITY.md) could not evaluate.

The sweep now audits the two historical cutoff windows **once each**, then
reuses immutable integer tuples of (requested, eligible, eligible positive-line
unit sum) to evaluate every declared ceiling. The standalone single-ceiling
API calls the same shared collection and arithmetic helpers. Thus two historical
evaluations serve 2–8 scenarios, rather than running two evaluations per
ceiling. **This is a structural reduction in calls, not a measured wall-clock
speedup.** Results carry the same
earlier/later denominators, eligible counts, difference floor and ceiling,
and explicitly conditional direction. Widening a declared ceiling can
only decrease the difference floor and increase the difference ceiling;
the eligible observations remain unchanged.

**Additional disclosure gate:** by default, each window must have at least
three eligible dates **and** at least 80% exact eligible-date coverage.
Both conditions must hold in **both windows** before any hypothetical
mean or difference is exposed. The check uses integer multiplication
(`eligible * 100 >= requested * minimum_coverage_percent`) without
rounding; for example 4/7 passes 57% but fails 58%. If a gate fails,
all scenario means, mean differences and sign labels are suppressed,
while requested and eligible counts and the failed-gate status remain.
The caller may explicitly choose a weaker gate for invented research
(`minimum_eligible_per_window >= 2`, coverage 1–100%), but that is a
documented assumption, not statistical evidence or privacy certification.

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
scenarios unchanged. Single-eligible-day windows abstain for all ceilings. A full-window
fixture passes the default gate, while incomplete windows suppress
means unless explicitly overridden with a low research-only threshold.
Threshold rejection, 4/7 coverage at 57% versus 58%, and withholding
results when only one window misses the minimum are also tested.
A strict cap/shape/type validation and incomplete release rejection are
also tested. Regression tests compare each optimized result against the
independent single-ceiling API (including withheld, incomplete and complete
synthetic histories), and instrument the history evaluator to prove eight
scenarios call it exactly twice at the correct cutoffs.

Claim **MM-SWEEP-003** documents the two-audit invariant through
`tests/unit/test_retail_sensitivity_sweep.py::test_eight_scenarios_run_exactly_two_historical_audits`.

Claims **MM-SWEEP-002** (default gate) and **MM-SWEEP-001**
(monotonicity under an explicit weak research gate) map to
`tests/unit/test_retail_sensitivity_sweep.py::test_default_coverage_gate_hides_all_scenario_means_but_preserves_denominators`
and

`tests/unit/test_retail_sensitivity_sweep.py::test_incomplete_windows_can_lose_direction_robustness_as_ceiling_increases`.

Review checklist: inspect time-of-publication assumptions, verify no
excluded value is consulted by the underlying diagnostic, test the same
inputs at ceiling 0 and 1,000,000, check no private invoice/stock/customer
identifiers in receipts, and confirm that no population, bias or forecast
accuracy claim is inferred. A real retail diagnostic still requires
approved sources, authenticated vintages, proper exposure calendars,
independent evaluation and production governance.
