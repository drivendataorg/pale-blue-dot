import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling


def composite(file1, file2, output_path):

    def align_and_resize(paths, target_crs, target_transform, target_shape):
        sum_array = np.zeros(target_shape, dtype=np.float32)
        count_array = np.zeros(target_shape, dtype=np.float32)

        for path in paths:
            with rasterio.open(path) as src:
                src_array = src.read(1)
                src_crs = src.crs
                src_transform = src.transform

                output_array = np.empty(target_shape, dtype=src_array.dtype)
                reproject(
                    source=src_array,
                    destination=output_array,
                    src_transform=src_transform,
                    src_crs=src_crs,
                    dst_transform=target_transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest
                )

                valid_mask = output_array != src.nodata
                sum_array[valid_mask] += output_array[valid_mask]
                count_array[valid_mask] += 1

        with np.errstate(divide='ignore', invalid='ignore'):
            average_array = sum_array / count_array
            average_array[count_array == 0] = 0

        return average_array

    # Paths to the individual band files for each Landsat image
    # List of file paths for the Landsat images
    # band4_paths = ['2023_12_27/red_band.TIF', '2024_01_21/red_band.TIF']
    # band5_paths = ['2023_12_27/nir_band.TIF', '2024_01_21/nir_band.TIF']
    band10_paths = [file1, file2]

    # Determine the target CRS, transform, and shape based on the first image of band 4
    with rasterio.open(band10_paths[0]) as src:
        target_crs = src.crs
        target_transform, target_width, target_height = calculate_default_transform(
            src.crs, src.crs, src.width, src.height, *src.bounds)
        target_shape = (target_height, target_width)

    # Align, resize, and blend each band
    # band4_composite_avg = align_and_resize(band4_paths, target_crs, target_transform, target_shape)
    # band5_composite_avg = align_and_resize(band5_paths, target_crs, target_transform, target_shape)
    band10_composite_avg = align_and_resize(band10_paths, target_crs, target_transform, target_shape)

    # Save the composite bands using the metadata of the first image
    with rasterio.open(band10_paths[0]) as src:
        meta = src.meta

    meta.update(count=1, height=target_shape[0], width=target_shape[1])

    output_paths = [output_path]
    for band, output_path in zip([band10_composite_avg], output_paths):
        with rasterio.open(output_path, 'w', **meta) as dst:
            dst.write(band, 1)

year = 2019
composite(str(year) + '/ST_B10_1.TIF', str(year) +'/ST_B10_2.TIF', str(year) + '/' + str(year) + '_composite_band_10.tif')

