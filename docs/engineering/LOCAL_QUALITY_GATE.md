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

### Census review corrections — descendant implementation head — 2026-11-25

Commit `3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6` is a Census-only follow-up
on local descendant branch `codex/m1-census-vintage-adapter`. It contains the
four reproduced review corrections: Decimal-context-independent metrics,
first-estimate/revision chronology and unanchored-revision exclusion, plus
fail-closed metric overflow/underflow. The test suite remains synthetic-only.
With WorldKernel `0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, its exact clean-head six-check gate
passed at `2026-11-26T01:48:54Z`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- Receipt: `results/local-quality-gate-3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6.json`.
- Status: `local_gate_passed_not_official_ci`; GitHub Actions was not checked.

This receipt covers the implementation and feature-documentation commit. The
subsequent status, backlog, handoff and gate-documentation edits require a new
exact clean-head gate. The branch is not pushed and has no separate PR while
consolidated PR #62 remains open; these Census fixes are not part of PR #62.

### Status-documentation-inclusive descendant — 2026-11-25

After the status, backlog, handoff, change-request and gate-receipt updates,
exact clean commit `a6e3ed3355a1e52712542e6ae0d80d908885a82b` passed all six
checks with 877 tests and zero skips. WorldKernel `0.0.1` remained pinned to
reviewed source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. One existing
Starlette/httpx TestClient deprecation warning appeared. Receipt:
`results/local-quality-gate-a6e3ed3355a1e52712542e6ae0d80d908885a82b.json`.
Status is `local_gate_passed_not_official_ci`; Actions remains unchecked. This
record does not include later edits to the gate record itself; gate any newer
tracked head separately.

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

## Census candidate after PR #62 merge — 2026-11-26

The separate Census branch includes merged `main` at
`a456034c55ed7634ad4768b26788fec09dab1d08` through ancestry-preserving merge
`55e91f7d73c67867edaf1aa790242f6cdbc611b9` (main is the second parent). The
exact merged candidate passed all six checks at
`2026-11-26T03:58:32.075461+00:00`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence and capability checks:
  all passed.
- WorldKernel `0.0.1` was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-55e91f7d73c67867edaf1aa790242f6cdbc611b9.json`.
- Status: `local_gate_passed_not_official_ci`; Actions were not checked by the
  local script.

This receipt covers the exact candidate before the current baseline, backlog,
handoff and change-request evidence update. Run the six checks on the final
documentation-inclusive SHA before pushing or opening the separate Census PR.
No receipt is official CI, and no source bytes, credential or licensed-data
permission is implied.
