"""Utility script to assemble compare_report.md without relying on Bash."""

from __future__ import annotations

import re
from pathlib import Path


def _parse_summary(log: str) -> tuple[int, int, int, int, str]:
    pattern = re.compile(
        r"(?:(?P<passed>\d+)\s+passed)?(?:,\s*)?"  # passed
        r"(?:(?P<failed>\d+)\s+failed)?(?:,\s*)?"  # failed
        r"(?:(?P<skipped>\d+)\s+skipped)?(?:,\s*)?"  # skipped
        r"(?:(?P<errors>\d+)\s+errors)?",
        re.IGNORECASE,
    )

    summary_line = ""
    for line in reversed(log.splitlines()):
        if {"passed", "failed", "errors"}.intersection(line.lower().split()):
            summary_line = line.strip()
            break

    match = pattern.search(summary_line) if summary_line else None

    def _extract(name: str) -> int:
        if match and match.group(name):
            return int(match.group(name))
        return 0

    return (
        _extract("passed"),
        _extract("failed"),
        _extract("skipped"),
        _extract("errors"),
        summary_line or "No summary captured",
    )


def main() -> None:
    root = Path(__file__).resolve().parent
    projects = [
        {
            "label": "Project A – Pre-Optimization",
            "path": root / "Project_A_Faulty",
            "log": "log_original.txt",
            "time": "time_original.txt",
        },
        {
            "label": "Project B – Post-Optimization",
            "path": root / "Project_B_Optimized",
            "log": "log_optimized.txt",
            "time": "time_optimized.txt",
        },
    ]

    rows = []
    for item in projects:
        log_content = (item["path"] / item["log"]).read_text(encoding="utf-8")
        time_content = (item["path"] / item["time"]).read_text(encoding="utf-8")

        passed, failed, skipped, errors, summary = _parse_summary(log_content)
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

        rows.append(
            {
                "label": item["label"],
                "summary": summary,
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

    improvement = rows[1]["accuracy"] - rows[0]["accuracy"]
    perf_gain = None
    if rows[0]["elapsed"] and rows[1]["elapsed"]:
        perf_gain = (rows[0]["elapsed"] - rows[1]["elapsed"]) / rows[1]["elapsed"]

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

    for row in rows:
        elapsed_fmt = f"{row['elapsed']:.4f}" if isinstance(row['elapsed'], (int, float)) else "n/a"
        lines.append(
            f"| {row['label']} | {row['passed']} | {row['failed']} | {row['accuracy']:.2%} | {row['error_rate']:.2%} | {elapsed_fmt} | {row['exit_code']} |"
        )

    if perf_gain is not None:
        perf_line = f"* Performance gain (relative speed-up): {perf_gain:.2%}."
    else:
        perf_line = "* Performance gain could not be computed (missing timing data)."

    lines.extend(
        [
            "",
            "## Key Observations",
            "",
            f"* Accuracy improvement after optimisation: {improvement:.2%}.",
            perf_line,
            "",
            "## Detailed Summaries",
            "",
        ]
    )

    for row in rows:
        lines.append(f"### {row['label']}")
        lines.append("")
        lines.append(f"Summary line: {row['summary']}")
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
            "",
        ]
    )

    (root / "compare_report.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
