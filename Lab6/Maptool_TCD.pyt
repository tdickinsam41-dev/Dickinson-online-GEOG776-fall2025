# -*- coding: utf-8 -*-

import arcpy, traceback


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]

## need a class for each tool in the toolbox
class GraduatedColorsRenderer:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "create a graduated color map for a layout based on one of its attributes"
        self.canRunInBackground = False
        self.category = "Map Tools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        ## parameter for source project name
        param0 = arcpy.Parameter(
            displayName="Input Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input",
        )
        ## input layer to classify
        param1 = arcpy.Parameter(
            displayName="Layer to classify",
            name="layerToclassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input",
        )
        ## output folder location 
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input",
        )
        ## output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="outputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )

        params = [param0, param1, param2, param3]
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
        arcpy.env.overwriteOutput = True


        ## define progressor variables
        readTime = 3    # time for users to read progress
        start = 0       # start position of progressor
        max = 100       # end position of progressor
        step = 33       # progress interval 

        ## initiate progressor
        try: 
            arcpy.SetProgressor("step", "Validating project file ...", start, max, step)
            time.sleep(readTime)    # pause the exection for 3 seconds
        except:
            arcpy.AddWarning("Progressor failed to initialize.")

        ## alert user of progress with message to Results pane
        arcpy.AddMessage("Validating project file ...")

        ## set project variable
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        ## set campus variable to the first map from the source project
        campus = project.listMaps()[0]

        ## increment progressor
        try:
            arcpy.SetProgressorPosition(start + step)
            ## alert user of progress with message to Results pane
            arcpy.SetProgressorLabel("Finding map layer ...")
            ## pause execution again
            time.sleep(readTime)    # pause the exection for 3 seconds
            arcpy.AddMessage("Searching for map layer ...")
        except:
            arcpy.AddWarning("Progressor failed to update at 33%.")
    
        ## Loop through the layers in the map to find the one to classify
        try:
            for layer in campus.listLayers():
                ## check if layer is a feature layer
                if layer.isFeatureLayer:
                    ## copy the layer's symbology
                    symbology = layer.symbology
                    ## verify that the symbology has a renderer property
                    if hasattr(symbology, 'renderer'):
                        ## check if the layer is the one provided by the user
                        if layer.name == parameters[1].valueAsText:
                            ## increment progressor
                            arcpy.SetProgressorPosition(start + step) ## move to 33%
                            arcpy.SetProgressorLabel("Updating layer symbology ...")
                            time.sleep(readTime)    # pause the execution
                            arcpy.AddMessage("Updating symbology for " + layer.name + " layer.")

                            ## update the copy's renderer to graduated colors
                            symbology.updateRenderer('GraduatedColorsRenderer')

                            ## update with field to base the chloropleth off of
                            symbology.renderer.classificationField = "Shape_Area"

                            ## increment progressor
                            arcpy.SetProgressorPosition(start + 2*step) ## move to 66%
                            arcpy.SetProgressorLabel("Cleaning up ...")
                            time.sleep(readTime)    # pause the execution
                            arcpy.AddMessage("Cleaning up ...") 

                            ## set the number of classes
                            symbology.renderer.breakCount = 7

                            ## set the color ramp
                            symbology.renderer.colorRamp = project.listColorRamps("Yellow-Orange-Brown (7 classes)")[0]

                            ## update the selected layer's symbology with the modified copy
                            layer.symbology = symbology

                            arcpy.AddMessage("Finshing Generating Layer.")
                        else:
                            print("No Layers to update.")
        except Exception:
            arcpy.AddError("General error during copy:")
            arcpy.AddError(traceback.format_exc().splitlines()[-1])
            raise

        ## increment progressor
        arcpy.SetProgressorPosition(start + step * 3) ## move to 99%   
        arcpy.SetProgressorLabel("Saving new project ...")
        time.sleep(readTime)    # pause the execution
        arcpy.AddMessage("Saving new project ...")     

        ## param 2 is the folder and param 3 is the target project name    
        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")       

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
