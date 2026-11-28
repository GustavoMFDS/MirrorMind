# Project status — current baseline, 2026-11-28

## Current baseline after PR #92 - 2026-11-28

Remote `main` is `843fc5f4ea8310947f2626f486561de56401f3e2`, the normal merge
of PR #92. PRs #87–#92 are integrated; #87 delivers the
bounded M2-03 orchestration correction at merge commit
`45a84d2a4528755a88fccf8d766b5ef18518b9d8`. Earlier local and hosted results
remain scoped to their recorded PR heads. No complete local gate has yet been
run on `843fc5f` itself; this branch's final exact-head gate is pending.

The current local candidate is
`codex/m2-05-usable-decision-workflow-20261128`, based on `843fc5f` through
ancestry-preserving merges. Its M2-05 change request is
[M2_05_LOCAL_DECISION_REPORT](changes/M2_05_LOCAL_DECISION_REPORT.md).
Implementation reuses M1F-02 and M2-03: default offline HTML keeps the exact
M1 payload; explicit `--agent-preview` adds matching bounded inputs, fixed
tool receipts and an untrusted digest-linked draft. An incomplete-history
request renders abstention and sanitized `tool_failed`. No API route, live
provider, persistence, data source or authorization is added. Capability
labels remain experimental. Feature commit
`2d592bd50b15c3b0d463c94e58a70be78553e8a6` passed the complete local gate:
1,032 tests, zero skips and all six checks, with the exact WorldKernel pin.
The receipt is
`results/local-quality-gate-2d592bd50b15c3b0d463c94e58a70be78553e8a6-workspace.json`.
That SHA had one existing Starlette/httpx deprecation warning. A sandboxed
attempt timed out in `test_health` because the Windows Proactor loopback
socketpair blocked inside the restricted sandbox; the unchanged isolated test
and full gate passed with loopback available. This is local environment
evidence, not official Actions. Any later documentation commit needs its own
exact-head gate before publication; the final PR body carries the published
SHA and receipt.
PR #99 is open against `main`, mergeable and ready for independent review.
Its preceding published head `756fe3d800f0652916d0b2da875eec1f2e2ce7dc`
passed the full local gate (1,032 tests, zero skips, six checks) and had 12
successful official check-runs plus two workflow-conditional skips (`deploy`
and `release-rehearsal`). These results apply only to that SHA. The live PR
body is authoritative for the current head and its gate after this status
update.

