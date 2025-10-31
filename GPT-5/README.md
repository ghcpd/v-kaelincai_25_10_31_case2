# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Regression Detection, Mitigation, and Optimization

## Overview
This repository contains two Python projects used to evaluate AI model capabilities in detecting and correcting regressions:

- **Project_A_Faulty**: Contains a deliberately regressed implementation in `original_code.py` that analyzes nested numeric data structures. Multiple bugs (logic, security, performance) are present.
- **Project_B_Optimized**: Contains the corrected and optimized implementation in `optimized_code.py` fixing logical errors, removing security vulnerabilities, and improving performance.

A shared `test_data.json` defines five structured test scenarios covering:
1. Normal numeric inputs
2. Deeply nested structures
3. Malformed inputs & negatives
4. Code injection attempt (security)
5. Large performance stress test

## Regression Scenario
Function: `analyze_numbers(data)`
Purpose: Traverse arbitrarily nested lists, tuples, sets, and dicts (with `value` fields) collecting numeric values, possibly embedded as strings, then compute statistics: count, sum, average, min, max.

### Faulty (Regression) Behavior
- Stops descending after shallow depth, missing deeper values.
- Uses `eval()` for string coercion causing security vulnerability.
- Skips negative numeric strings; treats `None` as zero inflating counts.
- Inefficient min/max via repeated scans (O(n^2) overall for aggregated operations).
- Ignores nested dict values except top-level `'value'` keys.

### Optimized Behavior
- Full iterative traversal (stack) for arbitrary depth.
- Safe numeric string detection via regex; rejects code-injection strings.
- Proper negative number parsing, excluding invalid values entirely.
- Single-pass metric aggregation; optional NumPy fast path for large datasets.
- Proper nested dict expansion.

## Files & Structure
```
Project_A_Faulty/
  original_code.py
  requirements_original.txt
  setup_original.sh
  test_original.py
  run_original.sh
  input_data.json
  log_original.txt (generated/placeholder)
  time_original.txt (generated/placeholder)
  test_data.json
Project_B_Optimized/
  optimized_code.py
  requirements_optimized.txt
  setup_optimized.sh
  test_optimized.py
  run_optimized.sh
  log_optimized.txt (generated/placeholder)
  time_optimized.txt (generated/placeholder)
  test_data.json
run_all.sh
compare_report.md (generated/placeholder)
README.md
```

## Execution Workflow
### Prerequisites
- Python 3.10+ recommended
- Bash environment (Git Bash / WSL on Windows) for `.sh` scripts.

### One-Click Project Runs
Run faulty project:
```bash
bash Project_A_Faulty/run_original.sh
```
Run optimized project:
```bash
bash Project_B_Optimized/run_optimized.sh
```
Run both + generate comparison report:
```bash
bash run_all.sh
```

## Generated Outputs
- `log_original.txt` / `log_optimized.txt`: Test case pass/fail details.
- `time_original.txt` / `time_optimized.txt`: Performance timing (10 runs over a large dataset).
- `results_original.json` / `results_optimized.json`: Structured test outcome data.
- `compare_report.md`: Side-by-side metrics (pass counts, rates, performance improvement).

## Test Case Semantics
Each test case includes:
- `expected_success_pre`: Whether the *faulty* implementation should produce correct stats (false when regression is demonstrated).
- `expected_success_post`: Whether the optimized implementation should succeed (always true here).

In the faulty project, tests for regression intentionally pass when results **do not** match expected output (verifying the regression exists). In the optimized project, strict equality is enforced (except performance case using approximate markers).

## Performance Measurement
Both versions process a 5,000-item random integer list 10 times. The optimized version uses a single-pass loop (and NumPy fast path if available) improving average time. The comparison report computes relative speedup: `(original_avg - optimized_avg) / original_avg`.

## Security Mitigation
The faulty implementation uses `eval()` allowing arbitrary code execution. The optimized version replaces this with a safe regex-based numeric parser, rejecting injection attempts (`__import__('os').getcwd()` test case).

## Reproducibility
Each project has an isolated virtual environment via its setup script. No shared state required. Re-run scripts to regenerate logs and report deterministically (random dataset controlled by seed 42).

## Limitations / Edge Cases
- Extremely large nested structures may benefit further from streaming / generator-based aggregation to reduce peak memory.
- Non-standard numeric formats (scientific notation, hex) currently ignored.
- Dictionary numeric values only accessed via `'value'` key or nested traversal; custom schemas not auto-detected.
- NumPy usage is optional; if unavailable performance improvement may be reduced.

## Next Possible Enhancements
- Add Dockerfiles for containerized reproducibility.
- Extend numeric parsing to scientific notation (e.g., `1e5`).
- Add property-based tests (Hypothesis) for fuzz coverage.
- Integrate benchmarking harness (pytest-benchmark).

## Running on Windows (PowerShell Alternative)
If Bash is unavailable, you can manually execute equivalent steps in PowerShell:
```powershell
python -m venv .venv_original; .\.venv_original\Scripts\activate; pip install -r Project_A_Faulty\requirements_original.txt; python Project_A_Faulty\test_original.py
python -m venv .venv_optimized; .\.venv_optimized\Scripts\activate; pip install -r Project_B_Optimized\requirements_optimized.txt; python Project_B_Optimized\test_optimized.py
```

## Evaluation Criteria Mapping
- Correctness: Verified by test suites and JSON results.
- Regression Detection: Faulty test harness expects mismatches for broken cases.
- Mitigation: Optimized version passes all cases.
- Security: Removal of `eval()` and injection rejection.
- Performance: Single-pass + optional NumPy acceleration measured in timing reports.

---
Run `bash run_all.sh` to generate empirical comparison now.
