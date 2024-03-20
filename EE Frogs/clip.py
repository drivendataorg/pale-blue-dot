import rasterio
import geopandas as gpd
from rasterio.mask import mask

def cut_raster_with_shapefile(tiff_path, shapefile_path, output_path):
    # Load the shapefile
    shapefile = gpd.read_file(shapefile_path)

    # Open the raster file
    with rasterio.open(tiff_path) as src:
        # Reproject the shapefile to match the raster's CRS
        shapefile = shapefile.to_crs(src.crs)

        # Convert the geometry to GeoJSON format
        geojson_geometry = [feature["geometry"] for feature in shapefile.__geo_interface__['features']]

        # Check the CRS of the raster and the shapefile
        print("Raster CRS: ", src.crs)
        print("Shapefile CRS: ", shapefile.crs)

        # Check the bounds of the raster and the shapefile
        print("Raster bounds: ", src.bounds)
        print("Shapefile bounds: ", shapefile.total_bounds)

        # Crop the raster using the GeoJSON geometry and invert the mask
        out_image, out_transform = mask(src, geojson_geometry, crop=True)
        out_meta = src.meta.copy()

        # Update the metadata to reflect the new raster size
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        # Write the cropped raster to a new file
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(out_image)

# Usage
year = 2023
# cut_raster_with_shapefile(str(year) + '/' + str(year) + '_composite_band_10.tif', 'TCA_shapefile/TCA_Island.shp', str(year) + '/' + str(year) + '_comp_clip.tif')
#cut_raster_with_shapefile('results/ndvi.tif', 'TCA_shapefile/TCA_Island.shp', 'NDVI_clip.tif')

cut_raster_with_shapefile('tci_dem.tif', 'TCA_shapefile/TCA_Island.shp', 'tci_dem_clip.tif')