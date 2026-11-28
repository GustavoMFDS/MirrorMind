# REX-09/10 - Coverage, typing and packaging

## Baseline

Independent review of merged main `51c90d2601b2fba16b03a13a8723df0a54437d92`
on 2026-11-27, Python 3.13.5, pinned optional WorldKernel installed,
coverage 7.17.5 and mypy 1.20.2. All 968 tests passed. Measured source
coverage: 4,974/5,541 statements (89.77%); 1,571/1,974 branches
(79.58%); combined 87.09%. Subprocess coverage is not configured,
so worker metrics do not capture all child-process execution.
Tests, examples and docs are outside the coverage denominator.
No coverage threshold or security claim follows.

Whole-package mypy (Python 3.11 target, ignore_missing_imports) returned
62 errors across 16 files (65 files checked). Largest groups:
selection_sensitivity 12, coverage_gate 9, eligible_values 9,
worldkernel_runner 6, census_evaluation 6, uci_xlsx_xml 5.
These are diagnostic findings, not necessarily runtime defects.
Do not hide errors with blanket ignores or alter domain behavior in
a maintenance change. The retrieval module passed strict typing (4 files);
make that narrow scope a CI check and expand only after reviewed fixes.
Track full-package typing debt separately.

## Integration status

PR #77 merged normally into `main` at `540c47411898cc820ac651c19430017ecd8c20fe`.
The reviewed PR head was `df7c450523a8f3475e0a8161936f6ac80e705720`; all nine
observed official contexts succeeded on that exact head, including the quality
and package jobs. The merge-SHA combined-status query returned no individual
entries; see [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md) for that distinction.
No distribution was uploaded. The exact coverage/type/package measurements
above describe the PR's reviewed candidate based on main `51c90d2`, not a new
measurement of merge SHA `540c474`.

## Reproduction

```bash
python -m pip install -e ".[dev,quality]"
python -m coverage run -m pytest -q -rs
python -m coverage report
python -m mypy --strict src/mirrormind/modules/retrieval
python -m mypy --ignore-missing-imports src/mirrormind
python -m build
```

The last mypy command is expected to fail until debt is resolved.
The [quality workflow](../../.github/workflows/quality.yml) measures
public coverage separately from local pinned-engine coverage, uploads
a JSON report and gates the scoped retrieval check. Do not compare
different environments as identical. Coverage is initially reported,
not thresholded; set a floor after collecting public baseline evidence.

## Package

Use SPDX license metadata and include LICENSE (setuptools >=77).
Add project README, URLs and alpha/Python classifiers. No release tag
or runtime version is changed. Build an sdist and a wheel from the
sdist, then install the wheel in a fresh environment outside the checkout.
Verify package/API versions, license metadata and synthetic execution.
The examples and offline HTML generator remain source-checkout tools.

The clean wheel smoke on the initial candidate failed at API import: the
synthetic fixture module imports openpyxl, previously declared only in
extras. Declare the existing openpyxl range as a runtime dependency;
retain the uci extra for compatibility. This fixes package metadata, not
source behavior or source-data permission.

No wheel or sdist is published by this change. The optional private
WorldKernel direct Git reference remains unchanged; it may prevent PyPI
publication and must be resolved independently before any upload.
Builds use resolved version ranges; the quality tools are pinned but
this is not a fully locked or bitwise reproducible distribution.
No third-party engine/data bundle, paid service or deployment.

## Coverage floor and typing debt follow-up

PR #82 exact head `f6fa2edd80b38b42c3374813816929c2c9d8b2cc` measured
86.41% combined public coverage (986 passed, three optional engine skips).
See [quality CI](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46082420260).
Introduce an initial 85% combined floor in the public quality job. Keep
branch measurement and source scope unchanged. This is a conservative
initial floor, not a per-module or production quality guarantee; the
existing server-required contexts are unchanged. Future integration reviews
must check the quality job too.

