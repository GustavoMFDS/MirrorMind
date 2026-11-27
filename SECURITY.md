# Security policy

## Supported scope

MirrorMind is experimental, pre-release research software. Review the
current default branch; no stable production release or supported-version
lifecycle is claimed. Do not deploy the experimental server as an
internet-facing decision service or use real customer data in its demos.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/GustavoMFDS/MirrorMind/security/advisories/new).
Do not publish exploit details, credentials or private data in public
issues, pull requests or logs. Include an affected commit, minimal
fictional reproduction, expected behavior, potential impact and redacted
diagnostics. Do not access third-party systems or data to reproduce an issue.
The maintainer will review reports on a best-effort basis; no response-time
or remediation SLA is promised.

Ordinary defects and documentation issues can go through the
[contribution guide](CONTRIBUTING.md). The existing
[technical security and evidence-handling guide](docs/SECURITY.md)
describes experimental trust boundaries, data minimization and
authorization constraints. Passing tests do not certify operational security.
