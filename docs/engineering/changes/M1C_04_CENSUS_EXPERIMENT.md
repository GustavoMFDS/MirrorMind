# Change request - fictional Census experiment identity and replay

## Goal and scope
The frozen schedule binds origins but not a prior data commitment. Add a
typed, pure in-process experiment specification binding the normalized
input manifest, schedule, declared Git revision, protocol and schemas.
Verify that commitment before scoring and verify a submitted complete
canonical receipt by local deterministic replay. No persistence, network,
new dependencies, API, CLI, real data or trusted registration.

## Acceptance
- Public normalized manifest helper shares the existing v2 serializer
  and input validation; historical v2 digest and result remain unchanged.
- Strict specification types, SHA syntax and split allowlist. Reject
  changed data, publication, revision, schedule or declared code before
  scoring; verify nested manifest after evaluation.
- Canonical JSON bytes, exact replay comparison, 4 MiB receipt bound.
  Reject even rehashed modified receipts; do not parse arbitrary input.
- All authority, attestation, holdout lock and inference flags remain false
  or abstained. Recomputed commitment is not independent registration.
- Preserve 250 total origins and all existing numeric/time constraints.
  At most 50 holdout origins cannot satisfy proposed 60-pair minimum.

## Impact map
| Layer | Path | Change |
|---|---|---|
| Core | census_evaluation.py | Public bounded manifest helper |
| Core | census_experiment.py | Typed identity and replay |
| Caller | census_split.py | Existing wrapper consumed unchanged |
| Tests | test_census_experiment.py | Synthetic identity and adverse replay |
| API, state, external contracts | None | No promotion |

## Evidence and limits
Existing synthetic dataset/model cards apply; full receipts include derived
values, so fictional use only. The code revision is caller-declared, not
runtime attestation. All records remain visible to the caller; no blind
holdout, independent timestamp or durable registration. No calibrated
interval or winner. B-01/B-02 remain open. Separate future storage adapter
requires its own review. Revert source-only changes if needed.
Independent review and exact-head gate pending.
