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
from get_unique_authors import get_authors_dict

i=0

"""
cleans data for article
and copies the data to local db
"""

authors_dict = get_authors_dict()

def chunk_preprocessing(sample_data):

    """
    Lower case everything
    """

    if not(sample_data['title'].isna().any()):
        sample_data['title'] = sample_data['title'].str.lower()

    if not(sample_data['content'].isna().any()):
        sample_data['content'] = sample_data['content'].str.lower()

    if not(sample_data['meta_description'].isna().any()):
        sample_data['meta_description'] = sample_data['meta_description'].str.lower()

    if not(sample_data['meta_keywords'].isna().any()):
        sample_data['meta_keywords'] = sample_data['meta_keywords'].str.lower() 

    if not(sample_data['tags'].isna().any()):
        sample_data['tags'] = sample_data['tags'].str.lower() 

    if not(sample_data['summary'].isna().any()):
        sample_data['summary'] = sample_data['summary'].str.lower() 
        
          
    """
    skip the row if id is not an int
    this occured at one point
    """          
    bol=pd.to_numeric(sample_data['id'], errors='coerce').notnull().all()
    if (bol == False):
        return None

# string = string.replace(u'\xa0', u' ')

    """for the xa0 byte, some encoding stuff which creates trouble"""
 
    sample_data['meta_keywords'].replace(to_replace=r'\\xa0', value='NULL', regex=True, inplace=True)

    sample_data['meta_keywords'].replace(to_replace=r'\[\'\'\]', value='NULL', regex=True, inplace=True)

    sample_data['meta_keywords'].replace(to_replace=r'[,]', value='', regex=True, inplace=True)
    """commas"""
    sample_data['content'].replace(to_replace=r'[,]', value='', regex=True, inplace=True)

    """whitespaces and tabs"""
    sample_data['content'].replace(to_replace=r'[ \t]{2,}', value='', regex=True, inplace=True) 
    
    """newline"""
    sample_data['content'].replace(to_replace=r'[\n]+', value='', regex=True, inplace=True)
    

    sample_data['title'].replace(to_replace=r'[,]', value='', regex=True, inplace=True)
    sample_data['title'].replace(to_replace=r'[ \t]{2,}', value='', regex=True, inplace=True) #whitespaces and tabs
    sample_data['title'].replace(to_replace=r'[\n]+', value='', regex=True, inplace=True) #newline

    sample_data['summary'].replace(to_replace=r'[,]', value='', regex=True, inplace=True)
    sample_data['summary'].replace(to_replace=r'[ \t]{2,}', value='', regex=True, inplace=True) #whitespaces and tabs
    sample_data['summary'].replace(to_replace=r'[\n]+', value='', regex=True, inplace=True) #newline

    sample_data['meta_description'].replace(to_replace=r'[,]', value='', regex=True, inplace=True)
    sample_data['meta_description'].replace(to_replace=r'[ \t]{2,}', value='', regex=True, inplace=True) #whitespaces and tabs
    sample_data['meta_description'].replace(to_replace=r'[\n]+', value='', regex=True, inplace=True) #newline

    """detects \. because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes"""
    sample_data['content'].replace(to_replace=r'(\\\.)', value='', regex=True, inplace=True) 
 

    sample_data['title'].replace(to_replace=r'(\\\.)', value='', regex=True, inplace=True)


    sample_data['summary'].replace(to_replace=r'(\\\.)', value='', regex=True, inplace=True)


    sample_data['meta_description'].replace(to_replace=r'(\\\.)', value='', regex=True, inplace=True)


    """detects \ because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes"""
    sample_data['content'].replace(to_replace=r'(\\)', value='', regex=True, inplace=True)
 
 

    sample_data['title'].replace(to_replace=r'(\\)', value='', regex=True, inplace=True)


    sample_data['summary'].replace(to_replace=r'(\\)', value='', regex=True, inplace=True)


    sample_data['meta_description'].replace(to_replace=r'(\\)', value='', regex=True, inplace=True)

    """
    Dates regex from project related exercises
    """
    sample_data['content'].replace(to_replace=days+months+year+r'(?=\D|$)', value='<DATE>', regex=True, inplace=True)

    sample_data['content'].replace(to_replace=months+days+year+r'(?=\D|$)', value='<DATE>', regex=True, inplace=True)

    sample_data['title'].replace(to_replace=days+months+year+r'(?=\D|$)', value='<DATE>', regex=True, inplace=True)

    sample_data['title'].replace(to_replace=months+days+year+r'(?=\D|$)', value='<DATE>', regex=True, inplace=True)

    sample_data['summary'].replace(to_replace=months+days+year+r'(?=\D|$)', value='<DATE>', regex=True, inplace=True)

    """
    emails, numbers and urls regex
    """
    sample_data['content'].replace(to_replace=r'\S+@\S+', value='<EMAIL>', regex=True, inplace=True)

    sample_data['summary'].replace(to_replace=r'[0-9]+', value='<NUM>', regex=True, inplace=True)

    sample_data['title'].replace(to_replace=r'[0-9]+', value='<NUM>', regex=True, inplace=True)
    
    sample_data['content'].replace(to_replace=r'[0-9]+', value='<NUM>', regex=True, inplace=True)

    sample_data['summary'].replace(to_replace=r'(https?:\/\/)?([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)', value='<URL>', regex=True, inplace=True)

    sample_data['title'].replace(to_replace=r'(https?:\/\/)?([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)', value='<URL>', regex=True, inplace=True)
    
    sample_data['content'].replace(to_replace=r'(https?:\/\/)?([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)', value='<URL>', regex=True, inplace=True)
    
    sample_data['authors'] = sample_data['authors'].map(authors_dict)

    print(sample_data['authors'])

    return sample_data 

chunk_list = []
"""
chunksize of 2000 was optimal for my system
"""
chunksize = 2000

col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']
df_chunk = pd.read_csv("1mio-raw.csv", chunksize=chunksize, usecols=col_names, low_memory=True)

months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
days = r'(?:[0-31]\d[,.]?) '
year = r'?(?:19[7-9]\d|2\d{3})? '
white_space = r'^\s*$'

for chunk in df_chunk:
    
    chunk_filter = chunk_preprocessing(chunk)

    if (chunk_filter is None):
        continue
 
    i=i+1

    """
    print progress
    """

    print(i * chunksize / 1000000 * 100, "%")

    chunk_list.append(chunk_filter)
    

df = pd.concat(chunk_list)    


# print(df)

print("one")

""" speeds up runtime of the program. 
Could give errors!(strikethrough) """
df['inserted_at'] = df['inserted_at'].astype(str) 
df['scraped_at'] = df['scraped_at'].astype(str) 
df['updated_at'] = df['updated_at'].astype(str) 

""" extracts columns """
dfs = [
    df['title'],
    df['content'],
    df['summary'], 
    df['authors'],
    df['meta_description'],
    df['meta_keywords'],
    df['inserted_at'],
    df['scraped_at'],
    df['updated_at']
    ]

print("two")
"""
nifty function to join all dfs
"""
val = df['id'].to_frame().join(dfs)

print("three")
"""
save final df in csv
"""
val.to_csv('yolo.csv', index=False, header=False)

# # CSV is opened so it can be copied
print("four")
"""
open it here for use in the copy_from function below
"""
f = open('yolo.csv', encoding="utf8")

print("five")
# # # writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'article', columns=('article_id', 'content', 'title','summary', 'authors', 'meta_description', 'meta_keywords', 'inserted_at',
'scraped_at', 'updated_at'), sep=',')
conn.commit()
cur.close()
