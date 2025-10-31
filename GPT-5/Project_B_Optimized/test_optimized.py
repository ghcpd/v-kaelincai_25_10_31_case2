"""Test harness for optimized implementation.
All cases should succeed (expected_success_post True).
Outputs JSON summary 'results_optimized.json'.
"""
import json, time, random
from pathlib import Path
from optimized_code import analyze_numbers

ROOT = Path(__file__).parent

def load_cases():
    with open(ROOT / 'test_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def materialize_input(inp):
    if isinstance(inp, dict) and 'generate_large_random' in inp:
        spec = inp['generate_large_random']
        size = spec.get('size', 1000)
        seed = spec.get('seed', 0)
        rnd = random.Random(seed)
        return [rnd.randint(-1000, 1000) for _ in range(size)]
    return inp


def run():
    cases = load_cases()
    results = []
    for case in cases:
        cid = case['id']
        expected = case['expected_output']
        raw_inp = materialize_input(case['input'])
        start = time.time()
        got = analyze_numbers(raw_inp)
        duration = time.time() - start
        # Large random dataset expected_output has approximate markers
        if expected['sum'] == 'approximate':
            # For performance test just validate count consistency
            passed = got['count'] == expected['count']
        else:
            passed = got == expected
        results.append({
            'id': cid,
            'description': case['description'],
            'expected_success_post': case['expected_success_post'],
            'passed': passed,
            'expected': expected,
            'got': got,
            'time': duration
        })
        status = 'PASS' if passed else 'FAIL'
        print(f"[Case {cid}] {status} got={got} expected={expected}")
    with open(ROOT / 'results_optimized.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    print(f"SUMMARY: {passed}/{total} tests passed.")

if __name__ == '__main__':
    run()
