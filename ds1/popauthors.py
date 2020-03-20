import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import csv
import psycopg2


print("File: popauthors.py")

# load data
# note that this returns a TextFileReader object, not a dataframe. 
# Iterating over it, will yield dataframes. By using chunksizes, we'll
# refer to the dataframes as chunks (valid point?)
reader = pd.read_csv(
    "1mio-raw.csv", 
    usecols = ['authors'],
    low_memory = True,
    chunksize = 2000,
    # if we use low_memory=True, we should aim to tell pandas 
    # what the type of the columns should be, to avoid mixed type inference. 
    # in this case, it's probably trivial, as we're only using the authors column.
    dtype = {'authors': str}
    )


def process_dfs(readerObj):
    firstFrame = next(reader)
    firstFrame.drop_duplicates(inplace=True)
    done_looping = False
    print("START iteration over reader-object")
    i = 0
    while not done_looping:
        try:
            df = next(readerObj)
        except StopIteration:
            print("STOP iteration over reader-object")
            done_looping = True
        else:
            df.drop_duplicates(inplace = True)
            firstFrame = firstFrame.append(df)
            print(i*2000/1000000*100, "%")
            i += 1

    return firstFrame

complete_df = process_dfs(reader)

complete_df.to_csv('author_clean.csv', index=False, header=False, sep=",")

f = open('author_clean.csv', encoding="utf8")

conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'author', sep=',')
conn.commit()
cur.close()




"""
# for DataFrame in TextFileReader object
# for chunk in reader
for df in tfReader:
    df.drop_duplicates(inplace=True) # keep='first' is default
    df_list.append(df)
"""




"""
for i in range(len(sample_data)):
    dirty_authors = sample_data.at[i, 'authors']

    if pd.isnull(dirty_authors):
        # print(dirty_authors)
        sample_data.at[i, 'authors'] = '<NULL>'

    if not pd.isnull(dirty_authors):
        if ("," in dirty_authors):
            splitted = dirty_authors.split(',')    
            sample_data.at[i, 'authors'] = splitted[0]
        else :
            if (dirty_authors.split() != 2):
                sample_data.at[i, 'authors'] = dirty_authors.split()[0] 
            # print(dirty_authors)




# cleaned data is converted to CSV
sample_data.to_csv('authors.csv', index=True, header=False)

# CSV is opened so it can be copied
f = open('authors.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'author', sep=',')
conn.commit()
cur.close()
"""