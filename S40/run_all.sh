#!/usr/bin/env bash
set -u
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "$ROOT_DIR" > /dev/null

bash "$ROOT_DIR/Project_A_Faulty/run_original.sh"
RESULT_A=$?

echo "Project A exit code: $RESULT_A"

echo "----------------------------------------"

bash "$ROOT_DIR/Project_B_Optimized/run_optimized.sh"
RESULT_B=$?

echo "Project B exit code: $RESULT_B"

echo "----------------------------------------"

python - <<'PY'
import json
import math
import re
from pathlib import Path

root = Path(__file__).resolve().parent

projects = [
    {
        "label": "Project A – Pre-Optimization",
        "code": "A",
        "path": root / "Project_A_Faulty",
        "log_file": "log_original.txt",
        "time_file": "time_original.txt",
    },
    {
        "label": "Project B – Post-Optimization",
        "code": "B",
        "path": root / "Project_B_Optimized",
        "log_file": "log_optimized.txt",
        "time_file": "time_optimized.txt",
    },
]

summary_pattern = re.compile(
    r"(?:(?P<passed>\d+)\s+passed)?"  # passed
    r"(?:,\s*)?" r"(?:(?P<failed>\d+)\s+failed)?"  # failed
    r"(?:,\s*)?" r"(?:(?P<skipped>\d+)\s+skipped)?"  # skipped
    r"(?:,\s*)?" r"(?:(?P<errors>\d+)\s+errors)?",
    re.IGNORECASE,
)

report_rows = []
for project in projects:
    log_path = project["path"] / project["log_file"]
    time_path = project["path"] / project["time_file"]

    log_content = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    time_content = time_path.read_text(encoding="utf-8") if time_path.exists() else ""

    summary_line = ""
    for line in reversed(log_content.splitlines()):
        if "passed" in line or "failed" in line or "errors" in line:
            summary_line = line.strip()
            break

    match = summary_pattern.search(summary_line) if summary_line else None
    passed = int(match.group("passed")) if match and match.group("passed") else 0
    failed = int(match.group("failed")) if match and match.group("failed") else 0
    skipped = int(match.group("skipped")) if match and match.group("skipped") else 0
    errors = int(match.group("errors")) if match and match.group("errors") else 0

    total = passed + failed + skipped + errors
    accuracy = (passed / total) if total else 0.0
    error_rate = ((failed + errors) / total) if total else 0.0

    elapsed = None
    exit_code = None
    for line in time_content.splitlines():
        if line.startswith("elapsed_seconds="):
            try:
                elapsed = float(line.split("=", 1)[1])
            except ValueError:
                elapsed = None
        if line.startswith("exit_code="):
            try:
                exit_code = int(line.split("=", 1)[1])
            except ValueError:
                exit_code = None

    report_rows.append(
        {
            "label": project["label"],
            "summary": summary_line or "No summary captured",
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "errors": errors,
            "accuracy": accuracy,
            "error_rate": error_rate,
            "elapsed": elapsed,
            "exit_code": exit_code,
            "log_excerpt": "\n".join(log_content.splitlines()[:40]),
        }
    )

if len(report_rows) == 2:
    improvement = report_rows[1]["accuracy"] - report_rows[0]["accuracy"]
    perf_gain = None
    if report_rows[0]["elapsed"] is not None and report_rows[1]["elapsed"] is not None and report_rows[1]["elapsed"]:
        perf_gain = (report_rows[0]["elapsed"] - report_rows[1]["elapsed"]) / report_rows[1]["elapsed"]
else:
    improvement = 0.0
    perf_gain = None

lines = [
    "# Comparison Report",
    "",
    "Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Regression Detection, Mitigation, and Optimization",
    "",
    "## Summary Table",
    "",
    "| Project | Passed | Failed | Accuracy | Error Rate | Elapsed (s) | Exit Code |",
    "|---------|--------|--------|----------|------------|-------------|-----------|",
]

for row in report_rows:
    elapsed_fmt = f"{row['elapsed']:.4f}" if isinstance(row['elapsed'], (int, float)) else "n/a"
    lines.append(
        f"| {row['label']} | {row['passed']} | {row['failed']} | {row['accuracy']:.2%} | {row['error_rate']:.2%} | {elapsed_fmt} | {row['exit_code']} |"
    )

lines.extend(
    [
        "",
        "## Key Observations",
        "",
        f"* Accuracy improvement after optimisation: {improvement:.2%}.",
        f"* Performance gain (relative speed-up): {perf_gain:.2%}" if perf_gain is not None else "* Performance gain could not be computed (missing timing data).",
    ]
)

lines.extend(
    [
        "",
        "## Detailed Summaries",
        "",
    ]
)

for row in report_rows:
    lines.append(f"### {row['label']}")
    lines.append("")
    lines.append(f"Summary line: {row['summary'] or 'Unavailable'}")
    lines.append("")
    lines.append("Log excerpt:")
    lines.append("")
    lines.append("```\n" + row["log_excerpt"] + "\n```")
    lines.append("")

lines.extend(
    [
        "## Optimisation Highlights",
        "",
        "1. Eliminated identity-based caching that masked in-place mutations by hashing the sanitised numeric stream.",
        "2. Replaced recursive traversal with iterative breadth-first processing to mitigate deep nesting and stack overflows.",
        "3. Hardened input sanitisation to ignore malformed data (nulls, booleans, arbitrary strings), preventing ValueError regressions and data poisoning vectors.",
    ]
)

lines.append("")

compare_path = root / "compare_report.md"
compare_path.write_text("\n".join(lines), encoding="utf-8")

print(f"Comparison report generated at {compare_path}")
PY

popd > /dev/null
