import pandas as pd
from typing import Tuple
import numpy as np

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    km = 6367 * c
    return km

def find_closest_points(wells_path: str, combined_data_path: str) -> pd.DataFrame:
    """
    For each well in wells_gambia.csv, find the closest point in combined_data_filled.csv
    and populate the columns DepthToGroundwater, GroundwaterProductivity, GroundwaterStorage.
    """
    # Load the data
    wells_df = pd.read_csv(wells_path)
    combined_df = pd.read_csv(combined_data_path)

    # Preparing new columns in wells dataframe
    wells_df['DepthToGroundwater'] = np.nan
    wells_df['GroundwaterProductivity'] = np.nan
    wells_df['GroundwaterStorage'] = np.nan

    # Iterate over each well
    for index, well in wells_df.iterrows():
        # Find the closest point in combined_data_filled.csv
        distances = combined_df.apply(
            lambda row: haversine(well['Latitude'], well['Longitude'], row['Y'], row['X']),
            axis=1
        )
        closest_idx = distances.idxmin()

        # Populate the new columns with the data from the closest point
        wells_df.at[index, 'DepthToGroundwater'] = combined_df.at[closest_idx, 'DepthToGroundwater']
        wells_df.at[index, 'GroundwaterProductivity'] = combined_df.at[closest_idx, 'GroundwaterProductivity']
        wells_df.at[index, 'GroundwaterStorage'] = combined_df.at[closest_idx, 'GroundwaterStorage']

    return wells_df

# Example usage
# wells_updated_df = find_closest_points(
#     wells_path='data/processed_data/igrac/wells_gambia.csv', 
#     combined_data_path='data/processed_data/british_geological_survey_africa/combined_data_filled.csv'
# )
# wells_updated_df.to_csv('data/processed_data/igrac/wells_gambia_updated.csv', index=False)
