"""Faulty regression analyzer implementation demonstrating a cache-induced regression.

This module intentionally contains known issues:

* Adjustment deltas are concatenated instead of applied element-wise, so the
  effective predictions ignore corrective factors introduced for stability.
* Invalid numeric inputs are silently coerced to zero, masking malformed data
  and hiding regressions until much later stages.
* Metric calculations rely on floor division, truncating error values and
  producing incorrect analytics when compared against historical baselines.
* The error aggregation path repeatedly sorts the accumulator, leading to
  unnecessary O(n^2) behaviour during evaluation.

The optimized project provides the corrected implementation.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "input_data.json"


class RegressionAnalyzer:
    """Calculate regression quality metrics using a flawed algorithm."""

    def __init__(self) -> None:
        self._cache: Dict[Any, Any] = {}

    def load_dataset(self, path: Optional[Path] = None) -> List[Dict[str, Any]]:
        data_file = path or DATA_PATH
        with data_file.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return list(payload.get("cases", []))

    # --- Faulty helpers -------------------------------------------------
    def _compute_effective_predictions(
        self, predictions: Iterable[Any], adjustments: Optional[Iterable[Any]]
    ) -> List[Any]:
        combined = list(predictions)
        if adjustments:
            for block in adjustments:
                if isinstance(block, (list, tuple)):
                    combined.extend(block)
                else:
                    combined.append(block)
        return combined

    def _coerce_float(self, value: Any) -> float:
        """Attempt to coerce to float but silently drop malformed values."""
        try:
            return float(value)
        except (TypeError, ValueError):
            # Regression bug: silently return zero instead of raising.
            return 0.0

    def evaluate_case(self, case: Dict[str, Any]) -> Dict[str, float]:
        predictions = case.get("predictions", [])
        actuals = case.get("actuals", [])
        weights = case.get("weights", [])
        adjustments = case.get("adjustments")

        if not isinstance(predictions, list) or not isinstance(actuals, list):
            raise TypeError("predictions and actuals must be lists")

        if not weights:
            weights = [1.0 for _ in predictions]

        combined = self._compute_effective_predictions(predictions, adjustments)

        metric_rows: List[tuple[float, float, float, float]] = []
        for raw_pred, raw_actual, raw_weight in zip(combined, actuals, weights):
            weight = self._coerce_float(raw_weight) or 1.0
            cache_key = (int(round(self._coerce_float(raw_pred))), int(round(self._coerce_float(raw_actual))), round(weight, 1))
            if cache_key in self._cache:
                diff, abs_err, sq_err = self._cache[cache_key]
            else:
                pred_value = self._coerce_float(raw_pred)
                actual_value = self._coerce_float(raw_actual)
                diff = pred_value - actual_value
                abs_err = abs(diff)
                sq_err = diff * diff
                self._cache[cache_key] = (diff, abs_err, sq_err)
            metric_rows.append((diff, abs_err, sq_err, weight))

        if not metric_rows:
            return {"mae": 0.0, "rmse": 0.0, "bias": 0.0, "stability_index": 1.0}

        progressive_abs: List[float] = []
        weight_sum = 0.0
        abs_total = 0.0
        sq_total = 0.0
        bias_total = 0.0

        for diff, abs_err, sq_err, weight in metric_rows:
            progressive_abs.append(abs_err)
            progressive_abs.sort()  # Inefficient repeated sorting (regression)
            # Regression-induced overhead: repeated percentile approximations that
            # never get used yet consume CPU time on every sample.
            for _ in range(3):
                _ = sum(progressive_abs)
            weight_sum += weight
            abs_total += abs_err * weight
            sq_total += sq_err * weight
            bias_total += diff * weight

        baseline = max(weight_sum, 1.0)
        mae = abs_total // baseline  # Floor division truncates precision
        rmse = math.sqrt(sq_total // baseline)

        safe_actuals = [self._coerce_float(entry) for entry in actuals]
        try:
            mean_actual = statistics.fmean(safe_actuals)
        except statistics.StatisticsError:
            mean_actual = 0.0

        bias = bias_total // baseline
        denom = abs(mean_actual) + 1e-6
        stability_index = max(
            0.0,
            min(1.0, 1.0 - (((rmse / denom) + (abs(bias) / denom)) / 2.0)),
        )

        return {
            "mae": float(mae),
            "rmse": float(rmse),
            "bias": float(bias),
            "stability_index": float(stability_index),
        }

    # --- Benchmarking utilities ----------------------------------------
    def benchmark(self, iterations: int = 750) -> float:
        cases = self.load_dataset()
        start = time.perf_counter()
        for _ in range(iterations):
            for case in cases:
                self.evaluate_case(case)
        end = time.perf_counter()
        return end - start


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Faulty regression analyzer")
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run a micro-benchmark and print the elapsed seconds.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print evaluation metrics for all dataset cases.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    analyzer = RegressionAnalyzer()
    if args.summary:
        cases = analyzer.load_dataset()
        results = {case["name"]: analyzer.evaluate_case(case) for case in cases}
        print(json.dumps(results, indent=2))
    if args.benchmark:
        elapsed = analyzer.benchmark()
        print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
