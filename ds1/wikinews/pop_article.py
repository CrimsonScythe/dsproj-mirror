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
print([header for header in df.columns])

dfs = [
    df['title'],
    df['content'],
    df['inserted_at'],
    df['updated_at'],
    df['scraped_at'],
    ]
val = df['article_id'].to_frame().join(dfs)
print(val)
val.to_csv('article_clean.csv', index=False, header=False)


f = open('article_clean.csv', encoding="utf8")




# # # writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor()
#cur.execute("SELECT * FROM pg_tables WHERE schemaname = 'wikinews'")
cur.execute("SELECT * FROM information_schema.columns WHERE table_schema = 'wikinews' AND table_name = 'article'")
res = cur.fetchall()
table_columns = [line[3] for line in res]
print("Columns found in table 'article' in db:\n", table_columns)


cur.copy_from(f, 'postgres.wikinews.article', sep=',')
conn.commit()
cur.close()
