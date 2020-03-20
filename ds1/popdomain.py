
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

var = 'NULL'
# load data

def chunk_preprocessing(sample_data):
          
    """
    skip the row if id is not an int
    this occured at one point
    """          
    bol=pd.to_numeric(sample_data['id'], errors='coerce').notnull().all()
    if (bol == False):
        return None

    return sample_data    

df_chunk = pd.read_csv("1mio-raw.csv", chunksize=2000, usecols = ['id', 'domain'])


chunk_list = []
"""
chunksize of 2000 was optimal for my system
"""
# chunksize = 2000

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']
# df_chunk = pd.read_csv("1mio-raw.csv", chunksize=chunksize, usecols=col_names, low_memory=True)

array = []

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']

for chunk in df_chunk:
    
    chunk_filter = chunk_preprocessing(chunk)

    if (chunk_filter is None):
        continue
 
    # i=i+1

    """
    print progress
    """
    # if i % 2 == 0:
        # print(i)

    chunk_list.append(chunk_filter)
    

df = pd.concat(chunk_list)   


# sample_data = sample_data.replace(np.nan, var, regex=True)


# cleaned data is converted to CSV
# 
val = df['id'].to_frame().join(df['domain'])
val.to_csv('domain.csv', index=False, header=False)




# CSV is opened so it can be copied
f = open('domain.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'domain', sep=',')
conn.commit()
cur.close()
