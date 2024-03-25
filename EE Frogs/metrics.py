import rasterio
import numpy as np

def scale_raster_values(raster_path, output_path, raster_type):
    # Define the value ranges for NDVI, DEM, and Slope
    ranges = {
        'ndvi': (-1, 1),
        'dem': (0, 80),
        'slope': (0, 10)  # Slope values are assumed to be in percentage
    }

    with rasterio.open(raster_path) as src:
        # Read the data
        data = src.read(1)
        
        # Determine min and max from the data for LST or use predefined ranges for others
        if raster_type == 'lst':
            value_min, value_max = np.nanmin(data), np.nanmax(data)
            print(f"Min: {value_min}, Max: {value_max}")
        elif raster_type in ranges:
            value_min, value_max = ranges[raster_type]
        else:
            raise ValueError("Invalid raster type. Expected 'lst', 'ndvi', or 'dem'.")

        # Invert and scale values from 0 to 10
        # High values (near value_max) become low (near 0), low values become high (near 10)
        scaled_data = 10 - ((data - value_min) / (value_max - value_min) * 10)

        # Address any potential divide-by-zero or NaN if max and min are the same
        scaled_data = np.nan_to_num(scaled_data, nan=10.0)

        # Update the metadata for one band only and data type as float32
        out_meta = src.meta.copy()
        out_meta.update({"count": 1, "dtype": 'float32'})

        # Write the scaled data to a new raster
        with rasterio.open(output_path, 'w', **out_meta) as dst:
            dst.write(scaled_data.astype('float32'), 1)




import rasterio
import numpy as np

def scale_raster_values(raster_path, output_path, raster_type):
    # Define the value ranges for NDVI, DEM, and Slope
    ranges = {
        'ndvi': (-1, 1),
        'dem': (0, 80),
        'slope': (0, 41.67)  # Slope values are assumed to be in percentage
    }

    with rasterio.open(raster_path) as src:
        # Read the data
        data = src.read(1)
        
        # Determine min and max from the data for LST or use predefined ranges for others
        if raster_type == 'lst':
            value_min, value_max = np.nanmin(data), np.nanmax(data)
        elif raster_type in ranges:
            value_min, value_max = ranges[raster_type]
        else:
            raise ValueError("Invalid raster type. Expected 'lst', 'ndvi', 'dem', or 'slope'.")

        # Invert and scale values from 0 to 10
        if raster_type == 'slope':
            # For slope, a higher percentage means a lower value on the scale
            scaled_data = 10 - ((data - value_min) / (value_max - value_min) * 9) - 1
        else:
            # For other types, high values become low (near 0), low values become high (near 10)
            scaled_data = 10 - ((data - value_min) / (value_max - value_min) * 10)

        # Address any potential divide-by-zero or NaN if max and min are the same
        scaled_data = np.nan_to_num(scaled_data, nan=10.0)

        # Update the metadata for one band only and data type as float32
        out_meta = src.meta.copy()
        out_meta.update({"count": 1, "dtype": 'float32'})

        # Write the scaled data to a new raster
        with rasterio.open(output_path, 'w', **out_meta) as dst:
            dst.write(scaled_data.astype('float32'), 1)


# Usage examples:
# For LST
scale_raster_values('results/lst_calc.tif', 'LST_scaled.tif', 'lst')

# For NDVI
scale_raster_values('NDVI_clip.tif', 'NDVI_scaled.tif', 'ndvi')

# For DEM
scale_raster_values('tci_dem_clip.tif', 'DEM_scaled.tif', 'dem')

# For Slope
scale_raster_values('Slope_tci_de1.tif', 'Slope_scaled.tif', 'slope')
