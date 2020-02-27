# -*- coding: utf-8 -*-

"""

First, you will have to perform the following steps to create a clean version of the data (see below for suggestions about which libraries to use):

1. Read the CSV file
2. In the content field, do the following:
- Tokenize and lower-case the text (end result should be an array of tokens where each token is a lexical unit or a punctuation).
  For example, “He said: ‘Don’t go there!’” => (he, said, :, ‘, don’t, go, there, !, ‘)
- Remove consecutive spaces and new lines
- Find and replace URLs with <URL>
- Find and replace dates with <DATE>
- Find and replace numbers with <NUM>
3. For the metadata fields:
- Fill all empty fields with a placeholder NULL

Next, perform an exploratory evaluation of the cleaned data and report the results. The exploration can include (but need not be limited to):
- counting the number of URLs in the data
- counting the number of dates in the data
- counting the number of numeric values in the data
- determining the 100 more frequent words that appear in the data
- plotting the frequency of the 10000 most occuring words (do you seen any interesting patterns?)

If you don't yet have a working copy of Python of our computer, please see the exercises from last week. We recommend using Anaconda with Python 3.* (https://docs.conda.io/en/latest/miniconda.html).

You will want to use the following python packages for performing these tasks:
clean-text - for cleaning the text (https://pypi.org/project/clean-text/)
datetime - for date/time conversions (https://docs.python.org/3/library/datetime.html)"""

import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re

sample_data = pd.read_csv("news_sample.csv")

# We wanna make an array of arrays, with the tokenization of one content field, being in one array.

array = []
months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
days = '(?:[0-31]\d[,.]?) '
year = '?(?:19[7-9]\d|2\d{3})? '
white_space = '^\s*$'
for i in range(len(sample_data)):
    token_array = []
    dirty_content = sample_data.at[i,'content']
    # dirty_content.replace("\n", " ")
    clean_content = clean(dirty_content, lower=True, no_urls = True, no_numbers=False, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)

    if (i == 1):
        x = re.sub(months+days+year+'(?=\D|$)', '<DATE>' ,clean_content)
        # if successful assign clean_content to x
        if x:
            clean_content = x
        # make another call to re.sub with a different ordering of the regex
        # out of a conditional since it doesn't need to depend on the result of the previous
        # call
        x = re.sub(days+months+year+'(?=\D|$)', '<DATE>' ,clean_content)
        if x:
            clean_content = x

    # call clean() again to replace numbers with arg being clean_content
    clean_content = clean(clean_content, lower=True, no_urls = True, no_numbers=True, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)

    clean_content = clean_content.split()

    token_array.append(clean_content)
    array.append(token_array)
# print(array)

meta_data = pd.read_csv("news_sample.csv", usecols = ['meta_description'])
# print(meta_data)
meta_data_cleaned = meta_data.replace(np.nan, 'NULL', regex=True)
# print(meta_data_cleaned)
meta_con = pd.read_csv("news_sample.csv", usecols = ['meta_keywords'])
# print(meta_con)
meta_con_cleaned = meta_con.replace('[\'\']', 'NULL')
# print(meta_con_cleaned)
