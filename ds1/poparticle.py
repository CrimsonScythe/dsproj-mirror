import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import psycopg2
import time
import math

chunksize = 1

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']
chunk = pd.read_csv("1mio-raw.csv", chunksize=chunksize, usecols=col_names, low_memory=True)
sample_data = pd.concat(chunk, ignore_index=True)
# We wanna make an array of arrays, with the tokenization of one content field, being in one array.

array = []
months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
days = r'(?:[0-31]\d[,.]?) '
year = r'?(?:19[7-9]\d|2\d{3})? '
white_space = r'^\s*$'

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']
df  = pd.DataFrame(columns = col_names)

for i in range(len(sample_data)):
    
    token_array = []
    dirty_content = sample_data.at[i,'content']

    print(type(sample_data.at[i,'content']))

    sample_data.at[i,'content'] = clean(sample_data.at[i,'content'], lower=True, no_urls = True, no_numbers=False, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)
   
    x = re.sub(months+days+year+'(?=\D|$)', '<DATE>' ,sample_data.at[i,'content'])
        # if successful assign clean_content to x
    if x:
        sample_data.at[i,'content'] = x
        # make another call to re.sub with a different ordering of the regex
        # out of a conditional since it doesn't need to depend on the result of the previous
        # call
    x = re.sub(days+months+year+'(?=\D|$)', '<DATE>' ,sample_data.at[i,'content'])
    if x:
        sample_data.at[i,'content'] = x

    # call clean() again to replace numbers with arg being clean_content
    sample_data.at[i,'content'] = clean(sample_data.at[i,'content'], lower=True, no_urls = True, no_numbers=True, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)

    
    # sample_data.at[i,'content'] = sample_data.at[i,'content'].split()

    sample_data.at[i,'content'] = re.sub('[,]', '\,' ,sample_data.at[i,'content'])
       
    # print(sample_data.at[i,'title'])
    # NAN
    if (not pd.isnull(sample_data.at[i,'title'])):
        sample_data.at[i,'title'] = re.sub('[,]', '\,' ,sample_data.at[i,'title'])
    
    # sample_data['summary'] = sample_data['summary'].astype(str)

    if (not pd.isnull(sample_data.at[i,'summary'])):
        sample_data.at[i,'summary'] = re.sub('[,]', '\,' ,sample_data.at[i,'summary'])


    if (not pd.isnull(sample_data.at[i,'meta_description'])):
        sample_data.at[i,'meta_description'] = re.sub('[,]', '\,' ,sample_data.at[i,'meta_description'])
    
    # print(sample_data)
    if (i==0):
        df = sample_data
        
    df.append(sample_data, ignore_index=True)

df.to_csv('yolo.csv', index=False, header=False)


dfs = [
    df['content'],
    df['title'],
    df['summary'], 
    df['meta_description'],
    df['inserted_at'],
    df['scraped_at'],
    df['updated_at']
    ]


val = df['id'].to_frame().join(dfs)
val.to_csv('yolo.csv', index=False, header=False)

# # CSV is opened so it can be copied
f = open('yolo.csv', encoding="utf8")

# # writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'article', columns=('article_id', 'content', 'title', 'summary', 'meta_description', 'inserted_at',
'scraped_at', 'updated_at'), sep=',')
conn.commit()
cur.close()
