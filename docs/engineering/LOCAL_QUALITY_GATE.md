# Temporary local quality gate while Actions quota is exhausted

The repository owner authorized a **temporary** alternative to GitHub Actions
while the monthly quota is unavailable. This is **not** a claim that the
official workflows ran or passed. All PRs retain clear evidence of the
specific reviewed revision and local environment.

## Run on the exact intended PR head

In a separate, clean checkout with Python 3.11+ and project development
dependencies installed (`python -m pip install -e ".[dev]"`), get the
current full commit SHA with `git rev-parse HEAD` and run:

```bash
python scripts/local_quality_gate.py --expected-head FULL_40_CHARACTER_SHA
```

Optionally add `--receipt results/local-quality-gate.json` after creating
the ignored `results/` directory. The receipt includes the full
revision, UTC execution time, ordered check names, exit codes and an
explicit `official_github_actions_status=not_checked_by_this_script`.
The tool refuses a dirty tracked checkout, a changed or truncated SHA,
and check failures; it stops on first failure. It does not copy raw logs,
source rows, invoices, customer IDs, credentials or environment variables
to the receipt. Untracked files are not included in the dirty-check
because local virtualenvs may be present; for provenance-sensitive reviews
use a fresh isolated checkout and avoid injecting files that shadow imports.

The fixed checks are:

1. Full `python -m pytest -q`.
2. `python -m ruff check src tests`.
3. AST source catalog `--check`.
4. Linked repository atlas `--check`.
5. Curated evidence reference `--check`.
6. Capability ledger `--check`.

### Restricted Windows sandbox note

`TestClient` may create a Windows asyncio event loop whose self-pipe uses a
local TCP socket pair. In a sandbox that blocks loopback sockets, the
`test_health` request can wait in `socket.accept` before application code
runs. A faulthandler stack in `_fallback_socketpair` and a bounded
`asyncio.new_event_loop()` child-process reproduction identify this as an
executor limitation for that run, not proof of a route defect. Do not skip
the test or alter its timeout to obtain a pass. Preserve the failed receipt,
then run the same exact clean SHA and all six checks in an already authorized
local environment where loopback is permitted. A passing local receipt still
does not stand in for GitHub Actions.

### Preserved PR #57 evidence

The owner-reported exact-head retest of `1bf178b5c4b31bcd68072b69748a14249c6c2649`
ran `tests/integration/test_api.py::test_health` successfully in 1.07 seconds,
then passed the complete six-check gate with 700 tests in 23.18 seconds on an
isolated checkout. A later exact-head gate on
`1cff92c1345ab20c0533281809502a33025cff10` passed 712 tests and all five
remaining checks in 22.68 seconds. Both receipts are explicitly
`local_gate_passed_not_official_ci`; neither resolves the cause of the older
`8f906b8` timeout. The current restricted execution separately reproduced a
stack wait during Windows asyncio fallback socket-pair setup; it is recorded
as executor-specific evidence and does not replace the independent pass.

The owner's PR #57 comments `7164856818`, `7164895449`, `7167002881` and
`7169397485` are the source for these decisions and exact results. GitHub
Actions remains unavailable within the approved free budget. Do not make
repeated workflow runs, paid usage, limit increases or runner/workflow changes
to obtain a remote green check. Keep all required check definitions and
repository protections unchanged.

Reviewers must inspect the relevant code, tests, assumptions, and source
rights separately. This local gate cannot validate cloud-specific runner
behavior or missing Linux-only integration details, substitute for
authenticated publisher vintages, or establish forecast calibration.
When quota is available, rerun both official workflows against the exact
integrated changes and investigate any discrepancy.

The [local-gate regressions](../../tests/unit/test_local_quality_gate.py)
verify fail-closed SHA checking, dirty-tree refusal, ordered manifest,
failure/timeouts, and honesty of the receipt. The source
[`scripts/local_quality_gate.py`](../../scripts/local_quality_gate.py)
is standalone and performs no remote calls or repository mutations.

## Stacked PR and final integration candidate

A passing gate on each PR head does not verify the combined tree. For a
stacked or topologically integrated candidate:

1. Preserve and review each branch head and its exact local receipt.
2. Integrate reviewed commits in dependency order on a separate candidate
   branch/worktree without force-pushing or discarding branch history.
3. Check conflicts, contracts, generated references, API capability parity
   and the final diff on the combined tree.
4. Run the six-check gate again on the exact clean integrated SHA and record a
   new receipt. Never reuse a child branch's receipt as evidence for the
   combined commit.
