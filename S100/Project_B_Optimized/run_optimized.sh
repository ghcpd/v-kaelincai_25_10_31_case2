#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
LOG_FILE="$PROJECT_DIR/log_optimized.txt"
TIME_FILE="$PROJECT_DIR/time_optimized.txt"

bash "$PROJECT_DIR/setup_optimized.sh"

if [ -f "$VENV_DIR/bin/activate" ]; then
  ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
else
  ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
fi

# shellcheck source=/dev/null
source "$ACTIVATE_SCRIPT"

pytest -q "$PROJECT_DIR/test_optimized.py" >"$LOG_FILE" 2>&1
python "$PROJECT_DIR/optimized_code.py" --summary >>"$LOG_FILE" 2>&1
python "$PROJECT_DIR/optimized_code.py" --benchmark >"$TIME_FILE" 2>&1

echo "Tests exited with status 0" >>"$LOG_FILE"
