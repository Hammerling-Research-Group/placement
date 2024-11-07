import unittest
import numpy as np
from PORSS import PORSS
import tempfile
import os
import pickle


class TestPORSSOptimization(unittest.TestCase):
    def setUp(self):
        """Set up test matrices and directories"""
        # Create sample detection matrices for testing
        self.small_matrix = np.array([
            [1, 0, 1, 0],
            [0, 1, 1, 1],
            [1, 1, 0, 0],
            [0, 0, 1, 1]
        ])

        # Create larger random matrix for more realistic testing
        np.random.seed(42)
        self.large_matrix = np.random.choice([0, 1], size=(20, 30), p=[0.7, 0.3])

        # Create empty matrix for edge cases
        self.empty_matrix = np.array([[]])

        # Create matrix with all zeros
        self.zero_matrix = np.zeros((5, 5))

        # Create matrix with all ones
        self.ones_matrix = np.ones((5, 5))

        # Create temporary directory for test results
        self.test_dir = tempfile.mkdtemp()

    def test_porss_initialization_basic(self):
        """Test basic PORSS initialization"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        self.assertEqual(porss.n_rows, 4)
        self.assertEqual(porss.n_cols, 4)
        self.assertEqual(porss.k, 2)
        self.assertEqual(porss.min_detected_sensor, 1)

    def test_porss_initialization_edge_cases(self):
        """Test PORSS initialization with edge cases"""
        # Test with zero matrix
        porss_zero = PORSS(self.zero_matrix, k=1, min_detected_sensor=1)
        self.assertEqual(porss_zero.n_rows, 5)
        self.assertEqual(porss_zero.n_cols, 5)

        # Test with ones matrix
        porss_ones = PORSS(self.ones_matrix, k=1, min_detected_sensor=1)
        self.assertEqual(porss_ones.n_rows, 5)
        self.assertEqual(porss_ones.n_cols, 5)

        # Test with different k values
        porss_large_k = PORSS(self.small_matrix, k=10, min_detected_sensor=1)
        self.assertEqual(porss_large_k.k, 10)

    def test_porss_parameters(self):
        """Test PORSS parameter calculations"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        self.assertIsInstance(porss.mut_prob, float)
        self.assertGreater(porss.mut_prob, 0)
        self.assertLess(porss.mut_prob, 1)
        self.assertIsInstance(porss.n_iters, int)
        self.assertGreater(porss.n_iters, 0)

    def test_population_initialization(self):
        """Test initial population creation"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        self.assertIsInstance(porss.population, np.ndarray)
        self.assertEqual(porss.population_size, 1)
        self.assertEqual(porss.population.shape[1], porss.n_rows)

    def test_objectives_calculation_basic(self):
        """Test basic objectives calculation"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        solution = np.array([1, 0, 1, 0])
        objectives = porss.objectives(solution)
        self.assertEqual(len(objectives), 2)
        self.assertIsInstance(objectives[0], (int, np.integer))
        self.assertIsInstance(objectives[1], (int, np.integer))

    def test_objectives_calculation_edge_cases(self):
        """Test objectives calculation with edge cases"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)

        # Test with all zeros solution
        zero_solution = np.zeros(4)
        zero_objectives = porss.objectives(zero_solution)
        self.assertEqual(zero_objectives[1], 0)  # Should have 0 sensors

        # Test with all ones solution
        ones_solution = np.ones(4)
        ones_objectives = porss.objectives(ones_solution)
        self.assertEqual(ones_objectives[1], 4)  # Should have 4 sensors

    def test_recombination_onepoint_properties(self):
        """Test properties of onepoint recombination"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        solution1 = np.array([1, 0, 1, 0])
        solution2 = np.array([0, 1, 0, 1])

        s1_rec, s2_rec = porss.recombination_onepoint(solution1, solution2)

        # Check lengths
        self.assertEqual(len(s1_rec), len(solution1))
        self.assertEqual(len(s2_rec), len(solution2))

        # Check if solutions are different from parents
        self.assertTrue(np.any(s1_rec != solution1) or np.any(s2_rec != solution2))

        # Check if solutions contain only 0s and 1s
        self.assertTrue(np.all(np.logical_or(s1_rec == 0, s1_rec == 1)))
        self.assertTrue(np.all(np.logical_or(s2_rec == 0, s2_rec == 1)))

    def test_recombination_uniform_properties(self):
        """Test properties of uniform recombination"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        solution1 = np.array([1, 0, 1, 0])
        solution2 = np.array([0, 1, 0, 1])

        s1_rec, s2_rec = porss.recombination_uniform(solution1, solution2)

        # Check lengths
        self.assertEqual(len(s1_rec), len(solution1))
        self.assertEqual(len(s2_rec), len(solution2))

        # Check if solutions contain only 0s and 1s
        self.assertTrue(np.all(np.logical_or(s1_rec == 0, s1_rec == 1)))
        self.assertTrue(np.all(np.logical_or(s2_rec == 0, s2_rec == 1)))

    def test_mutation_properties(self):
        """Test properties of mutation operation"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        solution1 = np.array([1, 0, 1, 0])
        solution2 = np.array([0, 1, 0, 1])

        s1_mut, s2_mut = porss.mutation(solution1, solution2)

        # Check lengths
        self.assertEqual(len(s1_mut), len(solution1))
        self.assertEqual(len(s2_mut), len(solution2))

        # Check if solutions contain only 0s and 1s
        self.assertTrue(np.all(np.logical_or(s1_mut == 0, s1_mut == 1)))
        self.assertTrue(np.all(np.logical_or(s2_mut == 0, s2_mut == 1)))

    def test_early_stop_condition(self):
        """Test early stopping condition"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)

        # Test with all same values
        self.assertTrue(porss.early_stop([1, 1, 1, 1]))

        # Test with different values
        self.assertFalse(porss.early_stop([1, 2, 1, 1]))

    def test_opt_val_upper_bound(self):
        """Test optimal value upper bound calculation"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        self.assertIsInstance(porss.opt_val_ub, (int, np.integer))
        self.assertGreaterEqual(porss.opt_val_ub, 0)
        self.assertLessEqual(porss.opt_val_ub, porss.n_cols)

    def test_population_size_changes(self):
        """Test population size updates"""
        porss = PORSS(self.small_matrix, k=2, min_detected_sensor=1)
        initial_size = porss.population_size

        # Add a new solution
        new_solution = np.zeros(porss.n_rows)
        porss.population = np.vstack((porss.population, new_solution))
        porss.population_size = porss.population.shape[0]

        self.assertEqual(porss.population_size, initial_size + 1)

    def tearDown(self):
        """Clean up temporary files after tests"""
        import shutil
        shutil.rmtree(self.test_dir)


if __name__ == '__main__':
    unittest.main(verbosity=2)
