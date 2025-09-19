## script for lab 4

## import modules
import arcpy, traceback

## set environment settings
arcpy.env.workspace = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab4"
arcpy.env.overwriteOutput = True   

## request valid buffer size in meters:
min_val, max_val = 1, 10000
while True:
    s = input(f"Please enter buffer distance in Meters from garage points({min_val}-{max_val}): ").strip()
    try:
        buf_dist = float(s)
        if not (min_val <= buf_dist <= max_val):
            print(f"Enter a value between {min_val} and {max_val}.")
            continue
        break
    except ValueError:
        print("Enter a valid number.")

print(f"Using buffer distance: {buf_dist} meters")


## define script variables
folder_path = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab4"
gdb_name = "myLab4.gdb"
gdb_path = folder_path + "\\" + gdb_name

## check if file gdb already exists, if not create it
try:
    if arcpy.Exists(gdb_path):
        print(f"File geodatabase {gdb_name} already exists.")
    else:
        arcpy.CreateFileGDB_management(folder_path, gdb_name)
        print(f"Creating file geodatabase {gdb_name}.") 

    ## load input file into feature layer
    csv_path = folder_path + "\\" + "garages.csv"
    garage_layer = "Garage_Points"
    garages = arcpy.MakeXYEventLayer_management(csv_path, "X", "Y", garage_layer)   

    ## save feature layer to geodatabase
    input_layer = garages
    arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
    garage_points = gdb_path + "\\" + garage_layer

    ## open campus file geodatabase and copy feature class to it
    campus_gdb = folder_path + "\\" + "campus.gdb"
    buildings_campus = campus_gdb + "\Structures"
    buildings = gdb_path + "\\" + "Buildings"

    #arcpy.CopyFeatures_management(buildings_campus, buildings)
    arcpy.Copy_management(buildings_campus, buildings)

except arcpy.ExecuteError:
    print("ArcPy tool error:")
    print(arcpy.GetMessages(2))   
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    print(traceback.format_exc())
    raise


## reprojection of garage points to match buildings
spatial_ref = arcpy.Describe(buildings).spatialReference
print(f"The spatial reference used is:", spatial_ref.name)

arcpy.Project_management(garage_points, gdb_path + "\\" + "\Garage_Points_reprojected", spatial_ref)

## buffer garages 
## use input to get buffer size in meters (meters are used because spatial reference is in meters)
garageBuffered = arcpy.Buffer_analysis(gdb_path + "\\" + "\Garage_Points_reprojected", gdb_path + "\\" + "Garage_Points_buffered", buf_dist)           

## select buildings that intersect buffered garages
##arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + "\\" + "Garage_Building_Intersection", "ALL")

##arcpy.TableToTable_conversion(gdb_path + "\\" + "Garage_Building_Intersection.dbf", folder_path, "nearbyBuildings.csv" )

try:
    arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', "ALL")
    arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', folder_path, 'nearbyBuildings.csv')
 ## arcpy.TabletoTable_conversion is deprecated
 ## suggested way to execute this
 ##   arcpy.conversion.ExportTable(gdb_path + "\Garage_Building_Intersection.dbf", folder_path + "\\clnearbyBuildings.csv")
    print("Intersection and export completed successfully.")
except arcpy.ExecuteError:
    print("ArcPy tool error:")
    print(arcpy.GetMessages(2))   
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    print(traceback.format_exc())
    raise

