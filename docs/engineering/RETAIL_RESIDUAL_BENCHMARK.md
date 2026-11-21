# MM-M1c — synthetic retrospective performance comparison

This is a **local engineering benchmark**, not a statistical backtest of
actual sales, CI validation, source authentication or calibration of the
heuristic residual envelope.

## Exactly what is measured

[`scripts/benchmarks/retail_residual.py`](../../scripts/benchmarks/retail_residual.py)
runs the **full** `evaluate_retail_residual_envelopes` call, including
publication validation, preprocessing, prediction, calibration and report
assembly. It uses identical deterministic fictional data and an unchanged
driver against two clean local checkouts:

- Before: `71450cee32b08d02726d7367bf373081d66f4ceb` (PR #34; forecast cache,
  repeated calibration scanning).
- After: `8642f5f77a6b2a3fa3040ff182e961dd640ddcad` (PR #35; rolling calibration).

Use the same Python interpreter, dependencies and machine for both.
The script loads a single checkout's `src/` in a **fresh process**, and refuses
the wrong full SHA or modified tracked files.

The default experiment uses a fictional single product, at most 200
positive-line event-days, a 30-day holdout, 60-day calibration and five
required residuals. `dense` publishes all rows on their event day;
`delayed` omits every 23rd day and declares a four-day publication delay
for every 11th remaining day. No customer, invoice, store or external
source records are read.

## Reproduction

Create separate clean checkouts at the two exact SHAs above, and install
the same project development dependencies once in a Python 3.11+
environment. The example assumes `BEFORE` and `AFTER` point to the
checkout roots and you run commands from the after checkout:

```bash
python scripts/benchmarks/retail_residual.py --source-root BEFORE --expected-head 71450cee32b08d02726d7367bf373081d66f4ceb --profile dense --repetitions 21 --warmups 3
python scripts/benchmarks/retail_residual.py --source-root AFTER --expected-head 8642f5f77a6b2a3fa3040ff182e961dd640ddcad --profile dense --repetitions 21 --warmups 3
```

Repeat both commands for `--profile delayed`. The program emits JSON
with revision, workload, samples, median/min/max time in milliseconds,
the **peak traced Python allocation** in KiB for one separate execution,
and a SHA-256 digest of the entire identifier-minimized report. The digests
must be identical between the two checkouts for the same workload.
Any digest mismatch blocks comparison, even if the times appear favorable.

The driver **does not** record process RSS, system-wide peak memory,
CPU energy, confidence intervals, true demand, a calibrated forecast
interval or usable production latency. Python allocation peaks are not
equivalent to whole-process memory. Results on one Windows computer can
vary with temperature, load, interpreter and scheduling; rerun before
making deployment or capacity decisions.

## Review and decision

Only record a comparative observation if both revisions pass their exact
Git SHA checks and **all** full report digests agree. Compare two
separate workloads, not one cherry-picked favorable case. Do not add a
performance gate to regular CI: the benchmark is opt-in, observational
and intentionally separate from deterministic correctness tests.
The existing local quality gate still independently runs pytest, Ruff,
catalog, atlas, evidence and capability checks. It does not execute
this benchmark and does not claim official GitHub Actions passed.
