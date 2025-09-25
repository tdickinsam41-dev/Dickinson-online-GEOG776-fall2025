# -*- coding: utf-8 -*-

import arcpy, traceback


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [BuildingProximity]


class BuildingProximity:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determine's which buildings are near a targeted building."
        self.category = "Building Tools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Campus GDB",
            name="CampusGDB",
            datatype="DEType",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        ## order of list will be the same in the execute function
        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        """Define variables from entered parameters."""
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        campus_gdb = parameters[4].valueAsText
        buf_dist = int(parameters[5].value)

        gdb_path = folder_path + "\\" + gdb_name

        ## set environment settings
        arcpy.env.workspace = r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab5"
        arcpy.env.overwriteOutput = True   

        ## request valid buffer size in meters:
        ## min_val, max_val = 1, 10000
  
        # print(f"Using buffer distance: {buf_dist} meters")

        ## check if file gdb already exists, if not create it
        try:
            if arcpy.Exists(gdb_path):
                ## print(f"File geodatabase {gdb_name} already exists.")
                arcpy.AddMessage(f"File geodatabase {gdb_name} already exists.")
            else:
                arcpy.CreateFileGDB_management(folder_path, gdb_name)
                ## print(f"Creating file geodatabase {gdb_name}.") 
                arcpy.AddMessage(f"Creating file geodatabase {gdb_name}.")

            ## load input file into feature layer
            ## csv_path = folder_path + "\\" + "garages.csv"
            ## garage_layer_name = "Garage_Points"
            ## garages = arcpy.MakeXYEventLayer_management(csv_path, "X", "Y", garage_layer_name)   
            garages = arcpy.MakeXYEventLayer_management(csv_path, "X", "Y", garage_layer_name)

            ## save feature layer to geodatabase
            input_layer = garages
            arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
            garage_points = gdb_path + "\\" + garage_layer_name

            ## open campus file geodatabase and copy feature class to it
            ## campus_gdb = folder_path + "\\" + "campus.gdb"
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

        return None

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
