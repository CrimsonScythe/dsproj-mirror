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


def chunk_preprocessing(sample_data, dict):
  

    sample_data['url'].replace(to_replace=r'[,]', value='', regex=True, inplace=True)


    sample_data['domain'].replace(dict, inplace=True)

    """ force convert id to int, converting non numeric values to nan """

    sample_data['id']=pd.to_numeric(sample_data['id'], errors='coerce')
    
    sample_data['id'] = sample_data['id'].astype('Int64')

    sample_data['domain'] = sample_data['domain'].astype('Int64')
    
    """ leave out the nan value """

    sample_data = sample_data[sample_data['id'].notna()]


    return sample_data    

conn1 = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur1 = conn1.cursor() 
cur1.execute('SELECT * FROM domain;')
types = cur1.fetchall()
temp_dict = dict(types)
# swap keys and values
my_dict = dict((v,k) for k,v in temp_dict.items())


df_chunk = pd.read_csv("1mio-raw.csv", chunksize=2000, usecols = ['id', 'url', 'domain'])


chunk_list = []


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
df.to_csv('web.csv', index=False, header=False)


print('5')
# CSV is opened so it can be copied
f = open('web.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'webpage', sep=',')
conn.commit()
cur.close()
