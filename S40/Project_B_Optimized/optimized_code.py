"""Optimised and regression-free implementation.

Key improvements over ``original_code``:

* Iterative breadth-first traversal prevents runaway recursion and honours
  deterministic ordering for caching and reproducibility.
* Numeric extraction skips ``None``, booleans, and unsafe textual values, while
  still parsing well-formed numeric strings.
* Content-aware caching hashes the extracted numeric signature rather than the
  input object's identity, eliminating stale outcomes after in-place
  mutations.
"""

from __future__ import annotations

from collections import deque
import hashlib
from typing import Any, Deque, Iterable, List

_structural_cache: dict[str, float] = {}


def clear_cache() -> None:
    """Clear memoised results so tests start from a clean slate."""

    _structural_cache.clear()


def compute_stability_index(payload: Any, *, minimum: float = 0.0) -> float:
    """Compute a stability index from arbitrarily nested payloads.

    ``payload`` may contain nested dictionaries, sequences, and scalar values.
    Numerics (including numeric strings) contribute to the result. ``None``,
    booleans, and malformed strings are ignored. The computation is stable
    against input mutation because caching uses a structural signature derived
    from the sanitised numeric stream instead of ``id(payload)``.
    """

    numbers, signature = _harvest_numbers(payload)

    if not numbers:
        return 0.0

    cached = _structural_cache.get(signature)
    if cached is not None:
        return cached

    total = sum(numbers)
    average = total / len(numbers)

    if average < minimum:
        average = 0.0

    _structural_cache[signature] = average
    return average


def load_payload(path: str) -> Any:
    """Load nested input data from JSON for convenience in tests."""

    import json

    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _sorted_iterable(items: Iterable[Any]) -> Iterable[Any]:
    try:
        return sorted(items, key=_sort_key)
    except TypeError:
        # ``items`` may contain unorderable values (e.g. dict + list). Fallback
        # to insertion order which is good enough for stable hashing.
        return list(items)


def _sort_key(value: Any) -> tuple[str, str]:
    return (type(value).__name__, repr(value))


def _harvest_numbers(payload: Any) -> tuple[List[float], str]:
    queue: Deque[Any] = deque([payload])
    numbers: List[float] = []
    signature_parts: List[str] = []

    while queue:
        node = queue.popleft()

        if isinstance(node, dict):
            for key in sorted(node.keys()):
                queue.append(node[key])
            continue

        if isinstance(node, (list, tuple, set)):
            queue.extend(_sorted_iterable(node))
            continue

        if node is None or isinstance(node, bool):
            continue

        if isinstance(node, (int, float)):
            value = float(node)
            numbers.append(value)
            signature_parts.append(f"n:{value:.12f}")
            continue

        if isinstance(node, str):
            cleaned = node.strip()
            if not cleaned:
                continue
            try:
                value = float(cleaned)
            except ValueError:
                continue
            numbers.append(value)
            signature_parts.append(f"s:{value:.12f}")
            continue

        # Ignore any other payload types such as complex objects.

    signature = hashlib.sha256("|".join(signature_parts).encode("utf-8")).hexdigest()
    return numbers, signature
