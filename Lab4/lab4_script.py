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



