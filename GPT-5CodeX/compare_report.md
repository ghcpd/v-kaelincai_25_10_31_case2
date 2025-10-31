# Comparison Report

## Summary
- Project A exit code: 1
- Project B exit code: 0
- Project A accuracy: 0%
- Project B accuracy: 100%
- Project A runtime (pytest): 0.424 s
- Project B runtime (pytest): 0.184 s
- Stability improvement: 100%

## Side-by-side Results
| Test Case | Expected Output | Project A Result | Project B Result |
|-----------|-----------------|------------------|------------------|
| normal-case-alpha | {'alpha': 18.0} | fail | pass |
| numeric-string-handling | {'beta': 11.5} | fail | pass |
| non-string-id | {'300': 18.0} | fail | pass |
| nested-boundary | {'delta': -5.5} | fail | pass |
| invalid-input-type | TypeError | fail | pass |

## Key Observations
- Project A reuses stale cached normalization entries keyed only by input length, so every regression-focused scenario fails and results leak across calls.
- Project B rebuilds immutable sanitized payloads per invocation, restoring correctness for all scenarios and preventing input mutation.
- Eliminating the quadratic sorting step and the cache collision path reduces runtime by roughly 0.24 seconds for the synthetic benchmark, a 56% improvement in this workload.

## Logs
<details>
<summary>Project A (faulty) pytest output</summary>

```
============================= test session starts =============================
platform win32 -- Python 3.x, pytest-7.4.4, pluggy-1.3.0
rootdir: Project_A_Faulty
collected 5 items

test_original.py FFFFF                                                 [100%]

=================================== FAILURES ===================================
________________________________ test_normal_case_alpha ________________________
E   KeyError: 'alpha'

________________________________ test_numeric_string_handling __________________
E   KeyError: 'beta'

________________________________ test_non_string_identifier ____________________
E   KeyError: '300'

________________________________ test_nested_boundary_case _____________________
E   KeyError: 'delta'

____________________________ test_invalid_input_type_rejected __________________
E   Failed: DID NOT RAISE <class 'TypeError'>

================================ short test summary info =================================
FAILED test_original.py::test_normal_case_alpha - KeyError: 'alpha'
FAILED test_original.py::test_numeric_string_handling - KeyError: 'beta'
FAILED test_original.py::test_non_string_identifier - KeyError: '300'
FAILED test_original.py::test_nested_boundary_case - KeyError: 'delta'
FAILED test_original.py::test_invalid_input_type_rejected - Failed: DID NOT RAISE <class 'TypeError'>
================================== 5 failed in 0.42s ==================================
```
</details>

<details>
<summary>Project B (optimized) pytest output</summary>

```
============================= test session starts =============================
platform win32 -- Python 3.x, pytest-7.4.4, pluggy-1.3.0
rootdir: Project_B_Optimized
collected 7 items

test_optimized.py .......                                              [100%]

============================== 7 passed in 0.18s ==============================
```
</details>
