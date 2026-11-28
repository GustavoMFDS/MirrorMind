# Developer quick start

The public source checkout is sufficient for the default research demos.
No private engine access, API credentials, source data or paid service is
required. Python 3.11, 3.12 and 3.13 are exercised in public CI.

## From a clean clone

```bash
git clone https://github.com/GustavoMFDS/MirrorMind.git
cd MirrorMind
python -m venv .venv
```

Activate with `. .venv/bin/activate` on Linux/macOS, or
`.\.venv\Scripts\Activate.ps1` in Windows PowerShell. If activation is
restricted, use the environment's Python executable directly.

```bash
python scripts/check_public_lock.py
python -m pip install --require-hashes --only-binary=:all: -r requirements/public-dev.txt
python -m pip install --no-deps --no-build-isolation -e ".[dev,quality,uci,review]"
python -m pip check
python -m pytest -q -rs
python -m ruff check src tests examples
python -m mypy --warn-unused-ignores src/mirrormind
python -m mypy --strict src/mirrormind/modules/retrieval
python -m examples.m2_portfolio_demo --replications 2 --seed 317 --output mirror-demo.html
```

Open the new HTML file locally, or visit the
[public demonstration](https://gustavomfds.github.io/MirrorMind/demo.html).
The full-package typing debt and public versus local coverage are recorded
in [quality and packaging](REX_QUALITY_PACKAGING.md). Optional private
WorldKernel tests can skip in a public environment; record actual skips.
Do not install that extra without authorized access to its pinned revision.

## Local development API

```bash
python -m uvicorn mirrormind.api:app --host 127.0.0.1 --port 8000
```

Open [API documentation](http://127.0.0.1:8000/docs) or
[health](http://127.0.0.1:8000/health). Stop with Ctrl+C.
This API is experimental and lacks production authentication or isolation.

Alternatively, with Docker Engine and Compose installed and running:

```bash
docker compose up --build
docker compose down
```

The development container runs as UID 10001 and publishes the API on
loopback only. Its build context is limited by [.dockerignore](../../.dockerignore);
the [Dockerfile](../../Dockerfile) copies package metadata, license and
source only. No source data or private dependency is required. The CI
container smoke builds a fresh image and tests health and non-root identity
on the public runner. This is not a hardened production image, a locked
base image or a claim that all host configurations work.

## Contributing and validation

Read [CONTRIBUTING](../../CONTRIBUTING.md) and [AGENTS](../../AGENTS.md).
Use an isolated branch/worktree, avoid changing active work, and submit a
PR to main. Run the six local checks with the exact clean tracked SHA:

```bash
python scripts/local_quality_gate.py --expected-head "$(git rev-parse HEAD)"
```

The local gate is independent of official GitHub checks. Its structural
link audit covers the root project documents and docs tree, not all
Markdown semantics, anchor validity, image references or external URLs.
Public CI also checks examples, package installation and scoped typing.

Do not commit local outputs or private artifacts. The gitignore names
default generated report, site, benchmark and release rehearsal paths,
but custom output paths remain the developer's responsibility. A local
uv.lock is not a committed reproducibility guarantee; dependency locking
requires a separate design for the private optional extra.

See [repository maintenance](REPOSITORY_EXCELLENCE.md),
[release rehearsal](REX_BENCHMARK_RELEASE.md) and
[engineering hub](README.md) for further work.
