#!/usr/bin/env bash
set -e
python -m venv .venv_optimized
source .venv_optimized/Scripts/activate || source .venv_optimized/bin/activate
pip install -r requirements_optimized.txt
python test_optimized.py | tee log_optimized.txt
python - <<'EOF' > time_optimized.txt
import time, random
from optimized_code import analyze_numbers
rnd = random.Random(42)
large = [rnd.randint(-1000, 1000) for _ in range(5000)]
start = time.time()
for _ in range(10):
    analyze_numbers(large)
elapsed = time.time() - start
print(f"Total_time_seconds={elapsed:.6f}")
print(f"Avg_time_per_run={(elapsed/10):.6f}")
EOF
echo "Optimized run complete. Logs: log_optimized.txt Timing: time_optimized.txt"
