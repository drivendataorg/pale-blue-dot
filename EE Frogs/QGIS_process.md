# Qgis

The steps taken to obtain the DEM and slope maps are outlined below.

1- The DEM is freely available on NASA’s Earthdata search, under the product name “ASTER Global Digital Elevation Model V003”. Navigating to the Turks and Caicos Islands (TCI)  region, download the two images that contain all the islands.
<img width="1083" alt="Screenshot 2024-01-26 at 4 20 23 PM" src="https://github.com/bastian6666/PBD_code/assets/57109930/d3c21128-182a-4d49-8d89-71a78f6d0877">


2- Next we opened the DEM in QGIS to clip to the TCI region using a boundary shapefile available on the Humanitarian Data Exchange.  

<img width="1092" alt="Screenshot 2024-01-26 at 4 20 37 PM" src="https://github.com/bastian6666/PBD_code/assets/57109930/5eec50c3-89b0-4b85-a324-9210900dc1ba">

3- Using the GDAL Raster analysis slope function from QGIS’ processing toolbox, we then calculated the slope map. The slope describes the percentage of vertical distance that equates to traveling the same horizontal distance; in other words, it describes how steep the terrain is. We found that the TCI terrain is relatively flat, with no drastic slope changes. 
