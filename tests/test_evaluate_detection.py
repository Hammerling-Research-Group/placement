import numpy as np
import pytest
import time
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

# Overall Detection Tests
class TestOverallDetection:
    def test_basic_functionality(self, sample_data):
        """Test normal cases for overall detection"""
        assert detection_overall(sample_data, 1.0, 2) == 1
        assert detection_overall(sample_data, 2.0, 2) == 0
        # Test exact threshold
        assert detection_overall(np.array([1.0, 1.0, 1.0]), 1.0, 3) == 1

    def test_edge_cases(self):
        """Test edge cases for overall detection"""
        assert detection_overall(np.array([]), 1.0, 1) == 0
        assert detection_overall(np.array([1.5]), 1.0, 1) == 1
        assert detection_overall(np.zeros(5), 1.0, 1) == 0
        assert detection_overall(np.ones(5), 1.0, 1) == 1

    def test_data_types(self):
        """Test different data types for overall detection"""
        assert detection_overall(np.array([1, 2, 3]), 1.0, 2) == 1
        assert detection_overall(np.array([1.0, 2.0, 3.0]), 1.0, 2) == 1
        assert detection_overall(np.array([1, 2.5, 3]), 1.0, 2) == 1

# Consecutive Detection Tests
class TestConsecutiveDetection:
    def test_basic_functionality(self, sample_data):
        """Test normal cases for consecutive detection"""
        assert detection_consecutive(sample_data, 1.0, 2) == 1
        assert detection_consecutive(np.array([1.5, 0.8, 1.2, 0.6]), 1.0, 2) == 0
        assert detection_consecutive(np.array([1.0, 1.0, 1.0]), 1.0, 3) == 1

    def test_edge_cases(self):
        """Test edge cases for consecutive detection"""
        assert detection_consecutive(np.array([]), 1.0, 1) == 0
        assert detection_consecutive(np.array([1.5]), 1.0, 1) == 1
        assert detection_consecutive(np.array([1.5, 0.5, 1.5, 0.5]), 1.0, 2) == 0
        assert detection_consecutive(np.array([1.5, 1.5, 1.5]), 1.0, 3) == 1

    def test_persistence_thresholds(self):
        """Test various persistence thresholds"""
        data = np.array([1.5, 1.5, 0.8, 0.9, 1.2])
        assert detection_consecutive(data, 1.0, 0.4) == 1
        assert detection_consecutive(data, 1.0, 0) == 0
        assert detection_consecutive(data, 1.0, len(data)) == 0

# Moving Window Detection Tests
class TestMovingWindowDetection:
    def test_basic_functionality(self, sample_data):
        """Test normal cases for moving window detection"""
        assert detection_movingWindow(sample_data, 3, 1.0, 2) == 1
        assert detection_movingWindow(sample_data, 3, 1.0, 2, stride=2) == 1
        assert detection_movingWindow(sample_data, 3, 2.0, 2) == 0

    def test_window_sizes(self, sample_data):
        """Test different window sizes"""
        assert detection_movingWindow(sample_data, 3, 1.0, 2) == 1
        assert detection_movingWindow(sample_data, 2, 1.0, 2) == 1
        assert detection_movingWindow(sample_data, 1, 1.0, 1) == 1

    def test_edge_cases(self):
        """Test edge cases for moving window detection"""
        # Empty array
        with pytest.raises(ValueError):
            detection_movingWindow(np.array([]), 1, 1.0, 1)

        # Single value
        assert detection_movingWindow(np.array([1.5]), 1, 1.0, 1) == 1

        # Window size equal to array size
        data = np.array([1.2] * 5)
        assert detection_movingWindow(data, 5, 1.0, 3) == 1

        # Test insufficient values above threshold
        data = np.array([1.2, 0.8, 1.2, 0.8, 1.2])
        assert detection_movingWindow(data, 5, 1.0, 4) == 0

    def test_persistence(self):
        """Test persistence thresholds for moving window"""
        data = np.array([1.2, 1.2, 0.8, 1.2, 1.2])
        assert detection_movingWindow(data, 3, 1.0, 2) == 1
        assert detection_movingWindow(data, 3, 1.0, 3) == 0

        # Test percentage-based persistence
        data = np.array([1.2, 1.2, 1.2, 0.8, 0.8])
        assert detection_movingWindow(data[:3], 3, 1.0, 0.7) == 1

# Integration and System Tests
class TestIntegrationAndSystem:
    def test_run_detection_integration(self, large_test_data):
        """Test all detection methods with large dataset"""
        # Test overall method
        result = run_detection(large_test_data, 'overall', 1.0, 2)
        assert result.shape == (5, 10)

        # Test consecutive method
        result = run_detection(large_test_data, 'consecutive', 1.0, 2)
        assert result.shape == (5, 10)

        # Test moving window method
        result = run_detection(large_test_data, 'movingWindow', 1.0, 2, window_len=3, stride=1)
        assert result.shape == (5, 10)

    def test_invalid_method(self, large_test_data):
        """Test handling of invalid detection method"""
        with pytest.raises(ValueError):
            run_detection(large_test_data, 'invalid_method', 1.0, 2)

    @pytest.mark.parametrize("test_data", [
        pytest.param(np.random.random((5, 10, 3)) * 1e-10, id="very_small_values"),
        pytest.param(np.random.random((5, 10, 3)) * 1e10, id="very_large_values"),
        pytest.param(np.random.random((5, 10, 3)) * np.array([1e-10, 1, 1e10]), id="mixed_scale")
    ])
    def test_numerical_stability(self, test_data):
        """Test numerical stability with extreme values"""
        result = run_detection(test_data, 'overall', 1.0, 2)
        assert result.shape == (3, 5)

    def test_performance(self, large_test_data):
        """Test performance and scalability"""
        methods = ['overall', 'consecutive', 'movingWindow']
        
        for method in methods:
            start_time = time.time()
            if method == 'movingWindow':
                result = run_detection(large_test_data, method, 1.0, 2, window_len=3, stride=1)
            else:
                result = run_detection(large_test_data, method, 1.0, 2)
            duration = time.time() - start_time
            
            # Basic performance assertion (adjust threshold as needed)
            assert duration < 1.0, f"{method} detection took too long: {duration:.2f}s"

    def test_consistency(self, large_test_data):
        """Test consistency of results across multiple runs"""
        results = []
        for _ in range(3):
            result = run_detection(large_test_data, 'overall', 1.0, 2)
            results.append(result)

        for i in range(1, len(results)):
            assert np.array_equal(results[0], results[i])

if __name__ == "__main__":
    pytest.main(["-v"])
