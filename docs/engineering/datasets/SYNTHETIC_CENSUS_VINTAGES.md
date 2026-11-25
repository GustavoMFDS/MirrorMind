# Synthetic aggregate release-vintage fixture card

## Purpose and status

This card describes invented aggregate monthly records used to test the
Census/ALFRED point-in-time selection contract. The fixture contains no
downloaded Census or FRED/ALFRED values, no API response, no credential and no
customer or household information. It is not a dataset permission grant or a
claim that a real source format has been implemented.

## Generated data

Tests construct a small set of monthly observations with fictional series and
release IDs, `Decimal` values, publication dates, release kinds and fixed
64-character digests. One reference month receives a later fictional
revision. The fixture is created inline in unit tests, so no data file is
persisted and no network or filesystem read is required.

The runnable baseline example separately generates 21 monthly first estimates
from January 2020 through September 2021 and one fictional November revision.
Validation and holdout origins are disjoint, and every date/value is invented.
The example evaluates three fixed horizons using publication-date selection;
it is only a deterministic mechanism demonstration.

The adapter's normalized record contract separates:

- `reference_month`: month described by an observation;
- `published_on`: date the release became public;
- `release_kind`: first estimate, monthly revision or annual revision;
- `release_id`: fictional identifier for the publication artifact;
- `snapshot_sha256`: syntactically valid digest associated with that artifact.

Values are non-negative fictional `Decimal` amounts. Missing months remain
absent; tests do not infer zero from absence. Tests select the latest record
whose publication date is strictly earlier than a requested release date.
Date-only timestamps provide no intraday ordering, so same-day duplicates
are rejected.

## Rights, privacy and retention

No real data is included or processed. This fixture is generated for testing
and may remain in the repository. It grants no rights to Census, FRED or
ALFRED data. Before any real source bytes are acquired or parsed, review the
exact table/series, source terms, attribution, snapshot, release timestamps,
privacy scope, local storage and retention/deletion procedure in
[`CENSUS_ALFRED_VINTAGE_PROTOCOL.md`](../CENSUS_ALFRED_VINTAGE_PROTOCOL.md).

The adapter validates a digest's syntax but does not verify source bytes,
source identity or legal authorization. Its result always keeps
`ingestion_authorized=false` and `forecast_eligible=false`. API keys are not
read by this fixture or stored in tests.

## Reproduction and limitations

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests/unit/test_census_vintages.py
.\.venv\Scripts\python.exe -m pytest -q tests/unit/test_census_vintage_evaluation.py tests/integration/test_census_vintage_evaluation_cli.py
.\.venv\Scripts\python.exe -m examples.m1_census_vintage_evaluation --split validation
```

These commands prove only deterministic selection and fixed-baseline arithmetic
over constructed records. They do not prove Census/ALFRED archive coverage,
real publication timestamps, source rights, forecast skill, revision quality,
or production readiness. A source-specific parser and empirical evaluation
remain separate, approval-gated work.
