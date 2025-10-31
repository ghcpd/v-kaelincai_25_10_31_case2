#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

if [ -f "$VENV_DIR/bin/activate" ]; then
  ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
else
  ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
fi

# shellcheck source=/dev/null
source "$ACTIVATE_SCRIPT"
python -m pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements_optimized.txt"

echo "Virtual environment ready at $VENV_DIR"
