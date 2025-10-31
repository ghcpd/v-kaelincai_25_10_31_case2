import json
import pathlib

import pytest

from original_code import RegressionAnalyzer

EXPECTED_TOTALS = {
    "alpha": 18.0,
    "beta": 11.5,
    "300": 18.0,
    "delta": -5.5,
}


@pytest.fixture(scope="module")
def records():
    data_path = pathlib.Path(__file__).with_name("input_data.json")
    with data_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_normal_case_alpha(records):
    analyzer = RegressionAnalyzer()
    analyzer.aggregate_scores([records[1]])  # Prime cache with same-length payload.
    result = analyzer.aggregate_scores([records[0]])
    assert result["alpha"] == pytest.approx(EXPECTED_TOTALS["alpha"])


def test_numeric_string_handling(records):
    analyzer = RegressionAnalyzer()
    analyzer.aggregate_scores([records[0]])
    result = analyzer.aggregate_scores([records[1]])
    assert result["beta"] == pytest.approx(EXPECTED_TOTALS["beta"])


def test_non_string_identifier(records):
    analyzer = RegressionAnalyzer()
    analyzer.aggregate_scores([records[0]])
    result = analyzer.aggregate_scores([records[2]])
    assert result["300"] == pytest.approx(EXPECTED_TOTALS["300"])


def test_nested_boundary_case(records):
    analyzer = RegressionAnalyzer()
    analyzer.aggregate_scores([records[0]])
    result = analyzer.aggregate_scores([records[3]])
    assert result["delta"] == pytest.approx(EXPECTED_TOTALS["delta"])


def test_invalid_input_type_rejected():
    analyzer = RegressionAnalyzer()
    with pytest.raises(TypeError):
        analyzer.aggregate_scores("this should not work")
