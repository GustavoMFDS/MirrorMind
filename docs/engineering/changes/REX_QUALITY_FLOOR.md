# REX follow-up - Coverage floor and typed validation

Goal: preserve coverage and reduce existing diagnostic debt without changing
domain or source authority. Scope: public quality workflow; existing stock-code
predicate, coverage gate and evidence-flow type narrowing; structural catalog
and maintenance guides. No source reread, new dependencies, contract redesign,
production ranking or branch deletion.

Acceptance: the existing focused retail and UCI synthetic tests and full
six-check gate pass; full-package diagnostic improves without ignores;
strict retrieval passes; public combined coverage remains at least 85%;
all applicable official PR contexts pass before integration. Branch audit
is read-only and exact-head based. Roll back through a reviewed PR if needed.

See [quality guide](../REX_QUALITY_PACKAGING.md) for baseline, scope and
limitations and [branch inventory](../REX_BRANCH_AUDIT.md).
