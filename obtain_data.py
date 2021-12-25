# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 19:08:10 2021
"""

import numpy as np
import griddb_python as griddb
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    # Get GridStore object
    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    # Define the container names
    language_tag_container = "language_tag_container"

    # Get the containers
    language_tag_data = gridstore.get_container(language_tag_container)
    
    # Fetch all rows - language_tag_container
    query = language_tag_data.query("select *")
    
    rs = query.fetch(False)
    print(f"{language_tag_container} Data")

    
    # Iterate and create a list
    retrieved_data= []
    while rs.has_next():
        data = rs.next()
        retrieved_data.append(data)

    # Convert the list to a pandas data frame
    by_tag_year = pd.DataFrame(retrieved_data, 
                                          columns=["ID","year","tag", "number", "year_total"])

    # Get the data frame details
    print(by_tag_year)
    by_tag_year.info()
    
    
    
    
    
except griddb.GSException as e:
    for i in range(e.get_error_stack_size()):
        print("[", i, "]")
        print(e.get_error_code(i))
        print(e.get_location(i))
        print(e.get_message(i))
        
#introducing fraction column
by_tag_year_fraction = by_tag_year.assign(fraction = by_tag_year['number']/by_tag_year['year_total'])


#Python tag over the years 2008-2018
python_over_time = by_tag_year_fraction[by_tag_year_fraction['tag'] == 'python']

python_over_time.plot.line(x = "year", y = "fraction")
plt.savefig("Figures/python_over_time.jpeg", dpi=200)
plt.show()

#few important python libraries
selected_tags = ["matplotlib","pandas", "numpy", "seaborn"]

selected_tags_over_time = by_tag_year_fraction[by_tag_year_fraction['tag'].isin(selected_tags)]

sns.lineplot(data=selected_tags_over_time , x='year', y='fraction', hue='tag')
plt.savefig("Figures/libraries_over_time.jpeg", dpi=200)
plt.show()

#highest six tags
sorted_tags = by_tag_year[['tag','number']].copy().groupby('tag').sum().sort_values(by=
                                                            ['number'], ascending=False)

top6_tags = sorted_tags.head(n=6).index.to_list()

by_tag_subset = by_tag_year_fraction[by_tag_year_fraction['tag'].isin(top6_tags)]

sns.lineplot(data=by_tag_subset , x='year', y='fraction', hue='tag')
plt.savefig("Figures/top6_over_time.jpeg", dpi=200)
plt.show()
