# Third-party licensing and data boundaries

MirrorMind's original project code and documentation use
[Apache License 2.0](../LICENSE), approved by the project owner on
2026-11-27. This does not grant rights to third-party material or imply
that the complete dependency graph has undergone a legal review.

## Python dependencies

The following is a metadata inspection of the installed review environment
on 2026-11-27, not a complete software bill of materials or legal opinion.
Version ranges in [pyproject.toml](../pyproject.toml) may resolve differently.

| Direct dependency or extra | Reviewed version | Declared license |
| --- | --- | --- |
| FastAPI | 0.165.0 | MIT |
| Pydantic | 2.14.4 | MIT |
| Uvicorn | 0.54.0 | BSD-3-Clause |
| openpyxl | 3.1.5 | MIT |
| cryptography | 46.0.7 | Apache-2.0 OR BSD-3-Clause |
| httpx | 0.28.1 | BSD-3-Clause |
| pytest | 9.2.0 | MIT |
| Ruff | 0.17.6 | MIT |
| WorldKernel (optional, independent) | 0.0.1 | No license declared in inspected package metadata |

Security follow-up: the reviewed cryptography 50.0.0 package declares
Apache-2.0 OR BSD-3-Clause, unchanged from the historical inspection above.
See [security maintenance](engineering/REX_QUALITY_PACKAGING.md) for the
resolved lock and advisory scope.

The public default installation does not install WorldKernel. Dependencies
are installed separately rather than vendored by this change. Preserve
their license texts, copyright notices and applicable obligations if
redistributing them. Transitive dependencies have their own terms (for
example certifi declares MPL-2.0); review the actual resolved artifacts
before any bundled binary or container release.

## WorldKernel

The optional integration references a private repository at the reviewed
commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
No general license or redistribution permission for that independent
engine is asserted. Apache-2.0 applies to MirrorMind's own gateway and
code-owned integration, not to the separately maintained engine. Do not
publish, bundle or relicense WorldKernel as part of this decision.

## Data

The committed demonstrations and automated test fixtures are synthetic.
No source-data rights are broadened by the software license.
UCI Online Retail #352 has a separately documented, bounded local research
scope; consult the [source review](engineering/datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
and [blockers](engineering/BLOCKERS.md). Do not redistribute private
workbooks or customer/invoice identifiers. Census and FRED/ALFRED source
acquisition remain subject to the documented artifact-specific restrictions.
Synthetic release vintages are not official archives.

## Review limits

The reviewed main history reported one Git author identity in shortlog;
this does not prove authorship or ownership of every line. The owner
authorized the license of original project material. A limited source
notice search and installed metadata review are not a full provenance,
license-compatibility or redistribution audit. Review actual notices and
dependency artifacts before packaging a public release or accepting
third-party code.
