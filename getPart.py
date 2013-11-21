

def get_Part():

    import arcpy

    table = "C:\\_GRID_SHAREPOINT_TEST\\4TextData\\02_20_2013\\BaseMapLayers\\ADJ_STATE_POLY.shp" # Path to a shapefile

    desc = arcpy.Describe(table)
    shapefieldname = desc.ShapeFieldName

    rows = arcpy.SearchCursor(table)

    for row in rows:
        feat = row.getValue(shapefieldname)

        print "Feature" + str(row.getValue("OBJECTID"))
        partnum = 0

        print "Part %i:" % partnum

        #for pnt in feat.getPart(partnum):
            #if pnt:
                ##print pnt.X, pnt.Y, pnt.M
            #else:
                #pass

        partnum += 1

get_Part()
