# Local quality gate and historical Actions fallback

## Current main and exact-head gate status - 2026-11-27

Current `main` is `d41e661d298255957979779691c2f9f4dbf36461`, following the
normal merge of PR #82 at `c31ecd6dbf3f68be8726bdba2b23a813226c2618`, the
typing-debt/public-coverage-floor follow-up at `128c266`, a public dependency
lock/evaluation-type follow-up at `c8b93da`, and the whole-package typing-gate
change at `d41e661`. PR #82's final exact head
`f6fa2edd80b38b42c3374813816929c2c9d8b2cc` passed 989 local tests, zero skips,
six local checks and 12 official exact-head checks; those results do not
transfer to the merge SHA or later `main`. The M2-03 branch is ancestry-synced
with that baseline. Checkpoint `a27027e` passed before the latest main merge,
as recorded below; it does not validate the current candidate. Re-run the
exact-head gate after synchronization and before review. The owner-authorized
temporary local gate remains separate from official CI.
Do not infer official status for a SHA without querying that exact commit.

The synchronized M2-03 worktree initially failed the newly required
whole-package mypy check with 25 diagnostics in three files. Those diagnostics
are resolved without changing runtime contracts. Focused M2-03 validation now
passes 21 tests, `mypy --warn-unused-ignores src/mirrormind` (71 modules),
`mypy --strict src/mirrormind/modules/retrieval` (five modules), and focused
Ruff. These are worktree checks, not an exact committed gate. Coverage and the
owner-authorized six-check gate were subsequently run on the exact committed
SHA below.

### M2-03 typing correction — exact commit `77c9d359`

On exact commit `77c9d359cda75bddcaca40e7912b13c693614af9`, the temporary
local gate passed **1,014 tests, zero skips and all six checks** (pytest, Ruff,
catalog, atlas, evidence and capability ledger). One existing
Starlette/httpx deprecation warning appeared. Receipt:
`results/local-quality-gate-77c9d359cda75bddcaca40e7912b13c693614af9-workspace.json`.
WorldKernel `0.0.1` remained installed from reviewed commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. The CI-equivalent coverage run
passed all 1,014 tests with **86.92% combined coverage** against the 85% floor;
whole-package mypy passed 71 modules and strict retrieval mypy passed five.

The source distribution and wheel built with `build 1.6.1`, existing
`setuptools 84.2.1` and `wheel 0.48.0` using `--no-isolation`. Isolated build
dependency installation was unavailable because DNS/network access to the
package index failed; no build source step had run in that attempt. The built
wheel was installed to a temporary target and smoke-tested from outside the
checkout with already installed `.venv` runtime dependencies: license/version,
API import and the non-authorizing synthetic decision workflow passed. The
Docker client is installed, but its Linux engine pipe is absent, so container
smoke was not run locally. GitHub Actions status was not checked for this SHA;
the owner reports its included allowance is exhausted. These results are local
only. A later documentation-only candidate needs its own exact-head six-check
gate before review.

### M2-03 pre-`d41e661` checkpoint — `a27027e`

On exact commit `a27027e835d157b0ea24ef1ae0d6fc1f94cb864a`, the complete local
gate passed **1,011 tests, zero skips and all six checks**: pytest, Ruff, symbol
catalog, repository atlas, evidence map and capability ledger. The run used
WorldKernel `0.0.1` from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Pytest reported one existing
Starlette/httpx deprecation warning. The exact receipt is
`results/local-quality-gate-a27027e835d157b0ea24ef1ae0d6fc1f94cb864a-workspace.json`;
it is a local ignored artifact and explicitly records that official GitHub
Actions status was not checked by the gate. This checkpoint predates the
`d41e661` main merge and later documentation updates; it is historical evidence
only. The synchronized current candidate needs a new exact-head gate before
review.

