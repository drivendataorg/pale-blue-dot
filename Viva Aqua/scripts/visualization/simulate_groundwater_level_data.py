# Read in gambia_lat_and_long.csv and simulate groundwater level data

import numpy as np

# Read in gambia_lat_and_long.csv
gambia_lat_and_long = np.genfromtxt('data/final_dataset/original/gambia_lat_and_long.csv', delimiter=',', skip_header=1)

# Simulate groundwater level data between 20 and 50
groundwater_level = np.random.uniform(20, 50, size=(gambia_lat_and_long.shape[0], 1))

# Save simulated groundwater level data with latitudes and longitudes
groundwater_level = np.hstack((gambia_lat_and_long, groundwater_level))
# Swap order of latitude and longitude
groundwater_level[:, [0, 1]] = groundwater_level[:, [1, 0]]
# Convert to float
groundwater_level = groundwater_level.astype(float)

# Add date column and set to 12-01-2023
date = np.full((gambia_lat_and_long.shape[0], 1), '12/1/2023')
groundwater_level = np.hstack((groundwater_level, date))

# Save to csv, including dates in strings
np.savetxt('simulated_groundwater_level.csv', groundwater_level, delimiter=',', header='Latitude,Longitude,Groundwater Level,Date', fmt='%s', comments='')

print('Simulated groundwater level data saved to simulated_groundwater_level.csv')