# Contributing to MirrorMind

MirrorMind is an experimental research and engineering project. Feedback,
reproducible bug reports and design discussions are welcome. A general
software license has not yet been selected; discuss proposed code
contributions with the maintainer before submitting them. Public visibility
does not constitute permission to redistribute or relicense the project.

## Report a problem

Use the repository's issues for ordinary bugs and documentation feedback.
Include the exact commit, Python version, operating system, minimal synthetic
reproduction, expected and observed behavior, and relevant redacted logs.
For vulnerabilities, use the private channel in [SECURITY.md](SECURITY.md).

Do not attach datasets, customer or invoice identifiers, credentials, private
source contents or unreleased third-party materials.

## Development and review

Read [AGENTS.md](AGENTS.md), the [engineering hub](docs/engineering/README.md),
[definition of done](docs/engineering/DEFINITION_OF_DONE.md) and
[change request template](docs/engineering/CHANGE_REQUEST_TEMPLATE.md).
Keep PRs narrow, preserve source and temporal boundaries, add adverse-case
regressions, document capabilities and limitations, and report actual tests
and skips. Synthetic fixtures are the default. No real-data acquisition,
paid services, new external dependency or license changes without explicit
scope approval.

Use Python 3.11+ and the public development extra:

```bash
python -m pip install -e ".[dev]"
python -m pytest -q -rs
python -m ruff check src tests examples
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

The pinned WorldKernel extra requires separately authorized access while
its repository remains private. Record optional test skips honestly.
The standard GitHub-hosted workflows and local receipts are separate
evidence. Keep source rights, review authority and production readiness
separate from test success.
