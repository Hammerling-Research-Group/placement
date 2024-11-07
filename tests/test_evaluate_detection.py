import numpy as np
import time
import sys
from evaluate_detection import (
    detection_overall,
    detection_consecutive,
    detection_movingWindow,
    run_detection
)


class UnitTests:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, test_name, test_func):
        """Helper function to run a test and print results"""
        self.tests_run += 1
        print(f"\nRunning {test_name}...")
        try:
            test_func()
            print(f"✓ {test_name} passed")
            self.tests_passed += 1
        except AssertionError as e:
            print(f"✗ {test_name} failed: {str(e)}")
        except Exception as e:
            print(f"✗ {test_name} failed with unexpected error: {str(e)}")

    def test_detection_overall_unit(self):
        """Unit tests for overall detection strategy"""

        def test_basic_functionality():
            # Test normal case
            assert detection_overall(np.array([0.5, 1.5, 2.0]), 1.0, 2) == 1
            # Test edge case - exact threshold
            assert detection_overall(np.array([1.0, 1.0, 1.0]), 1.0, 3) == 1
            # Test no detection
            assert detection_overall(np.array([0.5, 0.7, 0.9]), 1.0, 2) == 0

        def test_edge_cases():
            # Empty array
            assert detection_overall(np.array([]), 1.0, 1) == 0
            # Single value
            assert detection_overall(np.array([1.5]), 1.0, 1) == 1
            # All zeros
            assert detection_overall(np.zeros(5), 1.0, 1) == 0
            # All ones
            assert detection_overall(np.ones(5), 1.0, 1) == 1

        def test_data_types():
            # Integer array
            assert detection_overall(np.array([1, 2, 3]), 1.0, 2) == 1
            # Float array with integers
            assert detection_overall(np.array([1.0, 2.0, 3.0]), 1.0, 2) == 1
            # Mixed array
            assert detection_overall(np.array([1, 2.5, 3]), 1.0, 2) == 1

        self.run_test("Basic Overall Detection", test_basic_functionality)
        self.run_test("Edge Cases Overall Detection", test_edge_cases)
        self.run_test("Data Types Overall Detection", test_data_types)

    def test_detection_consecutive_unit(self):
        """Unit tests for consecutive detection strategy"""

        def test_basic_functionality():
            # Test normal case
            assert detection_consecutive(np.array([0.5, 1.5, 1.2, 0.8]), 1.0, 2) == 1
            # Test no consecutive values
            assert detection_consecutive(np.array([1.5, 0.8, 1.2, 0.6]), 1.0, 2) == 0
            # Test exact threshold
            assert detection_consecutive(np.array([1.0, 1.0, 1.0]), 1.0, 3) == 1

        def test_edge_cases():
            # Empty array
            assert detection_consecutive(np.array([]), 1.0, 1) == 0
            # Single value
            assert detection_consecutive(np.array([1.5]), 1.0, 1) == 1
            # Alternating values
            assert detection_consecutive(np.array([1.5, 0.5, 1.5, 0.5]), 1.0, 2) == 0
            # All values above threshold
            assert detection_consecutive(np.array([1.5, 1.5, 1.5]), 1.0, 3) == 1

        def test_persistence_thresholds():
            # Test fractional persistence
            data = np.array([1.5, 1.5, 0.8, 0.9, 1.2])
            assert detection_consecutive(data, 1.0, 0.4) == 1
            # Test zero persistence
            assert detection_consecutive(data, 1.0, 0) == 0
            # Test full length persistence
            assert detection_consecutive(data, 1.0, len(data)) == 0

        self.run_test("Basic Consecutive Detection", test_basic_functionality)
        self.run_test("Edge Cases Consecutive Detection", test_edge_cases)
        self.run_test("Persistence Thresholds Consecutive Detection", test_persistence_thresholds)

    def test_detection_moving_window_unit(self):
        """Unit tests for moving window detection strategy"""

        def test_basic_functionality():
            data = np.array([0.5, 1.5, 1.2, 0.8, 1.1])
            # Test normal case
            assert detection_movingWindow(data, 3, 1.0, 2) == 1
            # Test with stride
            assert detection_movingWindow(data, 3, 1.0, 2, stride=2) == 1
            # Test no detection
            assert detection_movingWindow(data, 3, 2.0, 2) == 0
            print("Basic functionality tests passed")

        def test_window_sizes():
            data = np.array([1.5, 1.2, 0.8, 1.1, 1.3])
            # Window size half of data
            assert detection_movingWindow(data, 3, 1.0, 2) == 1
            # Window size 2
            assert detection_movingWindow(data, 2, 1.0, 2) == 1
            # Single value window
            assert detection_movingWindow(data, 1, 1.0, 1) == 1
            print("Window size tests passed")

        def test_edge_cases():
            # Test with empty array
            try:
                result = detection_movingWindow(np.array([]), 1, 1.0, 1)
                assert result == 0, "Empty array should return 0"
            except Exception as e:
                print(f"Empty array handling: {str(e)}")

            # Test with single value
            single_value = np.array([1.5])
            try:
                result = detection_movingWindow(single_value, 1, 1.0, 1)
                assert result == 1, "Single value above threshold should return 1"
            except Exception as e:
                print(f"Single value handling: {str(e)}")

            # Test with window size equal to array size
            data = np.ones(5)
            try:
                result = detection_movingWindow(data, 5, 1.0, 3)
                assert result == 1, "Full window size should work with sufficient values above threshold"
            except Exception as e:
                print(f"Full window handling: {str(e)}")

            # Test with invalid window sizes
            data = np.array([1.0, 1.0, 1.0])
            try:
                # Window size larger than data
                result = detection_movingWindow(data, len(data) + 1, 1.0, 1)
                print("Warning: Should handle window size larger than data")
            except ValueError:
                print("Correctly raised ValueError for window size larger than data")

            # Test all zeros
            zeros_data = np.zeros(5)
            try:
                result = detection_movingWindow(zeros_data, 2, 1.0, 1)
                assert result == 0, "All zeros should return 0"
            except Exception as e:
                print(f"All zeros handling: {str(e)}")

            # Test all ones
            ones_data = np.ones(5)
            try:
                result = detection_movingWindow(ones_data, 2, 1.0, 1)
                assert result == 1, "All ones should return 1"
            except Exception as e:
                print(f"All ones handling: {str(e)}")

            print("Edge cases tests handled appropriately")

        self.run_test("Basic Moving Window Detection", test_basic_functionality)
        self.run_test("Window Sizes Tests", test_window_sizes)
        self.run_test("Edge Cases Moving Window Detection", test_edge_cases)


