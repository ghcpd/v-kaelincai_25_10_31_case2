#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
LOG_FILE="$PROJECT_DIR/log_original.txt"
TIME_FILE="$PROJECT_DIR/time_original.txt"

bash "$PROJECT_DIR/setup_original.sh"

# shellcheck source=/dev/null
if [ -f "$VENV_DIR/bin/activate" ]; then
	ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
else
	ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
fi

# shellcheck source=/dev/null
source "$ACTIVATE_SCRIPT"

set +e
pytest -q "$PROJECT_DIR/test_original.py" >"$LOG_FILE" 2>&1
TEST_EXIT=$?
set -e

python "$PROJECT_DIR/original_code.py" --summary >>"$LOG_FILE" 2>&1
python "$PROJECT_DIR/original_code.py" --benchmark >"$TIME_FILE" 2>&1

echo "Tests exited with status $TEST_EXIT" >>"$LOG_FILE"
exit $TEST_EXIT
