#!/usr/bin/env bash
set +e  # allow test script to continue even if expectations produce 'fail'
python -m venv .venv_original
source .venv_original/Scripts/activate || source .venv_original/bin/activate
pip install -r requirements_original.txt
python test_original.py | tee log_original.txt
# Performance timing on large random dataset
python - <<'EOF' > time_original.txt
import time, random
from original_code import analyze_numbers
rnd = random.Random(42)
large = [rnd.randint(-1000, 1000) for _ in range(5000)]
start = time.time()
for _ in range(10):
    analyze_numbers(large)
elapsed = time.time() - start
print(f"Total_time_seconds={elapsed:.6f}")
print(f"Avg_time_per_run={(elapsed/10):.6f}")
EOF
echo "Faulty run complete. Logs: log_original.txt Timing: time_original.txt"
