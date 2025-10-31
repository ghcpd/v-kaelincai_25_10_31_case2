"""Test harness for faulty implementation.
For cases where expected_success_pre is False we assert inequality to highlight regression presence.
Outputs a JSON summary 'results_original.json'.
"""
import json, time, random
from pathlib import Path
from original_code import analyze_numbers

ROOT = Path(__file__).parent

def load_cases():
    with open(ROOT / 'test_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def materialize_input(inp):
    # For large random generation
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
        error = None
        try:
            got = analyze_numbers(raw_inp)
        except Exception as e:  # capture regression-caused crashes
            got = None
            error = f"Exception: {type(e).__name__}: {e}"
        duration = time.time() - start
        # Determine pass condition for faulty version
        if case['expected_success_pre']:
            passed = (error is None and got == expected)
        else:
            # We expect mismatch OR an exception to reveal regression
            passed = (error is not None) or (got != expected)
        results.append({
            'id': cid,
            'description': case['description'],
            'expected_success_pre': case['expected_success_pre'],
            'passed': passed,
            'expected': expected,
            'got': got,
            'error': error,
            'time': duration
        })
        status = 'PASS' if passed else 'FAIL'
        print(f"[Case {cid}] {status} - expected_success_pre={case['expected_success_pre']} got={got} expected={expected} error={error}")
    with open(ROOT / 'results_original.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    # Aggregate summary
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    print(f"SUMMARY: {passed}/{total} conditions met for regression expectations.")

if __name__ == '__main__':
    run()
