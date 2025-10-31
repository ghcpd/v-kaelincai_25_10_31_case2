import json
from pathlib import Path

import pytest

from original_code import RegressionAnalyzer

BASE_DIR = Path(__file__).resolve().parent


def load_case(name: str) -> dict:
    data = json.loads((BASE_DIR / "input_data.json").read_text(encoding="utf-8"))
    for case in data["cases"]:
        if case["name"] == name:
            return case
    raise KeyError(f"case {name!r} not found")


def approx_dict(expected: dict, rel: float = 1e-3):
    return {key: pytest.approx(value, rel=rel) for key, value in expected.items()}


def test_balanced_normal_metrics_match():
    analyzer = RegressionAnalyzer()
    result = analyzer.evaluate_case(load_case("balanced-normal"))
    expected = {
        "mae": 1.775,
        "rmse": 1.8822,
        "bias": 0.115,
        "stability_index": 0.99,
    }
    assert result == approx_dict(expected)


def test_boundary_zero_stability_is_exact():
    analyzer = RegressionAnalyzer()
    result = analyzer.evaluate_case(load_case("boundary-zero"))
    assert result["mae"] == pytest.approx(0.0, abs=1e-12)
    assert result["rmse"] == pytest.approx(0.0, abs=1e-12)
    assert result["bias"] == pytest.approx(0.0, abs=1e-12)
    assert result["stability_index"] == pytest.approx(1.0, abs=1e-12)


def test_invalid_data_should_raise():
    analyzer = RegressionAnalyzer()
    case = load_case("invalid-malformed")
    with pytest.raises(ValueError):
        analyzer.evaluate_case(case)


def test_hidden_vulnerability_metrics_match_documentation():
    analyzer = RegressionAnalyzer()
    result = analyzer.evaluate_case(load_case("hidden-vulnerability"))
    expected = {
        "mae": 0.5309,
        "rmse": 0.6207,
        "bias": 0.5053,
        "stability_index": 0.9515,
    }
    assert result == approx_dict(expected)


def test_complex_nested_adjustments_applied_elementwise():
    analyzer = RegressionAnalyzer()
    case = load_case("complex-nested")
    result = analyzer.evaluate_case(case)
    expected = {
        "mae": 5.02,
        "rmse": 6.4555,
        "bias": 3.2943,
        "stability_index": 0.976,
    }
    assert result == approx_dict(expected)
