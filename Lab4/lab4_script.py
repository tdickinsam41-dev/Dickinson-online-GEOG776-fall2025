## script for lab 4

## import modules
import arcpy

## set environment settings
arcpy.env.workspace = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab4"
arcpy.env.overwriteOutput = True    

## define script variables
folder_path = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab4"
gdb_name = "lab4.gdb"
gdb_path = folder_path + "\\" + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

## load input file into feature layer
csv_path = folder_path + "\\" + "garages.csv"
garage_layer = "Garage_Points"
garages = arcpy.MakeXYEventLayer_management(csv_path, "X", "Y", garage_layer)   

## save feature layer to geodatabase
input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_fc = gdb_path + "\\" + garage_layer

## open campus file geodatabase and copy feature class to it
campus_gdb = folder_path + "\\" + "campus.gdb"
buildings_campus = campus_gdb + "\Structures"
buildings = gdb_path + "\\" + "Buildings"

#arcpy.CopyFeatures_management(buildings_campus, buildings)
arcpy.Copy_management(buildings_campus, buildings)

## reprojection of garage points to match buildings
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + "\\" + "\Garage_Points_reprojected", spatial_ref)

## buffer garages 150 feet
garageBuffered = arcpy.Buffer_analysis(gdb_path + "\\" + "\Garage_Points_reprojected", gdb_path + "\\" + "Garage_Points_buffered", "150 Feet")           

## select buildings that intersect buffered garages
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + "\\" + "Garage_Building_Intersection", "ALL")

arcpy.TableToTable_conversion(gdb_path + "\\" + "Garage_Building_Intersection.dbf", folder_path, "nearbyBuildings.csv" )

