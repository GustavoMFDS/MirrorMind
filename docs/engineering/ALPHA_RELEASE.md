# First public alpha source release

The tag `v0.1.0-alpha.1` corresponds to Python package/API version
`0.1.0a1`. The tag is an experimental baseline, not a promise of stable
interfaces or production support. Only the reviewed MirrorMind source
and a generated synthetic HTML example are intended for release.

## Reproduce from the tagged source

From a fresh checkout of the tag, in a virtual environment:

```bash
python -m pip install -e ".[dev]"
python -m examples.m2_portfolio_demo --as-of 2011-01-26 --replications 2 --seed 317 --output mirror-demo.html
python -m pytest -q -rs
python -m ruff check src tests examples
```

Open the HTML locally and select a lead-time case. The attached release
report (when available) is generated with those parameters and contains
only the existing fictional fixture output, not a live server, new
simulation, ranking or approval. See the [report walkthrough](PORTFOLIO_DEMO.md).

## Release acceptance

Verify the exact tagged source, local gate and current GitHub-hosted CI;
record actual test skips. Inspect the generated report for fictional-only
content, nonauthorization flags and the original trace digest. Publish no
private inputs, credentials, optional private engine, wheels, containers,
or third-party dependency bundles. The [license and third-party boundaries](../THIRD_PARTY.md)
apply. Keep the UCI candidate and unresolved source research separate.

Package version is set in `pyproject.toml` and `mirrormind.__version__`;
the FastAPI application uses that constant. The regression
`test_openapi_version_matches_project_version` compares the project
metadata, Python constant and OpenAPI version; it is not an installed-wheel
or compatibility certification. The WorldKernel version pin remains
unchanged. See [changelog](../../CHANGELOG.md) for included functionality
and limitations.

Release notes record the commit, report SHA-256, test results and links to
official CI. Never replace a published tag or silently overwrite a release
artifact to correct evidence; create a subsequent prerelease instead.
