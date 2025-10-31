# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Regression Detection, Mitigation, and Optimization

## Experiment Overview

This repository contains two standalone Python projects that model a regression scenario in a risk scoring pipeline. The scenario targets the ability of AI-assisted workflows to detect, diagnose, and correct regressions that were introduced while attempting to cache expensive metric calculations. The faulty implementation silently flattens nested adjustment deltas and coerces malformed inputs to zero, producing deceptively stable metrics. The optimized implementation restores element-wise adjustments, enforces strict data validation, and improves runtime with single-pass aggregation.

The shared dataset (`input_data.json`) contains structured regression cases covering:

- Balanced nominal load (`balanced-normal`)
- Boundary conditions (`boundary-zero`)
- Malformed payloads (`invalid-malformed`)
- Hidden vulnerability under skewed weights (`hidden-vulnerability`)
- Complex nested adjustments (`complex-nested`)

Automated tests exercise normal, boundary, malformed, hidden vulnerability, and complex nested scenarios. The optimized project demonstrates precise handling of each class while surfacing regressions that the faulty project misses.

## Repository Layout

```
├── Project_A_Faulty/
│   ├── input_data.json
│   ├── original_code.py
│   ├── requirements_original.txt
│   ├── run_original.sh
│   ├── setup_original.sh
│   ├── test_data.json
│   ├── test_original.py
│   ├── log_original.txt
│   └── time_original.txt
├── Project_B_Optimized/
│   ├── input_data.json
│   ├── optimized_code.py
│   ├── requirements_optimized.txt
│   ├── run_optimized.sh
│   ├── setup_optimized.sh
│   ├── test_data.json
│   ├── test_optimized.py
│   ├── log_optimized.txt
│   └── time_optimized.txt
├── test_data.json               # Shared canonical test descriptions
├── generate_compare_report.py   # Script that builds compare_report.md
├── compare_report.md            # Generated comparison summary
├── run_all.sh                   # Orchestrates both projects and report generation
└── README.md                    # This document
```

## Regression Scenario

- **Input format:** JSON documents containing lists of predictions, actuals, optional weight vectors, and nested adjustment deltas.
- **Expected output:** Per-case metrics including mean absolute error (MAE), root mean squared error (RMSE), aggregate bias, and a stability index in `[0, 1]`.
- **Regression cause:** An attempted micro-optimization appended adjustment deltas to predictions instead of applying them element-wise, reused cached integer-rounded tuples, and silently coerced malformed inputs to zero. Metrics looked “better” while masking bias and runtime degraded due to repeated percentiles.
- **Fix outcome:** The optimized implementation validates inputs eagerly, applies nested adjustments correctly, aggregates metrics in a single pass, and skips malformed cases during performance runs, producing accurate analytics with a 55% runtime improvement on the supplied benchmark workload.

## Reproducible Execution

Each project is self-contained with its own virtual environment requirements and automation scripts.

### Project A – Pre-Optimization (Faulty)

```bash
cd Project_A_Faulty
bash setup_original.sh      # One-time environment setup
bash run_original.sh        # Runs pytest, captures failing log/time artifacts
```

Artifacts written:
- `log_original.txt` – pytest output plus metric summary highlighting failures.
- `time_original.txt` – benchmark runtime showing degraded performance.

### Project B – Post-Optimization (Improved)

```bash
cd Project_B_Optimized
bash setup_optimized.sh     # One-time environment setup
bash run_optimized.sh       # Runs pytest, captures successful log/time artifacts
```

Artifacts written:
- `log_optimized.txt` – passing pytest output and corrected metrics.
- `time_optimized.txt` – faster benchmark runtime.

### Master Orchestration

From the repository root you can run:

```bash
bash run_all.sh
```

This command executes both projects sequentially, regenerates `compare_report.md` via `generate_compare_report.py`, and writes an execution digest to `artifacts/run_all_summary.txt`. The script exits with the optimized project’s status to ensure regressions remain visible if the fix ever fails.

## Automated Test Coverage

- `test_original.py` (faulty) demonstrates regression detections by expecting correct metrics and ensuring malformed inputs raise `ValueError` – the assertions fail, proving the regression exists.
- `test_optimized.py` (optimized) provides the same coverage plus dataset summary and a performance sanity bound. It validates normal, boundary, malformed, hidden vulnerability, and complex nested cases.
- `test_data.json` documents the five structured scenarios and can be reused by external harnesses.

## Logs and Performance Measurements

| Project | Tests Passed | Tests Failed | Benchmark (s) | Notes |
|---------|--------------|--------------|---------------|-------|
| Project_A_Faulty | 1 | 4 | 0.030643 | Regression present; malformed inputs coerced to zero, adjustments ignored. |
| Project_B_Optimized | 7 | 0 | 0.013595 | Fix applied; strict validation and efficient aggregation yield ~55% speedup. |

The detailed comparison including per-scenario metrics is available in `compare_report.md`.

## Environment & Reproducibility Notes

- Both projects target Python 3.10+ and specify dependencies via `requirements_original.txt` and `requirements_optimized.txt` (only `pytest` is required).
- `setup_*.sh` scripts create isolated virtual environments (`.venv/`) and work on macOS, Linux, or Windows (via Git Bash) thanks to cross-platform activation logic.
- No external services are required; all datasets are bundled locally. Dockerfiles are optional and therefore omitted, but virtual environments provide deterministic runtimes.

## Limitations & Further Work

- The provided benchmark simulates workload intensity with synthetic data. Real-world latency may vary with larger datasets.
- Only one deliberately malformed scenario is supplied; extending the dataset with additional adversarial payloads (e.g., NaNs, deeply nested jagged arrays) would further harden the pipeline.
- The optimized implementation skips malformed cases in performance measurements to keep comparisons stable. If future requirements demand penalizing malformed inputs within runtime metrics, adjust `benchmark()` accordingly.
- While the optimized tests enforce a micro-benchmark upper bound, they do not provide full statistical performance profiling. Integrating `pytest-benchmark` or `perf` tooling would offer deeper insights.

## License

All assets were generated for evaluation purposes in this task and are intended to be reproducible and modifiable in downstream experiments.
