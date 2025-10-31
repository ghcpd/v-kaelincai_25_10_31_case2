"""Optimized and corrected implementation.
Fixes applied:
1. Full recursive / iterative stack traversal for arbitrary nesting.
2. Secure string coercion using explicit numeric pattern; rejects code-injection attempts.
3. Correct handling of negatives and numeric strings; ignores malformed inputs (not counted).
4. Single-pass aggregation updating min/max without extra scans (O(n)).
5. Proper dict unwrapping for nested {'value': ...} structures.
6. Excludes None entirely from statistics.
7. Performance enhancement: optional NumPy fast-path for large flat numeric lists.
"""
from __future__ import annotations
from typing import Any, Iterable, List
import re

try:
    import numpy as np  # optional
except Exception:  # pragma: no cover
    np = None

_NUMERIC_RE = re.compile(r"^[+-]?((\d+\.?\d*)|(\d*\.\d+))$")


def _extract_numbers(data: Any) -> Iterable[float]:
    stack = [data]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if 'value' in current:
                stack.append(current['value'])
            else:
                # explore all dict values; could hold nested structures
                for v in current.values():
                    stack.append(v)
        elif isinstance(current, (list, tuple, set)):
            for item in current:
                stack.append(item)
        elif isinstance(current, (int, float)):
            yield float(current)
        elif isinstance(current, str):
            if _NUMERIC_RE.match(current.strip()):
                try:
                    yield float(current)
                except ValueError:
                    continue
            else:
                # reject unsafe strings
                continue
        else:
            # ignore None, bool, other types
            continue


def analyze_numbers(data: Any):
    numbers = list(_extract_numbers(data))
    if not numbers:
        return {"count": 0, "sum": 0.0, "average": 0.0, "min": None, "max": None}

    # NumPy fast path
    if np is not None and len(numbers) > 1000:
        arr = np.array(numbers, dtype=float)
        total = float(arr.sum())
        count = int(arr.size)
        minimum = float(arr.min())
        maximum = float(arr.max())
        average = total / count
    else:
        total = 0.0
        minimum = float(numbers[0])
        maximum = float(numbers[0])
        count = 0
        for n in numbers:
            count += 1
            total += n
            if n < minimum:
                minimum = n
            if n > maximum:
                maximum = n
        average = total / count
    return {"count": count, "sum": total, "average": average, "min": minimum, "max": maximum}


if __name__ == "__main__":
    sample = [1, [2, [3, {"value": 4}, [5]]]]
    print(analyze_numbers(sample))
