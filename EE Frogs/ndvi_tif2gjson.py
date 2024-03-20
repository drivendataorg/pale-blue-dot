import rasterio
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import geopandas as gpd
from pyproj import Transformer
import numpy as np

def convert_ndvi_tiff_to_geojson(ndvi_tiff_path, output_geojson_path):
    with rasterio.open(ndvi_tiff_path) as src:
        print(f"Raster CRS: {src.crs}")

        ndvi_image = src.read(1)
        contour_set = plt.contour(ndvi_image, levels=np.linspace(-1, 1, num=20))  # NDVI typically ranges from -1 to 1
        plt.close()

        transformer = Transformer.from_crs(src.crs, 'epsg:4326', always_xy=True)

        contours = []
        ndvi_values = []
        for level, contours_in_level in enumerate(contour_set.allsegs):
            for contour in contours_in_level:
                if len(contour) >= 2:
                    x, y = zip(*[(src.xy(row, col)) for col, row in contour])
                    lon, lat = transformer.transform(x, y)
                    line = LineString(zip(lon, lat))
                    contours.append(line)
                    ndvi_values.append(contour_set.levels[level])

        gdf = gpd.GeoDataFrame({'geometry': contours, 'NDVI': ndvi_values})
        gdf.crs = 'epsg:4326'
        gdf.to_file(output_geojson_path, driver='GeoJSON')

# Usage

convert_ndvi_tiff_to_geojson('NDVI_clip.tif', 'results/ndvi.geojson')