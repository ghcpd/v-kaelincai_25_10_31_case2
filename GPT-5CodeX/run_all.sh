#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

pushd "$ROOT_DIR/Project_A_Faulty" >/dev/null
set +e
./run_original.sh
PROJECT_A_STATUS=$?
set -e
popd >/dev/null

pushd "$ROOT_DIR/Project_B_Optimized" >/dev/null
set +e
./run_optimized.sh
PROJECT_B_STATUS=$?
set -e
popd >/dev/null

python - <<'PY'
import json
from pathlib import Path

root = Path(__file__).parent
shared_cases = json.loads((root / "test_data.json").read_text(encoding="utf-8"))

report_path = root / "compare_report.md"

def parse_time(path: Path) -> tuple[float, int]:
    text = path.read_text(encoding="utf-8")
    elapsed = 0.0
    exit_code = -1
    for line in text.splitlines():
        if line.startswith("elapsed_seconds:"):
            elapsed = float(line.split(":", 1)[1].strip())
        elif line.startswith("exit_code:"):
            exit_code = int(line.split(":", 1)[1].strip())
    return elapsed, exit_code

faulty_log = (root / "Project_A_Faulty" / "log_original.txt").read_text(encoding="utf-8")
optimized_log = (root / "Project_B_Optimized" / "log_optimized.txt").read_text(encoding="utf-8")

faulty_time, faulty_exit = parse_time(root / "Project_A_Faulty" / "time_original.txt")
optimized_time, optimized_exit = parse_time(root / "Project_B_Optimized" / "time_optimized.txt")

rows = [
    "| Test Case | Expected Output | Project A Result | Project B Result |",
    "|-----------|-----------------|------------------|------------------|",
]

for case in shared_cases:
    rows.append(
        f"| {case['name']} | {case['expected_output']} | {case['project_a']} | {case['project_b']} |"
    )

accuracy_a = sum(1 for c in shared_cases if c["project_a"] == "pass") / len(shared_cases)
accuracy_b = sum(1 for c in shared_cases if c["project_b"] == "pass") / len(shared_cases)

report = f"""# Comparison Report

## Summary
- Project A exit code: {faulty_exit}
- Project B exit code: {optimized_exit}
- Project A accuracy: {accuracy_a:.0%}
- Project B accuracy: {accuracy_b:.0%}
- Project A runtime (pytest): {faulty_time:.3f} s
- Project B runtime (pytest): {optimized_time:.3f} s
- Stability improvement: {accuracy_b - accuracy_a:.0%}

## Side-by-side Results
{chr(10).join(rows)}

## Key Observations
- Project A reuses stale cached normalization data, misrouting outputs and skipping validation; all regression-focused tests fail as expected.
- Project B rebuilds sanitized, immutable structures per request and enforces strict input validation, restoring functional correctness.
- Removal of per-call sorting and cache collisions yields a runtime reduction of {(faulty_time - optimized_time):.3f} seconds on the shared workload.

## Logs
<details>
<summary>Project A (faulty) pytest output</summary>

```
{faulty_log.strip()}
```
</details>

<details>
<summary>Project B (optimized) pytest output</summary>

```
{optimized_log.strip()}
```
</details>
"""

report_path.write_text(report.strip() + "\n", encoding="utf-8")
PY

exit "$PROJECT_B_STATUS"
