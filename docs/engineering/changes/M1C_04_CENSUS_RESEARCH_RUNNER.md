# Change request - runnable fictional Census research experiment

## Goal and acceptance
Compose the existing experimental schedule, identity, replay and journal
contracts in a local example CLI. Generate one fixed fictional dataset and
predeclared 50-origin schedule, with six-month embargo gaps. Prepare a
commitment without writing a journal; run with a caller-retained expected
digest and explicit absolute journal path. A one-command demo uses a
temporary journal and self-generated digest, explicitly not preregistered.
Run validation by default, holdout or both only by explicit selection.
Produce deterministic JSON summary with provenance, per-horizon metrics,
coverage, abstentions and receipt digests; no full paired-loss rows.
Reopen and explicitly replay each stored digest. Reject mismatch before
opening journal, malformed options, invalid path and journal errors without
success output. Each split commits separately; failure of a later split
does not roll back an earlier receipt. Never claim independent registration,
runtime attestation, calibrated inference or holdout lock.

## Impact map
| Layer | Path | Change |
|---|---|---|
| Entrypoint | examples/m1_census_research_runner.py | Fixed fictional CLI |
| Core/state | census_experiment.py, census_experiment_journal.py | Reuse unchanged |
| Tests | tests/integration/test_census_research_runner.py | CLI replay and failures |
| API/external | None | No promotion |

Existing synthetic model/data cards apply; new deterministic generated
fixture is not source data. No arbitrary input file, source acquisition,
provider, deployment, external service, dependency or API changes.
Caller revision is declaratory. No independent custody or blind holdout.
B-01/B-02 remain open. Source-only rollback; persistent demo journals are
caller-owned and never automatically removed. Temporary demo files only
are cleaned up. Independent review pending.
