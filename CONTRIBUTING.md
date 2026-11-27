# Contributing to MirrorMind

MirrorMind is an experimental research and engineering project. Feedback,
reproducible bug reports and design discussions are welcome. The project is licensed under [Apache 2.0](LICENSE). By intentionally
submitting contributions for inclusion, you agree to its contribution terms
(section 5), unless explicitly agreed otherwise. Submit only material you
have the right to contribute; preserve applicable third-party notices.

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

## Set up a development environment

Follow the [developer quick start](docs/engineering/DEVELOPER_QUICK_START.md)
for clean public installation, checks and local API instructions. Use an
isolated branch and submit a PR; do not push directly to main.
