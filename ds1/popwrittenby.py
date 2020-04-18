
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
from get_unique_authors import get_authors_dict

"""
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
query = "INSERT INTO written_by (article_id, author_id) VALUES (%s, %s)"

for i in range(len(sample_data)):
    vals = (i, i)
    cur.execute(query, vals)

conn.commit()
cur.close()
"""

# get author dict that allows us to map author_name to author_id (pkey in author table)
authors_dict = get_authors_dict()

# load data
chunksize = 2000
col_names = ['id', 'authors']
tf_reader = pd.read_csv("1mio-raw.csv",
						chunksize=chunksize,
						usecols=col_names,
						low_memory=True)

conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor()
query = """INSERT INTO written_by (article_id, author_id) VALUES (%s, %s)"""

# example df: 
#  id | authors:
# " 2 | Ronnie Kasrils, Marcus Barnett, Yash Tandon, Henning Melber"

# for progress
i = 0
j = 0

for df in tf_reader:
	for index, row in df.iterrows():
		if j % chunksize == 0:
			print(i*j*chunksize / 1000000 * 100, "%")
		article_id = row['id']
		authors_string = row['authors']

		if authors_string is not np.nan:
			authors_list = (authors_string.lower()).split(",")

			for author in authors_list:
				vals = (article_id, authors_dict[author])
				#print("vals = ({}, {})".format(article_id, authors_dict[author]))
				cur.execute(query, vals)

		j += 1
	i += 1
				
conn.commit()
cur.close()





