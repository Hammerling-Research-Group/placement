import numpy as np
import time
import os
import pickle
from placement.PORSS import PORSS

# specify dirs
data_dir = './demo/output_data/'
valid_locations_result_dir = './demo/results_valid_locations/'
os.makedirs(valid_locations_result_dir, exist_ok=True)
fenceline_locations_result_dir = './demo/results_fenceline_locations/'
os.makedirs(fenceline_locations_result_dir, exist_ok=True)

# load data
detection_valid = np.load(data_dir + 'detection_valid_locations.npy')
detection_fenceline = np.load(data_dir + 'detection_fenceline_locations.npy')


# define main function 
def run_porss(matrix, budget, min_detected_sensor, n_trials, verbose=False, save_dir='./'):
    n_locations, n_scenarios = matrix.shape
    for i in range(n_trials):
        porss = PORSS(matrix, sensor_budget, min_detected_sensor, recombination='onepoint',  verbose = False)
        start_time = time.time()
        porss_solution, coverage = porss.main()
        runtime = time.time() - start_time
    
        print(f'########## Run #{i} ##########')
        print(f'Best coverage by PORSS solution: {coverage/n_scenarios}')
        print(f'Runtime: {runtime} seconds')
        
        # save result
        result_dict = {'PORSS solution' : porss_solution,
                       'PORSS solution coverage' : coverage,
                       'PROSS runtime' : runtime}
    
        filename = f'PORSS_best_{budget}_sensor_placement_trial_{i}_coverage_{coverage}.pkl'
    
        with open(save_dir + filename, "wb") as pickle_file:
            pickle.dump(result_dict, pickle_file)
    

# run optimization 
n_trials = 10
sensor_budget = 4
min_detected_sensor = 1

## valid sensor locations

print('Run PORSS on valid sensor locations.')
run_porss(detection_valid, sensor_budget, min_detected_sensor, n_trials, save_dir=valid_locations_result_dir)

## fenceline sensor locations
print('Run PORSS on fenceline sensor locations.')
run_porss(detection_valid, sensor_budget, min_detected_sensor, n_trials, save_dir=fenceline_locations_result_dir)
