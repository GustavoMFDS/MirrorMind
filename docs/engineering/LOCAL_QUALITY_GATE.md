# Temporary local quality gate while Actions quota is exhausted

The repository owner authorized a **temporary** alternative to GitHub Actions
while the monthly quota is unavailable. This is **not** a claim that the
official workflows ran or passed. All PRs retain clear evidence of the
specific reviewed revision and local environment. No Actions spend, quota
increase, workflow edit or protection change is authorized by this procedure.

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

TestClient may create a Windows asyncio event loop whose self-pipe uses a
local TCP socket pair. In a sandbox that blocks loopback sockets, the
test_health request can wait in socket.accept before application code runs.
A faulthandler stack in the Windows fallback socket-pair setup plus a bounded
event-loop child-process reproduction identify an executor limitation for
that run, not proof of a route defect. Do not skip the test or alter its
timeout to obtain a pass. Preserve the failed receipt, then run the same exact
clean SHA and all six checks in an already authorized local environment where
loopback is permitted. A passing local receipt still does not stand in for
GitHub Actions.

Reviewers must inspect the relevant code, tests, assumptions, and source
rights separately. This local gate cannot validate cloud-specific runner
behavior or missing Linux-only integration details, substitute for
authenticated publisher vintages, or establish forecast calibration.
For a stack, validate each exact PR head as needed, independently review its
diff, reconcile the full dependency stack without duplicate commits, and run
the same six checks again on the exact clean integrated candidate. Preserve
that receipt separately from branch receipts. Do not infer required-check or
branch-protection status from a local pass. When ordinary official Actions
execution is available again, check both workflows on the exact integrated
revision and investigate any discrepancy; until then, report official CI as
failed or not executed according to the actual remote check state.

B-08 also records the no-cost self-hosted runner assessment. No runner is
registered by this procedure. GitHub documents that self-hosted execution is
not charged against included compute, but running pull request code requires
an isolated disposable host and does not prove the current pre-start account
annotation would be bypassed. Keep using this local procedure until a
separately reviewed host and runner path are selected.

The [local-gate regressions](../../tests/unit/test_local_quality_gate.py)
verify fail-closed SHA checking, dirty-tree refusal, ordered manifest,
failure/timeouts, and honesty of the receipt. The source
[`scripts/local_quality_gate.py`](../../scripts/local_quality_gate.py)
is standalone and performs no remote calls or repository mutations.

On Windows, API tests may create local socket pairs while starting the
asyncio Proactor event loop. B-07 records a restricted execution where this
blocked in `socket.accept`, while the exact selector passed in the authorized
local process. If reproduced, capture a bounded faulthandler stack and run the
same exact-head gate in an environment that permits local socket creation;
do not skip tests or change their timeout to hide the environment failure.
