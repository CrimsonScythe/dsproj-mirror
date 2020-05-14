import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import psycopg2
import time
import math
from io import StringIO

"""
open it here for use in the copy_from function below
"""

df = pd.read_csv("wikinews_data_clean.csv", low_memory=True)

dfs = [
	df['domain_id'],
	df['url']
	]

val = df['article_id'].to_frame().join(dfs)

# free up resources
del df

print(val)
val.to_csv('domain_clean.csv', index=True, header=False)

f = open('domain_clean.csv', encoding="utf8")

# # # writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor()
#cur.execute("SELECT * FROM pg_tables WHERE schemaname = 'wikinews'")
cur.execute("SELECT * FROM information_schema.columns WHERE table_schema = 'wikinews' AND table_name = 'domain'")
res = cur.fetchall()
table_columns = [line[3] for line in res]
print("Columns found in table 'domain' in db:\n", table_columns)
print([header for header in val.columns])

cur.copy_from(f, 'postgres.wikinews.article', sep=',')
conn.commit()
cur.close()
