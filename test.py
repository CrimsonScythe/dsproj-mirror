
"""
(a) For each table, devise a script employing the text cleaning library to clean the data
(you can re-use the code/data from the earlier exercise) and
extract the data corresponding to the table from the cleaned dataset into a CSV file;

(b)  Load the CSV file into the corresponding database table by using PostgreSQL’s COPY command.
"""
import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import csv
import psycopg2
import math

# load data
# sample_data = pd.read_csv("1mio-raw.csv", usecols = ['meta_description'])
sample_data = pd.read_csv("1mio-raw.csv")
print(list(sample_data))

# sample_data_cleaned = sample_data.replace(np.nan, '<NULL>', regex=True)


# we clean the data by
# keeping only the first name and discarding the rest
# sample_data = sample_data.replace('nan', 'isa', regex=True, inplace=True)  
# for i in range(len(sample_data)):
    # dirty_authors = sample_data.at[i, 'keywords']   
    # print(dirty_authors)
    # if math.isnan(float(dirty_authors)):
        # sample_data.at[i, 'keywords'] = '<NULL>'
    # if pd.isnull(dirty_authors):
        # print(dirty_authors)
        # sample_data.at[i, 'keywords'] = '<NULL>'

        # print("yes!")
        #     print(dirty_authors)
        #     print(sample_data.at[i, 'keywords'])
        
    # if not pd.isnull(dirty_authors):
    #     if ("," in dirty_authors):
    #         splitted = dirty_authors.split(',')    
    #         sample_data.at[i, 'authors'] = splitted[0]
    #     else :
    #         if (dirty_authors.split() != 2):
    #             sample_data.at[i, 'authors'] = dirty_authors.split()[0] 
            



# cleaned data is converted to CSV
# 
# sample_data_cleaned.to_csv('domain.csv', index=True, header=False)

# # CSV is opened so it can be copied
# f = open('domain.csv', encoding="utf8")

# # writing to DB
# conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
# cur = conn.cursor() 
# cur.copy_from(f, 'domain', sep=',')
# conn.commit()
# cur.close()