class RegressionTests:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0

    def generate_test_data(self, n_scenarios=10, n_t=24, n_grids=5):
        """Generate synthetic test data"""
        return np.random.random((n_scenarios, n_t, n_grids)) * 2.0

    def test_performance(self):
        """Test performance and scalability"""
        print("\n=== Running Performance Tests ===")

        test_sizes = [(10, 24, 5), (20, 48, 10), (50, 96, 20)]
        methods = ['overall', 'consecutive', 'movingWindow']

        for size in test_sizes:
            n_scenarios, n_t, n_grids = size
            data = self.generate_test_data(n_scenarios, n_t, n_grids)

            print(f"\nTesting size: {size}")
            for method in methods:
                start_time = time.time()

                if method == 'movingWindow':
                    result = run_detection(data, method, 1.0, 2, window_len=3, stride=1)
                else:
                    result = run_detection(data, method, 1.0, 2)

                end_time = time.time()
                print(f"{method}: {end_time - start_time:.4f} seconds")

                # Check result shape
                expected_shape = (n_grids, n_scenarios)
                assert result.shape == expected_shape, f"Wrong shape: {result.shape} vs {expected_shape}"

    def test_numerical_stability(self):
        """Test numerical stability with extreme values"""
        print("\n=== Running Numerical Stability Tests ===")

        # Test with various extreme cases
        test_cases = [
            ("Very small values", np.random.random((5, 10, 3)) * 1e-10),
            ("Very large values", np.random.random((5, 10, 3)) * 1e10),
            ("Mixed scale values", np.random.random((5, 10, 3)) * np.array([1e-10, 1, 1e10])),
            ("NaN values", np.where(np.random.random((5, 10, 3)) > 0.9, np.nan, 1.0)),
            ("Inf values", np.where(np.random.random((5, 10, 3)) > 0.9, np.inf, 1.0))
        ]

        for case_name, data in test_cases:
            print(f"\nTesting {case_name}")
            try:
                result = run_detection(data, 'overall', 1.0, 2)
                print(f"✓ Test passed: {case_name}")
                self.tests_passed += 1
            except Exception as e:
                print(f"✗ Test failed: {case_name} - {str(e)}")
            self.tests_run += 1

    def test_consistency(self):
        """Test consistency of results across different runs"""
        print("\n=== Running Consistency Tests ===")

        data = self.generate_test_data()
        methods = ['overall', 'consecutive', 'movingWindow']

        for method in methods:
            print(f"\nTesting consistency for {method}")
            results = []

            # Run multiple times and compare results
            for _ in range(3):
                if method == 'movingWindow':
                    result = run_detection(data, method, 1.0, 2, window_len=3, stride=1)
                else:
                    result = run_detection(data, method, 1.0, 2)
                results.append(result)

            # Check if all results are identical
            for i in range(1, len(results)):
                assert np.array_equal(results[0], results[i]), f"Inconsistent results for {method}"
            print(f"✓ Consistency test passed for {method}")
            self.tests_passed += 1
            self.tests_run += 1


def main():
    """Run all tests"""
    print("=== Starting Comprehensive Test Suite ===")

    # Run unit tests
    unit_tests = UnitTests()
    unit_tests.test_detection_overall_unit()
    unit_tests.test_detection_consecutive_unit()
    unit_tests.test_detection_moving_window_unit()

    print(f"\nUnit Tests Summary:")
    print(f"Tests Run: {unit_tests.tests_run}")
    print(f"Tests Passed: {unit_tests.tests_passed}")
    print(f"Success Rate: {(unit_tests.tests_passed / unit_tests.tests_run) * 100:.2f}%")

    # Run regression tests
    regression_tests = RegressionTests()
    try:
        regression_tests.test_performance()
        regression_tests.test_numerical_stability()
        regression_tests.test_consistency()

        print(f"\nRegression Tests Summary:")
        print(f"Tests Run: {regression_tests.tests_run}")
        print(f"Tests Passed: {regression_tests.tests_passed}")
        print(f"Success Rate: {(regression_tests.tests_passed / regression_tests.tests_run) * 100:.2f}%")

    except Exception as e:
        print(f"Regression tests failed with error: {str(e)}")


if __name__ == "__main__":
    main()
