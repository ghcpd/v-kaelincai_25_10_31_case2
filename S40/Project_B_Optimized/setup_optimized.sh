#!/usr/bin/env bash
set -eo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -d .venv ]]; then
  python -m venv .venv
fi

if [[ -f .venv/Scripts/python.exe ]]; then
  VENV_PY="${SCRIPT_DIR}/.venv/Scripts/python.exe"
else
  VENV_PY="${SCRIPT_DIR}/.venv/bin/python"
fi

"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements_optimized.txt
