# Dataset card — synthetic UCI event-time protocol fixture

## Status and intended use

This card describes only the fictional, deterministic XLSX created in memory by [`examples/m1_uci_event_time_research.py`](../../../examples/m1_uci_event_time_research.py). It exists to test the `UciWorkbookReadResult` to event-time evaluation flow. No official UCI workbook, downloaded row, customer record or real product code is used.

## Provenance and construction

| Property | Value |
| --- | --- |
| Generator | `build_synthetic_workbook()` |
| Source period | Fictional event dates spanning 2010-12-01 through 2011-12-09 |
| File handling | `BytesIO`; deterministic normalized ZIP metadata and in-process SHA-256 |
| Sheet and columns | One `Online Retail` sheet with the exact eight synthetic UCI-shaped columns |
| Positive observations | One fictional product appears once per source date except a deliberately absent product-day; a second fictional product first appears in validation |
| Exclusion cases | One cancellation-marked row, one zero-quantity row and one negative non-cancellation row |
| Extra fields | Fictional descriptions, customer IDs and country values verify field minimization; none are returned |
| Date completeness | A synthetic caller declaration covers every date in the fixed source period; tests also remove dates to verify abstention |
| Output | 377 parsed rows (374 accepted positive rows plus three excluded rows), aggregate counts, digest, fixed metrics and ordinal-only product results |

The deliberate absent product-day is a zero only because the generated fixture's date declaration is complete for that day. A missing date declaration instead abstains. This fixture does not establish completeness for a real source.

## Rights, privacy and retention

All identifiers and values are invented. No external license applies to these generated values. The original [UCI source review](UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) is separate; its CC BY 4.0 catalog statement does not clear the additional privacy, handling, permitted-use, storage or retention gates for actual workbook processing. Automated tests must continue to use synthetic data.

The example holds workbook bytes and parsed rows in memory and prints no row-level values. It writes no source file. This is not proof of secure memory erasure or process isolation. For any separately approved original data, use private local storage outside the repository and follow the reviewed retention/deletion plan; never commit raw or identifying records.

## Limitations and checks

The synthetic fixture establishes parser and protocol wiring, deterministic output, fixed split behavior, missing-date abstention and identifier omission. It does not establish original workbook compatibility, publication history, true demand, rights, real-world baseline skill, uncertainty calibration or inventory impact.

Relevant regressions:

- `tests/integration/test_uci_event_time_cli.py::test_synthetic_cli_is_reproducible_and_keeps_event_time_limitations`
- `tests/unit/test_uci_event_time.py::test_incomplete_target_day_abstains_instead_of_becoming_zero`
- `tests/unit/test_uci_event_time.py::test_validation_scores_do_not_depend_on_locked_holdout_values`

See the [event-time walkthrough](../M1_UCI_EVENT_TIME_RESEARCH.md) and [model card](../model_cards/SYNTHETIC_UCI_EVENT_TIME.md) for reproduction steps and interpretation.
