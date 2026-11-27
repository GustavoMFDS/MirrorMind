# REX-06–08 - Security and community workflow

## Security settings

On 2026-11-27, the repository was public and the API confirmed secret
scanning and push protection enabled, Dependabot alerts enabled (HTTP
204), automated security fixes enabled and not paused, and private
vulnerability reporting enabled. CodeQL default setup was requested and
read back as configured; initial scan [46062565112](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46062565112)
must be checked for completion and actual language coverage. An initial
open-alert query returned zero secret-scanning and Dependabot alerts;
code scanning returned no analysis found. These are point-in-time
results, not security certification.

Use the free public-repository features. No private registry credentials,
paid security products, automatic merging, or permission to redistribute
WorldKernel or data. Dependabot may propose changes; each must pass normal
review and current main checks. Private optional dependencies can limit
dependency analysis. Review security alerts privately; never reproduce
secret values in logs or comments. Do not test push protection by committing
a real secret. Version-update scheduling and dependency submission are
deferred pending a review of the optional private dependency.

## Community workflow

Issue templates cover bugs, feature proposals and research, with a link
to private disclosure. The PR template requests exact-head evidence,
limitations, data and authority boundaries. Existing labels are preserved;
area, priority and status labels and milestone groups support triage.
No arbitrary due dates or new product commitments are implied.

See [issue templates](../../.github/ISSUE_TEMPLATE),
[PR template](../../.github/pull_request_template.md),
[contribution guide](../../CONTRIBUTING.md) and [security policy](../../SECURITY.md).
Existing issue and PR history is retained; the active UCI work is not
modified by this change.

Server-side changes and scan results are recorded separately in the
integration PR. Never infer operational security from template presence or
a successful API request.
