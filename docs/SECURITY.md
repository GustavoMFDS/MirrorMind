# Security, privacy and safety expectations

- Data connector credentials are opt-in and are never committed. `.env` and user datasets are gitignored.
- Ingestion must honor authorization, licenses, tenant access, retention and source freshness. Web search text and RAG documents are **untrusted input**, never instructions with tool privileges.
- Human approval for sensitive writes; simulation must never silently execute business changes.
- Model calls and job execution must have server-side budgets, timeouts, cancellation and audit once they are implemented; prompt-only limits are insufficient.
- Track provenance and evaluated model versions; do not present simulated outcomes as guaranteed forecasts or causal proof.
- Logging must redact credentials and sensitive user content.
- The M0 scaffold has **no real authentication, connectors or execution enforcement** and is not production-ready.

## Experimental M1 synthetic fixture boundary

The standalone [M1 data preflight](engineering/M1_DATA_PREFLIGHT.md)
is intentionally synthetic-only. It enforces local byte,
row and declared calendar cutoffs but **does not** verify
source authorization, provenance truth or historical data
availability. Do not use private or customer data as a
shortcut demonstration, do not promote its source labels
to verified evidence, and do not describe its numerical
summary as a forecast or business outcome.

## Local CSV staging is not source authorization

The [source-level staging parser](engineering/M1_LOCAL_CSV_STAGING.md)
accepts **bytes supplied by a trusted caller** and an expected
digest. Matching SHA-256 checks bytes only; it does not
authenticate the publisher, grant licenses, ensure tenant
separation or validate the source's original reporting time.
The parser has no I/O, logging or public API endpoint,
but its returned `StagedSnapshot` includes raw internal
rows; a future consumer must enforce access permissions,
minimization and retention before forwarding those rows
to an API, AI model or any external service. Avoid
using customer data in examples or unit tests.

## Offline baseline evaluator inherits staging trust limits

The [staged rolling evaluator](engineering/M1_STAGED_ROLLING_BASELINES.md)
uses immutable but **source-unverified** observations.
It does not enforce legal rights, producer identity,
tenant isolation, model-call/compute budgets, private
data deletion or a secure inference API. Even when
its generated fixture produces zero MAE, its
result is **not** a verified business recommendation.
A future deployed consumer must authorize each
source and control recipients of raw staged rows.

## Source discovery is not a permission grant

The candidate [M5 source-rights review](engineering/datasets/M5_ACCESS_REVIEW.md)
is explicitly **proposed, not approved**.
Do not use public Kaggle/Zenodo accessibility
as permission for the future commercial product,
nor assume the licensing of a published paper
covers the underlying competition dataset.
The next real-data milestone must include an
independently reviewed source grant, approved
retention/distribution scope and actual
publication-time provenance before acquisition.

## Bounded reading does not authorize data access

The [local bounded stream staging function](engineering/M1_LOCAL_CSV_STAGING.md)
is a limited resource-control primitive.
A trusted caller supplies an open binary
stream; the function does not choose a path,
authenticate source rights, verify a publisher
or authorize users. Its generic `OSError`
translation avoids copying paths into the
direct exception text but is not a system-wide
logging/redaction policy. Preserve independent
access-control, privacy, licensing and
retention reviews before any real-data use.

## Even licensed source data require minimization

The [UCI Online Retail license candidate](engineering/datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
offers an official CC BY 4.0 statement,
but it contains customer and invoice
identifiers. A source-specific approved
pipeline must minimize identifiers **before**
storage or model consumption, respect
attribution and retention, and keep original
files out of Git and CI. The license does
not turn transaction event dates into
verified historical data-release timestamps.
No data are approved or ingested by
this documentation-only review.

## Aggregate quality diagnostics do not declassify source data

The [snapshot quality report](engineering/M1_LOCAL_CSV_STAGING.md)
does not return raw rows or series IDs,
but still exposes date boundaries,
row counts and a snapshot hash.
For genuine customer datasets, those
can be sensitive business metadata.
A future caller must enforce access
rights and retention even for aggregate
reports; internal checks do not authenticate
source provenance, legal permissions or
publication-time history.

## UCI-shaped retail projection does not authorize upstream files

The [retail-domain projection](engineering/UCI_RETAIL_PROJECTION.md)
is a bounded **in-memory** transformation, not
a dataset acquisition or permissions service.
It does not access `CustomerID`,
`Description`, `UnitPrice` or `Country`
values supplied in extra mapping columns.
However, a caller may already have processed
sensitive rows. Its outputs still contain
product codes, event dates and aggregate
counts, which can be business-sensitive.
Enforce access control and retention before
processing approved customer data, and keep
raw workbook files and identifiers out of
Git, logs and model prompts.
The original UCI source review still requires
attribution/privacy approval; event timestamps
do **not** authenticate publication times.

## A bounded XLSX reader is not hostile-file isolation

The optional [UCI-shaped workbook reader](engineering/UCI_WORKBOOK_READER.md)
checks compressed input length, caller-declared
SHA-256, ZIP member sizes/ratios and forbidden
active content markers before invoking a
read-only `openpyxl` parser on an in-memory
stream. These checks reduce some input risks
but **do not** sandbox malicious XML, guarantee
CPU/memory limits or confer legal source
authorization. The caller must independently
approve source rights and privacy, and
no original UCI customer data belongs in
source control, logs or test fixtures.
Extra spreadsheet fields may be parsed
internally by openpyxl; only the four
reviewed transaction columns are forwarded
to the application projection. Its output
remains business-sensitive, not declassified.

## Fictional evidence retrieval is not access control

The experimental [M2 retrieval library](engineering/M2_EVIDENCE_RETRIEVAL.md)
uses generated documents and a caller-provided principal/collection context.
Filtering before indexing is a useful local invariant, but the context is not
an authenticated identity, tenant boundary or source-use grant. The example
has a fixed fictional scope, emits excerpts as `untrusted_evidence`, and does
not expose a retrieval route, fetch URLs, write data or call a model. Never
pass customer/private content to the example or treat its BM25 score and
citation digest as proof of truth, origin, rights or freshness. Any persistent
or served retriever requires reviewed identity, authorization, tenant,
retention, deletion and prompt-injection controls first.
