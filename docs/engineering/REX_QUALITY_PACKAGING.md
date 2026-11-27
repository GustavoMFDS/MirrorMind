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

No wheel or sdist is published by this change. The optional private
WorldKernel direct Git reference remains unchanged; it may prevent PyPI
publication and must be resolved independently before any upload.
Builds use resolved version ranges; the quality tools are pinned but
this is not a fully locked or bitwise reproducible distribution.
No third-party engine/data bundle, paid service or deployment.
