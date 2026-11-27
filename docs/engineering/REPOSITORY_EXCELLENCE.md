# Repository Excellence (REX)

Parallel maintenance track, independent from domain implementation. Keep the
default branch usable, public presentation accurate and development reproducible.
Zero paid services; preserve Codex's active checkout and source permissions.

| ID | Task | State |
| --- | --- | --- |
| REX-01 | Editorial rewrite of both READMEs | Integrated via PR #74 |
| REX-02 | Visual hierarchy and narrative | Integrated via PR #74; existing SVGs reused |
| REX-03 | Remote branch inventory | Inventory complete; no deletion authorized |
| REX-04 | Main protection and integration policy | Active main-only ruleset 28260524; verified via PR #75 |
| REX-05 | CI caching, permissions and compatibility | Integrated via PR #75; Python 3.11/3.12/3.13 CI passed |
| REX-06 | Free dependency and secret security checks | Enabled; first Python/Actions analysis passed; PR #76 |
| REX-07 | Issue and PR templates | Integrated via PR #76 |
| REX-08 | Labels and milestones | Ten labels and five milestones confirmed; PR #76 |
| REX-09 | Coverage and static analysis | Integrated via PR #77; full-package typing debt remains |
| REX-10 | Packaging and reproducibility | Integrated via PR #77; clean wheel smoke passed |
| REX-11 | Static Pages demo | Published from 5100ebf4; PR #79 and deployment 46072981620 |
| REX-12 | Documentation portal | Curated public index online; full rendered docs deferred |
| REX-13 | Reproducible benchmarks | Fixed synthetic benchmark candidate |
| REX-14 | Release automation | Read-only preparation candidate; publication manual |
| REX-15 | Developer experience review | Proposed |

See [branch audit](REX_BRANCH_AUDIT.md) and [CI and governance plan](REX_CI_GOVERNANCE.md). REX-01/02 acceptance is recorded
in the integration PR, not inferred from this document. Keep the first
alpha tag immutable, retain release-specific evidence and do not imply
that the public site will execute live models or simulations.

For CI, retain existing checks and actual skip evidence, then measure
before and after. For protection, confirm the exact required checks,
permissions and solo-maintainer workflow before changing rules. Avoid
simultaneous edits to the active UCI branch; independent work uses a
separate worktree.
