
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
sample_data = pd.read_csv("1mio-raw.csv", usecols = ['id', 'keywords'], nrows=100000)

# sample_data_cleaned = sample_data.replace(np.nan, '<NULL>', regex=True)

sample_data = sample_data.replace(np.nan, var, regex=True)

# cleaned data is converted to CSV
# 
sample_data.to_csv('keywords.csv', index=False, header=False)

# CSV is opened so it can be copied
f = open('keywords.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'keyword', sep=',')
conn.commit()
cur.close()
