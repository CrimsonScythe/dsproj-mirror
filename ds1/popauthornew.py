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

authors_dict = get_authors_dict()

col1_author_id = list(authors_dict.values())
col2_author_name = list(authors_dict.keys())

data_dict = {'col1': col1_author_id,
			 'col2': col2_author_name}

df = pd.DataFrame(data=data_dict, columns=['col1', 'col2'])

print(df)

df.to_csv('author.csv', index=False, header=False, sep="~")

f = open('author.csv', encoding="utf8")

conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor()
cur.copy_from(f, 'author', sep='~')
conn.commit()
cur.close()
