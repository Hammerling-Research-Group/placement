import numpy as np
import pytest
from placement.evaluate_detection import (
    detection_overall,
    detection_consecutive,
    detection_movingWindow,
    run_detection
)


# Test data fixtures
@pytest.fixture
def sample_data():
    return np.array([0.5, 1.5, 2.0, 0.8, 1.2])


@pytest.fixture
def large_test_data():
    return np.random.random((10, 24, 5)) * 2.0


# Overall detection tests
def test_detection_overall_basic(sample_data):
    assert detection_overall(sample_data, 1.0, 2) == 1
    assert detection_overall(sample_data, 2.0, 2) == 0


def test_detection_overall_edge_cases():
    assert detection_overall(np.array([]), 1.0, 1) == 0
    assert detection_overall(np.array([1.5]), 1.0, 1) == 1
    assert detection_overall(np.zeros(5), 1.0, 1) == 0
    assert detection_overall(np.ones(5), 1.0, 1) == 1


def test_detection_overall_data_types():
    assert detection_overall(np.array([1, 2, 3]), 1.0, 2) == 1
    assert detection_overall(np.array([1.0, 2.0, 3.0]), 1.0, 2) == 1
    assert detection_overall(np.array([1, 2.5, 3]), 1.0, 2) == 1


# Consecutive detection tests
def test_detection_consecutive_basic(sample_data):
    assert detection_consecutive(sample_data, 1.0, 2) == 1
    assert detection_consecutive(np.array([1.5, 0.8, 1.2, 0.6]), 1.0, 2) == 0


def test_detection_consecutive_edge_cases():
    assert detection_consecutive(np.array([]), 1.0, 1) == 0
    assert detection_consecutive(np.array([1.5]), 1.0, 1) == 1
    assert detection_consecutive(np.array([1.5, 0.5, 1.5, 0.5]), 1.0, 2) == 0


def test_detection_consecutive_persistence():
    data = np.array([1.5, 1.5, 0.8, 0.9, 1.2])
    assert detection_consecutive(data, 1.0, 0.4) == 1
    assert detection_consecutive(data, 1.0, 0) == 0
    assert detection_consecutive(data, 1.0, len(data)) == 0


# Moving window detection tests
def test_detection_moving_window_basic(sample_data):
    assert detection_movingWindow(sample_data, 3, 1.0, 2) == 1
    assert detection_movingWindow(sample_data, 3, 1.0, 2, stride=2) == 1
    assert detection_movingWindow(sample_data, 3, 2.0, 2) == 0


def test_detection_moving_window_sizes(sample_data):
    assert detection_movingWindow(sample_data, 3, 1.0, 2) == 1
    assert detection_movingWindow(sample_data, 2, 1.0, 2) == 1
    assert detection_movingWindow(sample_data, 1, 1.0, 1) == 1


def test_detection_moving_window_edge_cases():
    # Empty array
    with pytest.raises(ValueError):
        detection_movingWindow(np.array([]), 1, 1.0, 1)

    # Single value
    assert detection_movingWindow(np.array([1.5]), 1, 1.0, 1) == 1

    # Window size equal to array size
    data = np.array([1.2, 1.2, 1.2, 1.2, 1.2])
    assert detection_movingWindow(data, 5, 1.0, 3) == 1

    # Test when not enough values are above threshold
    data = np.array([1.2, 0.8, 1.2, 0.8, 1.2])
    assert detection_movingWindow(data, 5, 1.0, 4) == 0


def test_detection_moving_window_persistence():
    """Test different scenarios for moving window persistence thresholds"""
    # Test with integer persistence
    data = np.array([1.2, 1.2, 0.8, 1.2, 1.2])
    assert detection_movingWindow(data, 3, 1.0, 2) == 1  # Window size 3, need 2 values
    assert detection_movingWindow(data, 3, 1.0, 3) == 0  # Window size 3, need all 3

    # Test with sufficient values for 70% persistence
    data = np.array([1.2, 1.2, 1.2, 0.8, 0.8])
    # For window size 3 and 70% persistence, need ceil(3 * 0.7) = 3 values
    assert detection_movingWindow(data[:3], 3, 1.0, 0.7) == 1


# Integration tests
def test_run_detection_integration(large_test_data):
    # Test overall method
    result = run_detection(large_test_data, 'overall', 1.0, 2)
    assert result.shape == (5, 10)  # (n_grids, n_scenarios)

    # Test consecutive method
    result = run_detection(large_test_data, 'consecutive', 1.0, 2)
    assert result.shape == (5, 10)

    # Test moving window method
    result = run_detection(large_test_data, 'movingWindow', 1.0, 2, window_len=3, stride=1)
    assert result.shape == (5, 10)


def test_run_detection_invalid_method(large_test_data):
    with pytest.raises(ValueError):
        run_detection(large_test_data, 'invalid_method', 1.0, 2)


# Numerical stability tests
@pytest.mark.parametrize("test_data", [
    np.random.random((5, 10, 3)) * 1e-10,  # Very small values
    np.random.random((5, 10, 3)) * 1e10,  # Very large values
    np.random.random((5, 10, 3)) * np.array([1e-10, 1, 1e10]),  # Mixed scale values
])
def test_numerical_stability(test_data):
    result = run_detection(test_data, 'overall', 1.0, 2)
    assert result.shape == (3, 5)


def test_performance_consistency(large_test_data):
    """Test that multiple runs produce consistent results"""
    results = []
    for _ in range(3):
        result = run_detection(large_test_data, 'overall', 1.0, 2)
        results.append(result)

    # Check if all results are identical
    for i in range(1, len(results)):
        assert np.array_equal(results[0], results[i])
