# -*- coding: utf-8 -*-

import arcpy


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
        ## define progressor variables
        readTime = 3    # time for users to read progress
        start = 0       # start position of progressor
        max = 100       # end position of progressor
        step = 33       # progress interval 

        ## initiate progressor
        arcpy.SetProgressor("step", "Validating project file ...", start, max, step)
        ## sleep
        time.sleep(readTime)    # pause the exection for 3 seconds

        ## alert user of progress with message to Results pane
        arcpy.AddMessage("Validating project file ...")

        ## set project variable
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        ## set campus variable to the first map from the source project
        campus = project.listMaps()[0]

        ## increment progressor
        arcpy.SetProgressorPosition(start + step)
        ## alert user of progress with message to Results pane
        arcpy.SetProgressorLabel("Finding map layer ...")
        ## pause execution again
        time.sleep(readTime)    # pause the exection for 3 seconds

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
