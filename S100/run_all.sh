#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PROJECT_A="$ROOT/Project_A_Faulty"
PROJECT_B="$ROOT/Project_B_Optimized"

mkdir -p "$ROOT/artifacts"
SUMMARY_FILE="$ROOT/artifacts/run_all_summary.txt"
: >"$SUMMARY_FILE"

declare -A STATUS

echo "Running Project_A_Faulty (expected to detect regression)..."
"$PROJECT_A/run_original.sh"
STATUS[Project_A_Faulty]=$?

echo "Running Project_B_Optimized (should pass)..."
"$PROJECT_B/run_optimized.sh"
STATUS[Project_B_Optimized]=$?

echo "Regenerating comparison report..."
python3 "$ROOT/generate_compare_report.py"

{
  echo "Run summary generated $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "Project_A_Faulty exit=${STATUS[Project_A_Faulty]}"
  echo "Project_B_Optimized exit=${STATUS[Project_B_Optimized]}"
  echo "Comparison report: $ROOT/compare_report.md"
} >>"$SUMMARY_FILE"

cat "$SUMMARY_FILE"

# Exit with the status of the optimized project so that failures after the fix are surfaced.
exit "${STATUS[Project_B_Optimized]}"
