import numpy as np
import pandas as pd

# specify dirs
data_dir = './demo/output_data/'
save_dir = './demo/output_data/'

ch4_sim = np.load(data_dir + 'ch4_sim_grid_locations.npy') # shape = (n_scenarios, n_t, n_grids)
n_scenarios, n_t, n_grids = ch4_sim.shape

df_valid_sensor_locs = pd.read_csv(data_dir + 'valid_sensor_locations.csv')
df_fenceline_sensor_locs = pd.read_csv(data_dir + 'fenceline_sensor_locations.csv')

# Different detection strategies 

# Overall detection strategy: Checks if the total number of values exceeding a threshold
# meets or exceeds the persistence threshold
def detection_overall(data, amp_thresh, persistence_thresh):
    data = np.array(data)  # Convert input data to a NumPy array for efficient calculations

    # If persistence_thresh is less than 1, treat it as a fraction of data length
    if persistence_thresh < 1:
        persistence_thresh = int(np.ceil(len(data) * persistence_thresh))

    # Check if the number of values above amp_thresh meets or exceeds persistence_thresh
    if (data >= amp_thresh).sum() >= persistence_thresh:
        return 1  # Detection is confirmed
    else:
        return 0  # No detection


## Consecutive detection strategy: Checks if there is a consecutive sequence of values
## exceeding a threshold that meets or exceeds the persistence threshold
def detection_consecutive(data, amp_thresh, persistence_thresh):
    data = np.array(data)  # Convert input data to a NumPy array

    # If persistence_thresh is less than 1, treat it as a fraction of data length
    if persistence_thresh < 1:
        persistence_thresh = int(np.ceil(len(data) * persistence_thresh))

    count = 0  # Counter for consecutive values above threshold

    # Iterate through the data to find consecutive values above amp_thresh
    for value in data:
        if value >= amp_thresh:
            count += 1  # Increment counter for consecutive values above threshold
            if count == persistence_thresh:
                return 1  # Detection is confirmed when consecutive count meets threshold
        else:
            count = 0  # Reset counter if a value falls below the threshold

    return 0  # No detection


## Moving window detection strategy: Checks if any sliding window has a sufficient number
## of values exceeding the threshold based on the persistence threshold
def detection_movingWindow(data, window_len, amp_thresh, persistence_thresh, stride=1):
    # Determine the required count of values above threshold based on persistence_thresh
    if persistence_thresh < 1:
        required_count = int(np.ceil(window_len * persistence_thresh))
    else:
        required_count = persistence_thresh

    # Create sliding windows of specified length
    windows = np.lib.stride_tricks.sliding_window_view(data, window_shape=window_len)
    
    # Apply stride to the windows to skip elements as specified
    windows = windows[::stride]
    
    # Count the number of values above amp_thresh in each window
    count_greater_than_amp_thresh = np.sum(windows > amp_thresh, axis=1)

    # Check if any window has enough values above the threshold to meet the required count
    if np.any(count_greater_than_amp_thresh >= required_count):
        return 1  # Detection is confirmed
    else:
        return 0  # No detection

# Main function to perform methane detection based on the specified method
def run_detection(ch4_sim, method, amp_thresh, persistence_thresh, window_len=None, stride=None, save_dir='./'):
    """
    Applies a specified methane detection strategy across simulation data.

    Parameters:
        ch4_sim (np.ndarray, shape = (n_scenarios, n_t, n_grids)) [ppm]: 2D array of methane simulation data where each row represents a scenario and each column represents a grid location.
        method (str): Detection method to use. Options are 'overall', 'consecutive', or 'movingWindow'.
        amp_thresh (float) [ppm]: Amplitude threshold to use for detection.
        persistence_thresh (int or float): Persistence threshold, as a count or fraction of data length.
        window_len (int, optional): Length of the moving window for the 'movingWindow' method. Required if method is 'movingWindow'.
        stride (int, optional): Stride length for the moving window in 'movingWindow' method. Default is None.

    Raises:
        ValueError: If an unsupported detection method is specified.

    Returns:
        detection (np.ndarray, shape = (n_scenarios, n_grids)) : 2D array of detection reulsts. 1 for detection, 0 for non-detection. 
    """

    # Use the 'overall' detection method to check if total values above the threshold meet persistence
    if method == 'overall':
        detection = np.apply_along_axis(detection_overall, axis=1, 
                                        arr=ch4_sim,
                                        amp_thresh=amp_thresh, 
                                        persistence_thresh=persistence_thresh)  # shape = (n_scenarios, n_grids) 
        
    # Use the 'consecutive' detection method to find sequences of consecutive values meeting the threshold
    elif method == 'consecutive':
        detection = np.apply_along_axis(detection_consecutive, axis=1, 
                                        arr=ch4_sim,
                                        amp_thresh=amp_thresh, 
                                        persistence_thresh=persistence_thresh)  # shape = (n_scenarios, n_grids) 

    # Use the 'movingWindow' detection method to apply a sliding window with stride for detection
    elif method == 'movingWindow':
        detection = np.apply_along_axis(detection_movingWindow, axis=1, 
                                        arr=ch4_sim,
                                        window_len=window_len,  # Specify the window length
                                        amp_thresh=amp_thresh, 
                                        persistence_thresh=persistence_thresh,
                                        stride=stride)  # shape = (n_scenarios, n_grids) 

    # Raise an error if an unsupported method is provided
    else:
        raise ValueError(f"Unsupported detection method '{method}'. "
                         "Please choose from 'overall', 'consecutive', or 'movingWindow'.")

    # Transpose detection matrix so that rows are locations and columns are emission scenarios
    detection = np.transpose(detection) # new shape = (n_grids, n_scenarios)
    
    # Save the detection results to a file for further analysis or visualization
    np.save(save_dir + 'detection_grid_locations.npy', detection)

    return detection




# Run detection
method = 'overall'
amp_thresh, persistence_thresh = 1, .2
detection = run_detection(ch4_sim, method, amp_thresh, persistence_thresh, save_dir=save_dir)  # shape = (n_grids, n_scenarios)

# Detection matrix for valid sensor locations
rows_valid_locs = df_valid_sensor_locs['loc_index'].tolist()
detection_valid_sensors = detection[rows_valid_locs, :]
np.save(save_dir + 'detection_valid_locations.npy', detection_valid_sensors)

# Detection matrix for fenceline sensor locations
rows_fenceline_locs = df_fenceline_sensor_locs['loc_index'].tolist()
detection_fenceline_sensors = detection[rows_fenceline_locs, :]
np.save(save_dir + 'detection_fenceline_locations.npy', detection_fenceline_sensors)
