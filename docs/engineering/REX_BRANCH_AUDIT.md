# REX-03 - Remote branch inventory

Snapshot: 2026-11-27. Main: `af97e34520b043dbac1c438507f91f6200a821bf`.

This is an inventory, not deletion approval. Remote refs were fetched; the
latest 100 PRs (all states) and local linked worktrees were checked.
No remote or local branch was removed.

- preserve_active: main, active local branch or open PR dependency.
- ancestor_integrated: exact remote tip is an ancestor of main.
- merged_pr_exact_head: merged PR matches remote tip and its merge commit is
  reachable from main. Squash or edited merges may differ; not proof of
  identical content or retention of original commits.
- manual_review: no integration evidence under these rules.

Before any deletion, refresh the live refs and PRs, check other collaborators
and dependent branches, verify retention of unique work and obtain the
maintenance decision. Do not delete the active UCI or Census branch, rewrite
history, or prune local worktrees. This snapshot does not establish that
all historical PR content is safe to expose or that all branches are obsolete.

| Classification | Count |
| --- | ---: |
| ancestor_integrated | 15 |
| merged_pr_exact_head | 57 |
| preserve_active | 3 |

Total: 75.

| Remote branch | Exact head | Classification | Matching merged PR |
| --- | --- | --- | --- |
| `chore/local-qa-gate-receipt` | `6b897be85412944a3d7170259310e391d12a06bf` | merged_pr_exact_head | #29 |
| `codex/eng-02-examples-ruff` | `ca97ab61d15347aa271ee9ac8468a0714bdc3402` | ancestor_integrated | #64 |
| `codex/g01-current-head-service` | `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29` | ancestor_integrated | #61 |
| `codex/m1-census-vintage-adapter` | `ffd3d770d5c7e9bafba975544de7947bcf20f1fc` | preserve_active | #63 |
| `codex/m1-engine-provenance` | `0bed1269613eb689e84ad971c7d8f1878767d6cf` | ancestor_integrated | #62 |
| `codex/m1b-01-source-review` | `1cff92c1345ab20c0533281809502a33025cff10` | ancestor_integrated | - |
| `codex/m1b-02-synthetic-evidence-flow` | `b431d11bf0ac841ff30353a06263d23fb901307c` | ancestor_integrated | #52 |
| `codex/m1c-01-synthetic-retail-evaluation` | `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | ancestor_integrated | - |
| `codex/m1d-01-disjoint-residual-calibration` | `e993391a61a99d63008bc970cb19af673be4c18c` | ancestor_integrated | - |
| `codex/m1e-01-worldkernel-mapping` | `56aa92a6920a429b83458380231642fe59feaf08` | ancestor_integrated | - |
| `codex/m1e-03-synthetic-policy-simulation` | `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8` | ancestor_integrated | - |
| `codex/m1f-01-decision-trace-contract` | `4d220066c3e9ab83a321ac9517bbabc8fc22e293` | ancestor_integrated | - |
| `codex/m1f-02-dependency-stack` | `35ecc83936a6115cadf1f4c854d27fca6f7404ac` | ancestor_integrated | - |
| `codex/m1f-02-synthetic-decision-workflow` | `887d85af92173d7004c0db9a60f10511ca7cac88` | ancestor_integrated | - |
| `codex/m2-01-permission-filtered-retrieval` | `fafdedae3a76398e0450773065e40384c96d1ed7` | ancestor_integrated | #60 |
| `codex/uci352-pilot-20261126` | `11de60127ab0b31b609d98ada1b764a3dde542f9` | preserve_active | - |
| `docs/apache-2-license` | `346bf4812d2ff89c68f88bb85dcbb2a561096d2c` | merged_pr_exact_head | #71 |
| `docs/first-alpha-release` | `3fa490850626b507ba50e67a42604e3b9c63f247` | merged_pr_exact_head | #73 |
| `docs/living-engineering-knowledge-v1` | `913abd484c521de54d9f524ca20fc2df4b89b466` | merged_pr_exact_head | #1 |
| `docs/mm-a1-atlas-coverage` | `50ccee34387ba67a528fbea58d993056e1fb926b` | merged_pr_exact_head | #2 |
| `docs/mm-a2-semantic-evidence` | `7bfe334e0a503a7f62c81af2bd9613ee7efcacdf` | merged_pr_exact_head | #3 |
| `docs/mm-a3-capability-truth` | `2a7402807707ba3e99a374cf67182998f092ca37` | merged_pr_exact_head | #4 |
| `docs/mm-a4-research-evaluation-gates` | `3f78a0e06327ee56996ad87b95bd1abb12fa4ee9` | merged_pr_exact_head | #6 |
| `docs/mm-delegation-execution-guide` | `df8d14543628f484036c3df436fe6a58f0ffb307` | merged_pr_exact_head | #51 |
| `docs/mm-m1b-source-rights-review` | `3c8b68f81e05a573993758c5120b5700a3e314b6` | merged_pr_exact_head | #12 |
| `docs/mm-m1b-uci-retail-source-review` | `1070889e29969fee31df3cfd70a6e6728a0b1be2` | merged_pr_exact_head | #16 |
| `docs/portfolio-bilingual` | `6e37fbc0d38e54323c48200a744de79814b6389b` | merged_pr_exact_head | #69 |
| `docs/portfolio-visual-governance` | `4da265518155b9b5a6d0f870095f14fda9ae89e3` | merged_pr_exact_head | #70 |
| `docs/public-portfolio-readme` | `42295fa34f873282e4fd237dda6ac0fafc3b00b9` | merged_pr_exact_head | #68 |
| `feat/m1b-atomic-governed-publisher` | `1599bd38a434704d5f494d25fb3add83919a013e` | merged_pr_exact_head | #45 |
| `feat/m1b-authority-transcript-contract` | `8c7804d279c99a07585c0ba2da6a05b4d6e897a1` | merged_pr_exact_head | #42 |
| `feat/m1b-declared-calendar-coverage` | `89138eda270d544932f85e433b8efc0e9b641bb5` | merged_pr_exact_head | #21 |
| `feat/m1b-declared-retail-asof-audit` | `77bd472bab454ccf980582df37841853720526b9` | merged_pr_exact_head | #22 |
| `feat/m1b-local-checkpoint-publisher` | `018bfbdefb75f42b433a247531675cea0cf05f89` | merged_pr_exact_head | #43 |
| `feat/m1b-local-review-registry-cas` | `1c36a0e913b66c195fc91704c9c4a248addd9019` | merged_pr_exact_head | #39 |
| `feat/m1b-operator-governance-registry` | `f20cca318299ca1fd1322596db601db29479159d` | merged_pr_exact_head | #44 |
| `feat/m1b-retail-coverage-diagnostics` | `3cbd302e40417b7f3b9a9b2b37f1a677ef858f77` | merged_pr_exact_head | #20 |
| `feat/m1b-signed-external-head-checkpoint` | `99f369720bd7d86efc965e865a31758a71ff0697` | merged_pr_exact_head | #41 |
| `feat/m1b-signed-review-revocation` | `2c1d6837aba1888893134fdf949b16c1df00cc5f` | merged_pr_exact_head | #38 |
| `feat/m1b-source-review-packet` | `b33aabea91a0618f3df262e1d1c59f8544cca872` | merged_pr_exact_head | #37 |
| `feat/m1b-sqlite-review-registry` | `90e8b9033937312c2ed0819f13959320b1f75550` | merged_pr_exact_head | #40 |
| `feat/m1c-eligible-retail-value-comparison` | `6c075802fd5efe3149e435d74008c856d1cb021e` | merged_pr_exact_head | #27 |
| `feat/m1c-excluded-target-sensitivity` | `8d15f467a6a22da97ede96d4dddb0f5683b698e9` | merged_pr_exact_head | #28 |
| `feat/m1c-prequential-residual-envelope` | `8272509c2605bf400663d3164425c711d1549811` | merged_pr_exact_head | #25 |
| `feat/m1c-retail-coverage-gate` | `25ed88ef346fcedc8bf0c1bae03edc3f4a275fae` | merged_pr_exact_head | #24 |
| `feat/m1c-retail-declared-release-backtest` | `de073dbbb525873d7b9019f96c0b2768f2153724` | merged_pr_exact_head | #23 |
| `feat/m1c-retail-eligibility-drift-audit` | `c934736ace9d32708f9986f750cf019cdd4fdbb6` | merged_pr_exact_head | #26 |
| `feat/m1c-retail-sensitivity-sweep` | `7ca3b0c7d547c7ef81029bcdd299dad18a729130` | merged_pr_exact_head | #30 |
| `feat/m1c-reuse-sensitivity-audit` | `33579fd0f7b269d52b1bd461c8ca8be8707cc3ee` | merged_pr_exact_head | #32 |
| `feat/m1c-sensitivity-coverage-policy` | `4af79d6f14684fb44b510a7f1742196a3ed8493f` | merged_pr_exact_head | #31 |
| `feat/mm-m1a-synthetic-observation-preflight` | `e7eb9ceafa7ab27cb83c2de6d1bb5f2f908acefc` | merged_pr_exact_head | #5 |
| `feat/mm-m1b-bounded-binary-stream` | `701dc257ce2eadb0eca5943af1ba7d357c562aec` | merged_pr_exact_head | #15 |
| `feat/mm-m1b-bounded-uci-xlsx-reader` | `4adbf2fc8311eaa8e33da346d1c3f03f47606b9c` | merged_pr_exact_head | #19 |
| `feat/mm-m1b-dual-witness-fence-continuity` | `67c46b9aeb71895c334175ce03cb271597a0020f` | merged_pr_exact_head | #48 |
| `feat/mm-m1b-https-challenged-head-read` | `63cc3c66fa096d6003344dfc5d0df2c4a3c5d5c4` | merged_pr_exact_head | #50 |
| `feat/mm-m1b-local-snapshot-quality` | `29583193134dc160bcde4cf117694768d38b01fd` | merged_pr_exact_head | #17 |
| `feat/mm-m1b-policy-bound-publication` | `5c378aa5f4135e5e12cad85e9fd8d44f49066874` | merged_pr_exact_head | #46 |
| `feat/mm-m1b-separate-durable-fence-pin` | `57eb697f522366b40b128a856053cd03a49e1049` | merged_pr_exact_head | #49 |
| `feat/mm-m1b-signed-integrated-head-fence` | `a34161cf0dd3adf9507f7e3d752432bbdabd8d58` | merged_pr_exact_head | #47 |
| `feat/mm-m1b-staged-csv-snapshot` | `2604bfa22d4dc637732da6478b34c70772286530` | merged_pr_exact_head | #10 |
| `feat/mm-m1b-synthetic-availability-gate` | `d3488d940809039f76b8c1251f93458265874fdf` | merged_pr_exact_head | #8 |
| `feat/mm-m1b-uci-transaction-projection` | `b35aeebb9ebca2433f35e3f3f285bd00892d73c7` | merged_pr_exact_head | #18 |
| `feat/mm-m1c-availability-aware-rolling` | `ff1eec122ef8a43d824ef705343dc462601e246a` | merged_pr_exact_head | #9 |
| `feat/mm-m1c-origin-audit-ledger` | `ffaa24619c0fe9ee6b60c83cbd3f399e9d19d2d6` | merged_pr_exact_head | #13 |
| `feat/mm-m1c-staged-rolling-baselines` | `039dbb994f2784516a0d001055ebd68dc409436d` | merged_pr_exact_head | #11 |
| `feat/mm-m1c-synthetic-rolling-backtest` | `83968ae03219c58bac8e0724555dbfe317ce60ec` | merged_pr_exact_head | #7 |
| `feat/portfolio-local-demo` | `b90c95d870fb532f36c4f377682e91f17ad93cb5` | merged_pr_exact_head | #72 |
| `fix/mm-m1c-min-observed-history` | `8d1300c7e0642670d27164db2e193c244d51568a` | merged_pr_exact_head | #14 |
| `main` | `af97e34520b043dbac1c438507f91f6200a821bf` | preserve_active | - |
| `perf/m1c-cache-prequential-forecast` | `723869fee21abd6fea4b359c733e7cb4c1be57a4` | merged_pr_exact_head | #33 |
| `perf/m1c-incremental-calibration-window` | `8b0b6572ca64ddb2460f98f5fed5b26ab94e86c8` | merged_pr_exact_head | #35 |
| `perf/m1c-reproducible-retail-benchmark` | `bb84fc122bcbc06a87e04c6f027eab4a2b9c0224` | merged_pr_exact_head | #36 |
| `review/census-canonical-fingerprint` | `a9e66f6110b7e0974bc79e91321e118d80eebf40` | ancestor_integrated | #67 |
| `review/nov27-consolidate-60-61-64` | `ed9dc38c3ffc900b1340f762c11c1ae4ecb56e9e` | ancestor_integrated | #66 |
| `test/m1c-adversarial-cache-equivalence` | `41a0696e44e8b92590295e99444f5b9c14814b90` | merged_pr_exact_head | #34 |

## Refresh: 2026-11-28 UTC

Main: `c31ecd6dbf3f68be8726bdba2b23a813226c2618`. Live refs, latest 100 PRs and linked worktrees checked.
No deletion performed. Local divergent heads, main, active worktrees and
open PR dependencies are preserved. Exact squash delta equality compares
binary full-index diffs against the original merge base and merge parent;
it does not preserve original commit identities. Exact ancestor candidates
are the first proposed cleanup batch, subject to fresh checks and a
separate deletion decision.

| Classification | Count |
| --- | ---: |
| exact_ancestor | 18 |
| exact_squash_delta | 64 |
| preserve | 2 |

| Remote branch | Exact head | Classification | Matching PR |
| --- | --- | --- | --- |
| `chore/local-qa-gate-receipt` | `6b897be85412944a3d7170259310e391d12a06bf` | exact_squash_delta | #29 |
| `chore/rex-benchmark-release` | `e6a28acd5cf0470c8d8628d6ee5957f3815d3f67` | exact_squash_delta | #80 |
| `chore/rex-ci-governance` | `9ecb4e2ea5136f42bce08ce4199389fa74e2482c` | exact_squash_delta | #75 |
| `chore/rex-developer-experience` | `41e6db8618a00c93f3a00ca6638ed96ab623dcbc` | exact_squash_delta | #81 |
| `chore/rex-public-portal` | `b5c1bcc3dff7106e2f370c648c836b3251b17f45` | exact_squash_delta | #79 |
| `chore/rex-quality-packaging` | `df7c450523a8f3475e0a8161936f6ac80e705720` | exact_squash_delta | #77 |
| `chore/rex-security-community` | `3bb2d43eeb2a311c851627762c4636b8fd8429e5` | exact_squash_delta | #76 |
| `codex/eng-02-examples-ruff` | `ca97ab61d15347aa271ee9ac8468a0714bdc3402` | exact_ancestor | - |
| `codex/g01-current-head-service` | `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29` | exact_ancestor | - |
| `codex/m1-census-vintage-adapter` | `ffd3d770d5c7e9bafba975544de7947bcf20f1fc` | preserve | - |
| `codex/m1-engine-provenance` | `0bed1269613eb689e84ad971c7d8f1878767d6cf` | exact_ancestor | - |
| `codex/m1b-01-source-review` | `1cff92c1345ab20c0533281809502a33025cff10` | exact_ancestor | - |
| `codex/m1b-02-synthetic-evidence-flow` | `b431d11bf0ac841ff30353a06263d23fb901307c` | exact_ancestor | - |
| `codex/m1c-01-synthetic-retail-evaluation` | `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | exact_ancestor | - |
| `codex/m1d-01-disjoint-residual-calibration` | `e993391a61a99d63008bc970cb19af673be4c18c` | exact_ancestor | - |
| `codex/m1e-01-worldkernel-mapping` | `56aa92a6920a429b83458380231642fe59feaf08` | exact_ancestor | - |
| `codex/m1e-03-synthetic-policy-simulation` | `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8` | exact_ancestor | - |
| `codex/m1f-01-decision-trace-contract` | `4d220066c3e9ab83a321ac9517bbabc8fc22e293` | exact_ancestor | - |
| `codex/m1f-02-dependency-stack` | `35ecc83936a6115cadf1f4c854d27fca6f7404ac` | exact_ancestor | - |
| `codex/m1f-02-synthetic-decision-workflow` | `887d85af92173d7004c0db9a60f10511ca7cac88` | exact_ancestor | - |
| `codex/m2-01-permission-filtered-retrieval` | `fafdedae3a76398e0450773065e40384c96d1ed7` | exact_ancestor | - |
| `codex/m2-02-retrieval-evaluation-20261127` | `f6fa2edd80b38b42c3374813816929c2c9d8b2cc` | exact_ancestor | - |
| `codex/mm009-mm023-reconcile-20261127` | `8c8f8627a7162cb766a70d264569d3fcc2d442c8` | exact_ancestor | - |
| `codex/uci352-pilot-20261126` | `77b3afd6aeb2a2fe7b27489f9b9c4aabb59b9a88` | exact_ancestor | - |
| `docs/apache-2-license` | `346bf4812d2ff89c68f88bb85dcbb2a561096d2c` | exact_squash_delta | #71 |
| `docs/first-alpha-release` | `3fa490850626b507ba50e67a42604e3b9c63f247` | exact_squash_delta | #73 |
| `docs/living-engineering-knowledge-v1` | `913abd484c521de54d9f524ca20fc2df4b89b466` | exact_squash_delta | #1 |
| `docs/mm-a1-atlas-coverage` | `50ccee34387ba67a528fbea58d993056e1fb926b` | exact_squash_delta | #2 |
| `docs/mm-a2-semantic-evidence` | `7bfe334e0a503a7f62c81af2bd9613ee7efcacdf` | exact_squash_delta | #3 |
| `docs/mm-a3-capability-truth` | `2a7402807707ba3e99a374cf67182998f092ca37` | exact_squash_delta | #4 |
| `docs/mm-a4-research-evaluation-gates` | `3f78a0e06327ee56996ad87b95bd1abb12fa4ee9` | exact_squash_delta | #6 |
| `docs/mm-delegation-execution-guide` | `df8d14543628f484036c3df436fe6a58f0ffb307` | exact_squash_delta | #51 |
| `docs/mm-m1b-source-rights-review` | `3c8b68f81e05a573993758c5120b5700a3e314b6` | exact_squash_delta | #12 |
| `docs/mm-m1b-uci-retail-source-review` | `1070889e29969fee31df3cfd70a6e6728a0b1be2` | exact_squash_delta | #16 |
| `docs/portfolio-bilingual` | `6e37fbc0d38e54323c48200a744de79814b6389b` | exact_squash_delta | #69 |
| `docs/portfolio-visual-governance` | `4da265518155b9b5a6d0f870095f14fda9ae89e3` | exact_squash_delta | #70 |
| `docs/public-portfolio-readme` | `42295fa34f873282e4fd237dda6ac0fafc3b00b9` | exact_squash_delta | #68 |
| `docs/rex-editorial-portfolio` | `364b3f32ee9e3aa9f22a6ec43014367aa4c94c0e` | exact_squash_delta | #74 |
| `feat/m1b-atomic-governed-publisher` | `1599bd38a434704d5f494d25fb3add83919a013e` | exact_squash_delta | #45 |
| `feat/m1b-authority-transcript-contract` | `8c7804d279c99a07585c0ba2da6a05b4d6e897a1` | exact_squash_delta | #42 |
| `feat/m1b-declared-calendar-coverage` | `89138eda270d544932f85e433b8efc0e9b641bb5` | exact_squash_delta | #21 |
| `feat/m1b-declared-retail-asof-audit` | `77bd472bab454ccf980582df37841853720526b9` | exact_squash_delta | #22 |
| `feat/m1b-local-checkpoint-publisher` | `018bfbdefb75f42b433a247531675cea0cf05f89` | exact_squash_delta | #43 |
| `feat/m1b-local-review-registry-cas` | `1c36a0e913b66c195fc91704c9c4a248addd9019` | exact_squash_delta | #39 |
| `feat/m1b-operator-governance-registry` | `f20cca318299ca1fd1322596db601db29479159d` | exact_squash_delta | #44 |
| `feat/m1b-retail-coverage-diagnostics` | `3cbd302e40417b7f3b9a9b2b37f1a677ef858f77` | exact_squash_delta | #20 |
| `feat/m1b-signed-external-head-checkpoint` | `99f369720bd7d86efc965e865a31758a71ff0697` | exact_squash_delta | #41 |
| `feat/m1b-signed-review-revocation` | `2c1d6837aba1888893134fdf949b16c1df00cc5f` | exact_squash_delta | #38 |
| `feat/m1b-source-review-packet` | `b33aabea91a0618f3df262e1d1c59f8544cca872` | exact_squash_delta | #37 |
| `feat/m1b-sqlite-review-registry` | `90e8b9033937312c2ed0819f13959320b1f75550` | exact_squash_delta | #40 |
| `feat/m1c-eligible-retail-value-comparison` | `6c075802fd5efe3149e435d74008c856d1cb021e` | exact_squash_delta | #27 |
| `feat/m1c-excluded-target-sensitivity` | `8d15f467a6a22da97ede96d4dddb0f5683b698e9` | exact_squash_delta | #28 |
| `feat/m1c-prequential-residual-envelope` | `8272509c2605bf400663d3164425c711d1549811` | exact_squash_delta | #25 |
| `feat/m1c-retail-coverage-gate` | `25ed88ef346fcedc8bf0c1bae03edc3f4a275fae` | exact_squash_delta | #24 |
| `feat/m1c-retail-declared-release-backtest` | `de073dbbb525873d7b9019f96c0b2768f2153724` | exact_squash_delta | #23 |
| `feat/m1c-retail-eligibility-drift-audit` | `c934736ace9d32708f9986f750cf019cdd4fdbb6` | exact_squash_delta | #26 |
| `feat/m1c-retail-sensitivity-sweep` | `7ca3b0c7d547c7ef81029bcdd299dad18a729130` | exact_squash_delta | #30 |
| `feat/m1c-reuse-sensitivity-audit` | `33579fd0f7b269d52b1bd461c8ca8be8707cc3ee` | exact_squash_delta | #32 |
| `feat/m1c-sensitivity-coverage-policy` | `4af79d6f14684fb44b510a7f1742196a3ed8493f` | exact_squash_delta | #31 |
| `feat/mm-m1a-synthetic-observation-preflight` | `e7eb9ceafa7ab27cb83c2de6d1bb5f2f908acefc` | exact_squash_delta | #5 |
| `feat/mm-m1b-bounded-binary-stream` | `701dc257ce2eadb0eca5943af1ba7d357c562aec` | exact_squash_delta | #15 |
| `feat/mm-m1b-bounded-uci-xlsx-reader` | `4adbf2fc8311eaa8e33da346d1c3f03f47606b9c` | exact_squash_delta | #19 |
| `feat/mm-m1b-dual-witness-fence-continuity` | `67c46b9aeb71895c334175ce03cb271597a0020f` | exact_squash_delta | #48 |
| `feat/mm-m1b-https-challenged-head-read` | `63cc3c66fa096d6003344dfc5d0df2c4a3c5d5c4` | exact_squash_delta | #50 |
| `feat/mm-m1b-local-snapshot-quality` | `29583193134dc160bcde4cf117694768d38b01fd` | exact_squash_delta | #17 |
| `feat/mm-m1b-policy-bound-publication` | `5c378aa5f4135e5e12cad85e9fd8d44f49066874` | exact_squash_delta | #46 |
| `feat/mm-m1b-separate-durable-fence-pin` | `57eb697f522366b40b128a856053cd03a49e1049` | exact_squash_delta | #49 |
| `feat/mm-m1b-signed-integrated-head-fence` | `a34161cf0dd3adf9507f7e3d752432bbdabd8d58` | exact_squash_delta | #47 |
| `feat/mm-m1b-staged-csv-snapshot` | `2604bfa22d4dc637732da6478b34c70772286530` | exact_squash_delta | #10 |
| `feat/mm-m1b-synthetic-availability-gate` | `d3488d940809039f76b8c1251f93458265874fdf` | exact_squash_delta | #8 |
| `feat/mm-m1b-uci-transaction-projection` | `b35aeebb9ebca2433f35e3f3f285bd00892d73c7` | exact_squash_delta | #18 |
| `feat/mm-m1c-availability-aware-rolling` | `ff1eec122ef8a43d824ef705343dc462601e246a` | exact_squash_delta | #9 |
| `feat/mm-m1c-origin-audit-ledger` | `ffaa24619c0fe9ee6b60c83cbd3f399e9d19d2d6` | exact_squash_delta | #13 |
| `feat/mm-m1c-staged-rolling-baselines` | `039dbb994f2784516a0d001055ebd68dc409436d` | exact_squash_delta | #11 |
| `feat/mm-m1c-synthetic-rolling-backtest` | `83968ae03219c58bac8e0724555dbfe317ce60ec` | exact_squash_delta | #7 |
| `feat/portfolio-local-demo` | `b90c95d870fb532f36c4f377682e91f17ad93cb5` | exact_squash_delta | #72 |
| `fix/mm-m1c-min-observed-history` | `8d1300c7e0642670d27164db2e193c244d51568a` | exact_squash_delta | #14 |
| `main` | `c31ecd6dbf3f68be8726bdba2b23a813226c2618` | preserve | - |
| `perf/m1c-cache-prequential-forecast` | `723869fee21abd6fea4b359c733e7cb4c1be57a4` | exact_squash_delta | #33 |
| `perf/m1c-incremental-calibration-window` | `8b0b6572ca64ddb2460f98f5fed5b26ab94e86c8` | exact_squash_delta | #35 |
| `perf/m1c-reproducible-retail-benchmark` | `bb84fc122bcbc06a87e04c6f027eab4a2b9c0224` | exact_squash_delta | #36 |
| `review/census-canonical-fingerprint` | `a9e66f6110b7e0974bc79e91321e118d80eebf40` | exact_ancestor | - |
| `review/nov27-consolidate-60-61-64` | `ed9dc38c3ffc900b1340f762c11c1ae4ecb56e9e` | exact_ancestor | - |
| `test/m1c-adversarial-cache-equivalence` | `41a0696e44e8b92590295e99444f5b9c14814b90` | exact_squash_delta | #34 |
