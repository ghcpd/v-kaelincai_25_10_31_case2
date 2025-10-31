"""Faulty regression-prone implementation.

This module intentionally contains a regression introduced during an attempted
micro-optimization. The regression manifests in two major ways:

1. A global cache keyed by ``id(payload)`` returns stale results when the
   caller mutates the data structure between invocations. The cache was
   bolted on to avoid re-traversing nested structures but now hides real data
   updates.
2. Sanitisation of optional readings was replaced with a hard failure. ``None``
   values and nested non-numeric entries previously got ignored; the new
   behaviour raises ``ValueError`` and halts processing, which breaks callers
   that legitimately send sparse payloads.

The accompanying tests describe the expected behaviour that used to work prior
to the regression. They now fail against this implementation.
"""

from __future__ import annotations

from typing import Any, Iterable

_last_signature: int | None = None
_last_result: float | None = None


def _iter_nested(node: Any) -> Iterable[Any]:
    """Yield every leaf value found inside ``node``.

    This helper is intentionally over-permissive; it attempts to coerce nearly
    any container type into the traversal in order to milk as much reuse as
    possible from a single implementation. Unfortunately, it also walks across
    strings character by character and does not guard against deep recursion.
    Those issues are outside the scope of this specific regression but add to
    the fragility of the module.
    """

    if isinstance(node, dict):
        for value in node.values():
            yield from _iter_nested(value)
    elif isinstance(node, (list, tuple, set)):
        for value in node:
            yield from _iter_nested(value)
    else:
        yield node


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
            raise ValueError("Null reading encountered; aborting computation")
        total += float(item)
        count += 1

    average = total / count if count else 0.0

    if average < minimum:
        average = 0.0

    _last_signature = signature
    _last_result = average
    return average


def clear_cache() -> None:
    """Reset the global cache used by :func:`compute_stability_index`."""

    global _last_signature, _last_result
    _last_signature = None
    _last_result = None


def load_payload(path: str) -> Any:
    """Load nested input data from JSON."""

    import json

    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
