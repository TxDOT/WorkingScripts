'''
Created by David Hickman
david.hickman [@] txdot.gov
'''

import arcpy
from arcpy import env
import os
from xlwt import Workbook
from xlrd import open_workbook,cellname

def gatherDbStats(database_name, db_source):
    env.workspace = db_source
    db_Dict = {}
    dataset_list = arcpy.ListDatasets()
    table_list = arcpy.ListTables()
    for table in table_list:
        count = int(arcpy.GetCount_management(table).getOutput(0))
        fields = arcpy.ListFields(str(table))
        field_list = []
        for field in fields:
            field_list.append(str(field.name))
        desc = arcpy.Describe(table)
        print "Table: {0}".format(desc.baseName.split(".")[1])
        print "...Row Count: {0}".format(count)
        db_Dict[str(env.workspace) + os.sep + str(table)] = {"path": "Home", "name": format(desc.baseName.split(".")[1]), "object_type": "table", "row_count": count, "fields": field_list}
        print db_Dict
        break
    for dataset in dataset_list:
        print "Dataset: {0}".format(dataset.split(".")[2])
        env.workspace = db_source + os.sep + dataset
        feature_list = arcpy.ListFeatureClasses()
        ds_table_list = arcpy.ListTables()
        for fc in feature_list:
            count = int(arcpy.GetCount_management(fc).getOutput(0))
            fields = arcpy.ListFields(fc)
            field_list = []
            for field in fields:
                field_list.append(str(field.name))
            desc = arcpy.Describe(fc)
            shape_type = str(desc.shapeType)
            print "...Feature Class: {0}".format(desc.baseName.split(".")[2])
            print "......Feature Type: {0}".format(desc.featureType)
            print "......Shape Type: {0}".format(desc.shapeType)
            print "......Feature Count: {0}".format(count)
            print "......Spatial Index: {0}".format(desc.hasSpatialIndex)
            print "......Measures: {0}".format(desc.hasM)
            print "Workspace: {2} Dataset: {0} FC: {1}".format(dataset, fc, env.workspace)
            db_Dict[str(env.workspace) + os.sep + str(fc)] = {"path": format(dataset.split(".")[2]), "name":format(desc.baseName.split(".")[2]), "object_type": "feature class", "shape_type": shape_type, "feature_count": count, "fields": field_list}
            print db_Dict
            break
        for ds_table in ds_table_list:
            count = int(arcpy.GetCount_management(ds_table).getOutput(0))
            fields = arcpy.ListFields(str(ds_table))
            field_list = []
            for field in fields:
                field_list.append(str(field.name))
            desc = arcpy.Describe(ds_table)
            print "...Table: {0}".format(desc.baseName.split(".")[2])
            print "......Row Count: {0}".format(count)
            db_Dict[str(env.workspace) + os.sep + str(ds_table)] = {"path":format(dataset.split(".")[2]), "name": format(desc.baseName.split(".")[2]), "object_type": "table", "row_count": count, "fields": field_list}
            print db_Dict
            break
        break
    writeOutputFile(db_Dict)

def writeOutputFile(db_dict):
    book = Workbook()
    path_list = []
    index_sheet = book.add_sheet("Index")
    index_list = []
    counter = 0
    for k,v in db_dict.iteritems():
        obj_name = k.split("\\")[2:3]
        if obj_name not in index_list:
            print "obj_name: {0}".format(obj_name)
            index_list.append(obj_name)
            index_sheet.write(counter, 0,str(obj_name))
            counter += 1

    book.save("C:\\Users\\DHICKMA\\Dropbox\\testing.xls")

gatherDbStats("Comanche", "Database Connections\\Connection to Comanche.sde")