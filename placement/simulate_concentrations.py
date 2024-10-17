import sys
from datetime import datetime
import numpy as np
import pandas as pd
import time
## import fast Gaussian puff model
puff_dir = './FastGaussianPuff/'
sys.path.insert(0, puff_dir)
bin_dir = puff_dir + 'bin'  # by default, makefile stores the .so file here. needs to be on the python path to get imported.
sys.path.insert(0, bin_dir)
from GaussianPuff import GaussianPuff as GP

################################# specify dir paths #################################
input_data_dir = './demo/input_data/'
output_data_dir = './demo/output_data/'
save_data_dir = './demo/output_data/'

################################# load data #################################
df_emission_scenarios = pd.read_csv(output_data_dir + 'emission_scenarios.csv')  # emission scenarios from step 1
df_domain = pd.read_csv(input_data_dir + 'domain.csv') # domain boundaries of the site
df_grid_locs = pd.read_csv(output_data_dir + 'grid_locations.csv') # grid locations from step 2

################################# main function #################################
def run_gp(df_emission_scenarios, grid_ranges, grid_nums, obs_dt, sim_dt, puff_dt, save_dir='./'):
    # Convert time column to datetime format
    df_emission_scenarios['TimeStamp.Mountain'] = df_emission_scenarios['TimeStamp.Mountain'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S%z') if isinstance(x, str) else x)
    
    nx, ny, nz = grid_nums # number of grids in x, y, z directions
    ch4_sim_all = [] # Initialize an empty list to store simulated ch4 concentrations
    
    for i, scenario in df_emission_scenarios.groupby('ChunkIndex'):
        print(f"Working on #{i} emision scenario.")
        times = scenario['TimeStamp.Mountain'].tolist()
        start_time = times[0]
        end_time = times[-1]
        ws = scenario['WindSpeed.m/s'].to_numpy()
        wd = scenario['WindDirection.degree'].to_numpy()
        source_x = scenario['Source_x.m'].tolist()[0]
        source_y = scenario['Source_y.m'].tolist()[0]
        source_z = scenario['Source_z.m'].tolist()[0]
        source_loc = [[source_x, source_y, source_z]] # shape = (n_active_source, 3)
        emission_rate = [scenario['EmissionRate.kg/h'].tolist()[0]] # shape = (n_active_source, 1)
    
        # run Gaussian puff model
        grid_puff = GP(obs_dt, sim_dt, puff_dt,
                       start_time, end_time,
                       source_loc, emission_rate,
                       ws, wd, 
                       grid_coordinates=grid_ranges,
                       using_sensors=False,
                       nx=nx, ny=ny, nz=nz,
                       puff_duration=1080,
                       quiet=True, unsafe=False)
                    
        grid_puff.simulate() # simulation results. shape of grid_puff.ch4_obs = (nt, nx, ny, nz)
    
        # Reshape the array to 2D shape (nt, nx*ny*nz)
        ch4_sim = grid_puff.ch4_obs.reshape(grid_puff.ch4_obs.shape[0], -1) # shape = (nt, nx*ny*nz)
        ch4_sim_all.append(ch4_sim)
    
    ch4_sim_all = np.array(ch4_sim_all) # shape=(n_emissionscenarios, nt, nx*ny*nz)
    np.save(save_dir + 'ch4_sim_grid_locations.npy', ch4_sim_all) 


################################# run #################################
## location variables
x_min, x_max, y_min, y_max, z_min, z_max, dx, dy, dz = df_domain.iloc[0]
nx = int((x_max - x_min) / dx) + 1
ny = int((y_max - y_min) / dx) + 1
nz = int((z_max - z_min) / dz) + 1
grid_ranges = (x_min, y_min, z_min, x_max, y_max, z_max)
grid_nums = (nx, ny, nz)

## Gaussian puff related variables
obs_dt, sim_dt, puff_dt = 60, 1, 4 # [seconds]

## run Gaussian puff on given data
runtime_start = time.time()
run_gp(df_emission_scenarios, grid_ranges, grid_nums, obs_dt, sim_dt, puff_dt, save_dir=save_dir)
print('############################################')
print(f'Entire simulation is done in {time.time() - runtime_start} seconds.')



