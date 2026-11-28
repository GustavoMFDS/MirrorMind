# Change request — predeclared fictional Census origin schedule

## Goal
M1C-04 descriptive v1 binds a single caller-declared split but cannot verify
that validation and holdout schedules belong to the same predeclared plan.
Add a pure local immutable schedule with fixed 60/20/20 chronological
partitioning and independent expected-digest comparison before evaluation.
No real data, source access, authenticated registration or persistent lock.

## Acceptance
- Exact unique monthly origin dates and increasing issue dates, 10–250 total;
  each issue must follow the end of its own reference month.
- Floor cumulative 60% and 80% boundaries; preserve missing calendar months.
  Do not filter eligible/scored rows to select a more favorable split.
- Reserve the last six months of target reach at each split boundary:
  reject a schedule if a preceding split's latest possible target is
  not strictly earlier than the next split's first origin month.
  Gaps must be deliberately predeclared; never silently remove origins.
- Since publication may lag reference months, additionally verify the
  actual first-estimate publication of every earlier split target is
  strictly before the next split's first issue date, or reject evaluation.
  Missing target labels reject the cross-split verification.
- Bind series, immutable origin schedule and protocol to a canonical digest.
  Verify an independently retained expected digest before any scoring.
  A digest is not proof of pre-registration or independent custody.
- Return separate experimental wrapper, keep existing descriptive/v2
  entrypoints, abstention and non-authorizing flags unchanged.

## Impact
Core: census_split.py (new), existing descriptive evaluator as downstream
caller. Tests: test_census_split.py. Guide: CENSUS_VINTAGE_EVALUATION.md.
No API, dependency, persistence, existing data or authority change.
Review B-01/B-02 remains required. Existing synthetic cards apply. No
inference or empirical score promoted. Independent review before integration.