The preceding main before PR #82 was `10b94c9d7b01bc7072a18d8124cbc8090a6b1925`, normal merge of
[PR #81](https://github.com/GustavoMFDS/MirrorMind/pull/81) after
[PR #80](https://github.com/GustavoMFDS/MirrorMind/pull/80) and
[PR #79](https://github.com/GustavoMFDS/MirrorMind/pull/79) at
`5100ebf42265e01b65856e7ba91b659ff1b487c7`. PR #79 head
`b5c1bcc3dff7106e2f370c648c836b3251b17f45` passed 970 tests, zero skips and
six local checks; its receipt is `%TEMP%/mm-rex-public-portal.json` at
`2026-11-27T21:48:33.983163+00:00`. Seven observed PR workflow jobs succeeded:
quality/package in
[46072708700](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072708700),
symbol catalog in
[46072708733](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072708733),
Python API test/compatibility in
[46072708789](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072708789),
and site build in
[46072708801](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072708801);
the guarded `deploy` job was skipped.

PR #80 head `e6a28acd5cf0470c8d8628d6ee5957f3815d3f67` passed 976 tests, zero
skips and six local checks; its receipt is `%TEMP%/mm-rex-benchmark-release.json`
at `2026-11-27T22:17:07.127571+00:00`. Eight observed PR workflow jobs
succeeded: symbol catalog in
[46075726159](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46075726159),
benchmark in
[46075726114](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46075726114),
site build in
[46075726057](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46075726057),
quality/package in
[46075726238](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46075726238),
and Python API test/compatibility in
[46075726059](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46075726059).
The main-only Pages deployment and manual release rehearsal were skipped by
their workflow conditions. Combined-status queries recorded for the PR #79/#80
heads, merge commits `5100ebf` and `7efced5`, and then-current `main` `7efced5`
returned no individual entries, so preserve the evidence at each exact PR
head. These results do not transfer to the M2-02 candidate.

PR #81 exact head `41e6db8618a00c93f3a00ca6638ed96ab623dcbc` passed 977 tests,
zero skips and six local checks; its receipt is
`%TEMP%/mm-rex-developer-experience.json` at
`2026-11-27T22:29:07.300466+00:00`. Five official workflows completed:
documentation catalog
([46076949626](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46076949626)),
public site
([46076949610](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46076949610)),
repository quality/package/container smoke
([46076949702](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46076949702)),
Python API test and compatibility
([46076949561](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46076949561)),
and research benchmark
([46076949612](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46076949612)).
Nine applicable jobs succeeded. Guarded deployment and release-rehearsal jobs
were skipped by their conditions. Combined-status queries for PR head `41e6db8`
and merge/current-main `10b94c9` returned no individual entries, so retain
workflow evidence only for the exact PR head. This result does not validate the
M2-02 candidate; its clean exact-head six-check gate and PR workflows remain
required.

### M2-02 integrated candidate diagnostic - 2026-11-27

Candidate `e3e55d4635a2ee0dd355de995ff704cca4afe0e3` first timed out only when
the full gate ran inside the restricted sandbox: `pytest` reached its fixed
900-second limit and returned `124` (receipt
`results/local-quality-gate-e3e55d4635a2ee0dd355de995ff704cca4afe0e3.json`).
A diagnostic trace localized the wait to Windows asyncio Proactor self-pipe
startup inside Starlette TestClient/AnyIO (`socket.accept`); a standalone
`socketpair()` probe did not return in five seconds under the same sandbox.
Without changing source or tests, the isolated API health test passed outside
the sandbox with one Starlette deprecation warning. The unchanged full gate
then passed on the exact candidate: 989 tests, zero skips, and all six checks.
Its receipt is
`results/local-quality-gate-e3e55d4635a2ee0dd355de995ff704cca4afe0e3-workspace.json`.
The subsequent exact-head gate on `4ccff24cbc73045a4d01fdc9a5aa299d69e59038`
also passed 989 tests, zero skips and all six checks; its receipt is
`results/local-quality-gate-4ccff24cbc73045a4d01fdc9a5aa299d69e59038-workspace.json`.
Both are local-only evidence, not GitHub Actions. Run a new receipt for the
final PR head after any subsequent tracked changes, and verify that PR's
official checks independently.

PR #82 initial candidate opened at exact head
`d542e5e129e091dc649e1a187c96e18c59ccc695`. Diagnostics pinned all results to
that head. Its local gate passed 989 tests, zero skips and all six checks with
the reviewed WorldKernel pin; receipt:
`results/local-quality-gate-d542e5e129e091dc649e1a187c96e18c59ccc695-workspace.json`.
Twelve official checks succeeded and two condition-controlled jobs were skipped.
Python API test/compatibility 3.12/3.13 passed in
[46081696063](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46081696063);
quality, package and non-root container smoke passed in
[46081696099](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46081696099);
site build passed and guarded deployment skipped in
[46081696082](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46081696082);
symbol catalog passed in
[46081696007](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46081696007);
synthetic benchmark passed and release rehearsal skipped in
[46081696075](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46081696075);
and both CodeQL language analyses passed in
[46081693804](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46081693804).
The CodeQL check reported no new alerts
([check details](https://github.com/GustavoMFDS/MirrorMind/runs/140782041800)).
The quality workflow completed coverage measurement and strict retrieval
typing. One non-blocking annotation warns that Actions using Node.js 20 are
being forced onto Node.js 24; it did not fail a check. These are historical
PR-head results only; PR #82 later merged at `c31ecd6`. They do not establish
checks on the merge commit, current main or current M2-03 candidate. Any later
PR head needs its own exact checks.

## PR #77 public CI baseline - 2026-11-27

PR #77 merged normally as `540c47411898cc820ac651c19430017ecd8c20fe` over
main `51c90d2`; reviewed PR head was
`df7c450523a8f3475e0a8161936f6ac80e705720`. Nine official contexts completed
successfully on that exact PR head: `test`, compatibility 3.12/3.13,
`symbol-catalog`, `Analyze (actions)`, `Analyze (python)`, `quality`,
`package` and `CodeQL`. Run links:
[46066734014](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46066734014),
[46066733925](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46066733925),
[46066734009](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46066734009),
[46066732130](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46066732130)
and [140733898759](https://github.com/GustavoMFDS/MirrorMind/runs/140733898759).
The query for combined status on merge commit `540c474` returned no entries;
do not conflate PR-head evidence with checks on the merge SHA.

The PR #77 body records its exact-head local gate: 968 tests, zero skips,
six checks, one known warning and its temporary receipt
`%TEMP%/mm-rex-quality-packaging-final.json` at
`2026-11-27T20:53:44.941779+00:00`. Separate quality evidence measured
89.77% statement coverage, 79.58% branch coverage and 87.09% combined coverage;
strict typing passed on four retrieval files while whole-package mypy found
62 diagnostic errors across 16 files; wheel/sdist build and clean installed
wheel smoke passed on Python 3.13.5. These are PR-head results and do not
validate later commits or the current M2-02 candidate. The pre-PR #77 exact-main
`51c90d2` receipt passed 968 tests, zero skips and six local checks with the
reviewed WorldKernel pin; historic receipt is described below.

The owner-authorized temporary six-check local gate remains complementary for
exact-head validation and the optional pinned WorldKernel dependency. It is
not official Actions evidence. The PR #77 workflows ran on public GitHub-hosted
runners without a paid service, budget increase or protection change. Historical
pre-start failures remain unexplained and are not attributed to billing without
evidence. Preserve zero paid usage and do not register a self-hosted runner or
weaken, bypass or disable checks.

## PR #78 MM-024 exact-head validation

The final published head `8c8f8627a7162cb766a70d264569d3fcc2d442c8` passed
the full temporary local gate at `2026-11-27T21:45:12.655657Z`: 968 tests,
zero skips, all six checks and one existing Starlette/httpx `TestClient`
deprecation warning. WorldKernel `0.0.1` was installed from reviewed source
commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-8c8f8627a7162cb766a70d264569d3fcc2d442c8.json`.
Six official jobs succeeded on that exact PR head across three workflows:
documentation catalog in
[46072345590](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345590),
Python API test and compatibility jobs in
[46072345631](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345631),
and repository quality/package jobs in
[46072345603](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345603).
Combined-status queries for its merge commit and current `main` returned no
entries; do not assign those PR-head results to another SHA.

Earlier exact PR head `7059dc55f2f5f2d1bf69c5fc26e3bcbc981c44b7` also passed
at `2026-11-27T21:38:27.280983Z` with 968 tests, zero skips, six local checks,
the same WorldKernel pin and receipt
`results/local-quality-gate-7059dc55f2f5f2d1bf69c5fc26e3bcbc981c44b7.json`;
nine official contexts were observed on that earlier head. Both local receipts
mark GitHub Actions as not checked by the script. These records document the
merged docs-only policy change and do not authorize another source read. Any
later tracked change requires its own exact-head gate.

## PR #65 synchronized candidate

### Integrated main receipt - `51c90d2`

PR #65 merged normally at `51c90d2601b2fba16b03a13a8723df0a54437d92`, with
pre-merge main `2a7641b88b0d97a239d44102d4da9497460f21d1` and reviewed head
`77b3afd6aeb2a2fe7b27489f9b9c4aabb59b9a88` as parents. Exact-main GitHub
checks passed as recorded above. The full local gate passed at
`2026-11-27T20:57:20.907650Z`: 968 tests, zero skips and all six local checks,
with WorldKernel `0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; one existing Starlette/httpx
`TestClient` deprecation warning. Receipt:
`results/local-quality-gate-51c90d2601b2fba16b03a13a8723df0a54437d92.json`.
This is exact-merge local evidence, not a replacement for official checks.

The ancestry-preserving merge of current main `2a7641b` is complete at
`0182eba`. The previous local receipt predates this latest main; it does not
validate the newly combined tree. Every candidate needs the full six-check
local gate on the exact synchronized, documentation-inclusive SHA before
publication. Published head `35bff7824970ebc511e05add240088b2ffd74057`
passed at `2026-11-27T20:26:36.841691Z`: 968 tests, zero skips and all six
local checks, with reviewed WorldKernel `0.0.1` at source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-35bff7824970ebc511e05add240088b2ffd74057.json`.
All seven observed GitHub checks succeeded on that exact head: `test` and
Python 3.12/3.13 compatibility in
[run 46063704228](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46063704228),
`symbol-catalog` in
[run 46063704465](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46063704465),
`Analyze (actions)` and `Analyze (python)` in
[run 46063699783](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46063699783),
and `CodeQL` at
[run 140723990206](https://github.com/GustavoMFDS/MirrorMind/runs/140723990206).
These results do not transfer to descendants; any
later tracked change requires a new exact-head gate and check observation.
These pre-merge candidate receipts remain historical; PR #65 was later
reviewed and merged at `51c90d2` as recorded above.

The documentation-only descendant
`d454b48477af4691a363622ecf8b2fd85a7e5a60` passed at
`2026-11-27T20:40:28.598238Z`: 968 tests, zero skips and all six local checks,
with WorldKernel `0.0.1` installed from the same reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-d454b48477af4691a363622ecf8b2fd85a7e5a60.json`.
All seven observed GitHub checks succeeded on that exact head: `test` and
Python 3.12/3.13 compatibility in
[run 46065329990](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46065329990),
`symbol-catalog` in
[run 46065330030](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46065330030),
`Analyze (actions)` and `Analyze (python)` in
[run 46065326027](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46065326027),
and `CodeQL` at
[run 140729286173](https://github.com/GustavoMFDS/MirrorMind/runs/140729286173).
These checks are public CI; the optional private dependency remains covered by
the separate local gate. A later documentation-only descendant requires its
own local gate, publication and exact-head check observation.

### Pre-latest-main synchronized candidate receipts

Exact head `53a932295c4c981590e6bee105247a65a357eba6` passed at
`2026-11-27T20:08:46.341800Z`: 960 tests passed, zero skips, all six checks,
and one existing Starlette/httpx `TestClient` deprecation warning. WorldKernel
`0.0.1` was installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-53a932295c4c981590e6bee105247a65a357eba6.json`.

Its immediately preceding exact documentation candidate
`0ead3ec51e6400e9d216250aa6babef75e3a10f8` passed at
`2026-11-27T20:06:38.086100Z`: 960 tests passed, zero skips, all six checks,
and one existing Starlette/httpx `TestClient` deprecation warning. WorldKernel
`0.0.1` was installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-0ead3ec51e6400e9d216250aa6babef75e3a10f8.json`.
Both are `local_gate_passed_not_official_ci`; the script did not check GitHub
Actions. These receipts apply only to their named SHAs and predate the latest
main merges through `f6e10e0` and `2a7641b`. Re-run all six checks on the
final publication head.

### Previous PR #65 code-head receipt - `c6c1326`

Before the latest scalar-payload correction, exact code head
`c6c1326be9332e51b160931de4dd994d54868793` passed the complete local gate:
881 tests, zero skips and all six checks, with WorldKernel `0.0.1` installed
at reviewed source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-c6c1326be9332e51b160931de4dd994d54868793-loopback.json`.
An earlier restricted-sandbox invocation timed out before producing a pass;
its separate failure record is
`results/local-quality-gate-c6c1326be9332e51b160931de4dd994d54868793.json`.
The successful receipt applies only to `c6c1326`, not the current synchronized
candidate, and is local evidence rather than Actions CI.

## Run on the exact intended PR head

In a separate, clean checkout with Python 3.11+ and project development
dependencies installed (`python -m pip install -e ".[dev]"`), get the
current full commit SHA with `git rev-parse HEAD` and run:

```bash
python scripts/local_quality_gate.py --expected-head FULL_40_CHARACTER_SHA
```

Optionally add `--receipt results/local-quality-gate.json` after creating
the ignored `results/` directory. The receipt includes the full
revision, UTC execution time, ordered check names, exit codes and an
explicit `official_github_actions_status=not_checked_by_this_script`.
The tool refuses a dirty tracked checkout, a changed or truncated SHA,
and check failures; it stops on first failure. It does not copy raw logs,
source rows, invoices, customer IDs, credentials or environment variables
to the receipt. Untracked files are not included in the dirty-check
because local virtualenvs may be present; for provenance-sensitive reviews
use a fresh isolated checkout and avoid injecting files that shadow imports.

The fixed checks are:

1. Full `python -m pytest -q`.
2. `python -m ruff check src tests`.
3. AST source catalog `--check`.
4. Linked repository atlas `--check`.
5. Curated evidence reference `--check`.
6. Capability ledger `--check`.

### Restricted Windows sandbox note

`TestClient` may create a Windows asyncio event loop whose self-pipe uses a
local TCP socket pair. In a sandbox that blocks loopback sockets, the
`test_health` request can wait in `socket.accept` before application code
runs. A faulthandler stack in `_fallback_socketpair` and a bounded
`asyncio.new_event_loop()` child-process reproduction identify this as an
executor limitation for that run, not proof of a route defect. Do not skip
the test or alter its timeout to obtain a pass. Preserve the failed receipt,
then run the same exact clean SHA and all six checks in an already authorized
local environment where loopback is permitted. A passing local receipt still
does not stand in for GitHub Actions.

### Preserved PR #57 evidence

The owner-reported exact-head retest of `1bf178b5c4b31bcd68072b69748a14249c6c2649`
ran `tests/integration/test_api.py::test_health` successfully in 1.07 seconds,
then passed the complete six-check gate with 700 tests in 23.18 seconds on an
isolated checkout. A later exact-head gate on
`1cff92c1345ab20c0533281809502a33025cff10` passed 712 tests and all five
remaining checks in 22.68 seconds. Both receipts are explicitly
`local_gate_passed_not_official_ci`; neither resolves the cause of the older
`8f906b8` timeout. The current restricted execution separately reproduced a
stack wait during Windows asyncio fallback socket-pair setup; it is recorded
as executor-specific evidence and does not replace the independent pass.

The owner's PR #57 comments `7164856818`, `7164895449`, `7167002881` and
`7169397485` are the source for these decisions and exact results. GitHub
Actions remains unavailable within the approved free budget. Do not make
repeated workflow runs, paid usage, limit increases or runner/workflow changes
to obtain a remote green check. Keep all required check definitions and
repository protections unchanged.

Reviewers must inspect the relevant code, tests, assumptions, and source
rights separately. This local gate cannot validate cloud-specific runner
behavior or missing Linux-only integration details, substitute for
authenticated publisher vintages, or establish forecast calibration.
When quota is available, rerun both official workflows against the exact
integrated changes and investigate any discrepancy.

## PR #60 integration receipts — 2026-11-26

The M2-01 branch was synchronized with PR #62's merged `main` using the
ancestry-preserving merge `a5186a680b307c4ecd9d56321321a5b27048731d`. The
exact merge head passed 845 tests with zero skips, Ruff, source catalog,
repository atlas, evidence and capability checks at
`2026-11-26T03:43:45.974393+00:00`. WorldKernel was installed from reviewed
source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-a5186a680b307c4ecd9d56321321a5b27048731d.json`.

The docs candidate `26e45b4620e9e13e12a745db3c99ead196c656d0` passed the same
exact-head gate at `2026-11-26T03:51:23.258821+00:00`: 845 tests, zero skips,
all six checks, and one existing Starlette/httpx `TestClient` deprecation
warning. Receipt:
`results/local-quality-gate-26e45b4620e9e13e12a745db3c99ead196c656d0.json`.
Both receipts say `local_gate_passed_not_official_ci`; Actions were not checked
by these scripts. The installed WorldKernel source revision was
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Any subsequent tracked change
requires another exact-head gate before publication or review.

The [local-gate regressions](../../tests/unit/test_local_quality_gate.py)
verify fail-closed SHA checking, dirty-tree refusal, ordered manifest,
failure/timeouts, and honesty of the receipt. The source
[`scripts/local_quality_gate.py`](../../scripts/local_quality_gate.py)
is standalone and performs no remote calls or repository mutations.

## Stacked PR and final integration candidate

A passing gate on each PR head does not verify the combined tree. For a
stacked or topologically integrated candidate:

1. Preserve and review each branch head and its exact local receipt.
2. Integrate reviewed commits in dependency order on a separate candidate
   branch/worktree without force-pushing or discarding branch history.
3. Check conflicts, contracts, generated references, API capability parity
   and the final diff on the combined tree.
4. Run the six-check gate again on the exact clean integrated SHA and record a
   new receipt. Never reuse a child branch's receipt as evidence for the
   combined commit.
5. Obtain the required independent code/review evidence. If an official
   required check cannot run, leave the PR in review state and report the
   specific unavailable check. A local pass is not a remote check and cannot
   be used to bypass or weaken repository rules.

Do not label a per-branch gate as the final integrated-candidate gate. Record
both sets of evidence separately in the backlog and change report.

### Integrated M1 candidate receipt — 2026-11-25

The local candidate that combines PR #57 with the M1F/M1E stack passed the
exact clean-head gate on `42560e441f5020a5b4319a0f7b56474ef0485681`:

- Pytest: 828 passed in 28.32 seconds.
- Ruff, source catalog, repository atlas, curated evidence and capability
  checks: all passed.
- One existing Starlette/httpx `TestClient` deprecation warning appeared.
- Receipt: `%TEMP%\mirrormind-integrated-42560e441f50-local-gate.json`.
- Status: `local_gate_passed_not_official_ci`; the script explicitly records
  `official_github_actions_status=not_checked_by_this_script`.

This exact receipt covers the combined tree, including the synthetic UCI
evaluator and both exact-pin WorldKernel paths. It does not cover later
documentation commits, GitHub Actions, independent approval of the combined
diff, real-source rights, point-in-time availability, forecast calibration,
or production isolation. Rerun the same command after any subsequent tracked
change; do not reuse this receipt as evidence for a later SHA.

### Corrected engine-provenance candidate — 2026-11-25

The independent review of predecessor `995f55dd4ba039e9990ec7db9aaf2321fa44266a`
found that the selected WorldKernel metrics still declared the test-double
contract. Corrected commit
`74330d811145f10fcaaddadc56c3f95e7c8b7a85` adds selected-engine execution
records and a separately linked test-double parity-oracle record. With the
optional `worldkernel==0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, its exact-head six-check gate
completed at `2026-11-25T21:43:47.564941+00:00`:

- Pytest: 832 passed; no skipped tests.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- One existing Starlette/httpx `TestClient` deprecation warning appeared.
- Status: `local_gate_passed_not_official_ci`; the script records Actions as
  `not_checked_by_this_script`.

This gate covers code commit `74330d8`; it does not attest to later status and
handoff edits. After the consolidated PR documentation is committed, rerun the
same exact-head command with `--receipt results/local-quality-gate-<head>.json`.
`results/` is ignored local evidence: preserve it for inspection, but do not
claim it as a repository artifact or official CI. Record the actual final
head and outcome in the PR discussion.

### Census review corrections — descendant implementation head — 2026-11-25

Commit `3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6` is a Census-only follow-up
on local descendant branch `codex/m1-census-vintage-adapter`. It contains the
four reproduced review corrections: Decimal-context-independent metrics,
first-estimate/revision chronology and unanchored-revision exclusion, plus
fail-closed metric overflow/underflow. The test suite remains synthetic-only.
With WorldKernel `0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, its exact clean-head six-check gate
passed at `2026-11-26T01:48:54Z`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence map and capability ledger:
  all passed.
- Receipt: `results/local-quality-gate-3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6.json`.
- Status: `local_gate_passed_not_official_ci`; GitHub Actions was not checked.

This receipt covers the implementation and feature-documentation commit. The
subsequent status, backlog, handoff and gate-documentation edits require a new
exact clean-head gate. The branch is not pushed and has no separate PR while
consolidated PR #62 remains open; these Census fixes are not part of PR #62.

### Status-documentation-inclusive descendant — 2026-11-25

After the status, backlog, handoff, change-request and gate-receipt updates,
exact clean commit `a6e3ed3355a1e52712542e6ae0d80d908885a82b` passed all six
checks with 877 tests and zero skips. WorldKernel `0.0.1` remained pinned to
reviewed source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. One existing
Starlette/httpx TestClient deprecation warning appeared. Receipt:
`results/local-quality-gate-a6e3ed3355a1e52712542e6ae0d80d908885a82b.json`.
Status is `local_gate_passed_not_official_ci`; Actions remains unchecked. This
record does not include later edits to the gate record itself; gate any newer
tracked head separately.

### DecisionTrace V2 chronology correction — 2026-11-25

The independent PR #62 review reproduced acceptance of execution evidence
dated after its enclosing trace. Code commit
`20e7b50f88df046eaf3541c5ea706b2e3b051aad` compares timezone-aware instants
and rejects later evidence while preserving earlier/equal timestamps. With
WorldKernel `0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`, its exact clean-head gate passed:

- Pytest: 835 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning.
- Ruff, source catalog, repository atlas, evidence and capability checks:
  all passed.
- Receipt: `results/local-quality-gate-20e7b50f88df046eaf3541c5ea706b2e3b051aad.json`.
- Status: `local_gate_passed_not_official_ci`; GitHub Actions remains unchecked.

This receipt covers code commit `20e7b50`, not the status, backlog, handoff
and gate-documentation update that records it. Rerun the six-check gate on the
exact clean documentation-inclusive SHA before publishing the branch. Preserve
that final SHA and receipt in the PR discussion; never treat either local
receipt as official Actions or integration approval.

## Published Census PR #63 baseline — 2026-11-26

The separate Census branch includes merged `main` at
`a456034c55ed7634ad4768b26788fec09dab1d08` through ancestry-preserving merge
`55e91f7d73c67867edaf1aa790242f6cdbc611b9` (main is the second parent). The
exact merged candidate passed all six checks at
`2026-11-26T03:58:32.075461+00:00`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence and capability checks:
  all passed.
- WorldKernel `0.0.1` was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-55e91f7d73c67867edaf1aa790242f6cdbc611b9.json`.
- Status: `local_gate_passed_not_official_ci`; Actions were not checked by the
  local script.

The candidate was published as the separate open PR #63 at head
`b5e989314bcdcb566df479931794a5f56c07d477`. Pilot-status reconciliation
commit `162268ded05eb8ba291025b6cc98e5658ae2e0a1` passed the exact six-check
gate at `2026-11-26T04:49:09.425850+00:00`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence and capability checks:
  all passed.
- WorldKernel `0.0.1` was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-162268ded05eb8ba291025b6cc98e5658ae2e0a1.json`.
- Status: `local_gate_passed_not_official_ci`; the script records Actions as
  `not_checked_by_this_script`.

The follow-up documentation head `941d72956d9d00f6fd281fd3a3039a1786777c70`
passed the exact six-check gate at `2026-11-26T04:52:25.496219+00:00`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx TestClient
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence and capability checks all
  passed.
- WorldKernel `0.0.1` was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-941d72956d9d00f6fd281fd3a3039a1786777c70.json`.
- Status: `local_gate_passed_not_official_ci`; the script records Actions as
  `not_checked_by_this_script`.

The previously published baseline-documentation head
`42a9746d7925e023a97445a6fe6cd4db324173fa` passed the exact gate at
`2026-11-26T05:49:17.262178Z`: 877 tests, zero skips and all six checks. Its
receipt is `results/local-quality-gate-42a9746d7925e023a97445a6fe6cd4db324173fa.json`.
The current status refresh has a separate exact-head gate; its final receipt
is maintained in PR #63. This is local evidence, not official CI; no source
bytes, credential or licensed-data permission is implied. See
[B-08](BLOCKERS.md) for the exact pre-start Actions annotations and their
unresolved alternatives.

### PR #63 published head — 2026-11-26

The exact clean head `5ec904dc0be6555d3651f947ef1f02fdd6ce20f7` passed the
complete temporary local gate at `2026-11-26T15:42:29.443936+00:00`:

- Pytest: 877 passed, zero skipped; one existing Starlette/httpx
  `TestClient` deprecation warning.
- Ruff, source catalog, repository atlas, evidence and capability checks: all
  passed.
- WorldKernel `0.0.1` was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-5ec904dc0be6555d3651f947ef1f02fdd6ce20f7-authorized-local.json`.
- Status: `local_gate_passed_not_official_ci`; Actions were not checked by the
  local script.

The exact-head Actions attempts and unresolved alternatives-only annotation
are recorded in [B-08](BLOCKERS.md). This result covers local synthetic tests
and source guards. It does not establish real-source permission, empirical
accuracy, official Actions success or production readiness.

### Census period-close chronology correction — 2026-11-26

Code and feature-documentation commit
`00311c6344e8a70bb72315afc10f4fbd02926d26` rejects any normalized first
estimate or revision published before its reference month closes. The focused
Census selector/evaluator/CLI suite passed 47 tests. Its exact clean-head gate
passed at `2026-11-26T17:35:07.989722+00:00`:

- Pytest: 882 passed, zero skipped; one existing Starlette/httpx `TestClient`
  deprecation warning appeared.
- Ruff, source catalog, repository atlas, evidence and capability checks: all
  passed.
- WorldKernel `0.0.1` was installed from reviewed source commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
- Receipt: `results/local-quality-gate-00311c6344e8a70bb72315afc10f4fbd02926d26.json`.
- Status: `local_gate_passed_not_official_ci`; Actions were not checked.

The restricted sandbox run stalled in `socket.accept` during Windows
`asyncio` self-pipe creation for `tests/integration/test_api.py::test_health`.
A bounded faulthandler reproduction confirmed the known executor limitation;
the interrupted run emitted no gate receipt. The same exact clean SHA then
passed the full gate in the authorized local environment, with all checks
enabled. Status, handoff, backlog and gate-documentation commit
`a09b4c332519547c3ebc81890170873d4bfeee27` passed the same exact-head gate at
`2026-11-26T17:41:09.165939+00:00`: 882 tests, zero skips and all six checks.
Receipt:
`results/local-quality-gate-a09b4c332519547c3ebc81890170873d4bfeee27.json`.
The final acceptance-marker commit receives its own exact-head gate before
publication; the current PR head and final receipt are recorded in PR #63.
Neither local result establishes GitHub Actions success, real-source rights,
publisher authenticity or empirical forecast quality.

### PR #62 merge and separate review branches — 2026-11-26

Independent final review of PR #62 head `0bed1269613eb689e84ad971c7d8f1878767d6cf`
passed the exact six-check local gate with WorldKernel pin
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`: 835 tests, zero skips, one
existing warning. The ancestry-preserving merge `a456034c55ed7634ad4768b26788fec09dab1d08`
was independently compared to the reviewed head with no tree differences and
passed 835 tests, zero skips, six checks. The post-merge receipt is
`%TEMP%\mirrormind-independent-main-a456034c.json` at
`2026-11-26T03:11:16.900697+00:00`.

Exact published main-based review heads also have these complete local gates:

| PR / head | Pytest | Other checks | Receipt / status |
| --- | --- | --- | --- |
| #60 `fafded...` | 845 passed, zero skips; one existing TestClient deprecation warning. | Ruff, catalog, atlas, evidence and capabilities passed. | `results/local-quality-gate-fafdedae3a76398e0450773065e40384c96d1ed7.json`; `local_gate_passed_not_official_ci`. |
| #63 `b5e989314bcdcb566df479931794a5f56c07d477` | 877 passed, zero skips; one existing TestClient deprecation warning. | Ruff, catalog, atlas, evidence and capabilities passed with the exact WorldKernel pin installed. | `results/local-quality-gate-b5e989314bcdcb566df479931794a5f56c07d477.json`; `local_gate_passed_not_official_ci`. |
| #61 merge head `66fc9fa001eaa6bd3adbc8f8d1606f3743239d21` | 841 passed, zero skips; one existing TestClient deprecation warning. | Ruff, catalog, atlas, evidence and capabilities passed with the exact WorldKernel pin installed. | `results/local-quality-gate-66fc9fa001eaa6bd3adbc8f8d1606f3743239d21.json`; `local_gate_passed_not_official_ci`. |

PR #61 documentation refresh commit
`47fdceb58a2c3802f8e66e5aea51318a698ffe62` passed its exact six-check gate
at `2026-11-26T04:30:28.981947+00:00`: 841 tests, zero skips, Ruff, symbol
catalog, atlas, evidence and capability checks. The one existing warning is
the Starlette/httpx TestClient deprecation. WorldKernel `0.0.1` was installed
from source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-47fdceb58a2c3802f8e66e5aea51318a698ffe62.json`;
status `local_gate_passed_not_official_ci`.

The status/documentation follow-up `20ce86bde740d5b46d7aeba4d13138884e211dba`
also passed the exact six-check gate at `2026-11-26T04:34:17.237663+00:00`:
841 tests, zero skips, all checks passed and one existing TestClient
deprecation warning. The same exact WorldKernel pin was installed. Receipt:
`results/local-quality-gate-20ce86bde740d5b46d7aeba4d13138884e211dba.json`;
status `local_gate_passed_not_official_ci`. The #61 PR body carries the latest
head and receipt; re-run the gate after any additional tracked change.

These receipts cover only the named exact revisions. A later documentation
commit on PR #61 requires a fresh exact-head gate. GitHub Actions was not
checked by these local runs. No runner, paid usage, workflow change or
protection bypass was used. The independent #62 review also recommends keeping
the Census changes separate and retaining #52–#59 as ancestors of the merge.
