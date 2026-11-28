# Change request - local replay-checked Census experiment journal

## Scope and acceptance
Add a metadata-only SQLite adapter to the pure experiment contract. Register
only a recomputed matching specification. Admit a complete canonical receipt
only through verify_census_experiment_receipt; repeat identical admission
idempotently, reject conflicting receipt. Explicit replay checks stored digest.
Persist only commitment fields and result digests. No raw data, loss values,
credentials or receipt bodies. Maximum 1000 experiments and two split keys.
Use BEGIN IMMEDIATE, foreign keys, bounded busy timeout, recheck specification
after replay outside transaction, atomic rollback on failure. Reject foreign
or incompatible schemas, including unexpected schema objects. No migration
from unpublished prototype DBs. Existing contract and API unchanged.

## Impact map
| Layer | Path | Change |
|---|---|---|
| Core | census_experiment.py | Existing typed replay dependency |
| State | census_experiment_journal.py | Local explicit-path SQLite adapter |
| Tests | test_census_experiment_journal.py | Synthetic replay, rejection, concurrency, recovery |
| API / external authority | None | No promotion |

## Limits
Caller controls path, inputs and expected digest; storage is not a trusted
registry, independent timestamp, code attestation or blind holdout lock.
Plain reads do not replay receipts. External database edits can remain
undetected until explicit replay; no hostile-file isolation or power-loss
guarantee. No B-01/B-02 resolution, inference, source acquisition, deployment
or automatic actions. No new dependencies. Independent review pending.
