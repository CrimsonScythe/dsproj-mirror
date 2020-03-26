import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import psycopg2

##### VIRKER IKKE.

# sample_data = pd.read_csv("1mio-raw.csv", dtype={'id': int, 'domain': object, 'type': object, 'url': object, 'content': object,
# 'scraped_at': object, 'inserted_at': object, 'updated_at': object, 'title': object, 'authors': object, 'keywords': object, 'meta_description': object,
# 'tags': object, 'summary': object})

sample_data = pd.read_csv("1mio-raw.csv")

sample_data['summary'] = sample_data['summary'].to_frame().replace(np.nan, '<NULL>', regex=True)
sample_data['summary'] = sample_data['summary'].to_frame().replace('[,]', '\,', regex=True)
sample_data['meta_description'] = sample_data['meta_description'].to_frame().replace(np.nan, '<NULL>', regex=True)
sample_data['meta_description'] = sample_data['meta_description'].to_frame().replace('[,]', '\,', regex=True)


sample_data['id'].to_frame().to_csv('tags.csv', index=True, header=False)


# CSV is opened so it can be copied
f = open('tags.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'tags', columns=('keyword_id','article_id'), sep=',')
conn.commit()
cur.close()
