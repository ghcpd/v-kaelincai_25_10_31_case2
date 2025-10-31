#!/usr/bin/env bash
set -e
bash Project_A_Faulty/run_original.sh || echo "Faulty project completed with expected regressions"
bash Project_B_Optimized/run_optimized.sh
python - <<'EOF'
import json, re, os, pathlib
root = pathlib.Path('.')
orig = root/'Project_A_Faulty'
opt = root/'Project_B_Optimized'
report_path = root/'compare_report.md'
# Load JSON results if present
ro = []
if (orig/'results_original.json').exists():
    ro = json.load(open(orig/'results_original.json','r',encoding='utf-8'))
rn = []
if (opt/'results_optimized.json').exists():
    rn = json.load(open(opt/'results_optimized.json','r',encoding='utf-8'))
# Timing files
def parse_time(p):
    if not p.exists():
        return None
    text = p.read_text(encoding='utf-8')
    m_total = re.search(r'Total_time_seconds=(\d+\.\d+)', text)
    m_avg = re.search(r'Avg_time_per_run=(\d+\.\d+)', text)
    return {
        'total': float(m_total.group(1)) if m_total else None,
        'avg': float(m_avg.group(1)) if m_avg else None
    }
orig_t = parse_time(orig/'time_original.txt') or {}
opt_t = parse_time(opt/'time_optimized.txt') or {}
# Compute metrics
orig_pass = sum(1 for r in ro if r['passed'])
opt_pass = sum(1 for r in rn if r['passed'])
orig_total = len(ro)
opt_total = len(rn)
accuracy_improvement = (opt_pass/opt_total - orig_pass/max(1,orig_total)) if opt_total else 0
perf_improvement = None
if orig_t.get('avg') and opt_t.get('avg'):
    perf_improvement = (orig_t['avg'] - opt_t['avg']) / orig_t['avg']
lines = []
lines.append('# Comparison Report')
lines.append('')
lines.append('## Summary Table')
lines.append('| Metric | Faulty | Optimized | Improvement |')
lines.append('|--------|--------|-----------|-------------|')
lines.append(f"| Test cases | {orig_total} | {opt_total} | - |")
lines.append(f"| Pass count | {orig_pass} | {opt_pass} | {opt_pass - orig_pass} |")
lines.append(f"| Pass rate | {orig_pass/max(1,orig_total):.2%} | {opt_pass/max(1,opt_total):.2%} | {accuracy_improvement:.2%} |")
if perf_improvement is not None:
    lines.append(f"| Avg time per run | {orig_t['avg']:.6f}s | {opt_t['avg']:.6f}s | {perf_improvement:.2%} faster |")
report_path.write_text('\n'.join(lines),'utf-8')
print('Generated compare_report.md')
EOF
echo "All runs complete. See compare_report.md"
