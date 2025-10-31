# Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Regression Detection, Mitigation, and Optimization

This repository demonstrates a controlled regression scenario together with its
remediation. Two separate Python projects highlight pre- and post-optimisation
states of a nested payload aggregator that computes a stability index from
heterogeneous telemetry data.

## Projects at a glance

| Project | Path | Purpose |
| --- | --- | --- |
| Project A – Pre-Optimization | `Project_A_Faulty/` | Contains the intentionally faulty implementation that regressed after a misguided caching optimisation. Automated tests codify the expected historical behaviour and currently fail, exposing the regression. |
| Project B – Post-Optimization | `Project_B_Optimized/` | Hosts the corrected and hardened implementation with breadth-first traversal, structural caching, and full input sanitisation. Automated tests pass and confirm the fix together with performance improvements. |

## Regression scenario

* **Input format:** Arbitrarily nested dictionaries, lists, tuples, and sets
  containing telemetry readings (`int`, `float`, or numeric strings) with
  optional metadata (booleans, `None`, nested text, or objects).
* **Output format:** A floating-point stability index (average of valid
  readings) respecting a configurable minimum threshold.
* **Root cause:** The faulty build cached results using `id(payload)` and
  attempted to coerce every entry to `float()`. In-place mutations therefore
  returned stale results, null readings raised `ValueError`, and malformed data
  could poison the calculation or crash the service.
* **Fix overview:** The optimised build hashes the sanitised numeric stream to
  memoise safely, traverses iteratively to avoid recursion limits, and ignores
  unsafe entries without exceptions. It therefore reflects live mutations,
  survives malformed data, and runs faster on deep payloads.

## Test data and coverage

Each project ships a `test_data.json` enumerating five crafted cases:

1. **Normal nested payload** – ensures sparse null entries no longer crash.
2. **Mutated dataset** – verifies caches refresh after in-place updates.
3. **Invalid nested strings** – confirms textual noise is skipped.
4. **Hidden vulnerability (deep nesting)** – stresses traversal depth.
5. **Non-numeric entries** – checks booleans and metadata are discarded.

The combined suite covers normal, boundary, malformed, vulnerability, and
complex nested scenarios.

## Reproducible setup

Both projects isolate dependencies via `requirements_*.txt` and ship a dedicated
`setup_*.sh` script creating a Python virtual environment and installing
`pytest`. You may run the scripts with Git Bash on Windows, macOS Terminal, or a
POSIX shell.

## One-click execution

From the repository root:

1. Ensure Bash is available (`Git Bash` on Windows).
2. Run `./run_all.sh` to execute both projects sequentially (Git Bash or any
  POSIX shell). The script:
   * Bootstraps isolated environments for each project.
   * Executes their test suites, persisting output in `log_*.txt` and timings in
     `time_*.txt`.
   * Generates an aggregated comparison in `compare_report.md`.

  **PowerShell-only alternative:** Run each `run_*.sh` manually (or replicate
  the steps in PowerShell) and finish by executing
  `python generate_compare_report.py` from the repository root to refresh the
  comparison report using the captured logs.

Alternatively, run each project individually via:

* `Project_A_Faulty/run_original.sh`
* `Project_B_Optimized/run_optimized.sh`

## Outputs

* `log_original.txt` / `log_optimized.txt` – Raw test execution logs.
* `time_original.txt` / `time_optimized.txt` – Timing and exit-code metadata.
* `compare_report.md` – Automatically produced summary contrasting accuracy,
  stability, and performance.

## Known limitations

* The timing measurement relies on Python wall-clock time. For robust
  benchmarking consider multiple iterations or profiling tools.
* Scripts assume a functional Python 3.10+ interpreter is available on the
  host system.
* Dockerfiles are omitted to keep the demonstration lightweight, but virtual
  environments provide reproducibility. Container definitions can be added if
  needed.

## Next steps

* Integrate CI pipelines to capture regressions automatically on every change.
* Extend logging to include percentile latency metrics across datasets.
* Consider adding fuzz testing to explore extreme malformed payloads.
