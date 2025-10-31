#!/usr/bin/env bash
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

bash "$SCRIPT_DIR/setup_original.sh"

if [[ -f .venv/Scripts/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/Scripts/activate
elif [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python - <<'PY'
import pathlib
import subprocess
import sys
import time

root = pathlib.Path(__file__).resolve().parent
log_path = root / "log_original.txt"
time_path = root / "time_original.txt"

command = [sys.executable, "-m", "pytest", "test_original.py", "--disable-warnings", "-q"]

start = time.perf_counter()
proc = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
elapsed = time.perf_counter() - start

log_path.write_text(proc.stdout)
time_path.write_text(f"elapsed_seconds={elapsed:.6f}\nexit_code={proc.returncode}\n", encoding="utf-8")

sys.exit(proc.returncode)
PY
