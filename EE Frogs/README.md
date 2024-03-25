# PBD_code

## Solar Panel Suitability Analysis for the Turks and Caicos Islands
In this repository we can find the code for a project focused on assessing the suitability for solar panel installation in the Turks and Caicos Islands. This project is grounded in an analysis of various key geographical and environmental factors that are crucial in determining the optimal locations for solar energy harvesting. The analysis incorporates a detailed examination of the Land Surface Temperature (LST), the Normalized Difference Vegetation Index (NDVI), elevation profiles, and the slope of the terrain across the islands. By evaluating the LST, the project identifies areas with the most suitable temperature conditions for solar panel efficiency (Between 20 and 26 Cº). The NDVI analysis helps in understanding vegetation density, which is vital for selecting areas with minimal shading on the panels. Elevation and slope analyses ensure that areas chosen for solar panel installation are not only accessible but also receive maximum sunlight exposure. This approach ensures that the most strategic and efficient locations are identified for solar panel installation, thereby maximizing energy output and contributing to the sustainable energy goals of the Turks and Caicos Islands.

## Code Repository Overview for Landsat Image Processing and Analysis for Solar Panel Suitability in Turks and Caicos Islands

This repository contains a suite of Python scripts specifically designed to process and analyze Landsat 8 and 9 images. The goal is to evaluate the suitability of locations in the Turks and Caicos Islands for solar panel installation. The scripts are listed in the order they are typically used in the process:

1- composite.py: Creates composite images from the Landsat 8 and 9 data, providing a comprehensive view of the region over time.

2- clip.py: Clips the composite Landsat images using a shapefile of the Turks and Caicos Islands, focusing the analysis on this specific geographic area.

3- NDVI.py: Computes the Normalized Difference Vegetation Index (NDVI) from the clipped Landsat images. NDVI helps assess vegetation cover to identify suitable non-vegetative areas for solar panels.

4- LST_calc.py: Calculates the Land Surface Temperature (LST) from the clipped Landsat images, a crucial factor in determining optimal locations for solar panel installation.

5- dem_tif2gjson.py: Converts Digital Elevation Model (DEM) data into GeoJSON format. DEM, obtained through QGIS, is essential for understanding the topography of the area, which impacts solar panel placement.

6- lst_average.py: Calculates the average Land Surface Temperature over the study area, providing a broader context for the LST data.

7- ndvi_tif2gjson.py: Transforms NDVI data from TIFF to GeoJSON format for use in dynamic visualizations.

8 -lst_tiff2geojson.py: Converts LST data from TIFF to GeoJSON format, facilitating integration with Kepler.gl for dynamic visualization.

9- metrics.py: Generates suitability metrics for solar panel installation on a scale of 0 to 10, based on NDVI, LST, DEM, and slope data. The slope data is obtained using QGIS.
