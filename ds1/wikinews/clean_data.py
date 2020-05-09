"""
For the wikinews, the cleaning process has been seperated from the populate scripts, to delegate responsibility!
"""
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

def clean_df(df, print_df=False):
    print("[{}][Status] Cleaning DataFrame".format(datetime.now()))

    column_names = [col for col in df.columns]
    """
    Lower case everything
    """
    for col_name in column_names:
        if not(df[col_name].isna().any()):
            df[col_name] = df[col_name].str.lower()

    """
    Insert missing 'id' column and fill 
    with values from 0 to length of df.
    """
    global cur_row_index
    df_len = len(df)
    headers = ['article_id']
    for header in df.columns:
        headers.append(header)
    df.insert(0, 'article_id', range(cur_row_index, cur_row_index + df_len))
    print(headers)
    df.columns = headers 
    # change cur_row_index for next df to be processed.
    cur_row_index = cur_row_index + df_len

    """
    detects \. because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes
    """
    for col_name in column_names:
        if not(df[col_name].isna().any()):
            df[col_name].replace(to_replace=r'(\\\.)', value='', regex=True, inplace=True) 

    """
    detects \ because it is needed to detect EOF in CSV. the extra backslashes are needed
    for escaping purposes
    """
    for col_name in column_names:
        if not(df[col_name].isna().any()):
            df[col_name].replace(to_replace=r'(\\)', value='', regex=True, inplace=True)

    """
    Replaces dates with '<DATE>'
    """
    cols = ['title', 'content']
    for col in cols:
        if not(df[col].isna().any()):
            df[col].replace(to_replace=days+months+year+r'(?=\D|$)', value='<DATE>', regex=True, inplace=True)

    """
    Replaces emails with '<EMAIL>'
    """
    cols = ['content']
    for col in cols:
        df[col].replace(to_replace=r'\S+@\S+', value='<EMAIL>', regex=True, inplace=True)


    cols = ['title', 'content']
    for col in cols:
        """
        Replaces numbers with '<NUM>'
        """
        df[col].replace(to_replace=r'[0-9]+', value='<NUM>', regex=True, inplace=True)

        """
        Replaces urls with '<URL>'
        """
        df[col].replace(to_replace=r'(https?:\/\/)?([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)', value='<URL>', regex=True, inplace=True)


    """
    for the xa0 byte, some encoding stuff which creates trouble
    """
    cols = []
    for col in cols:
        df[col].replace(to_replace=r'\\xa0', value='NULL', regex=True, inplace=True)
        df[col].replace(to_replace=r'\[\'\'\]', value='NULL', regex=True, inplace=True)
        df[col].replace(to_replace=r'[,]', value='', regex=True, inplace=True)

    """
    Remove commas, whitespaces and newlines
    """
    cols = ['content', 'title']
    for col in cols:
        df[col].replace(to_replace=r'[,]', value='', regex=True, inplace=True)
        df[col].replace(to_replace=r'[ \t]{2,}', value='', regex=True, inplace=True) 
        df[col].replace(to_replace=r'[\n]+', value='', regex=True, inplace=True)


    """
    Supply missing  
    """

    if print_df == True:
        print("Output df:\n", df)

    return df

# constants
# can be None or any number. Feel free to change.
chunksize = None

now = datetime.now()
print("[{}][Options] Chunksize =".format(now), str(chunksize))

# regex constants
months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
days = r'(?:[0-31]\d[,.]?) '
year = r'?(?:19[7-9]\d|2\d{3})? '
white_space = r'^\s*$'

# variables that change during program execution
cur_row_index = 0
cleaned_df_list = []

# load file
print("[{}][Status] Loading CSV file".format(datetime.now()))
df_reader = pd.read_csv("wikinews_data.csv", chunksize=chunksize)
print("[{}][Status] Loading done".format(datetime.now()))


if str(type(df_reader)) == "<class 'pandas.io.parsers.TextFileReader'>":
    now = datetime.now()
    print("[{}][Status] df_reader is a TextFileReader".format(now))
    i = 0
    for df in df_reader:
        # If chunksize is set, df_reader will in fact be a df_reader
        # and we can do the following processing of each df
        cleaned_df = clean_df(df, print_df=True)

        if (cleaned_df is None):
            continue

        # print progress
        i = i+1
        now = datetime.now()
        print("[{}][Progress]".format(now), i * chunksize / 5077 * 100, "%")

        cleaned_df_list.append(cleaned_df)

elif str(type(df_reader)) == "<class 'pandas.core.frame.DataFrame'>":
    now = datetime.now()
    print("[{}][Status] df_reader is a DataFrame".format(now))
    # If chunksize is False, df_reader is actually a df. 
    # There will only be one df to process then.
    cleaned_df = clean_df(df_reader, print_df=True)
    cleaned_df_list.append(cleaned_df)

else:
    now = datetime.now()
    print("[][Error] Not sure what type(df_reader) is".format(now))

df = pd.concat(cleaned_df_list) 

now = datetime.now()
print("[{}][Status] Cleaning complete".format(now))

headers = [header for header in df.columns]
print("[{}][Status] Headers in final dataframe: {}".format(now, headers))

df.to_csv('wikinews_data_clean.csv', index=False, header=True)