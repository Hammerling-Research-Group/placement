import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import os
import tempfile
import shutil
from simulate_concentrations import run_gp


class TestSimulateConcentrations(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        os.chmod(self.test_dir, 0o755)

        # Create sample emission scenarios
        self.df_emission_scenarios = pd.DataFrame({
            'ChunkIndex': [1, 1, 1, 2, 2, 2],
            'TimeStamp.Mountain': [
                '2024-01-01 00:00:00-07:00',
                '2024-01-01 00:01:00-07:00',
                '2024-01-01 00:02:00-07:00',
                '2024-01-01 00:03:00-07:00',
                '2024-01-01 00:04:00-07:00',
                '2024-01-01 00:05:00-07:00'
            ],
            'WindSpeed.m/s': [2.0, 2.1, 2.2, 2.3, 2.4, 2.5],
            'WindDirection.degree': [90, 91, 92, 93, 94, 95],
            'Source_x.m': [100, 100, 100, 200, 200, 200],
            'Source_y.m': [100, 100, 100, 200, 200, 200],
            'Source_z.m': [2, 2, 2, 2, 2, 2],
            'EmissionRate.kg/h': [1.0, 1.0, 1.0, 2.0, 2.0, 2.0]
        })

        self.grid_ranges = (-500, -500, 0, 500, 500, 10)
        self.grid_nums = (10, 10, 2)
        self.obs_dt = 60
        self.sim_dt = 1
        self.puff_dt = 4

    def test_valid_simulation(self):
        """Test that a valid simulation runs successfully."""
        output_file = os.path.join(self.test_dir, 'ch4_sim_grid_locations.npy')

        try:
            run_gp(
                self.df_emission_scenarios.copy(),
                self.grid_ranges,
                self.grid_nums,
                self.obs_dt,
                self.sim_dt,
                self.puff_dt,
                save_dir=self.test_dir + '/'
            )

            self.assertTrue(os.path.exists(output_file), "Output file was not created")
            ch4_sim_all = np.load(output_file)

            self.assertIsNotNone(ch4_sim_all)
            self.assertTrue(isinstance(ch4_sim_all, np.ndarray))
            self.assertEqual(ch4_sim_all.ndim, 3)

            n_scenarios = len(self.df_emission_scenarios['ChunkIndex'].unique())
            n_grid_points = self.grid_nums[0] * self.grid_nums[1] * self.grid_nums[2]
            self.assertEqual(ch4_sim_all.shape[0], n_scenarios)
            self.assertEqual(ch4_sim_all.shape[2], n_grid_points)

        except Exception as e:
            self.fail(f"Valid simulation failed with error: {str(e)}")

    def test_input_data_types(self):
        """Test input data type validation."""
        # Test with missing required columns
        invalid_df = self.df_emission_scenarios.copy()
        invalid_df = invalid_df.drop('WindSpeed.m/s', axis=1)

        with self.assertRaises(Exception):
            run_gp(
                invalid_df,
                self.grid_ranges,
                self.grid_nums,
                self.obs_dt,
                self.sim_dt,
                self.puff_dt,
                save_dir=self.test_dir + '/'
            )

    def test_time_parameters(self):
        """Test time parameter validation."""
        # Test valid time parameters
        try:
            run_gp(
                self.df_emission_scenarios.copy(),
                self.grid_ranges,
                self.grid_nums,
                obs_dt=60,
                sim_dt=1,
                puff_dt=4,
                save_dir=self.test_dir + '/'
            )
        except Exception as e:
            self.fail(f"Valid time parameters failed: {str(e)}")

        # Test invalid time parameter relationships
        invalid_combinations = [
            (60, 4, 1),  # puff_dt < sim_dt
            (30, 60, 120),  # obs_dt < sim_dt
        ]

        for obs, sim, puff in invalid_combinations:
            with self.assertRaises(SystemExit, msg=f"Failed for obs={obs}, sim={sim}, puff={puff}"):
                run_gp(
                    self.df_emission_scenarios.copy(),
                    self.grid_ranges,
                    self.grid_nums,
                    obs_dt=obs,
                    sim_dt=sim,
                    puff_dt=puff,
                    save_dir=self.test_dir + '/'
                )

    def test_timestamp_format(self):
        """Test timestamp format validation."""
        invalid_df = self.df_emission_scenarios.copy()
        invalid_df['TimeStamp.Mountain'] = ['Invalid_date'] * len(invalid_df)

        with self.assertRaises(Exception):
            run_gp(
                invalid_df,
                self.grid_ranges,
                self.grid_nums,
                self.obs_dt,
                self.sim_dt,
                self.puff_dt,
                save_dir=self.test_dir + '/'
            )

    def test_output_consistency(self):
        """Test output data consistency across multiple runs."""
        output_file = os.path.join(self.test_dir, 'ch4_sim_grid_locations.npy')

        # First run
        run_gp(
            self.df_emission_scenarios.copy(),
            self.grid_ranges,
            self.grid_nums,
            self.obs_dt,
            self.sim_dt,
            self.puff_dt,
            save_dir=self.test_dir + '/'
        )
        result1 = np.load(output_file)

        # Second run with same parameters
        run_gp(
            self.df_emission_scenarios.copy(),
            self.grid_ranges,
            self.grid_nums,
            self.obs_dt,
            self.sim_dt,
            self.puff_dt,
            save_dir=self.test_dir + '/'
        )
        result2 = np.load(output_file)

        # Check if results are consistent
        np.testing.assert_array_almost_equal(result1, result2)

    def test_chunked_data(self):
        """Test processing of chunked data."""
        # Create test data with multiple chunks
        multi_chunk_df = pd.concat([
            self.df_emission_scenarios,
            self.df_emission_scenarios.assign(ChunkIndex=lambda x: x['ChunkIndex'] + 2)
        ]).reset_index(drop=True)

        output_file = os.path.join(self.test_dir, 'ch4_sim_grid_locations.npy')

        run_gp(
            multi_chunk_df,
            self.grid_ranges,
            self.grid_nums,
            self.obs_dt,
            self.sim_dt,
            self.puff_dt,
            save_dir=self.test_dir + '/'
        )

        result = np.load(output_file)
        n_chunks = len(multi_chunk_df['ChunkIndex'].unique())
        self.assertEqual(result.shape[0], n_chunks)

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        try:
            if os.path.exists(self.test_dir):
                shutil.rmtree(self.test_dir)
        except Exception as e:
            print(f"Cleanup failed: {str(e)}")


if __name__ == '__main__':
    unittest.main(verbosity=2)

