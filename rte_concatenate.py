__author__ = 'DHICKMA'


def rte_concatenate(table, group_field="RTE_ID", from_field="FROM_DFO", to_field="TO_DFO",
                    concatenate_field_name="CONCATENATE", mark_overlap=True, overlap_field_name="OVERLAPS"):
    """
    Adds a field for route concatenate and populates a concatenation index. This value marks records that belong
    to the same linear segment. Optionally, checks for overlapping measures.

    Example 1:
    route_concatenate("C:\\Test.gdb\\test")

    Example 2:
    route_concatenate("C:\\Test.gdb\\test", "Route_ID", "FRM_Mea", "TO_Mea", "Concat", True, "Overlap")

    Args:
        table_name (str): Full path to the route table
        group_field (str, optional): Field name containing field for concatenation ("RTE_ID","C_SEC"); default: "RTE_ID"
        from_field (str, optional): Field name containing from measure; default: "FROM_DFO"
        to_field (str, optional): Field name containing to measure; default: "TO_DFO"
        concatenate_field_name (str, optional): Specify custom name for concatenate field
        mark_overlap (boolean, optional): Mark if the measures are overlapping; default: True
        overlap_field_name (str, optional): Specify custom name for concatenate field; default: "RTE_OVERLAP"
    """

    # Import arcpy module
    import arcpy
    import time

    # Establish start time
    start_time = time.time()

    # Create field list to check that valid field exists
    field_list = arcpy.ListFields(table)
    add_field_list = [concatenate_field_name]

    # Add field for marking overlap if specified by user
    if mark_overlap is True:
        add_field_list.append("overlap_field_name")

    # Iterate through table, checking if the add field already exist
    for field in field_list:
        if field.name == concatenate_field_name:
            add_field_list.remove(concatenate_field_name)
        elif field.name == overlap_field_name and mark_overlap is True:
            add_field_list.remove(overlap_field_name)
    del field_list

    # If valid field does not exist, add the field
    if len(add_field_list) == 0:
        pass
    else:
        for field in add_field_list:
            print "Adding Field: {0}".format(field)
            arcpy.AddField_management(table, field, "LONG")

    # Create update cursor to populate the concatenation value
    sort_string = str("{0} A; {1} A".format(group_field, from_field))
    fields_subset = "[group_field, from_field, to_field, concatenate_field_name, overlap_field_name]"
    rows = arcpy.UpdateCursor(table, "", "", fields_subset, sort_string)
    row = rows.next()

    # Create baseline variables
    previous = ""
    previous_to = ""
    counter = 0
    concatenate_index = 1

    # begin cursor
    while row:
        current = row.getValue(group_field)
        current_from = row.getValue(from_field)
        current_to = row.getValue(to_field)

        # Sets initial values for the first record in the table
        if counter == 0:
            row.setValue(concatenate_field_name, concatenate_index)
            row.setValue(overlap_field_name, 0)

        # Marks a records as belonging to the same segment as previous
        elif previous == current and previous_to >= current_from:
            row.setValue(concatenate_field_name, concatenate_index)
            if mark_overlap is True:
                if previous_to > current_from:
                    row.setValue(overlap_field_name, 1)
                else:
                    row.setValue(overlap_field_name, 0)

        # Marks the first record of a new segment in the same route
        elif previous == current and previous_to < current_from:
            concatenate_index += 1
            row.setValue(concatenate_field_name, concatenate_index)
            row.setValue(overlap_field_name, 0)

        # Marks the first record of a new route
        else:
            concatenate_index = 1
            row.setValue(concatenate_field_name, concatenate_index)
            row.setValue(overlap_field_name, 0)

        # Sets the current records as previous for the next row
        previous = current
        previous_to = current_to

        # Saves changes to the current row and get the next row object
        rows.updateRow(row)
        row = rows.next()

        # Increment's counter value and print progress feedback
        counter += 1
        print counter

    del row, rows
    end_time = time.time()
    print "Elapsed time: {0}".format(time.strftime('%H:%M:%S', time.gmtime(end_time - start_time)))
