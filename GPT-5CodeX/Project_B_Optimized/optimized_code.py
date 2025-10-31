"""Optimized and regression-free implementation of the metric aggregator.

Key fixes over the faulty baseline:
- Stable, content-aware normalization with fresh immutable structures per call
  eliminates stale-cache collisions and input mutation.
- Strict input validation rejects malformed iterables early, restoring the
  previously guaranteed TypeError for unsafe inputs.
- Recursive sanitisation now copies data, skips invalid metrics when allowed,
  and keeps critical context for precise error messages when validation fails.
- Numerical parsing is guarded and avoids repeated sorting by walking the data
  once, improving large-input performance.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Sequence, Tuple, Union

Number = Union[int, float]


@dataclass(frozen=True)
class SanitizedMetric:
    name: str
    weight: float
    value: Optional[float] = None
    children: Optional[Tuple["SanitizedMetric", ...]] = None

    def is_leaf(self) -> bool:
        return self.children is None


class RegressionAnalyzer:
    """Aggregate nested metric definitions into per-record totals."""

    def aggregate_scores(
        self, records: Iterable[Mapping[str, object]], *, drop_invalid: bool = True
    ) -> dict[str, float]:
        normalized_records = self._prepare_records(records, drop_invalid)
        results: dict[str, float] = {}
        for record_id, metrics in normalized_records:
            total = sum(self._metric_contribution(metric) for metric in metrics)
            results[str(record_id)] = round(total, 6)
        return results

    def _prepare_records(
        self,
        records: Iterable[Mapping[str, object]],
        drop_invalid: bool,
    ) -> Tuple[Tuple[object, Tuple[SanitizedMetric, ...]], ...]:
        if isinstance(records, Mapping):
            raise TypeError("records must be an iterable of mapping objects")
        if isinstance(records, (str, bytes)):
            raise TypeError("records must not be a string")

        if isinstance(records, Sequence):
            iterable = records
        else:
            iterable = list(records)

        prepared = []
        for index, record in enumerate(iterable):
            if not isinstance(record, Mapping):
                raise TypeError(f"record at position {index} is not a mapping")
            record_id = record.get("id")
            metrics = record.get("metrics") or []
            sanitized = self._sanitize_metrics(metrics, drop_invalid, lineage=(str(record_id),))
            prepared.append((record_id, tuple(sanitized)))
        return tuple(prepared)

    def _sanitize_metrics(
        self,
        metrics: Iterable[Mapping[str, object]],
        drop_invalid: bool,
        *,
        lineage: Tuple[str, ...],
    ) -> Tuple[SanitizedMetric, ...]:
        sanitized: list[SanitizedMetric] = []
        for position, raw_metric in enumerate(metrics):
            metric = self._sanitize_single_metric(
                raw_metric, drop_invalid, lineage=lineage + (f"metric[{position}]",)
            )
            if metric is not None:
                sanitized.append(metric)
        return tuple(sanitized)

    def _sanitize_single_metric(
        self,
        metric: Mapping[str, object],
        drop_invalid: bool,
        *,
        lineage: Tuple[str, ...],
    ) -> Optional[SanitizedMetric]:
        if not isinstance(metric, Mapping):
            if drop_invalid:
                return None
            raise ValueError(f"{'.'.join(lineage)} must be a mapping")

        if metric.get("enabled", True) is False:
            return None

        name = str(metric.get("name", "")) or ".".join(lineage)
        try:
            weight = float(metric.get("weight", 1.0))
        except (TypeError, ValueError):
            if drop_invalid:
                return None
            raise ValueError(f"{'.'.join(lineage)} has non-numeric weight")

        submetrics = metric.get("submetrics")
        if submetrics is not None:
            if isinstance(submetrics, (str, bytes)) or not isinstance(submetrics, Iterable):
                if drop_invalid:
                    return None
                raise ValueError(f"{'.'.join(lineage)}.submetrics must be an iterable")
            children: list[SanitizedMetric] = []
            for position, child in enumerate(submetrics):
                normalized_child = self._sanitize_single_metric(
                    child,
                    drop_invalid,
                    lineage=lineage + (f"sub[{position}]",),
                )
                if normalized_child is not None:
                    children.append(normalized_child)
            if not children and drop_invalid:
                return None
            return SanitizedMetric(name=name, weight=weight, children=tuple(children))

        if "value" not in metric:
            if drop_invalid:
                return None
            raise ValueError(f"{'.'.join(lineage)} missing value")

        value = metric.get("value")
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            if drop_invalid:
                return None
            raise ValueError(f"{'.'.join(lineage)} value is not numeric")

        return SanitizedMetric(name=name, weight=weight, value=numeric_value)

    def _metric_contribution(self, metric: SanitizedMetric) -> float:
        if metric.children:
            subtotal = sum(self._metric_contribution(child) for child in metric.children)
            return subtotal * metric.weight
        assert metric.value is not None
        return metric.value * metric.weight


def load_records(path: str) -> list[dict[str, object]]:
    import json
    from pathlib import Path

    return json.loads(Path(path).read_text(encoding="utf-8"))
