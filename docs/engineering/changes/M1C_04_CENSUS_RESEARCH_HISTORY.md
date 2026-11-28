# Change request - fictional experiment history

## Acceptance and scope
Read existing local journal via SQLite read-only URI, never initialize it.
One consistent bounded snapshot, at most 1000 experiments and 2000 split
receipts. Check exact schema, commitment identities and digest syntax.
Deterministic order by identity, not chronology: schema has no timestamps.
No metrics in metadata-only view. Optional explicit experiment and split
replays a known fixed fixture with current code and compares the stored
digest; reject missing/conflicting digest or unknown fixture. Never write
to journal on inspection. Label declared revision, not executed revision.
Do not silently evaluate holdout. Output exclusive local offline HTML.
No raw data, network, service, schema migration, new trust, or inference.

| Layer | Path | Impact |
|---|---|---|
| State | census_experiment_journal.py | Read-only bounded snapshot |
| Example | examples/m1_census_research_history.py | History and explicit replay HTML |
| Tests | tests/integration/test_census_research_history.py | Read-only, replay, failure, determinism |

No chronological or execution-count claims: repeated identical commits
are idempotent. No independent registration, attestation, blind holdout,
or empirical authority. Existing fictional cards and B-01/B-02 apply.
Independent review pending. No user file deletion.
