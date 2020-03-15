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

i=0


def chunk_preprocessing(sample_data):

    """
    Commented out code below because it was giving trouble with nan values.
    Will have to revisit it later when the regex part is fixed.
    """

    # sample_data.at[i,'content'] = clean(sample_data.at[i,'content'], lower=True, no_urls = True, no_numbers=False, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)
    # print(type(sample_data['content']))
    # re.sub(r'([A-Z])', replacement, sample_data['content'])
    # sample_data['content'].replace(to_replace=r'([A-Z])', value='2', regex=True)

    # if not(sample_data['title'].isna().item()):
    #     sample_data['title'] = sample_data['title'].str.lower()

    # if not(sample_data['content'].isna().item()):
    #     sample_data['content'] = sample_data['content'].str.lower()

    # if not(sample_data['meta_description'].isna().item()):
    #     sample_data['meta_description'] = sample_data['meta_description'].str.lower()

    # if not(sample_data['meta_keywords'].isna().item()):
    #     sample_data['meta_keywords'] = sample_data['meta_keywords'].str.lower() 

    # if not(sample_data['tags'].isna().item()):
    #     sample_data['tags'] = sample_data['tags'].str.lower() 

    # if not(sample_data['summary'].isna().item()):
    #     sample_data['summary'] = sample_data['summary'].str.lower()   


    """commas, + is probably not necessary"""
    sample_data['content'].replace(to_replace=r'[,]+', value='s', regex=True, inplace=True)

    """whitespaces and tabs"""
    sample_data['content'].replace(to_replace=r'[ \t]{2,}', value='s', regex=True, inplace=True) 
    
    """newline"""
    sample_data['content'].replace(to_replace=r'[\n]+', value='s', regex=True, inplace=True)
    

    sample_data['title'].replace(to_replace=r'[,]+', value='s', regex=True, inplace=True)
    sample_data['title'].replace(to_replace=r'[ \t]{2,}', value='s', regex=True, inplace=True) #whitespaces and tabs
    sample_data['title'].replace(to_replace=r'[\n]+', value='s', regex=True, inplace=True) #newline

    sample_data['summary'].replace(to_replace=r'[,]+', value='s', regex=True, inplace=True)
    sample_data['summary'].replace(to_replace=r'[ \t]{2,}', value='s', regex=True, inplace=True) #whitespaces and tabs
    sample_data['summary'].replace(to_replace=r'[\n]+', value='s', regex=True, inplace=True) #newline

    sample_data['meta_description'].replace(to_replace=r'[,]+', value='s', regex=True, inplace=True)
    sample_data['meta_description'].replace(to_replace=r'[ \t]{2,}', value='s', regex=True, inplace=True) #whitespaces and tabs
    sample_data['meta_description'].replace(to_replace=r'[\n]+', value='s', regex=True, inplace=True) #newline

    """detects \. because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes"""
    sample_data['content'].replace(to_replace=r'(\\\.)', value='s', regex=True, inplace=True) 
 

    sample_data['title'].replace(to_replace=r'(\\\.)', value='s', regex=True, inplace=True)


    sample_data['summary'].replace(to_replace=r'(\\\.)', value='s', regex=True, inplace=True)


    sample_data['meta_description'].replace(to_replace=r'(\\\.)', value='s', regex=True, inplace=True)


    """detects \ because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes"""
    sample_data['content'].replace(to_replace=r'(\\)', value='s', regex=True, inplace=True)
 
 

    sample_data['title'].replace(to_replace=r'(\\)', value='s', regex=True, inplace=True)


    sample_data['summary'].replace(to_replace=r'(\\)', value='s', regex=True, inplace=True)


    sample_data['meta_description'].replace(to_replace=r'(\\)', value='s', regex=True, inplace=True)

    """detects " because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes"""
    sample_data['content'].replace(to_replace=r'(\")', value='s', regex=True, inplace=True)
 
 

    sample_data['title'].replace(to_replace=r'(\")', value='s', regex=True, inplace=True)


    sample_data['summary'].replace(to_replace=r'(\")', value='s', regex=True, inplace=True)


    sample_data['meta_description'].replace(to_replace=r'(\")', value='s', regex=True, inplace=True)
    


    return sample_data 

chunk_list = []
chunksize = 2000

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']
df_chunk = pd.read_csv("1mio-raw.csv", chunksize=chunksize, usecols=col_names, low_memory=True, nrows=500000)

array = []
months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
days = r'(?:[0-31]\d[,.]?) '
year = r'?(?:19[7-9]\d|2\d{3})? '
white_space = r'^\s*$'

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']

for chunk in df_chunk:
    
    chunk_filter = chunk_preprocessing(chunk)

 
    i=i+1

    if i % 2 == 0:
        print(i)

    chunk_list.append(chunk_filter)
    

df = pd.concat(chunk_list)    


# print(df)

print("one")

""" speeds up runtime of the program. 
Could give errors! """
df['inserted_at'] = df['inserted_at'].astype(str) 
df['scraped_at'] = df['scraped_at'].astype(str) 
df['updated_at'] = df['updated_at'].astype(str) 

dfs = [
    df['content'],
    df['title'],
    df['summary'], 
    df['meta_description'],
    df['inserted_at'],
    df['scraped_at'],
    df['updated_at']
    ]

print("two")
val = df['id'].to_frame().join(dfs)

print("three")
val.to_csv('yolo.csv', index=False, header=False)


# # CSV is opened so it can be copied
print("four")
f = open('yolo.csv', encoding="utf8")

print("five")
# # # writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'article', columns=('article_id', 'content', 'title', 'summary', 'meta_description', 'inserted_at',
'scraped_at', 'updated_at'), sep=',')
conn.commit()
cur.close()