The open M1C-04 Census stack contains #93, #94, #95, #96, #97, #98 and #100.
They remain linearly dependent (#94 on #93 through #98, then #100 on #98),
open and mergeable. #93 is ready for independent review; #94–#98 and #100
remain drafts. Review submissions and inline threads were empty at the latest
query. A source audit of the diffs in dependency order found no confirmed
defect; this is not independent approval. The exact #93 head has 12 successful
official check-runs and two conditional skips. No PR-triggered workflow runs
or combined statuses were returned for #94–#98 or #100.

The full local gate passed on the exact remote #98 tree
`dda5ebd9ca82cd0b2bbc2b6eec4e330afa3710e1` (1,116 tests, zero skips, six
checks) and the integrated #100 tree
`6df9d110c05fb8238d1d0270abcd835c46396b0c` (1,162 tests, zero skips, six
checks). Both runs used scratch commits with matching tree IDs, not the
published commit IDs; local-only receipts are
`results/local-quality-gate-pr98-tree-dda5ebd9ca82cd0b2bbc2b6eec4e330afa3710e1.json`
and
`results/local-quality-gate-pr100-tree-6df9d110c05fb8238d1d0270abcd835c46396b0c.json`.
These are local tree-equivalent results, not official CI or independent
review. Keep the stack synthetic and
do not integrate without the separate review/decision. B-01/B-02 still block
real-source bytes and empirical claims. PRs #60 and #61 are already merged;
do not replay their commits.

The user-approved UCI #352 local reader profile remains tightly scoped. The
MM-024 classification is implemented and its synthetic regression set passed
11 tests: six-digit IDs process normally, exact uppercase `C` plus six digits
means cancellation, other single ASCII-letter prefixes are excluded under one
aggregate class, and other forms fail closed. The earlier attempt already
excluded those rows before aggregation and exceeded the 250,000 product-day
group ceiling; no complete projection or metrics exist. Do not retry, chunk,
sample or expand the cap. Delete the private snapshot by `2026-12-26`.
B-01/B-02 still gate Census/ALFRED source bytes and empirical temporal claims;
B-04 remains a separate WorldKernel production-isolation gate.

Metadata review on 2026-11-28 refreshed the B-01/B-02 artifact candidate to
the October 2026 Advance MARTS report (CB26-181), released November 17. The
official sales page exposes the report and tables, while the historical
archive explicitly omits the most-current data and currently lists through
September. This is a proposal for one quarantined notice/provenance/schema
inspection only; it is not source approval. No Census/FRED/ALFRED bytes or
credentials were acquired. Keep the direct Census artifact behind owner
approval and a separate rights/processing decision, and keep FRED/ALFRED
excluded under current service/API terms. See the
[Census vintage protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md).

Historical continuation text below records the pre-#87-merge baseline and
must not be read as current PR or branch status.

## Historical pre-#87 review reconciliation - 2026-11-28

Remote `main` is `00e6cf11ac05a94055242573fd3cfc18086bad10`, merged through
PR #88 as a direct child
of `d41e661d298255957979779691c2f9f4dbf36461`. Its change is limited to the
cryptography 50 dependency constraints, public lock and related supply-chain
documentation. The exact commit has 11 completed GitHub check-runs, all
successful; those results apply only to `00e6cf1`. PR #87 was open and
unmerged at published head `48fc51d` when synchronization began. The local
M2-03 branch now includes `main` through ancestry-preserving merge
`66b591317b375a270b5d0ed682c94e161d52a956`, with no conflicts. The full local
six-check gate on that exact merge commit passed 1,014 tests, zero skips and
all six checks. Receipt:
`results/local-quality-gate-66b591317b375a270b5d0ed682c94e161d52a956-workspace.json`.

The restricted-sandbox attempt at `66b5913` stalled in the API `TestClient`
startup and was interrupted before its timeout; it emitted no receipt and is
not counted as a gate result. The same clean SHA passed unchanged in the
authorized local environment with loopback access in 34.21 seconds. One
existing Starlette/httpx deprecation warning remains. This matches the known
Windows sandbox limitation in [B-07](BLOCKERS.md). That `66b5913` receipt was
created while the local venv still had `cryptography 46.0.7`. The venv has now
been aligned to the synchronized `50.0.0` dependency. Do not reuse the earlier
receipt as evidence for that runtime; the live PR body holds the exact
documentation-inclusive receipt and current PR check status. The exact-main
checks on `00e6cf1` are separate evidence. Recheck after any later push. See
[LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md) and [B-08](BLOCKERS.md).

M2-03 remains bounded to a typed local registry, fixed fictional retrieval
and decision tools, and a scripted provider test double. The provider cannot
author forecasts, simulations, writes or business actions; no live provider,
route, persistence or authenticated identity is present. The prior published
head `b931bbe2279dd0865f535e0f56e5165ed402ef96` passed the local gate with
1,014 tests and zero skips; 12 of 14 exact-head official check-runs succeeded
and `deploy` plus `release-rehearsal` were skipped by conditions. Independent
review reproduced Pydantic `model_copy(update=...)` bypasses in nested
provider turns. Correction commit `48e7efe98aae2df3811302fbf7875a2bd8a48dc4`
revalidates each exact turn from plain data before dispatch or draft handling,
with regressions for malformed fields, invariants and missing payloads. Its
full local gate passed 1,019 tests, zero skips and six checks. Current
published SHA and official check-run state are recorded in the live PR #87;
independent re-review remains pending. Local
Docker remains unavailable. Never transfer evidence between SHAs.

The bounded UCI reader and MM-024 classification are already implemented in
main with synthetic regressions. The approved source call stopped above the
250,000 product-day group limit without returning a projection, complete
exclusion counts or metrics. The owner's MM-024 clarification preserves exact
six-digit identifiers, treats only uppercase `C` plus six digits as
cancellation, and excludes other one-letter ASCII prefixes before sales
aggregation under one aggregate category. It changes exclusion labels, not
accepted rows or group cardinality. Do not chunk, sample, reread or raise the
cap. Preserve the local snapshot deletion deadline `2026-12-26`. B-01/B-02
still gate empirical and point-in-time claims; B-04 remains open for broad
service isolation and deployment acceptance.

The MM-024 documentation-only candidate was merged through
[PR #78](https://github.com/GustavoMFDS/MirrorMind/pull/78) at
`291562a5e5358f2ed8327ba611737a33511e2fc9`; its final head was
`8c8f8627a7162cb766a70d264569d3fcc2d442c8`. That exact head passed the local
gate (968 tests, zero skips, six checks) and six observed official jobs in
three workflows: documentation catalog
([46072345590](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345590)),
Python API test/compatibility
([46072345631](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345631)),
and repository quality/package
([46072345603](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345603)).
Combined-status queries for the #78 head, merge commit and current main
returned no entries; the PR workflow runs are scoped to the PR head only. This
increment changes no parser contract and did not reread the private workbook.
Its exact local receipt is
`results/local-quality-gate-8c8f8627a7162cb766a70d264569d3fcc2d442c8.json`.
PR #82 has since integrated M2-02's fictional/offline retrieval evaluator into
main. Continue on the separate M2-03 orchestration slice and other existing
G-02 criteria without claiming production retrieval or real-source quality.

PR #79 merged at `5100ebf42265e01b65856e7ba91b659ff1b487c7`. Its exact head
`b5c1bcc3dff7106e2f370c648c836b3251b17f45` passed 970 tests, zero skips and
six local checks; seven observed GitHub Actions jobs succeeded, with the
main-only deployment job skipped. PR #80 merged normally at
`7efced55a6821bb1de84190eab5ab3db654da4b8`. Its exact head
`e6a28acd5cf0470c8d8628d6ee5957f3815d3f67` passed 976 tests, zero skips and
six local checks. Five PR workflows were observed: eight jobs succeeded and
the main-only Pages deployment and release-rehearsal jobs were skipped by
their conditions. The release rehearsal only prepares a synthetic bundle;
no tag or release is created. Combined-status queries for merge commits
`5100ebf` and `7efced5`, including then-current `main` `7efced5`, returned no
entries; keep PR-head evidence scoped to those heads. See
[LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md) for run links and timestamps.

PR #81 / REX-15 merged normally at `10b94c9d7b01bc7072a18d8124cbc8090a6b1925`.
Its exact head `41e6db8618a00c93f3a00ca6638ed96ab623dcbc` passed 977 tests,
zero skips and six local checks; nine applicable jobs succeeded across five
official workflows, including package and non-root container smoke, with
main-only deployment and release rehearsal skipped. Local Docker was
unavailable for that authoring run, so only the official CI container-smoke
job is evidence. Combined-status queries for the exact PR head and merge SHA
returned no individual entries.

**Current main:** `d41e661d298255957979779691c2f9f4dbf36461`, after PR #82 merged
normally at `c31ecd6dbf3f68be8726bdba2b23a813226c2618`. PR #52–#59 remain
incorporated through #62; #60/#61/#64 through #66; Census #63 through #67;
PRs #68–#81 through their existing merges, including MM-024 (#78), the curated
portfolio/index (#79), synthetic benchmarks/read-only release preparation
(#80), and developer onboarding/container smoke (#81). PR #82 adds the bounded
fictional M2-02 retrieval evaluator. The later `128c266` commit reduces typing
debt and establishes a public coverage floor; `c8b93da` locks public
development dependencies and narrows evaluation types. Commit `d41e661` closes
remaining package typing diagnostics and adds whole-package typing to the
quality workflow; no exact-current-main check result is asserted here.
WorldKernel and dataset terms remain separate. No combined-status or exact-main
gate result is inferred from PR-head checks.
The exact #62 post-merge receipt and review remain in
[comments 7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)
and [7181477141](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181477141).

| Review item | Current exact state | Limits |
| --- | --- | --- |
| PRs #60, #61, #64 | Closed as merged through PR #66; main ancestry preserved at `4efba1e830f2836b6d4f9c9b4f5ed776126e55cc`. The combined local gate passed 856 tests, zero skips, six checks and examples Ruff. | Retrieval remains experimental and caller scope is not authenticated identity; responder is in-process only; ENG-02 is example lint maintenance. |
| PR #63 | Closed as merged through PR #67 at `858211d6f87d483d151013205bc5737cb4585ed2`; exact combined local gate passed 904 tests, zero skips and six checks. | Synthetic Census evaluator only; no Census/ALFRED source bytes, API responses or credentials; no empirical result. |
| PR #65 | Closed as merged at `51c90d2601b2fba16b03a13a8723df0a54437d92`; exact integrated main passed 968 local tests, zero skips and six checks. | Reader accepted within bounded synthetic scope. UCI attempt remains stopped above 250,000 groups; no projection or metric. Preserve `2026-12-26` deletion deadline. |
| PR #77 | Closed as merged at `540c47411898cc820ac651c19430017ecd8c20fe`; nine official contexts succeeded on exact reviewed head `df7c450`. | Quality checks measure public coverage, strict retrieval typing and packaging. No release upload, private dependency change, empirical result or production readiness. |
| PR #78 (MM-024 UCI documentation) | Merged normally at `291562a`; final head `8c8f862` passed 968 tests, zero skips, six local checks and six observed official jobs. Existing MM-022 code and synthetic tests implement the approved classification. | No empirical UCI metric: the approved call stopped above the 250,000-group ceiling. Keep source-processing stop and deletion deadline. |
| PR #79 / REX-11/12 | Merged normally at `5100ebf`; exact head `b5c1bcc` passed 970 tests, six local checks and seven observed successful workflow jobs; guarded deployment was skipped. | Static site and curated index only; no live model, source processing or automatic deployment. |
| PR #80 / REX-13/14 | Merged normally at `7efced5`; exact head `e6a28ac` passed 976 tests, six local checks and eight observed successful jobs across five workflows; two guarded main-only jobs were skipped. | Synthetic timing only; release bundle is non-authorizing preparation. No tag, release or production benchmark claim. |
| PR #81 / REX-15 | Merged normally at `10b94c9`; exact head `41e6db8` passed 977 tests, six local checks and nine applicable official jobs across five workflows. Deployment and release rehearsal were skipped by conditions. | Public onboarding and CI container smoke only; no claim of local Docker validation or production deployment. |
| PR #82 / M2-02 retrieval evaluation | Merged normally at `c31ecd6` into current main. Exact PR head `f6fa2ed` passed 989 local tests, zero skips and six checks; 12 official exact-head checks passed, with deploy and release rehearsal skipped by conditions. | Evidence is scoped to the PR head. Synthetic retrieval remains experimental; no live source or production retrieval claim. |
| PR #88 / cryptography 50 lock | Merged at `00e6cf11ac05a94055242573fd3cfc18086bad10`; 11 completed exact-SHA official check-runs succeeded. | Updates public dependency constraints and lock; does not infer account billing state or explain historical pre-start failures. |
| M2-03 bounded tool orchestration / [PR #87](https://github.com/GustavoMFDS/MirrorMind/pull/87) | The ancestry-synced branch includes `main` `00e6cf1` through merge `66b5913`. Commit `48e7efe` fixes the nested Pydantic `model_copy(update=...)` bypass. | Exact correction commit passed 1,019 tests, zero skips and six local checks. Current published SHA and official checks are in the live PR; independent re-review remains pending. Provider is scripted; tools are fixed/fictional. No route, persistence or action authority. |

Metadata-first Census due diligence on 2026-11-27 proposes direct MARTS
original release files for one verified national seasonally adjusted
retail-and-food-services total. Exact table, unit and methodology edition
must be checked before use; the annual-revision index spans January 1992
through August 2026 but does not prove complete first-release vintages. The
official schedule gives 8:30 a.m. for advance sales without stating a timezone
in its table; any unorderable same-day correction must remain ambiguous.
Census documents the April 2025 removal of nonemployers, so methodology and
coverage comparability must be reviewed before pooling outcomes.

The [Census citation guidance](https://www.census.gov/about/policies/citation.html)
supports attribution when deriving estimates from disseminated tables and
assigns analytical conclusions to the analyst. Its [research transparency
policy](https://www2.census.gov/foia/ds_policies/ds027.pdf) states that works
created by Census employees generally are not subject to U.S. copyright, with
foreign and non-Census creator exceptions. These are general policy statements,
not file-specific clearance for MARTS release artifacts. The source proposal
now distinguishes project-scope approval from artifact-rights review; see the
[Census/ALFRED protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md). No Census file
was downloaded into the workspace or pilot store. Search previews incidentally
displayed published aggregate values; none was retained or used in evaluation.

Current FRED Services terms apply to ALFRED and the API, prohibit storage,
caching or archiving service content, and the API terms prohibit use in
connection with software/AI development. FRED/ALFRED is therefore NO-GO for
this development and archival route absent St. Louis Fed written authorization
or revised terms, and separate clearance of any series-owner rights; this is
not a finding on the separate original Census files.
The owner proposal is non-commercial internal research with attribution,
access-controlled local storage, no redistribution, and 30-day retention of
value-bearing artifacts followed by deletion. The proposed temporal protocol
uses a 60/20/20 chronological development/validation/locked holdout, first
estimates as primary targets, fixed baselines at 1/3/6 horizons, date-only
strict-before selection, and a 12-month moving-block bootstrap only with at
least 60 matched holdout origins per horizon. These are proposals requiring
approval, not authorized use or completed Census evaluation. No Census file,
FRED/ALFRED response, account or credential was acquired. The privately held
UCI workbook was acquired and its one approved bounded attempt stopped without
a projection or score; it remains subject to its deletion deadline. See the
[Census/ALFRED protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md) and UCI source card.

At the pre-integration baseline, `ruff check examples` found five pre-existing
findings in three M1 examples (I001, RUF007, F401). ENG-02 was merged through
PR #66; its pairwise change has empty/singleton/consecutive/gap regressions,
preserves the missing-day failure, and passed `ruff check examples`. It does
not alter forecast results or capability claims.

## Historical PR #51 baseline — 2026-11-23

## Historical integration candidate - 2026-11-27

The separately reviewed heads of PRs #64 (example maintenance), #60
(experimental scoped BM25 retrieval), and #61 (in-process current-head
responder) are included by normal merges, preserving their ancestry. This
candidate is intended for a single ancestry-preserving PR to main; the
independent combined gate and merge decision are recorded in its PR.
Do not infer approval from this document alone. Once integrated, begin M2-02
against the retrieval interface and continue G-02 only within its scoped
offline contract. No authenticated RBAC, deployed authority, empirical
forecast or production readiness is implied.

PR #63 (synthetic Census) and #65 (UCI reader) remain separate. The latter
records the owner's narrow UCI approval MM-017 through MM-022, a source
snapshot held privately, and a fail-closed stop above 250,000 product-day
groups without metrics. No new source processing, partitioning, cap increase
or Census acquisition is authorized by this integration. Preserve the
2026-12-26 deletion deadline and see the live PR #65 and its manifest for the
latest source-specific evidence. B-01/B-02 and B-08 remain open. The
following dated records retain historical gate and branch information;
where they differ from this queue, use the live PRs and current evidence.

**Baseline:** 2026-11-26 (Brazil local date); merged `main`
`a456034c55ed7634ad4768b26788fec09dab1d08`, ancestry-preserving merge of PR
#62. This is the latest confirmed main baseline, not a claim that the open
follow-up branches have been accepted.

## Historical merged baseline — 2026-11-26

**Historical main baseline:** `a456034c55ed7634ad4768b26788fec09dab1d08` integrates PR #62 by an
ancestry-preserving merge. PR #62's final independent review recommended this
method; #52–#59 are incorporated and their branches remain available. The
independent post-merge gate reported 835 tests, zero skips, all six checks,
one known warning and the exact WorldKernel pin
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; receipt:
`%TEMP%\mirrormind-independent-main-a456034c.json`. This is local evidence,
not GitHub Actions.

The integrated M1 workflow is experimental and synthetic. It joins evidence
staging, temporal baselines, uncertainty diagnostics, three-policy simulation
and a v2 decision trace; the optional WorldKernel path is locally pinned and
records the test-double parity run separately. It does not establish real-data
rights, temporal source availability, empirical forecast accuracy, production
isolation or approval to act. B-01/B-02 remain open. B-04 is resolved only
for the reviewed local compatibility slice; broader service/deployment
acceptance remains open. B-08 remains open under the owner's zero-paid-budget
decision.

**Historical independent review queue at this baseline:**

| PR | Current published head | State and exact local evidence | Limits |
| --- | --- | --- | --- |
| #60 | `fafdedae3a76398e0450773065e40384c96d1ed7` | Open, non-draft, based on `main`; 845 tests, zero skips, six checks. | Experimental lexical retrieval; scope is caller-declared, not authenticated RBAC. |
| #61 | Current exact head and receipt are maintained in the live PR body; documentation baseline gate `20ce86bde740d5b46d7aeba4d13138884e211dba` passed 841 tests, zero skips and all six checks. | Open, non-draft, based on `main`, ready for independent review. Any later commit receives a fresh exact-head gate; no CI result is claimed. | Read-only in-process responder; no route, persistence, authentication or deployed authority. |
| #63 | `b5e989314bcdcb566df479931794a5f56c07d477` | Open, non-draft, separate from #60/#61; 877 tests, zero skips, six checks on the final docs head. | Synthetic Census vintage protocol only; no real source bytes or authorization. |

The #62 final comments in this historical baseline are [7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)
and [7181477141](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181477141).
They confirm technical approval of experimental synthetic M1, recommend
preserving #52–#59 ancestry, and keep Census separate from #62. No real
UCI/Census bytes, paid Actions usage or limit increase are authorized. The
UCI then Census/ALFRED pilot sequence remains preparation-only; automated
tests stay synthetic.

The pre-existing `ruff check examples` findings were resolved by ENG-02 in PR #66; the separate PR is retained in the historical record below.

---

The following entries are a **historical evidence archive** captured before
PR #62 was integrated. Their branch heads, PR states and next steps are not
the current queue; use the baseline above plus live GitHub metadata for current
status. Historical receipts remain useful for tracing exact revisions.

**Baseline:** 2026-11-23 (Brazil local date); main
`e4f05a152aefcf68fa8ec22f3baa3b61adb8519d` (PR #51 merge commit).
This was the latest confirmed merged-main baseline after the handoff-doc
update. PR #50 (`036b8d6`) is its parent. It is retained as historical
evidence, not as a working-branch or current PR inventory.

**Independent post-merge evidence:** the exact `a456034` tree passed the local
six-check gate with 835 tests, zero skips and one existing TestClient warning;
WorldKernel was installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt and independent reviewer
attestation are linked in [PR #62 comment 7181477141](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181477141).
This is local evidence only. GitHub Actions did not run successfully, no paid
usage is approved, and no real source bytes were acquired.

PR #62 integrates the exact published heads of #52–#59 without duplicate
merges; ancestry checks confirm each published head is an ancestor of
`a456034`. PR #52 is already closed as merged. PRs #53–#59 have been closed
as incorporated after exact-head ancestry checks; all branches remain
available. #60 (M2-01 retrieval) and #61 (G-01 current
head responder) remain separate. #60 now contains the new main through
ancestry-preserving merge `a5186a680b307c4ecd9d56321321a5b27048731d`; the
exact sync-head gate passed 845 tests with zero skips and all six checks. The
docs candidate `26e45b4620e9e13e12a745db3c99ead196c656d0` also passed the same
gate; its receipt is recorded in `LOCAL_QUALITY_GATE.md`. The current status
refresh still needs its exact gate before push and independent review. #61
still needs synchronization and an exact gate.

## Historical consolidated M1 candidate before PR #62 merge — 2026-11-25

The published candidate is branch `codex/m1-engine-provenance`, PR #62 against
`main`, at head `0bed1269613eb689e84ad971c7d8f1878767d6cf`. GitHub metadata
verified on 2026-11-26 UTC reports it open and mergeable. Its history preserves
the published ancestry of PRs #52–#59; #60 and #61 are excluded. Commit
`74330d8` fixes selected-engine provenance, and `20e7b50` rejects DecisionTrace
V2 execution evidence later than trace creation. The exact docs-inclusive #62
head passed its six-check local gate with 835 tests, zero skips and the
reviewed WorldKernel pin; receipt:
`results/local-quality-gate-0bed1269613eb689e84ad971c7d8f1878767d6cf.json`.
This is local evidence, not official Actions or merge approval. No real source
bytes were acquired and `main` was not changed.

The local branch `codex/m1-census-vintage-adapter` descends from the published
#62 head through merge `8560ad6`. Its Census corrections remain outside PR #62
and are not pushed as a separate PR while the consolidated candidate awaits
review. Independent review comment
[7179081819](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7179081819)
reproduced Decimal-context drift, invalid release chronology, unanchored
revisions entering features, and non-finite/underflowing metrics. Commit
`3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6` fixes those cases, advances the
experimental result envelope to `mirrormind.census.vintage_backtest.v2`, and
adds public evaluator, selector and CLI regressions. The focused Census suite
passed 42 tests. Its exact clean-head six-check local gate passed 877 tests,
zero skips, with WorldKernel `0.0.1` installed from reviewed commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; one existing Starlette/httpx
TestClient deprecation warning appeared. Receipt:
`results/local-quality-gate-3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6.json`.
These synthetic results do not establish source rights, archive completeness
or forecast quality. B-01/B-02 still gate real-source work, and B-08 keeps
official Actions unavailable under the zero-cost decision. The status,
backlog, handoff and gate-documentation commit
`a6e3ed3355a1e52712542e6ae0d80d908885a82b` then passed the exact six-check
gate with 877 tests, zero skips and the reviewed WorldKernel pin. Receipt:
`results/local-quality-gate-a6e3ed3355a1e52712542e6ae0d80d908885a82b.json`.
This is local evidence only; any later tracked change needs a gate on its own
exact clean SHA.

## Historical branch evidence — 2026-11-25

The merged M1 path is a complete **synthetic experimental** evidence-to-
comparison flow: fixed retail evidence, evaluation, residual diagnostics,
policy simulation, DecisionTrace V2 and optional exact-pin local WorldKernel
execution. The HTTP/default path still uses the Python test double. This does
not complete licensed ingestion, empirical forecasting, broad engine
isolation, authenticated review, production controls or human decision
acceptance. M1 remains incomplete.

The local Census descendant `codex/m1-census-vintage-adapter` contains the
separate synthetic vintage selector/evaluator and four review corrections.
Published candidate `da540a2` passed 877 tests, zero skips and all six local
checks, plus 64 focused tests, with the reviewed WorldKernel pin. Merge
`55e91f7` preserves its ancestry while including `a456034`; the reconciled
exact head still needs the full gate before publication as a separate PR. Its
fixtures do not resolve B-01/B-02 or authorize acquisition.

The separate `ruff check examples` inspection found five pre-existing
diagnostics in three tracked M1 example files: three import-order findings
(I001), one unused import (F401), and one `zip`/`pairwise` recommendation
(RUF007) flagged as unsafe to auto-fix. The integrated gate's Ruff check
targets `src` and `tests`; these examples were not changed in the integration
branch. Tracked as ENG-02 maintenance after PR consolidation, not as a gate
failure.

The approved pilot order remains A (UCI #352 event-time retrospective), then B
(aggregate Census/ALFRED publication-vintage evaluation). Preparation is
allowed; source bytes remain unauthorized until the source-specific terms,
privacy, minimization, storage, retention, vintage evidence and evaluation
gates in [B-01/B-02](BLOCKERS.md) are met. Keep automated tests synthetic.

## Historical branch evidence recorded before the PR #62 merge — 2026-11-25

The following dated snapshots preserve exact prior branch, review and local
gate evidence. Their PR states and branch heads are historical; use the
current baseline above and live GitHub metadata for present status.

The composed synthetic evidence flow is implemented in the history beginning
at `c51ab30370db47e9f7105c97f870008e4fc442c5`; the latest published PR #52
follow-up is `b431d11bf0ac841ff30353a06263d23fb901307c` on
`codex/m1b-02-synthetic-evidence-flow`, proposed in draft
[PR #52](https://github.com/GustavoMFDS/MirrorMind/pull/52). The PR is
unmerged. Its one new capability is experimental and uses only bounded
local fixtures and caller-declared dates.

The full local quality gate passed on exact published head `b431d11bf0ac841ff30353a06263d23fb901307c`
at 2026-11-25 03:51:25 UTC: all 696 tests, Ruff, symbol catalog, repository
atlas, evidence map and capability checks passed. The focused M1B-02 tests
also passed, including child-to-aggregate receipt equality, missing and late
availability abstention, calendar/release rejection, and digest/declaration
mismatch rejection. This is local evidence on the exact branch head; it is
not official CI or merge evidence.

The prior published heads `c093ba6` and `e3aedaf` also passed complete gates
at 03:48:38 and 03:35:40 UTC. An earlier restricted exact-gate run on
implementation commit `c51ab30`
timed out at 900 seconds while `tests/integration/test_api.py::test_health`
waited during asyncio socket-pair creation before application code. The
standalone reproduction occurred on Python 3.12 and 3.13.5. A host/sandbox
loopback cause was proposed but never established. The subsequent full gate
pass on the current head resolves that timeout as an active blocker for PR #52;
retain the failure as historical evidence only. See [B-07](BLOCKERS.md).

PR #53 is on `codex/m1c-01-synthetic-retail-evaluation`, stacked on PR #52.
Merge commit `e922b03` synchronizes it with PR #52 head `b431d11`; its current
published head is `79d3679013576c6a209bed9fa031b7f0fabd0d8d`. The PR remains a
draft and unmerged. It composes the staged synthetic evidence flow with
release-aware matched-origin baselines and a deterministic fictional CLI; no
real-data ingestion, HTTP forecast endpoint or predictive-skill evidence is
added. Four integration tests plus six retail backtest unit tests pass, and
the exact-head gate passed 700 tests plus Ruff, catalog, atlas, evidence and
capability checks at 2026-11-25 04:08:00 UTC. API tests ran; one existing
Starlette/httpx deprecation warning was emitted. This is local evidence only.
Current Actions runs [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354)
and [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397)
failed with no steps/logs and no specific cause recovered. B-01/B-02 still gate
real data and empirical evaluation; B-08 blocks official CI. The older B-07
timeout on #52 is historical, not evidence of failure on #53.

The active continuation branch `codex/m1f-01-decision-trace-contract`
implements M1F-01 on top of the M1C-01 stack. The local result contract
separates observations, estimates, conditional outcomes, assumptions, missing
evidence, cost measurement states and human review. Review correction commit
`f02459d977fd263b03ddf60264b9069ae08b189b` adds terminal-review chronology,
context-independent lossless Decimal hashing, and field/aggregate/reference
bounds; evidence links now name each regression function. The decision-trace
unit suite passes 28 tests. Ruff, source catalog, atlas, evidence and
capability checks pass locally, as does `git diff --check`. For the atlas
check, only the existing untracked Graphify output was excluded via
a temporary local Git exclude file; no source guard or project ignore rule was
changed. The published integrated candidate `4d220066c3e9ab83a321ac9517bbabc8fc22e293`
passed the complete local gate at 2026-11-25 04:25:37 UTC: 728 tests, Ruff,
catalog, atlas, evidence and capability checks. One existing
Starlette/httpx deprecation warning appeared. HTTP runtime was not tested and
no new route was added. The result digest remains a recomputable content hash,
not a signature; all source/model/engine references remain caller assertions.
The task remains interface-only and has no authenticated producer, storage,
decision ranking, execution permission or real engine evidence. The source
walkthrough is in [DECISION_TRACE_RESULT](DECISION_TRACE_RESULT.md). PR #54
remains a draft stacked on #53. Merge commit `e493b4c` synchronizes the local
branch with published PR #53 head `79d3679`, retaining both histories and the
nested-receipt regressions. The complete local gate passed on this integrated
candidate as recorded above. On published #54 head `4d22006`, the latest test
run [45546742718](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742718)
and symbol-catalog run
[45546742695](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742695)
failed before repository steps with the same alternative account annotation;
no code tests ran remotely. See [B-08](BLOCKERS.md).

## Historical PR #55 review correction and sync

Draft PR #55's implementation commit `8769241` builds a pure allowlisted
request for the versioned WorldKernel exchange. Review fix `07c405b`
revalidates the mutable `ScenarioSpec` at the mapping boundary and enforces
the effective minimum of scenario and operator `max_runs`. Regression tests
are `test_mapping_revalidates_mutated_scenario_before_budget_mapping` and
`test_mapping_preserves_lower_scenario_or_operator_run_ceiling`. The walkthrough
explains why unrepresentable scenario timeouts/model/output budgets must be
rejected or enforced by a future adapter. No engine is imported or executed;
B-04 remains open.

The prior integrated #52–#55 candidate `fd72b76` passed 756 tests plus all
five non-pytest gate checks. Merge commit `b9eba02` synchronizes PR #55 with
published PR #54 head `4d22006`, preserving both histories and PR #53's
nested-receipt regressions. Merge commit `b9eba02` and documentation head
`cc9bdb4739507baa55cb857579ef70f7c92430d8` both passed the full local gate.
On exact head `cc9bdb4` at 2026-11-25 04:37:00 UTC, all 756 tests, Ruff,
catalog, atlas, evidence and capability checks passed, with one existing
Starlette/httpx deprecation warning.
Published PR #55 head `56aa92a6920a429b83458380231642fe59feaf08` includes the
review correction and docs sync; its exact gate passed 756 tests plus Ruff,
catalog, atlas, evidence and capability checks at 2026-11-25 04:39:14 UTC.
Its latest Actions checks failed before job steps with the alternative account
annotation under B-08; no remote tests ran. The mapper remains request
construction only; no WorldKernel import or execution is claimed.

## PR #56 disjoint residual calibration

Merge `b9bb86d` integrates PR #53's receipt-parity regressions into PR #56.
Published head `e993391a61a99d63008bc970cb19af673be4c18c` passed the exact
local gate at 2026-11-25 05:02:30 UTC: 700 tests plus Ruff, symbol catalog,
atlas, evidence and capability checks. One existing Starlette/httpx
deprecation warning appeared. Its Actions test [45550857405](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45550857405)
and symbol-catalog [45550857276](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45550857276)
checks failed before job steps with an annotation listing alternative account
conditions; no remote tests ran. This remains experimental and does not prove
empirical calibration. The latest change and exact-head gate are recorded in
the [M1D-01 change request on PR #56](https://github.com/GustavoMFDS/MirrorMind/blob/e993391a61a99d63008bc970cb19af673be4c18c/docs/engineering/changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md).

## PR #58 synthetic policy comparison

PR #58's published head is `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8`.
It includes merge `5544bc0` with PR #55 head `56aa92a` and passed its exact
local gate with 768 tests plus Ruff, catalog, atlas, evidence and capability
checks. The arrival-day/one-day behavior stays an explicit toy-policy caveat;
paired streams and item mass balance remain tested. Actions on `37737c2` failed
before repository steps under B-08, with no job steps or logs. No policy
optimization or WorldKernel execution is claimed; actual engine acceptance
remains B-04.

## PR #57 source-review proposal

Draft PR #57 (`codex/m1b-01-source-review`, published head
`646e4db6991b1769c922cf87a0b85630039915da`) records UCI Online Retail II as a
candidate for narrowly scoped retrospective research and compares a no-download
Census/ALFRED release-vintage method. It distinguishes event time from first
availability, does not derive publication dates from `InvoiceDate`, and adds
no dataset bytes. The review task is decision-ready only as a proposal: source
rights, privacy/minimization, retention, exact scope and temporal-vintage
evidence still require owner/reviewer decisions under B-01/B-02. PR #57 remains
draft and must sync with current PR #53 before its documentation gate.

## PR #59 end-to-end synthetic workflow

The corrected PR #59 code integration commit is
`c000ebd3484e1d9a83f1a440a12369361f4a52b1`, with normal merge commit
`c000ebd` bringing in dependency base `35ecc83` and current PR #56/#58 work.
The review fixes include request-sensitive deterministic identity, versioned
artifact digests, a separate whole-response digest, and propagation of #58's
modeling caveats to affected trace outcomes. The exact integrated head passed
the full local gate: 790 tests, Ruff, symbol catalog, atlas, evidence and
capability checks. One existing Starlette/httpx deprecation warning appeared.
Actions runs [45616226536](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45616226536)
and [45616226367](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45616226367)
failed before repository steps; the connector exposed no steps/logs and did not
return the annotation text. This is not remote test evidence. The route remains
experimental, unauthenticated and without body-size/rate/concurrency controls;
WorldKernel execution and real-source claims remain blocked.

## Historical PR #60 and #61 evidence at their original heads

PR #60's excerpt-integrity correction is published at
`59deef2a780d7802d8b8d29b66dd0189e96365ea`; same-length excerpt tampering and
wrong well-formed digest regressions are present, and its prior exact-head gate
passed 738 tests plus all five other checks. It is based on PR #54 and currently
reports a base conflict; sync to published #54 head `4d22006` and re-gate before
review follow-up. Scope filtering remains caller-declared, not authenticated
RBAC.

PR #61's typed clock-failure correction is published at
`8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e`; expected clock errors produce the
generic bodyless 503 while unexpected programming errors remain visible. The
two regressions distinguish those cases, and the exact-head gate passed 697
tests plus all five other checks. Its current branch is independent of M1 and
reported mergeable; it remains draft for separate review. No HTTP adapter,
persistence, authentication or authority is claimed.

The local M1F dependency stack now integrates published PR #56 head `e993391`
and PR #58 head `37737c2` without cherry-picking their commits. Its merge
candidate `eb6601ddfec7f021a8377b32abda8934fed02640` passed the complete local
gate outside the restricted sandbox: 768 tests, Ruff, symbol catalog, atlas,
evidence and capability checks. This candidate validates the #56 calibration
consumer alongside #58's policy result, but PR #59's workflow consumer still
needs to be merged and gated before the #56 review follow-up is complete. See
[B-07](BLOCKERS.md) for the restricted-run limitation and [B-08](BLOCKERS.md)
for official Actions diagnostics. PRs remain drafts pending separate review
and integration decisions.

## Historical PR #60 and #61 evidence at their original heads

### M2-01 permission-filtered retrieval

Draft PR #60 retains the correction from `73c191050865b0865e582f31a78859cc24262efb`:
the result contract hashes the exact UTF-8 excerpt, and regression tests reject
same-length excerpt tampering and a wrong well-formed digest. The branch was
normally merged with the latest published PR #54 head `4d220066` at
`a3a342450b3aa72b69d10b52485175ca497ffd5d`. That merge's first full local
gate exposed one documentation inventory failure after shared status pages
from unrelated PR #55–#59 work were selected; 737 tests passed and
`tests/unit/test_docs_coverage.py::test_live_repository_passes_linked_inventory`
reported two absent M1E links. The shared pages have been restored to PR #54's
dependency scope. The exact corrected integration head
`d1d4f74d69a3d4e772ba3eeb3119493491921875` passed the complete local gate:
738 tests, Ruff, catalog, atlas, evidence and capability checks. One existing
Starlette/httpx TestClient deprecation warning appeared. The initial failure
and correction are both retained here; neither retrieval code nor verifiers
were changed to address the documentation mismatch. Local validation does not
resolve official Actions B-08.

The documentation-only evidence follow-up at published head
`5b0a026cc008bffb953b3a6ae7d3cbdd252bd161` was also gated exactly: 738 tests,
Ruff, catalog, atlas, evidence and capability checks passed with the same
existing warning. See the [retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md)
and [change request](changes/M2_01_PERMISSION_FILTERED_EVIDENCE_RETRIEVAL.md).
The corresponding Actions checks failed before repository steps; their exact
annotation text was not exposed, so this is not CI success or an account-cause
finding.

The scope filter is caller-declared, not authenticated RBAC. The digest binds
the excerpt bytes but does not authenticate the source snapshot or prove
absolute offsets without source bytes. Retrieval remains local, fictional and
experimental; no HTTP route or model call is exposed.

### G-01 current-head service

Draft PR #61's typed clock-failure correction is published at
`8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e`. Expected operational clock errors
produce the generic bodyless 503; unexpected programming errors remain
visible. The regressions distinguish those cases, and the exact-head gate
passed 697 tests plus Ruff, catalog, atlas, evidence and capability checks.
The branch is independent of M1 and remains draft for separate review. No HTTP
adapter, persistence, authentication or authority is claimed.

## Architecture and actual execution boundaries

| Area | Verified implementation / status | Missing product gate |
| --- | --- | --- |
| API and contracts | [FastAPI app](../../src/mirrormind/api/app.py), [system routes](../../src/mirrormind/api/routes/system.py), [scenario validation](../../src/mirrormind/api/routes/scenarios.py), [typed contracts](../../src/mirrormind/core/contracts.py) | No execution pipeline or tenant authorization implied |
| Evidence and retail staging | [CSV snapshots](../../src/mirrormind/modules/evidence/snapshots.py), [UCI-shaped workbook](../../src/mirrormind/domains/retail/uci_workbook.py), [intake packet](../../src/mirrormind/modules/evidence/intake_review.py), [composite retail preflight](../../src/mirrormind/domains/retail/evidence_flow.py), synthetic coverage/release diagnostics | Real permission, original snapshot/provenance, availability and authorized ingestion |
| Forecasting | [Offline baselines](../../src/mirrormind/modules/forecasting/baselines.py), [retail release backtest](../../src/mirrormind/domains/retail/release_backtest.py), [residual envelope](../../src/mirrormind/domains/retail/residual_envelope.py), selection/drift/sensitivity diagnostics | Locked empirical holdout, evaluated models, calibrated or explicitly limited uncertainty, real inference |
| Governance | [Signed review history](SIGNED_SOURCE_REVIEW.md), [atomic governed publisher](ATOMIC_GOVERNED_PUBLISHER.md), [signed fence](INTEGRATED_HEAD_FENCE.md), [two-witness transcript](INTEGRATED_FENCE_TRANSCRIPT.md), [separate local registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md), [HTTPS reader](REMOTE_FENCE_HEAD_CLIENT.md) | Server-side implementation and operational independence/custody, real source authorization |
| Simulation | [Synthetic retail policy comparison](M1_RETAIL_POLICY_SIMULATION.md), [SimulationGateway](../../src/mirrormind/modules/simulation/gateway.py), and strict pure [WorldKernel request mapping](../../src/mirrormind/modules/simulation/worldkernel_mapping.py) | Actual compatible optional engine adapter, execution, result validation and budgets |
| Decision, orchestration and UI | Experimental synthetic M1F-02 CLI/API workflow and typed trace | Approved-source evaluation, actual engine result, authenticated review, production transport controls, agent/RAG workflow and review interface |
| Operations and generalization | Scaffold Docker/CI and reviewed design | Auth, isolation, durable jobs, runtime limits, observability, recovery, second domain |

### Historical governance chain description

The combined local SQLite publisher checks current operator policy and
signed publication together. A distinct registry replays full signed
integrated fence transitions with two witnesses. The HTTPS reader
validates a fresh nonce-bound service signature and compares the
claimed head to the registry and publisher. These are experimental
metadata mechanisms; they do not authorize ingestion or forecasting.
The remote signer/server has not been deployed or contacted in
baseline tests. Even a fresh signature over a false old head can be
accepted if local state is rolled back to match. See
[protocol details](REMOTE_FENCE_HEAD_CLIENT.md).

## Evidence interpretation

The most recent known gate was local. Reproduce on the actual commit:

```powershell
Set-Location D:\MirrorMind
git status --short --branch
git log -1 --oneline
$head = (git rev-parse HEAD).Trim()
uv run --no-sync --extra dev python scripts/local_quality_gate.py --expected-head $head --receipt (Join-Path $env:TEMP "mirrormind-$($head.Substring(0,12))-quality.json")
```

For an isolated worktree, use its own correctly bound environment and
working directory; never import the canonical checkout by accident.
The [local gate guide](LOCAL_QUALITY_GATE.md) explains what it checks.
If the environment is missing, follow the setup in [README](../../README.md)
and record any dependency changes; do not silently commit generated
lockfiles or reuse an editable environment bound to another worktree.

## What is next

The [master plan](MASTER_EXECUTION_PLAN.md) and
[task backlog](TASK_BACKLOG.md) are the actionable sequence.
The [blocker register](BLOCKERS.md) explains why external source,
infrastructure and empirical claims remain gated. The
[definition of done](DEFINITION_OF_DONE.md) defines closure rather
than assigning a speculative percentage.

After a material change, update this baseline only using the
actual reviewed commit and verification. Distinguish branch-local
evidence, merged-main evidence, actual remote CI and deployment
evidence. Record outstanding work instead of declaring the product
finished because test counts increased.
