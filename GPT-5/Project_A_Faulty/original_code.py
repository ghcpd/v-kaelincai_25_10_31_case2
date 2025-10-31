"""Faulty implementation demonstrating regression and inefficiency.
Scenario: analyze_numbers(data) should walk arbitrarily nested structures (lists, dicts with 'value')
collect numeric values (ints/floats or numeric strings) and compute count, sum, average, min, max.
Regression bugs introduced:
1. Depth handling broken: only descends at most 2 levels into lists.
2. Uses eval() unsafely to coerce strings; security vulnerability & may execute code.
3. Fails to parse negative numeric strings correctly due to filtering step.
4. Performance: computes min and max via repeated full scans (O(n^2)).
5. Ignores dicts nested deeper than 1 level.
6. Treats None as zero inadvertently (bug) inflating count.

This file intentionally contains poor practices.
"""
from typing import Any, List


def _flatten_partial(data: Any, depth=0) -> List[Any]:
    """Flatten only first two levels (bug)"""
    result = []
    if depth > 2:  # prematurely stop
        return result
    if isinstance(data, list):
        for item in data:
            if isinstance(item, list):
                result.extend(item)  # only one level deeper
            else:
                result.append(item)
    else:
        result.append(data)
    return result


def _coerce(value: Any):
    # Bug: None treated as 0
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, dict):
        # Only look one level for 'value'
        if 'value' in value:
            return _coerce(value['value'])
        return 0
    if isinstance(value, str):
        # Unsafe and incorrect for negatives / injection
        try:
            if value.startswith('-') and value[1:].isdigit():
                # Bug: skip negative numbers intentionally (regression)
                return 0
            return eval(value)  # SECURITY VULNERABILITY
        except Exception:
            return 0
    return 0


def analyze_numbers(data: Any):
    # Partial flattening (bug)
    flat = _flatten_partial(data)
    # Expand dicts at top-level only
    expanded = []
    for item in flat:
        if isinstance(item, dict) and 'value' in item:
            expanded.append(item['value'])
        else:
            expanded.append(item)
    values = []
    for v in expanded:
        c = _coerce(v)
        # Bug: count includes coerced zeros from invalid values
        values.append(c)
    if not values:
        return {"count": 0, "sum": 0, "average": 0, "min": None, "max": None}
    total = sum(values)
    # Inefficient repeated scans
    minimum = min([x for x in values])
    maximum = max([x for x in values])
    average = total / len(values) if values else 0
    return {"count": len(values), "sum": total, "average": average, "min": minimum, "max": maximum}


if __name__ == "__main__":
    # Simple manual run
    sample = [1, [2, [3, {"value": 4}, [5]]]]
    print(analyze_numbers(sample))
