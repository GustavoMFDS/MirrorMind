# Model card — fictional UCI event-time baselines

## Status and intended use

These are two fixed one-day reference heuristics in the experimental local [`UCI event-time evaluator`](../M1_UCI_EVENT_TIME_RESEARCH.md): same-weekday last week and the mean of the preceding seven calendar days. They demonstrate evaluation mechanics on invented data. They are not fitted or tuned models, empirical forecasts, inventory policies or recommendations.

## Data and temporal protocol

The only runnable dataset is the [synthetic XLSX fixture](../datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md). The fit/cohort window ends 2011-08-30. Validation targets span 2011-09-01 through 2011-10-01; the locked holdout targets span 2011-10-02 through 2011-12-09. Both windows use fixed one-day forecasts and the same eligible product-origin pairs. Products enter the cohort only after a positive product-day in the fit window.

`InvoiceDate` is event time, not a record-publication timestamp. The output label is `event_time_retrospective_unverified_availability`. This protocol cannot establish which inputs were knowable at each historical origin. The holdout mutation regression proves only that the validation calculation does not consume later fixture values.

## Baselines and metrics

- `same_weekday_last_week`: prediction equals the positive invoice-line units seven calendar days earlier.
- `trailing_7_calendar_day_mean`: arithmetic mean over those same seven preceding calendar dates.
- `MAE`: average absolute error across matched eligible product-origin pairs.
- `RMSE`: square root of average squared error on the same pairs.
- `WAPE`: total absolute error divided by total actual positive invoice-line units; `null` when the denominator is zero.
- `coverage`: scored pairs divided by the frozen cohort's eligible pairs; target and history uncertainty remain distinct abstentions.

An absent product-day is zero only where the caller explicitly declared the entire event date complete. An undeclared target or any undeclared history date abstains. No missingness is imputed, no model is selected and no interval is calculated.

## Results, uncertainty and known risks

No empirical result is reported. Every fixture value is fictional. Positive invoice-line units are not latent unconstrained demand; returns, stock availability, product-code quality, transaction duplication and publisher revisions can change real interpretation. UCI has no row-level release vintages in this protocol. MAE/RMSE/WAPE are descriptive arithmetic, not uncertainty or calibration evidence.

## Review gates before any real source use

Before acquiring or processing the original workbook, an accountable owner must review the current source terms and attribution/change notice, approved research/commercial scope, minimal field projection, cancellation rules, local storage, retention/deletion and exact source manifest. Raw files and identifiers remain out of Git, CI, logs, prompts and external services. A later point-in-time evaluation needs authentic release vintages and a separate approved protocol; this card cannot be promoted to satisfy B-02.

The [research guide](../M1_UCI_EVENT_TIME_RESEARCH.md) links every metric and abstention rule to unit and integration regressions. Those tests verify behavior on synthetic fixtures only.
