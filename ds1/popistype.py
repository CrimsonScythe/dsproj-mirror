import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import csv
import psycopg2


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

i=0
var = 'NULL'
# load data

def chunk_preprocessing(sample_data, dict):
          
    """
    skip the row if id is not an int
    this occured at one point
    """          
    bol=pd.to_numeric(sample_data['id'], errors='coerce').notnull().all()
    if (bol == False):
        return None

    if (pd.isnull(sample_data['type'].all())):
        return None
    
    

    sample_data['type'].replace(dict, inplace=True)

    # for index, row in sample_data.iterrows():
    #     if (pd.isnull(row['type'])):
    #         continue
    #     row['type'] = dict[row['type']]
        # print(row['id'], row['type'])

    # print(sample_data)
    

    return sample_data    

conn1 = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur1 = conn1.cursor() 
cur1.execute('SELECT * FROM article_type;')
types = cur1.fetchall()
temp_dict = dict(types)
# swap keys and values
my_dict = dict((v,k) for k,v in temp_dict.items())


df_chunk = pd.read_csv("1mio-raw.csv", chunksize=2000, usecols = ['id', 'type'])


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
    
    chunk_filter = chunk_preprocessing(chunk, my_dict)

    if (chunk_filter is None):
        continue
    
    i=i+1
    
    if i % 2 == 0:
        print(i)

    chunk_list.append(chunk_filter)
    

df = pd.concat(chunk_list)   
df['type'] = df['type'].fillna(397)
df['type'] = df['type'].astype(int)
df.to_csv('is_type.csv', index=False, header=False)


print('5')
# CSV is opened so it can be copied
f = open('is_type.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'is_type', sep=',')
conn.commit()
cur.close()