5. Obtain the required independent code/review evidence. If an official
   required check cannot run, leave the PR in review state and report the
   specific unavailable check. A local pass is not a remote check and cannot
   be used to bypass or weaken repository rules.

Do not label a per-branch gate as the final integrated-candidate gate. Record
both sets of evidence separately in the backlog and change report.

### Integrated M1 candidate receipt — 2026-11-25

The local candidate that combines PR #57 with the M1F/M1E stack passed the
exact clean-head gate on `42560e441f5020a5b4319a0f7b56474ef0485681`:

- Pytest: 828 passed in 28.32 seconds.
- Ruff, source catalog, repository atlas, curated evidence and capability
  checks: all passed.
- One existing Starlette/httpx `TestClient` deprecation warning appeared.
- Receipt: `%TEMP%\mirrormind-integrated-42560e441f50-local-gate.json`.
- Status: `local_gate_passed_not_official_ci`; the script explicitly records
  `official_github_actions_status=not_checked_by_this_script`.

This exact receipt covers the combined tree, including the synthetic UCI
evaluator and both exact-pin WorldKernel paths. It does not cover later
documentation commits, GitHub Actions, independent approval of the combined
diff, real-source rights, point-in-time availability, forecast calibration,
or production isolation. Rerun the same command after any subsequent tracked
change; do not reuse this receipt as evidence for a later SHA.

### Corrected engine-provenance candidate — 2026-11-25

The independent review of predecessor `995f55dd4ba039e9990ec7db9aaf2321fa44266a`
found that the selected WorldKernel metrics still declared the test-double
contract. Corrected commit
`74330d811145f10fcaaddadc56c3f95e7c8b7a85` adds selected-engine execution
records and a separately linked test-double parity-oracle record. With the
optional `worldkernel==0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, its exact-head six-check gate
completed at `2026-11-25T21:43:47.564941+00:00`:

- Pytest: 832 passed; no skipped tests.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- One existing Starlette/httpx `TestClient` deprecation warning appeared.
- Status: `local_gate_passed_not_official_ci`; the script records Actions as
  `not_checked_by_this_script`.

This gate covers code commit `74330d8`; it does not attest to later status and
handoff edits. After the consolidated PR documentation is committed, rerun the
same exact-head command with `--receipt results/local-quality-gate-<head>.json`.
`results/` is ignored local evidence: preserve it for inspection, but do not
claim it as a repository artifact or official CI. Record the actual final
head and outcome in the PR discussion.

### DecisionTrace V2 chronology correction — 2026-11-25

The independent PR #62 review reproduced acceptance of execution evidence
dated after its enclosing trace. Code commit
`20e7b50f88df046eaf3541c5ea706b2e3b051aad` compares timezone-aware instants
and rejects later evidence while preserving earlier/equal timestamps. With
WorldKernel `0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, its exact clean-head gate passed:

- Pytest: 835 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence and capability checks:
  all passed.
- Receipt: `results/local-quality-gate-20e7b50f88df046eaf3541c5ea706b2e3b051aad.json`.
- Status: `local_gate_passed_not_official_ci`; GitHub Actions remains unchecked.

This receipt covers code commit `20e7b50`, not the status, backlog, handoff
and gate-documentation update that records it. Rerun the six-check gate on the
exact clean documentation-inclusive SHA before publishing the branch. Preserve
that final SHA and receipt in the PR discussion; never treat either local
receipt as official Actions or integration approval.

### UCI #352 bounded reader candidate — 2026-11-27

Code candidate `5ff334230b9a5f222993d626dbe76c385a2c92d1` passed the exact
clean-head local gate at `2026-11-27T00:33:13.845213+00:00`:

- Pytest: 863 passed, zero skipped; one existing Starlette/httpx `TestClient`
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence and capability checks: all
  passed.
- Python 3.13.5; WorldKernel `0.0.1` installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-5ff334230b9a5f222993d626dbe76c385a2c92d1.json`.
- Status: `local_gate_passed_not_official_ci`; GitHub Actions was not checked.

This gate verifies the code candidate and its synthetic regression suite; it
does not mean the real workbook projection completed. The approved UCI call
exceeded 250,000 product-day groups and returned no projection or metrics. The
source remains private under its deletion deadline. The status, backlog,
handoff and this gate record were updated afterward, so run all six checks
again on the exact clean documentation-inclusive head before publishing the
review candidate. Preserve that receipt separately; do not call it official
Actions or use it to bypass required checks.

### Published UCI PR #65 head before status refresh

PR #65 published the approved bounded reader on exact head
`75da34fc2cb91d3354cfbe49af43aeb40721164d`. Its complete temporary local gate
passed at `2026-11-27T00:38:35.670136+00:00`:

- Pytest: 863 passed, zero skips; one existing Starlette/httpx `TestClient`
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence and capability checks: all
  passed.
- Python 3.13.5; WorldKernel `0.0.1` installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-75da34fc2cb91d3354cfbe49af43aeb40721164d.json`.
- Status: `local_gate_passed_not_official_ci`; Actions is
  `not_checked_by_this_script`.