On the same head, full-package mypy 1.20.2 (Python 3.11 target,
ignore_missing_imports) found 62 errors in 16 files (66 checked).
The follow-up uses a TypeGuard for the existing exact stock-code predicate,
individual exact-int assertions for already validated backtest counters,
and an explicit string assertion for the conditional winner. The evidence
flow narrows the already-validated holdout count. No new source scope,
model, ranking, numeric policy or public result schema; no blanket ignores.
The same mypy diagnostic now reports 49 errors in 12 files; strict
retrieval remains a separate CI scope. Remaining issues include typed
backtest result contracts, Decimal exponent narrowing, runner payload
types and intentional version/publication inheritance contracts. Review
those with their existing owners rather than changing contracts to satisfy
a checker. Re-run the full diagnostic after concurrent changes.

## Hash-verified public development environment

The [public input](../../requirements/public-dev.in) includes base, dev,
quality, uci, review and build requirements. The [resolved lock](../../requirements/public-dev.txt)
contains 38 pinned package entries and distribution hashes. It excludes the
private optional engine and is not a lock for production Docker images.
It was generated with uv 0.11.21:

```bash
python scripts/check_public_lock.py
uv pip compile --universal --python-version 3.11 --generate-hashes --no-header --no-annotate --output-file requirements/public-dev.txt requirements/public-dev.in
```

When metadata changes, update the input to match, regenerate deliberately,
review the diff and verify clean installations. No credentials, private
sources or source data belong in either file. The checker detects direct
input drift, not arbitrary lock-file tampering or resolver correctness.
The primary and compatibility CI jobs use hash verification and wheel-only
dependencies, install the reviewed local checkout without extra resolution
or build isolation, and run pip check. The separate quality and package
jobs retain their independently resolved environments to detect compatible
range and packaging regressions. Other workflows are not locked yet.
A Windows 3.13.5 rehearsal installed all 38 entries, passed 20 focused
tests and generated the synthetic report; official Linux compatibility
evidence is tracked in the integration PR. This is not bitwise build
reproducibility or a guarantee of package availability/security.

## Second typing pass

The follow-up uses explicit typed keyword arguments rather than heterogeneous
kwargs dictionaries in eligibility drift, eligible values and selection
sensitivity. Exact integer assertions and non-optional arithmetic are scoped
to the existing ready branch. Census finite Decimal exponent handling is
explicitly narrowed. No changed comparison formula, cutoff, coverage rule,
or output schema; no blanket suppressions. Same full-package diagnostic:
49 errors/12 files to 18 errors/8 files (66 checked), with the remaining
XML parser, engine and governance contracts requiring separate review.
The [lock tests](../../tests/unit/test_public_lock.py) check input drift
and private-engine exclusion. They do not attest artifact safety.

## Third typing pass: whole-package gate

On main c8b93da2 the same diagnostic reported 18 errors across eight
files. The follow-up resolves 17 findings using existing validated data:
Expat XMLParserType, exact scalar/style narrowing, typed capture lists,
validated enrollment expiration, NoReturn for the verifier that always
refuses publication, explicit exchange identity/count/mapping checks,
typed demand streams and a narrow state cast immediately before the
existing exhaustive transition validator. The workflow checks exact
integer execution counts before creating outcomes.

One intentional compatibility exception remains: DecisionTraceV2 inherits
DecisionTrace but changes its immutable schema_version literal. A single
assignment-specific ignore preserves the legacy Python subtype and each
Pydantic schema's exact version discriminator. The regression test
test_trace_version_literals_remain_exact_and_v2_retains_legacy_subtype
checks subtype, both schema constants and refusal of a V1 version in V2.
Do not broaden the version literal or silently change inheritance merely
to satisfy a checker.

The same whole-package mypy target now reports zero unsuppressed
diagnostics in 66 source files with --warn-unused-ignores. Missing type
metadata exemptions are limited to openpyxl and the optional WorldKernel
package (including submodules), not all imports. Strict retrieval remains
a separate stronger check. This is not whole-package strict typing, does
not eliminate all Any values, and is not proof of runtime safety.
The new quality job step fails on new unsuppressed diagnostics or unused
ignores; the existing server-required contexts remain unchanged.
No source read, external engine change, new dependency, or authorization.
