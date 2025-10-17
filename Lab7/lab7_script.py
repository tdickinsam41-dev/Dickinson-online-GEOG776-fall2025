import arcpy

## set source and target folders
source = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab7\images"
target = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab7"

## assign bands
band1 = arcpy.sa.Raster(source + r"\band1.tif")
band2 = arcpy.sa.Raster(source + r"\band2.tif")
band3 = arcpy.sa.Raster(source + r"\band3.tif")
## commented out because too large for github
## band4 = arcpy.sa.Raster(source + r"\band4.tif")

## create composite
composite = arcpy.CompositeBands_management([band1, band2, band3], target + r"\composite.tif")

## create hillshade
azimuth = 315
altitude = 45
shadows = "No_Shadows"
z_factor = 1
arcpy.ddd.HillShade(source + f"\DEM.tif", target + r"\output_hillshade.tif", azimuth, altitude, shadows, z_factor)

## create slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\DEM.tif", target + r"\output_slope.tif", output_measurement, z_factor)

print("success")
