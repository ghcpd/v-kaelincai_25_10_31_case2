# Comparison Report

Evaluation of GPT-5-Codex, GPT-5, Claude Sonnet 4.5, S100, and S40 on Bug-related – Regression Detection, Mitigation, and Optimization

## Summary Table

| Project | Passed | Failed | Accuracy | Error Rate | Elapsed (s) | Exit Code |
|---------|--------|--------|----------|------------|-------------|-----------|
| Project A – Pre-Optimization | 0 | 5 | 0.00% | 100.00% | n/a | 1 |
| Project B – Post-Optimization | 6 | 0 | 100.00% | 0.00% | n/a | 0 |

## Key Observations

* Accuracy improvement after optimisation: 100.00%.
* Performance gain could not be computed (missing timing data).

## Detailed Summaries

### Project A – Pre-Optimization

Summary line: 5 failed in 0.08s

Log excerpt:

```
﻿FFFFF                                                                    [100%]
================================== FAILURES ===================================
________________________ test_null_entries_are_ignored ________________________

    def test_null_entries_are_ignored():
        payload = {
            "metrics": [1.0, None, 3.0, {"shadow": [2.0, None]}]
        }
>       result = module.compute_stability_index(payload)

test_original.py:23: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

payload = {'metrics': [1.0, None, 3.0, {'shadow': [2.0, None]}]}

    def compute_stability_index(payload: Any, *, minimum: float = 0.0) -> float:
        """Compute a pseudo "stability" index from nested payload readings.
    
        The regression-causing behaviour lives here: the function caches the last
        result by ``id(payload)``. Mutating a dictionary in-place retains the same
        object identity, meaning a fresh computation is skipped even though the
        data changed. Additionally, ``None`` values now raise ``ValueError`` during
        coercion to ``float``.
        """
    
        global _last_signature, _last_result
    
        signature = id(payload)
        if _last_signature == signature and _last_result is not None:
            return _last_result
    
        total = 0.0
        count = 0
    
        for item in _iter_nested(payload):
            if item is None:
>               raise ValueError("Null reading encountered; aborting computation")
E               ValueError: Null reading encountered; aborting computation

original_code.py:69: ValueError
```

### Project B – Post-Optimization

Summary line: 6 passed in 0.06s

Log excerpt:

```
﻿......                                                                   [100%]
6 passed in 0.06s

```

## Optimisation Highlights

1. Eliminated identity-based caching that masked in-place mutations by hashing the sanitised numeric stream.
2. Replaced recursive traversal with iterative breadth-first processing to mitigate deep nesting and stack overflows.
3. Hardened input sanitisation to ignore malformed data (nulls, booleans, arbitrary strings), preventing ValueError regressions and data poisoning vectors.
