import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import psycopg2

# sample_data = pd.read_csv("1mio-raw.csv", dtype={'id': int, 'domain': object, 'type': object, 'url': object, 'content': object,
# 'scraped_at': object, 'inserted_at': object, 'updated_at': object, 'title': object, 'authors': object, 'keywords': object, 'meta_description': object,
# 'tags': object, 'summary': object})


sample_data = pd.read_csv("news_sample.csv")

sample_data['summary'] = sample_data['summary'].to_frame().replace(np.nan, '<NULL>', regex=True)
sample_data['summary'] = sample_data['summary'].to_frame().replace('[,]', '\,', regex=True)
sample_data['meta_description'] = sample_data['meta_description'].to_frame().replace(np.nan, '<NULL>', regex=True)
sample_data['meta_description'] = sample_data['meta_description'].to_frame().replace('[,]', '\,', regex=True)

# sample_data['url'].to_frame().to_csv('web.csv', index=True, header=False)
val = sample_data['url'].to_frame().join(sample_data['id'].to_frame())

# val = sample_data['id'].to_frame().join(dfs)
val.to_csv('web.csv', index=True, header=False)

# sample_data['content'].to_csv('articlecontent.csv', index=False, header=True)

# print(val)

# CSV is opened so it can be copied
f = open('web.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'webpage', columns=('domain_id','url', 'article_id'), sep=',')
conn.commit()
cur.close()
