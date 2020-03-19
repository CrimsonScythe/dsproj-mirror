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

print("File: poparticleoptimized.py")

i=0

"""
cleans data for article
and copies the data to local db
"""

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

    #if not(sample_data['meta_keywords'].isna().any()):
    #    sample_data['meta_keywords'] = sample_data['meta_keywords'].str.lower() 

    #if not(sample_data['tags'].isna().any()):
    #    sample_data['tags'] = sample_data['tags'].str.lower() 

    if not(sample_data['summary'].isna().any()):
        sample_data['summary'] = sample_data['summary'].str.lower() 
        
          
    """
    skip the row if id is not an int
    this occured at one point
    """          
    bol=pd.to_numeric(sample_data['id'], errors='coerce').notnull().all()
    if (bol == False):
        return None



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

    return sample_data 

chunk_list = []

col_names =  [
            'id',
            #'domain',
            #'type',
            #'url',
            'content',
            'scraped_at',
            'inserted_at',
            'updated_at',
            'title',
            #'authors',
            #'keywords',
            #'meta_keywords',
            'meta_description',
            #'tags',
            'summary'
            ]


reader = pd.read_csv(
    "1mio-raw.csv",
    chunksize = 2000,
    usecols = col_names,
    low_memory = True,
    dtype = {
            #'id': int,
            #'domain',
            #'type',
            #'url',
            'content': str,
            'scraped_at': str,
            'inserted_at': str,
            'updated_at': str,
            'title': str,
            #'authors',
            #'keywords',
            #'meta_keywords',
            'meta_description': str,
            #'tags',
            'summary': str
             },
    sep="," # default
    )

array = []
months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
days = r'(?:[0-31]\d[,.]?) '
year = r'?(?:19[7-9]\d|2\d{3})? '
white_space = r'^\s*$'

# already declared further up?
# col_names =  ['id', 'domain', 'type', 'url', 'content', 'scraped_at', 'inserted_at', 'updated_at', 'title', 'authors', 'keywords', 'meta_keywords', 'meta_description', 'tags', 'summary']


def custom_for_loop(readerObj, function):
    firstFrame = function(next(readerObj))
    print(firstFrame)

    done_looping = False
    print("START iteration over reader-object")
    while not done_looping:
        try:
            df = next(readerObj)
        except StopIteration:
            print("STOP iteration over reader-object")
            done_looping = True
        except TypeError as msg:
            print(msg)
            exit()

        else:
            x = function(df)
            firstFrame = firstFrame.append(x)
            print(firstFrame)

    return firstFrame


complete_df = custom_for_loop(reader, chunk_preprocessing)

print("--------------------------------------------------")
print("------------------ COMPLETE DF -------------------")
print(complete_df)


"""
for df in reader:
    
    chunk_filter = chunk_preprocessing(df)

    if (chunk_filter is None):
        continue
 
    i=i+1

    if i % 2 == 0:
        print(i*chunksize)

    chunk_list.append(chunk_filter)
    

df = pd.concat(chunk_list)    
"""




# print(df)

print("one")

""" speeds up runtime of the program. 
Could give errors!(strikethrough) """
#df['inserted_at'] = df['inserted_at'].astype(str) 
#df['scraped_at'] = df['scraped_at'].astype(str) 
#df['updated_at'] = df['updated_at'].astype(str) 

""" extracts columns """
dfs = [
    complete_df['content'],
    complete_df['title'],
    complete_df['summary'], 
    complete_df['meta_description'],
    complete_df['inserted_at'],
    complete_df['scraped_at'],
    complete_df['updated_at']
    ]

print("two")
"""
nifty function to join all dfs
"""
val = complete_df['id'].to_frame().join(dfs)

print("three")
"""
save final df in csv
"""
val.to_csv('article_clean.csv', index=False, header=False, sep=",")

# # CSV is opened so it can be copied
print("four")
"""
open it here for use in the copy_from function below
"""
f = open('article_clean.csv', encoding="utf8")

print("five")
# # # writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'article', columns=('article_id', 'content', 'title', 'summary', 'meta_description', 'inserted_at',
'scraped_at', 'updated_at'), sep=',')
conn.commit()
cur.close()
