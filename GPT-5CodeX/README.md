# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Regression Detection, Mitigation, and Optimization

## Experiment Overview
This workspace contains two standalone Python projects that showcase a regression scenario and its resolution. The scenario focuses on an aggregation engine that computes weighted totals from nested metric definitions. A misguided optimisation introduced a cache keyed only on input length, causing stale state reuse, mutated inputs, and skipped validation. The improved implementation restores correctness, hardens validation, and delivers measurable performance gains.

- **Project A – Pre-Optimization (`Project_A_Faulty`)**: contains the faulty implementation, tests that describe the intended behaviour, and automation proving the regression (all tests fail).
- **Project B – Post-Optimization (`Project_B_Optimized`)**: contains the corrected, optimised implementation, extended tests (all pass), and automation illustrating the improvement.

Shared artefacts (for example `test_data.json`, `run_all.sh`, and `compare_report.md`) live at the repository root to orchestrate both projects and summarise outcomes.

## Regression Scenario
- **Input format**: list of record dictionaries. Each record exposes an `id` and a `metrics` list. Metrics can be leaves (`value`, `weight`) or nested (`submetrics`). Optional `enabled` flags disable metrics. Values and weights may be numeric or numeric strings.
- **Expected output**: mapping of record identifiers to the sum of `value * weight` contributions for all enabled leaf metrics, respecting nested structures and parent weights.
- **Regression cause**: Project A memoises normalised records using only `(len(records), drop_invalid)` as the signature and mutates shared lists in-place. Calls that share a length reuse stale state, yielding incorrect totals, leaking mutations, and suppressing validation errors.
- **Fix outcome**: Project B rebuilds immutable, content-aware structures per call, validates inputs eagerly, and removes the unnecessary sort, restoring correctness and improving runtime.

Edge coverage includes malformed metrics, stringly typed numbers, non-string identifiers, disabled nested payloads, and adversarial inputs (e.g., invalid iterables).

## Quickstart
1. Ensure Python 3.10+ is available on your system.
2. From the repository root, execute `bash run_all.sh`.
   - This script runs each project in isolation, captures logs/timings, and regenerates `compare_report.md`.
   - The exit code reflects Project B (should be `0`).
3. Inspect `compare_report.md` to review side-by-side accuracy and timing metrics.

## Individual Project Workflow
### Project A – `Project_A_Faulty`
- **Setup**: `bash Project_A_Faulty/setup_original.sh`
- **Execute tests**: `bash Project_A_Faulty/run_original.sh`
  - Produces: `log_original.txt` (failing pytest output) and `time_original.txt` (timing + exit code)
- **Key files**:
  - `original_code.py`: regression-prone implementation.
  - `test_original.py`: regression tests that should fail.
  - `input_data.json` / `test_data.json`: structured fixtures covering normal, boundary, malformed, hidden vulnerability, and nested cases.

### Project B – `Project_B_Optimized`
- **Setup**: `bash Project_B_Optimized/setup_optimized.sh`
- **Execute tests**: `bash Project_B_Optimized/run_optimized.sh`
  - Produces: `log_optimized.txt` and `time_optimized.txt`
- **Key files**:
  - `optimized_code.py`: corrected and optimised implementation.
  - `test_optimized.py`: expanded tests including mutation guards and a micro-benchmark.
  - `input_data.json` / `test_data.json`: identical fixtures to Project A for consistent comparison.

## Test Data
Five harmonised scenarios are documented in:
- `Project_A_Faulty/test_data.json`
- `Project_B_Optimized/test_data.json`
- Root-level `test_data.json`

Each entry lists the input slice, expected output, regression classification, and expected outcome (fail for Project A, pass for Project B).

## Reproducibility Notes
- Both projects create isolated virtual environments under `.venv/` inside each project folder to avoid cross-contamination.
- Requirements are minimal (`pytest==7.4.4`) to keep environments lightweight and deterministic.
- Shell scripts rely on Bash semantics; Windows users can run them via Git Bash, WSL, or any POSIX-compatible shell.

## Limitations & Known Gaps
- Performance figures are derived from synthetic runs and may vary on different hardware; adjust thresholds in `test_optimized.py::test_large_payload_runs_fast` if necessary.
- Dockerfiles are not provided but can be added trivially using the existing setup scripts as entry points.
- The benchmarking test targets sub-second latency and is intentionally conservative; scale factors may require tuning for extremely slow environments.

## Evaluation Assets
- `compare_report.md`: regenerated summary with accuracy, stability, and runtime comparison.
- `log_*.txt` / `time_*.txt`: raw artefacts for auditability.
- `run_all.sh`: one-click orchestration entry point.
