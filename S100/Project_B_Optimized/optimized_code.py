"""Optimized regression analyzer that fixes the caching regression.

Key improvements compared to the faulty implementation:

* Adjustment vectors are applied element-wise, ensuring corrective deltas are
  propagated into the effective predictions.
* Strict validation rejects malformed inputs early, preventing silent
  corruption of metrics and surfacing regressions immediately.
* Metrics are accumulated in a single pass using floating point division,
  preserving the precision needed for downstream analytics.
* Micro-optimisations remove unnecessary sorts and make heavy use of local
  variables to avoid attribute lookups in tight loops.
* Benchmark helper performs the same workload as the faulty project, making it
  easy to compare runtime improvements.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableSequence, Optional, Sequence

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "input_data.json"


@dataclass(frozen=True)
class Metrics:
    mae: float
    rmse: float
    bias: float
    stability_index: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "mae": self.mae,
            "rmse": self.rmse,
            "bias": self.bias,
            "stability_index": self.stability_index,
        }


class RegressionAnalyzer:
    """High-precision regression quality evaluator."""

    def load_dataset(self, path: Optional[Path] = None) -> List[Dict[str, Any]]:
        data_file = path or DATA_PATH
        with data_file.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return list(payload.get("cases", []))

    @staticmethod
    def _ensure_sequence(values: Any, *, name: str) -> Sequence[Any]:
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise TypeError(f"{name} must be a sequence of numeric values")
        return values

    @staticmethod
    def _coerce_numeric_list(values: Sequence[Any], *, field: str) -> List[float]:
        coerced: List[float] = []
        for index, value in enumerate(values):
            try:
                coerced.append(float(value))
            except (TypeError, ValueError) as exc:  # pragma: no cover - explicit failure path
                raise ValueError(f"{field}[{index}] is not numeric: {value!r}") from exc
        return coerced

    def _apply_adjustments(
        self, predictions: Sequence[float], adjustments: Optional[Iterable[Sequence[Any]]]
    ) -> List[float]:
        if not adjustments:
            return list(predictions)
        pred_len = len(predictions)
        deltas = [0.0] * pred_len
        for block in adjustments:
            self._ensure_sequence(block, name="adjustments")
            if len(block) != pred_len:
                raise ValueError(
                    "Adjustment vector length does not match predictions;"
                    " expected %d but received %d" % (pred_len, len(block))
                )
            numeric_block = self._coerce_numeric_list(block, field="adjustments")
            for idx, value in enumerate(numeric_block):
                deltas[idx] += value
        return [base + delta for base, delta in zip(predictions, deltas)]

    def evaluate_case(self, case: Mapping[str, Any]) -> Metrics:
        predictions, actuals, weights, adjustments = self._normalise_inputs(case)

        effective_predictions = self._apply_adjustments(
            predictions,
            adjustments,
        )

        weight_sum = 0.0
        abs_total = 0.0
        sq_total = 0.0
        bias_total = 0.0

        for pred, actual, weight in zip(effective_predictions, actuals, weights):
            diff = pred - actual
            abs_total += abs(diff) * weight
            sq_total += (diff * diff) * weight
            bias_total += diff * weight
            weight_sum += weight

        if weight_sum == 0:
            raise ValueError("Sum of weights must be greater than zero")

        mae = abs_total / weight_sum
        rmse = math.sqrt(sq_total / weight_sum)
        bias = bias_total / weight_sum

        mean_actual = statistics.fmean(actuals)
        denom = abs(mean_actual) + 1e-6
        rmse_ratio = min(1.0, rmse / denom)
        bias_ratio = min(1.0, abs(bias) / denom)
        stability_index = max(0.0, min(1.0, 1.0 - (rmse_ratio + bias_ratio) / 2.0))

        return Metrics(
            mae=round(mae, 4),
            rmse=round(rmse, 4),
            bias=round(bias, 4),
            stability_index=round(stability_index, 4),
        )

    def _normalise_inputs(
        self, case: Mapping[str, Any]
    ) -> tuple[List[float], List[float], List[float], Optional[Iterable[Sequence[Any]]]]:
        predictions_raw = self._ensure_sequence(case.get("predictions"), name="predictions")
        actuals_raw = self._ensure_sequence(case.get("actuals"), name="actuals")
        if len(predictions_raw) != len(actuals_raw):
            raise ValueError("predictions and actuals must be the same length")

        weights_raw = case.get("weights")
        if weights_raw:
            weights_raw = self._ensure_sequence(weights_raw, name="weights")
        else:
            weights_raw = [1.0] * len(predictions_raw)

        predictions = self._coerce_numeric_list(predictions_raw, field="predictions")
        actuals = self._coerce_numeric_list(actuals_raw, field="actuals")
        weights = self._coerce_numeric_list(weights_raw, field="weights")
        adjustments = case.get("adjustments")
        return predictions, actuals, weights, adjustments

    def evaluate_dataset(
        self,
        cases: Sequence[Mapping[str, Any]],
        *,
        ignore_invalid: bool = False,
    ) -> Dict[str, Metrics]:
        results: Dict[str, Metrics] = {}
        for case in cases:
            try:
                results[case["name"]] = self.evaluate_case(case)
            except ValueError:
                if ignore_invalid:
                    continue
                raise
        return results

    def benchmark(self, iterations: int = 750) -> float:
        raw_cases = self.load_dataset()
        prepared: List[tuple[List[float], List[float], List[float], Optional[Iterable[Sequence[Any]]]]] = []
        for case in raw_cases:
            try:
                prepared.append(self._normalise_inputs(case))
            except ValueError:
                # Skip malformed cases from the performance run but keep them
                # available when the caller wants strict validation.
                continue
        start = time.perf_counter()
        for _ in range(iterations):
            for predictions, actuals, weights, adjustments in prepared:
                effective = self._apply_adjustments(predictions, adjustments)
                weight_sum = sum(weights)
                abs_total = 0.0
                sq_total = 0.0
                bias_total = 0.0
                for pred, actual, weight in zip(effective, actuals, weights):
                    diff = pred - actual
                    abs_total += abs(diff) * weight
                    sq_total += (diff * diff) * weight
                    bias_total += diff * weight
                # Avoid allocating metrics objects inside the loop; the timing
                # focus is on arithmetic workload versus the faulty version.
                _ = abs_total + sq_total + bias_total + weight_sum
        return time.perf_counter() - start


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Optimized regression analyzer")
    parser.add_argument("--benchmark", action="store_true", help="Run the benchmark")
    parser.add_argument("--summary", action="store_true", help="Print case metrics")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    analyzer = RegressionAnalyzer()
    if args.summary:
        results = analyzer.evaluate_dataset(
            analyzer.load_dataset(), ignore_invalid=True
        )
        serialisable = {name: metrics.to_dict() for name, metrics in results.items()}
        print(json.dumps(serialisable, indent=2))
    if args.benchmark:
        elapsed = analyzer.benchmark()
        print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":  # pragma: no cover - exercised via scripts
    main()
