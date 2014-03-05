__author__ = 'DHICKMA'


import arcpy
from arcpy import env
import os


# Define the output folder location
output_path = "C://ControlSectionRouteTest"

# Create the output folder
print "Creating the output directory..."
os.mkdir(output_path)

# Create the file geodatabase to hold the output
print "Creating the file geodatabase..."
arcpy.CreateFileGDB_management(output_path, "ControlSectionRouteTest")

# Set the environment workspace
print "Setting the workspace variable..."
env.workspace = output_path + os.sep + "ControlSectionRouteTest.gdb"

# Allow file to be overwritten
env.overwriteOutput = True

# Define the output coordinate system
arcpy.env.outputCoordinateSystem = "GEOGCS['GCS_North_American_1983'," \
                                   "DATUM['D_North_American_1983'," \
                                   "SPHEROID['GRS_1980',6378137.0,298.257222101]]," \
                                   "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

def create_Control_Section_FC():
    '''
    Import TxDOT_Roadways and RTE_Control_Section route event table
    Route the events and export the
    '''
    # Copy Roadways from Comanche
    print "Copying the Roadways feature class..."
    arcpy.CopyFeatures_management(
        "Database Connections\Comanche USER Direct.sde\TPP_GIS.MCHAMB1.Roadways\TPP_GIS.MCHAMB1.TXDOT_Roadways",
        "Roadways_Projected")

    # Copy RTE_CONTROL_SECTION table from Comanche
    print "Copying the route event table..."
    arcpy.CopyRows_management("Database Connections\Comanche USER Direct.sde\TPP_GIS.MCHAMB1.RTE_CONTROL_SECTION",
                              "RTE_CONTROL_SECTION")

    # Make route event layer
    print "Routing the events..."
    arcpy.MakeRouteEventLayer_lr("Roadways_Projected", "RTE_ID", "RTE_CONTROL_SECTION", "RIA_RTE_ID LINE GIS_FROM GIS_TO",
                                 "Routed_CSEC")

    # Create features from route event layer
    print "Exported the routed events..."
    arcpy.CopyFeatures_management("Routed_CSEC", "CSEC_Features")