
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
sample_data = pd.read_csv("1mio-raw.csv", usecols = ['authors'])


# cleaned data is converted to CSV
# 
# sample_data_cleaned.to_csv('type.csv', index=True, header=False)

# CSV is opened so it can be copied
# f = open('type.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
# cur.copy_from(f, 'type', sep=',')
query = """ INSERT INTO written_by (article_id, author_id) VALUES (%s, %s)"""

for i in range(len(sample_data)):
    vals = (i, i)
    cur.execute(query, vals)

conn.commit()
cur.close()
