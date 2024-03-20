import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import geopandas as gpd
from pyproj import Transformer
import numpy as np

def convert_dem_tiff_to_geojson(dem_tiff_path, output_geojson_path, contour_start=0, contour_end=30, num_contour_levels=10):
    with rasterio.open(dem_tiff_path) as src:
        print(f"Raster CRS: {src.crs}")

        dem_image = src.read(1)
        
        # Set contour levels from 0 to 30, adjust the number of levels as desired
        contour_levels = np.linspace(contour_start, contour_end, num=num_contour_levels)
        
        contour_set = plt.contour(dem_image, levels=contour_levels)
        plt.close()

        transformer = Transformer.from_crs(src.crs, 'epsg:4326', always_xy=True)

        contours = []
        elevation_values = []
        for level, contours_in_level in enumerate(contour_set.allsegs):
            for contour in contours_in_level:
                if len(contour) >= 2:
                    x, y = zip(*[(src.xy(row, col)) for col, row in contour])
                    lon, lat = transformer.transform(x, y)
                    line = LineString(zip(lon, lat))
                    contours.append(line)
                    elevation_values.append(contour_set.levels[level])

        gdf = gpd.GeoDataFrame({'geometry': contours, 'Elevation': elevation_values})
        gdf.crs = 'epsg:4326'
        gdf.to_file(output_geojson_path, driver='GeoJSON')

# Usage
convert_dem_tiff_to_geojson('tci_dem_clip.tif', 'results/dem.geojson')
