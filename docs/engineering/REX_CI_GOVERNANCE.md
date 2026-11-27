# REX-04/05 - Main governance and public CI

## Review baseline

On 2026-11-27, main `f6e10e04d3135373c7a9cb60f767b8e655291519`
had two successful GitHub Actions check contexts, `test` and
`symbol-catalog`, from GitHub App integration 15368. No branch
protection or active ruleset was returned by the repository API.
The default workflow token was read-only. The older Python workflow ran
one 3.11 job on every push and pull request. Its sample job
[46060824041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46060824041)
took approximately 30 seconds from job start to completion.

## Workflow changes

- Keep the original `test` (Python 3.11) and `symbol-catalog` names,
  and all their existing test, lint and document checks. Include examples
  in Ruff and expose actual optional skips in pytest output.
- Add a parallel compatibility matrix for Python 3.12 and 3.13. No
  private WorldKernel install or secrets in public CI. The matrix is
  additional evidence, not a substitute for the pinned local gate.
- Trigger on pull requests to main, pushes to main and manual dispatch.
  Feature pushes before opening a PR no longer start automatic CI once
  this configuration is on the relevant branch; use the local gate and
  an open PR to obtain public checks. Old branches may retain the previous
  workflow until synchronized.
- Cancel obsolete runs only within a single PR and workflow; use unique
  run IDs for non-PR events so merged-main evidence is preserved.
- Use a ten-minute job timeout, explicit read-only contents permission,
  no persisted checkout credentials, and pip download caching keyed to
  pyproject.toml and the interpreter. The cache is not a lockfile or a
  reproducibility guarantee. No self-hosted runner or paid service.

See [Python CI](../../.github/workflows/ci.yml) and
[documentation CI](../../.github/workflows/docs.yml). Compare completed
runs and actual durations after integration; do not claim performance
gains from configuration alone. The added compatibility jobs increase
test executions per PR, while trigger and cancellation changes avoid
redundant runs. Maintain the local gate and public CI as separate evidence.

## Main protection policy

Proposed active rule for main only: require a PR, prevent deletion and
force pushes, require the two stable GitHub Actions check contexts, and
no bypass actors. No mandatory second-person approval while the owner
is the sole maintainer; a review comment by the same account is not
an independent GitHub approval. Preserve merge commits for integrated
ancestry. Do not require an up-to-date branch through the server rule
until the team has evaluated the impact on parallel work; independently
verify the combined candidate against the current base before integration.
The additional Python matrix should pass in the current review but is
not initially configured as a required context. Never bypass failing or
missing required checks. If a check cannot run, stop and investigate.
Rule creation and read-back evidence are recorded separately; this
document is not evidence that a server rule exists.

## Branch cleanup boundary

The [branch inventory](REX_BRANCH_AUDIT.md) identified 15 ancestor tips
and 57 exact merged-PR tips that are potential cleanup candidates.
The latter need explicit preservation analysis because squash may not
retain original commits. No deletion is performed in this change.
Keep main, open PR branches, linked worktrees, changed heads and any
branch used by active Codex work. Refresh all refs and dependencies and
obtain a maintenance decision before deleting branches.

## Rollout and acceptance

Validate the candidate with the existing six local checks and Ruff on
examples. Verify all current GitHub checks, including compatibility
jobs, before integration. Then verify the main checks. Any server rules
must be read back from GitHub, not inferred from a successful API
request. No modifications to billing, release tags or source permissions.
