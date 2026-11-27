# PORT-07 - Local interactive synthetic decision report

## Goal and scope

The existing M1 workflow and CLI return full structured JSON; the public
portfolio needs a readable interactive entrypoint. Add a local HTML report
generator that runs the existing synthetic workflow, embeds its exact result,
and lets the reader select an already-computed lead-time scenario. This is a
presentation layer, not an alternate forecast or simulation engine.

The CLI takes the existing bounded date, seed and replication inputs and an
explicit new HTML output path. No server, network, external JS/CSS, raw dataset,
WorldKernel, new dependencies, agent execution, business write or source
authorization. The only file write is the explicitly requested new report.
The report is a local snapshot, not a hosted or live dashboard.

## Acceptance and impact

- Run the existing validated workflow once, preserve the entire JSON result
  and render its actual forecast, conditional metrics, trace and limitations.
- Select the existing 1/2/3-day cases without inventing or recomputing metrics.
- Show the actual selected engine, cutoff, uncertainty limits and false
  authorization flags. Do not rank or recommend policies.
- Reject invalid bounded options and existing output paths; do not overwrite.
- Use no network resources and DOM textContent, escape embedded JSON and
  verify report round-trip and failure cases.
- CLI: examples/m2_portfolio_demo.py; template: examples/portfolio_demo.html;
  test: tests/integration/test_portfolio_demo.py. No API execution change;
  experimental capability declaration and ledger updated for discoverability.
- Preserve the existing M1 model card, data card, assumptions and contracts.
  No claim of empirical accuracy or production security.

See [report guide](../PORTFOLIO_DEMO.md) for reproducibility, evidence and limits.
