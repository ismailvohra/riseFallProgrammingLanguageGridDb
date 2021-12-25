# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 18:54:58 2021
"""

import griddb_python as griddb
import sys
import pandas as pd

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    #Reading csv file
    language_tag_unprocessed = pd.read_csv("by_tag_year.csv")
    
    #preprocessing
    language_tag_unprocessed['tag'] = language_tag_unprocessed['tag'].fillna("No tag")
    
    language_tag_unprocessed.index.name = 'ID'
    
    #save it into csv
    language_tag_unprocessed.to_csv("preprocessed.csv")
    
    #read the cleaned data from csv
    language_tag_data = pd.read_csv("preprocessed.csv")

    for row in language_tag_data.itertuples(index=False):
            print(f"{row}")

    # View the structure of the data frames
    language_tag_data.info()

    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    #Create container 
    language_tag_container = "language_tag_container"

    # Create containerInfo
    language_tag_containerInfo = griddb.ContainerInfo(language_tag_container,
                    [["ID", griddb.Type.INTEGER],
        		    ["year", griddb.Type.INTEGER],
         		    ["tag", griddb.Type.STRING],
                    ["number", griddb.Type.INTEGER],
                    ["year_total", griddb.Type.INTEGER]],
                    griddb.ContainerType.COLLECTION, True)
    
    language_tag_columns = gridstore.put_container(language_tag_containerInfo)

    print("container created and columns added")
    
    
    # Put rows
    language_tag_columns.put_rows(language_tag_data)
    
    print("Data Inserted using the DataFrame")

except griddb.GSException as e:
    print(e)
    for i in range(e.get_error_stack_size()):
        print(e)
        # print("[", i, "]")
        # print(e.get_error_code(i))
        # print(e.get_location(i))
        print(e.get_message(i))