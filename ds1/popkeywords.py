
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

# load data
sample_data = pd.read_csv("news_sample.csv", usecols = ['authors'])

# we clean the data by
# keeping only the first name and discarding the rest
for i in range(len(sample_data)):
    dirty_authors = sample_data.at[i, 'authors']

    if pd.isnull(dirty_authors):
        sample_data.at[i, 'authors'] = '<NULL>'

    if not pd.isnull(dirty_authors) and "," in dirty_authors:
        splitted = dirty_authors.split(',')    
        
        sample_data.at[i, 'authors'] = splitted[0]


# cleaned data is converted to CSV
sample_data.to_csv('authors.csv', index=True, header=False)

# CSV is opened so it can be copied
f = open('authors.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'author', sep=',')
conn.commit()
cur.close()
