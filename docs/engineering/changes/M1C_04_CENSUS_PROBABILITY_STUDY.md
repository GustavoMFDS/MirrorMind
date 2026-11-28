# Change request - fictional probabilistic study protocol
Fixed versioned two-scenario study, 32 paths per group, independent
deterministic SHA-256 counter draws (first byte modulo four, equiprobable
under ideal hash; deterministic fixture, not cryptographic random claims).
No holdout, tuning or imported records. Commit the fixed design and
declared revision before scoring. Five methods including privileged
oracle, exact discrete core scores, per-group/horizon means and event
transcript digest. Complete canonical receipt verification by replay,
bounded submitted bytes, mismatch before scoring. CLI prepare, demo
and run; no arbitrary parameters or files. Preserve two/five-model
protocols and journal. No data rights, trust, empirical calibration,
inference, deployment or new dependencies. Independent review pending.

| Layer | Path | Impact |
|---|---|
| Example | examples/m1_census_probability_study.py | Fixed experimental design and replay |
| Tests | tests/integration/test_census_probability_study.py | Identity, replay, causal inputs, exact scores |
| Core/API/storage | None | Reuse mathematical primitives |
