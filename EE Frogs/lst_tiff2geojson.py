import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from pyproj import Transformer

def convert_tiff_to_geojson(tiff_path, output_path):
    with rasterio.open(tiff_path) as src:
        # Check and print the CRS of the raster
        print(f"Raster CRS: {src.crs}")

        image = src.read(1)
        contour_set = plt.contour(image)
        plt.close()

        # Transformer for converting raster coordinates to geographic coordinates (EPSG:4326)
        transformer = Transformer.from_crs(src.crs, 'epsg:4326', always_xy=True)

        contours = []
        lst_values = []
        for level, contours_in_level in enumerate(contour_set.allsegs):
            for contour in contours_in_level:
                if len(contour) >= 2:
                    # Convert pixel coordinates (row, col) to (x, y)
                    x, y = zip(*[(src.xy(row, col)) for col, row in contour])
                    # Transform to geographic coordinates
                    lon, lat = transformer.transform(x, y)
                    line = LineString(zip(lon, lat))
                    contours.append(line)
                    lst_values.append(contour_set.levels[level])

        gdf = gpd.GeoDataFrame({'geometry': contours, 'LST': lst_values})
        gdf.crs = 'epsg:4326'
        gdf.to_file(output_path, driver='GeoJSON')

# convert_tiff_to_geojson('results/lst_calc.tif', 'results/output.geojson')
        
convert_tiff_to_geojson('NDVI_clip.tif', 'results/ndvi.geojson')
