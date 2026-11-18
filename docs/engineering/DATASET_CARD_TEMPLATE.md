# Data card template — authorization, availability and leakage

> Copy into a new reviewed file for **each permitted source/snapshot**.
> A card is a claim/evidence record, not a substitute for legal approval
> or an automated permission check. Use no real sensitive data in this template.

## 1. Owner, scope and permissions

- Card ID and review status: `proposed | authorized | revoked | superseded`
- Dataset owner and accountable reviewer:
- Provider, canonical URL or signed transfer provenance:
- License/contract terms with exact usage scope (training, evaluation, sharing):
- Permission proof and expiration/renewal date:
- Jurisdiction, privacy classification and PII determination:
- Allowed audience, retention period and deletion procedure:
- Prohibited uses, onward sharing and external model access:

**Stop condition:** missing permission proof means **no ingestion**,
even if a file is technically downloadable. Never treat a
user-supplied `source_id` or `usage_note` as permission evidence.

## 2. Reproducible snapshot and schema

- Snapshot identifier, captured UTC timestamp and content hash:
- Storage location (sanitized reference, no credential):
- File format, encoding, timezone and units:
- Series/entity keys and allowed values:
- Row count, unique keys, expected date/frequency coverage:
- Null/zero/negative and deduplication semantics:
- Schema version and compatibility/migration plan:
- Transformations, filters and aggregation code commit:

## 3. Temporal truth and leakage controls

For each field, distinguish:

| Time | Definition | How verified |
| --- | --- | --- |
| Observation time | When the described real-world event happened | |
| Publication/availability time | When that value was first knowable to the decision maker | |
| Snapshot extraction time | When this local copy was obtained | |
| Prediction/decision cutoff | What the model was allowed to know | |
| Target horizon | Period the later forecast/evaluation covers | |

A row with an early observation date may still contain
a value published or revised **after** the prediction cutoff.
Checking `observation_date <= cutoff` is necessary for the
synthetic preflight but not sufficient against temporal leakage.

- Source updates/revisions and known reporting delay:
- Prevent future-derived features, post-event labels and target leakage:
- Split by time (never randomly shuffle a temporal holdout):
- How to test a deliberately late-published row:
- Known missing days and whether absence differs from zero:

## 4. Quality, bias and limitations

- Missingness by source/series/date, and rejected invalid fields:
- Outliers, duplicates, gap policy and known stockout/censoring bias:
- Distribution shift, seasonality and coverage limitations:
- What the source does **not** measure (e.g. sales ≠ true demand):
- Redacted reproducible quality-check output:
- Independent test selectors and environment:
- Known risks, review decision, date and next review trigger:

## 5. Safe acceptance gate

- [ ] Source permission/licensing verified outside user text.
- [ ] Privacy/retention/access policy reviewed.
- [ ] Both event-time and availability-time rules tested.
- [ ] Data is versioned; raw observations never invented.
- [ ] Missing observations are not silently imputed as zeros.
- [ ] A reproducible temporal holdout is fixed before model tuning.
- [ ] Model/evaluation card names this exact snapshot.
- [ ] A human reviewer approves the card before enabling ingestion.

See [M1 delivery plan](M1_EXECUTION_PLAN.md),
[security expectations](../SECURITY.md),
and [synthetic preflight](M1_DATA_PREFLIGHT.md).
