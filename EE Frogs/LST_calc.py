import rasterio
import numpy as np
import geopandas as gpd
from rasterio.mask import mask

def calculate_indices_and_lst(thermal_band_path, output_path):

    with rasterio.open(thermal_band_path) as thermal_src:
        # Read the thermal band
        thermal_band = thermal_src.read(1).astype('float64')
        print(thermal_band)

        # Convert DN to TOA brightness temperature in Kelvin
        ML = 0.003342  # Replace with your actual value
        AL = 146  # Replace with your actual value
        thermal_band = thermal_band * ML + AL

        # Mask no data values
        thermal_band[thermal_band == thermal_src.nodata] = np.nan

        # Calculate LST in Celsius / Celsius
        lst = thermal_band - 273.15 # (thermal_band / (1 + (0.00115 * (thermal_band / 1.438)) * np.log(em)))
        lst[lst < 0] = np.nan
    print(np.nanmin(lst))
    print(np.nanmax(lst))

    # Update the metadata
    meta = thermal_src.meta
    meta.update(dtype=rasterio.float32)

    # Write the LST to a new file
    with rasterio.open(output_path, 'w', **meta) as dst:
        dst.write(lst.astype(rasterio.float32), 1)

# Usage
calculate_indices_and_lst('2022/2022_comp_clip.TIF', 'results/lst_calc.tif')