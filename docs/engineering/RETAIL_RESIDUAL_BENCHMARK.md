# Historical MM-M1c — synthetic retrospective performance comparison

**Status:** historical PR #34/#35 comparison. The current residual evaluator
uses a fixed disjoint calibration/holdout split, so these prior rolling-window
timings and allocation measurements do not characterize current code.

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

## One observed Windows run — 2026-11-21

The following readings were obtained with **Python 3.12.10** on an
authorized Windows computer, using the same virtual environment and
the same unmodified `71450cee32b08d02726d7367bf373081d66f4ceb` and
`8642f5f77a6b2a3fa3040ff182e961dd640ddcad` checkouts. Each variant
used three untimed warmups and 21 timed calls; allocations were measured
in a separate invocation using `tracemalloc`.

| Fictional profile | Median before (ms) | Median after (ms) | Observed reduction | Peak traced Python KiB before → after |
| --- | ---: | ---: | ---: | ---: |
| Dense published history (200 days, 30 origins scored) | 4.2998 | 2.1371 | 50.30% | 35.879 → 37.262 |
| Missing/delayed declarations (192 days, 13 origins scored) | 2.3704 | 1.3894 | 41.39% | 35.262 → 34.613 |

The **full report SHA-256 matched for each profile** across the two
implementations:

- Dense: `51db583fcc06b2633fdbf6e85abc821aae47ca546686e0b25bb0af4e73b16827`
- Missing/delayed: `bcb7fdc8f8047596cdf85f63d44518e67a91f0eb3699191bf89eb7943763a934`

For the dense case, Python's *traced allocation peak increased* by 3.85%
with the incremental implementation. For the missing/delayed case it
decreased by 1.84%. Neither is a process-RSS measurement, and neither
establishes an overall memory improvement. The timing reductions are
**observations from one local benchmarking session**, not guaranteed
speedups across machines, profiles, longer histories or production loads.
These measurements do not override the synthetic-only source restrictions.
