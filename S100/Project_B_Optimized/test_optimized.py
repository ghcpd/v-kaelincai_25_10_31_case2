import json
from pathlib import Path

import pytest

from optimized_code import Metrics, RegressionAnalyzer

BASE_DIR = Path(__file__).resolve().parent


def load_case(name: str) -> dict:
    data = json.loads((BASE_DIR / "input_data.json").read_text(encoding="utf-8"))
    for case in data["cases"]:
        if case["name"] == name:
            return case
    raise KeyError(f"case {name!r} not found")


def assert_metrics(metrics: Metrics, expected: dict):
    actual = metrics.to_dict()
    for key, value in expected.items():
        assert actual[key] == pytest.approx(value, rel=1e-3)


def test_balanced_normal_metrics_match_reference_values():
    analyzer = RegressionAnalyzer()
    metrics = analyzer.evaluate_case(load_case("balanced-normal"))
    assert_metrics(
        metrics,
        {"mae": 1.775, "rmse": 1.8822, "bias": 0.115, "stability_index": 0.99},
    )


def test_boundary_zero_case_is_stable():
    analyzer = RegressionAnalyzer()
    metrics = analyzer.evaluate_case(load_case("boundary-zero"))
    assert_metrics(
        metrics,
        {"mae": 0.0, "rmse": 0.0, "bias": 0.0, "stability_index": 1.0},
    )


def test_invalid_case_raises_value_error():
    analyzer = RegressionAnalyzer()
    with pytest.raises(ValueError):
        analyzer.evaluate_case(load_case("invalid-malformed"))


def test_hidden_vulnerability_regression_fixed():
    analyzer = RegressionAnalyzer()
    metrics = analyzer.evaluate_case(load_case("hidden-vulnerability"))
    assert_metrics(
        metrics,
        {
            "mae": 0.5309,
            "rmse": 0.6207,
            "bias": 0.5053,
            "stability_index": 0.9515,
        },
    )


def test_complex_nested_adjustments_respected():
    analyzer = RegressionAnalyzer()
    metrics = analyzer.evaluate_case(load_case("complex-nested"))
    assert_metrics(
        metrics,
        {
            "mae": 5.02,
            "rmse": 6.4555,
            "bias": 3.2943,
            "stability_index": 0.976,
        },
    )


def test_dataset_summary_contains_all_cases():
    analyzer = RegressionAnalyzer()
    cases = [
        case
        for case in analyzer.load_dataset()
        if case["name"] != "invalid-malformed"
    ]
    summary = analyzer.evaluate_dataset(cases)
    assert set(summary) == {
        "balanced-normal",
        "boundary-zero",
        "hidden-vulnerability",
        "complex-nested",
    }
    for metrics in summary.values():
        assert isinstance(metrics, Metrics)


def test_micro_benchmark_is_within_expected_bounds():
    analyzer = RegressionAnalyzer()
    # Keep runtime small while ensuring optimisation remains measurable.
    elapsed = analyzer.benchmark(iterations=120)
    assert elapsed < 0.25
