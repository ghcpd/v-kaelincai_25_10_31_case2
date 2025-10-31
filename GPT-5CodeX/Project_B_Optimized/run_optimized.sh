#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

./setup_optimized.sh
source .venv/Scripts/activate

python - <<'PY'
import io
import pathlib
import sys
import time
from contextlib import redirect_stdout, redirect_stderr

import pytest

log_path = pathlib.Path("log_optimized.txt")
time_path = pathlib.Path("time_optimized.txt")

buffer = io.StringIO()
start = time.perf_counter()
with redirect_stdout(buffer), redirect_stderr(buffer):
    exit_code = pytest.main(["-q", "test_optimized.py"])
elapsed = time.perf_counter() - start

log_path.write_text(buffer.getvalue(), encoding="utf-8")
time_path.write_text(
    f"elapsed_seconds: {elapsed:.6f}\nexit_code: {exit_code}\n",
    encoding="utf-8",
)

sys.exit(exit_code)
PY
