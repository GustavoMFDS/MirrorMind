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
