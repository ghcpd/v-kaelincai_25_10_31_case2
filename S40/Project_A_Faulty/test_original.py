import json
import math
from pathlib import Path

import pytest

import original_code as module

FIXTURES = Path(__file__).resolve().parent


@pytest.fixture(autouse=True)
def _reset_cache():
    module.clear_cache()
    yield
    module.clear_cache()


def test_null_entries_are_ignored():
    payload = {
        "metrics": [1.0, None, 3.0, {"shadow": [2.0, None]}]
    }
    result = module.compute_stability_index(payload)
    assert math.isclose(result, 2.0, rel_tol=1e-9)


def test_payload_mutation_triggers_recomputation():
    payload = {"readings": [1.0, 1.0]}
    first = module.compute_stability_index(payload)
    payload["readings"].append(9.0)
    second = module.compute_stability_index(payload)
    assert second > first


def test_textual_noise_is_skipped():
    payload = {
        "data": [[[{"value": 5.0}, "noise", 1.0]]]
    }
    result = module.compute_stability_index(payload)
    assert math.isclose(result, 3.0, rel_tol=1e-9)


def test_sample_payload_from_file():
    payload_path = FIXTURES / "input_data.json"
    payload = module.load_payload(str(payload_path))

    def expected_value(node):
        if isinstance(node, dict):
            total = 0.0
            count = 0
            for value in node.values():
                subtotal, subcount = expected_value(value)
                total += subtotal
                count += subcount
            return total, count
        if isinstance(node, (list, tuple, set)):
            total = 0.0
            count = 0
            for item in node:
                subtotal, subcount = expected_value(item)
                total += subtotal
                count += subcount
            return total, count
        if isinstance(node, bool):
            return 0.0, 0
        if isinstance(node, (int, float)):
            return float(node), 1
        # Ignore non-numeric types
        return 0.0, 0

    total, count = expected_value(payload)
    expected_average = (total / count) if count else 0.0

    result = module.compute_stability_index(payload)
    assert math.isclose(result, expected_average, rel_tol=1e-9)


def test_booleans_and_dicts_are_ignored():
    payload = {
        "readings": [True, False, 5.0, {"meta": {"score": 7.0}}]
    }
    result = module.compute_stability_index(payload)
    assert math.isclose(result, 6.0, rel_tol=1e-9)
