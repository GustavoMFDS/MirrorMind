# Changelog

## 0.1.0-alpha.1 - 2026-11-27

First public experimental research preview (Python version `0.1.0a1`).
This is a source release, not a stable product or a distribution of
third-party engines or datasets.

### Included

- Typed FastAPI contracts and a reproducible synthetic retail decision workflow.
- Bounded evidence staging, temporal eligibility, fixed forecast baselines,
  backtesting and heuristic residual diagnostics.
- Three fictional inventory policies over paired seeded demand streams,
  conditional lead-time comparisons and versioned execution provenance.
- Optional pinned local WorldKernel integration (separate private dependency);
  public default examples use the Python reference simulator.
- Synthetic Census release-vintage evaluation with 1/3/6-month horizons and
  deterministic lineage fingerprints.
- Experimental in-memory fictional BM25 retrieval and local checkpoint
  primitives, including a read-only in-process current-head responder.
- Offline interactive HTML report generated from the exact synthetic workflow.
- English and Brazilian Portuguese READMEs, engineering walkthroughs,
  capability and evidence ledgers, Apache-2.0 license and disclosure policy.

### Known limitations

- No empirical forecast skill, causal claims, real-source authorization,
  automatic decisions, authenticated RBAC, live agents or production readiness.
- The private optional WorldKernel engine is not redistributed.
- UCI real-source processing stopped at its approved group bound; the
  selective-reader candidate in PR #65 is not included in this release.
- Official CI does not exercise the private optional engine; independent
  local validation is separate. See the release's exact-commit evidence.
- No hosted service, PyPI upload or bundled dependency distribution.

See [release guide](docs/engineering/ALPHA_RELEASE.md), [roadmap](docs/ROADMAP.md)
and [third-party terms](docs/THIRD_PARTY.md).
