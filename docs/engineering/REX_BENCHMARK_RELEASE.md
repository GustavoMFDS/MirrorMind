# REX-13/14 - Synthetic benchmarks and release rehearsal

The benchmark measures three fixed in-process synthetic workloads:
28-day retail comparison (two replications, seed 317), Census validation,
and BM25 fixture construction plus search. Each workload is warmed once,
then timed 2–20 times with a monotonic clock. JSON serialization and digest
verification occur outside the measured interval. Report individual samples,
median/min/max, environment and deterministic output hash. Do not compare
different machines, Python versions or revisions as equivalent. No latency
threshold, production capacity, empirical model quality or speedup claim.
Only the default reference engine is measured; no private WorldKernel.

Run from a reviewed source checkout:

```bash
python -m pip install -e .
python -m examples.synthetic_benchmark --repeats 5 --output benchmark.json
python -m examples.prepare_alpha_release --expected-sha "$(git rev-parse HEAD)" --output alpha-candidate
```

Use new output paths. The release rehearsal checks a clean tracked checkout,
exact SHA and consistent alpha package/API version. It reuses the allowlisted
synthetic site builder and emits only the report, its SHA-256 and a manifest.
The suggested tag may already exist; this is not a new release. The manifest
explicitly denies publication authorization and official CI verification.
No tag, GitHub release, distribution, data acquisition or deployment is
performed. The maintainer must separately verify the exact main checks,
version uniqueness, source rights, changelog and artifact hashes before
publishing. Never overwrite existing release artifacts.

The [maintenance workflow](../../.github/workflows/research-maintenance.yml)
runs the benchmark on PRs and allows a manual main-only rehearsal.
Both jobs have read-only permissions, bounded timeouts and short-lived
artifacts. Results are observational, not a timing gate. A changed output
within one benchmark run fails rather than silently recording a different
workload. Tests exercise the report and refusal contracts; they do not
certify performance or package security.

See [benchmark source](../../examples/synthetic_benchmark.py),
[release preparation](../../examples/prepare_alpha_release.py),
[contract tests](../../tests/integration/test_research_maintenance.py),
[alpha release guide](ALPHA_RELEASE.md) and [portal guide](REX_PUBLIC_PORTAL.md).