A focused rerun of the UCI workbook, transaction projection, event-time and
workbook-flow suites passed 112 tests on this same checkout. This is additional
local test evidence, not a replacement for the exact full receipt. Automatic
Actions on this head failed before repository steps with the alternatives-only
account annotation; no jobs, steps, logs or combined status were available.
PR #65 remains open for independent review. The local gate does not clear the
250,000-group stop: the approved real-source call returned no complete
projection or empirical score. Do not retry, partition or increase the cap
without a separate owner decision. A later documentation-only status sync must
pass the same exact-head gate before it is pushed; report that new receipt on
PR #65 without treating it as official Actions evidence.

### MM-022 UCI invoice-classification correction — 2026-11-27

Code-bearing commit
`94c60b6ee20adbb5023e11aeded9b8fff90b1176` narrows the UCI-only cancellation
marker to exact uppercase `C`. Lowercase `c` now joins other single-letter
ASCII prefixes in the unverified class; the generic row projection remains
strict. Synthetic regressions cover the misclassification and the generic
contract. The real-source attempt used MM-021 and was not repeated.

The exact clean-head six-check local gate passed at
`2026-11-27T03:09:46.301016+00:00`:

- Pytest: 864 passed, zero skips; one existing Starlette/httpx `TestClient`
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- Python 3.13.5; WorldKernel `0.0.1` installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Focused UCI reader, generic projection, workbook-flow and event-time suites:
  113 passed.
- Receipt: `results/local-quality-gate-94c60b6ee20adbb5023e11aeded9b8fff90b1176.json`.
- Status: `local_gate_passed_not_official_ci`; GitHub Actions is not checked.

This verifies the new synthetic rule on this code commit. It does not apply
MM-022 to the real snapshot, produce an exclusion count or metric, clear the
250,000-group stop, or resolve independent review. Do not retry or partition
the source under the current approval.

### MM-022 all-prefix regression — 2026-11-27

The synthetic regression was broadened in commit
`2413df151fd6baa9bb4de472c713519f2d69937c` to iterate all 52 single ASCII
letters. It asserts that uppercase `C` alone is cancellation, all other
prefixes share one aggregate unverified-exclusion counter, source invoice IDs
do not appear in output, and malformed/non-ASCII forms fail closed. Focused
reader regressions passed 8 tests (`8 passed, 42 deselected`).

The exact clean-head temporary six-check gate passed at
`2026-11-27T05:47:01.681022+00:00`:

- Pytest: 867 passed, zero skipped; one existing Starlette/httpx `TestClient`
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- Python 3.13.5; WorldKernel `0.0.1` installed from reviewed commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-2413df151fd6baa9bb4de472c713519f2d69937c.json`.
- Status: `local_gate_passed_not_official_ci`; no GitHub Actions success is
  claimed.

The restricted sandbox attempt on this SHA was interrupted without a result;
the receipt is from the authorized local executor. The source attempt used
MM-021 and exceeded its 250,000-group ceiling. This regression does not reread
the workbook, generate source counts or metrics, or clear the stop. Never
retry, partition or enlarge the source call without a new bounded-method
decision.

### Published documentation-inclusive PR #65 head — 2026-11-27

After the all-prefix code/test commit, documentation updates were committed
and published on exact head
`5c1835f8862bbe12b9028707cfa3b9d893b9eda6`. The full local gate passed at
`2026-11-27T18:10:41.535466+00:00`:

- Pytest: 867 passed, zero skipped; one existing Starlette/httpx `TestClient`
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- Python 3.13.5; WorldKernel `0.0.1` installed from reviewed commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-5c1835f8862bbe12b9028707cfa3b9d893b9eda6.json`.
- Status: `local_gate_passed_not_official_ci`.

Automatic Actions on this exact head produced a test run and a catalog run
with failure; job steps/logs and combined statuses were unavailable through
the configured connector. The precise cause is undetermined. This local gate
does not imply Actions success, integration approval, or completion of the
stopped real-source evaluation.
