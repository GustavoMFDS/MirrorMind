# Offline interactive portfolio report

This experimental presentation layer is a reproducible local snapshot of the
existing synthetic decision workflow, not a new decision engine or live UI.
It is independent of the private WorldKernel dependency, and uses no network,
data download, external JavaScript, LLM, API credential or server.

## Reproduce

From the repository root with the development extra installed:

```bash
python -m examples.m2_portfolio_demo --as-of 2011-01-26 --replications 2 --seed 317 --output mirror-demo.html
```

Open the new HTML file in a browser. Choose a different lead time in the
selector to inspect the already-computed cases. To change the date, seed or
number of replications, run the command again with a new output filename.
The CLI rejects an existing path, non-HTML suffix, missing parent directory
and invalid bounded request. The report is the only explicit output file;
the workflow itself performs no business writes. Do not commit generated
reports with private content; this particular generator accepts only the
existing fictional fixture configuration.

## Source walkthrough

- [Generator](../../examples/m2_portfolio_demo.py): `main` parses the three
  existing request options and a new explicit path; `build_report` invokes
  the shared service, serializes the full JSON with nonfinite values rejected,
  escapes angle brackets and ampersands before embedding it in an inert JSON
  script element, and inserts the single payload marker.
- [Template](../../examples/portfolio_demo.html): `renderCase` selects an
  existing sensitivity case and displays the actual mean cost, fill rate,
  ending stock, orders and stockout days for each policy in original order.
  DOM construction uses textContent, not HTML interpolation. The inline
  script draws the fixed forecast profile, shows diagnostic JSON, facts,
  engine evidence, gaps, flags and full trace. No network requests are needed;
  a restrictive meta CSP disallows connections and external resources.
- [Workflow](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md): the same request
  validation, synthetic fixture, temporal cutoff, model card, policy engine,
  assumptions and trace contracts remain unchanged. The default engine is
  the reference policy test double, not WorldKernel.
- [Tests](../../tests/integration/test_portfolio_demo.py): MM-PORT-001 uses
  `test_offline_report_preserves_exact_workflow_result` to verify
  that the exact full result round-trips from the embedded JSON; additional
  regressions check script-terminator escaping, existing file preservation
  and invalid input rejection. Tests do not certify browser isolation.

## Debug and learn

If the generator rejects a request, inspect the existing workflow date
window, integer bounds and output path. If the page cannot render, inspect
the browser console and inert workflow-result payload; do not reinterpret
missing metrics as zero or change the engine to repair presentation.

Exercise: generate the baseline report, switch from two-day to one-day lead
time, then compare the displayed values to the same scenario in the original
workflow JSON. Identify why the trace SHA-256 remains constant when switching
the display. Re-run with another seed and new file to inspect the new trace.

The uncertainty display is a heuristic residual diagnostic, not a calibrated
prediction interval. No real forecast skill, ranking, human approval,
authorization, or production deployment follows from this report.
