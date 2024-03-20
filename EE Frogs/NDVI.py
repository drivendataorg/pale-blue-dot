import rasterio
import numpy as np

def calculate_ndvi(nir_band_path, red_band_path, ndvi_output_path):
    # Open the NIR band
    with rasterio.open(nir_band_path) as nir:
        nir_band = nir.read(1)

    # Open the red band
    with rasterio.open(red_band_path) as red:
        red_band = red.read(1)

    # Calculate NDVI
    ndvi = (nir_band.astype(float) - red_band.astype(float)) / (nir_band + red_band)

    # Write the NDVI image
    with rasterio.open(
        ndvi_output_path,
        'w',
        driver='GTiff',
        height=nir_band.shape[0],
        width=nir_band.shape[1],
        count=1,
        dtype=ndvi.dtype,
        crs=nir.crs,
        transform=nir.transform,
    ) as dst:
        dst.write(ndvi, 1)

# Example usage
calculate_ndvi('2023_12_27/nir_band.TIF', '2023_12_27/red_band.TIF', 'results/ndvi.tif')




