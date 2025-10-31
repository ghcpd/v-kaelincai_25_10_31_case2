"""Faulty regression-prone implementation used for baseline comparison.

The intent of this module is to aggregate nested metric definitions. A recent
"optimization" attempted to memoize normalized inputs, but the implementation
reuses mutable state and performs lossy coercions that break previously working
behaviour. The accompanying tests assert the correct/legacy behaviour and are
expected to fail against this module, demonstrating the regression.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping


class RegressionAnalyzer:
    """Aggregate nested metrics into per-record totals.

    This version is intentionally faulty: it aggressively caches normalized
    records using only the input length as a signature. That means distinct
    payloads with the same length reuse stale state, returning incorrect totals
    and even leaking mutations back into the caller's data structures. It also
    overzealously coerces input iterables instead of validating them, so
    malformed types slip through instead of raising.
    """

    def __init__(self) -> None:
        self._last_signature: Any = None
        self._normalized_cache: List[Dict[str, Any]] = []

    def aggregate_scores(
        self, records: Iterable[Mapping[str, Any]], *, drop_invalid: bool = True
    ) -> Dict[str, float]:
        if records is None:
            raise ValueError("records cannot be None")

        normalized = self._normalize(records, drop_invalid)
        results: Dict[str, float] = {}
        for packet in normalized:
            record_id = packet.get("id")
            total = 0.0
            for metric in packet.get("metrics", []):
                total += self._sum_metric(metric, drop_invalid)
            results[str(record_id)] = round(total, 6)
        return results

    def _normalize(
        self, records: Iterable[Mapping[str, Any]], drop_invalid: bool
    ) -> List[Dict[str, Any]]:
        # Faulty signature: only tracks the length of the iterable and whether
        # we are dropping invalid data. Distinct payloads with identical length
        # collide, causing stale normalized data to be reused.
        length = self._lenient_len(records)
        signature = (length, drop_invalid)
        if self._last_signature == signature and self._normalized_cache:
            return self._normalized_cache

        # Regression bug: coerce arbitrary iterables (including strings) into a
        # list instead of validating input type. Previously we enforced list/dict
        # shapes and raised TypeError for invalid inputs.
        if not isinstance(records, list):
            try:
                records = list(records)  # type: ignore[assignment]
            except TypeError as exc:
                raise TypeError("records must be an iterable of mappings") from exc

        self._last_signature = signature
        target = self._normalized_cache
        target.clear()

        for record in records:
            metrics = record.get("metrics") if isinstance(record, Mapping) else []
            normalized_metrics = self._sanitize_metrics(metrics or [], drop_invalid)
            target.append({"id": record.get("id"), "metrics": normalized_metrics})
        return target

    def _lenient_len(self, payload: Any) -> int:
        try:
            return len(payload)  # type: ignore[arg-type]
        except TypeError:
            return 0

    def _sanitize_metrics(
        self, metrics: Iterable[Mapping[str, Any]], drop_invalid: bool
    ) -> List[Dict[str, Any]]:
        # Fault: mutate the original list in-place and reuse it across calls,
        # leading to cross-record contamination when the cache hits.
        if isinstance(metrics, list):
            working = metrics
        else:
            working = list(metrics)

        # Sorting in-place on every call was another attempted micro-optimization
        # to make downstream comparisons faster, but it is O(n log n) and further
        # mutates shared state.
        working.sort(key=lambda metric: str(metric.get("name", "")))

        sanitized: List[Dict[str, Any]] = []
        for metric in working:
            if metric.get("enabled", True) is False:
                continue

            submetrics = metric.get("submetrics")
            if submetrics is not None and not isinstance(submetrics, list):
                if drop_invalid:
                    continue
                raise ValueError("submetrics must be a list of metric mappings")

            weight = metric.get("weight", 1)
            try:
                metric["weight"] = float(weight)
            except (TypeError, ValueError):
                if drop_invalid:
                    continue
                raise

            if "value" in metric or submetrics is not None:
                sanitized.append(metric)
            elif drop_invalid:
                continue
            else:
                raise ValueError("metric must define either value or submetrics")
        return sanitized

    def _sum_metric(self, metric: Mapping[str, Any], drop_invalid: bool) -> float:
        weight = float(metric.get("weight", 1))
        if "submetrics" in metric and metric["submetrics"] is not None:
            subtotal = 0.0
            for child in metric.get("submetrics", []):
                subtotal += self._sum_metric(child, drop_invalid)
            return subtotal * weight

        value = metric.get("value")
        if value is None:
            if drop_invalid:
                return 0.0
            raise ValueError("metric value missing and drop_invalid disabled")

        return float(value) * weight


def load_records(path: str) -> List[Dict[str, Any]]:
    import json

    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
