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

# We wanna make an array of arrays, with the tokenization of one content field, being in one array.

# array = []
# months = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may(?:ch)?|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)(?:[.,]?) '
# days = r'(?:[0-31]\d[,.]?) '
# year = r'?(?:19[7-9]\d|2\d{3})? '
# white_space = r'^\s*$'
# for i in range(len(sample_data)):
#     token_array = []
#     dirty_content = sample_data.at[i,'content']
#     # dirty_content.replace("\n", " ")
#     sample_data.at[i,'content'] = clean(sample_data.at[i,'content'], lower=True, no_urls = True, no_numbers=False, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)

#     if (i == 1):
#         x = re.sub(months+days+year+'(?=\D|$)', '<DATE>' ,sample_data.at[i,'content'])
#         # if successful assign clean_content to x
#         if x:
#             sample_data.at[i,'content'] = x
#         # make another call to re.sub with a different ordering of the regex
#         # out of a conditional since it doesn't need to depend on the result of the previous
#         # call
#         x = re.sub(days+months+year+'(?=\D|$)', '<DATE>' ,sample_data.at[i,'content'])
#         if x:
#             sample_data.at[i,'content'] = x

#     # call clean() again to replace numbers with arg being clean_content
#     sample_data.at[i,'content'] = clean(sample_data.at[i,'content'], lower=True, no_urls = True, no_numbers=True, no_line_breaks=True, replace_with_url="<URL>", replace_with_number="<NUM>", fix_unicode=True)

    
#     # sample_data.at[i,'content'] = sample_data.at[i,'content'].split()
#     sample_data.at[i,'content'] = re.sub('[,]', '\,' ,sample_data.at[i,'content'])

#     sample_data.at[i,'title'] = re.sub('[,]', '\,' ,sample_data.at[i,'title'])

#     # sample_data.at[i,'summary'] = re.sub('[,]', '\,' ,sample_data.at[i,'title'])
sample_data['summary'] = sample_data['summary'].to_frame().replace(np.nan, '<NULL>', regex=True)
sample_data['summary'] = sample_data['summary'].to_frame().replace('[,]', '\,', regex=True)
sample_data['meta_description'] = sample_data['meta_description'].to_frame().replace(np.nan, '<NULL>', regex=True)
sample_data['meta_description'] = sample_data['meta_description'].to_frame().replace('[,]', '\,', regex=True)




# dfs = [sample_data['id'].to_frame(), sample_data[''].to_frame()]

# sample_data['url'].to_frame().to_csv('web.csv', index=True, header=False)
sample_data['id'].to_frame().to_csv('new.csv', index=True, header=False)


# CSV is opened so it can be copied
f = open('new.csv', encoding="utf8")

# writing to DB
conn = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur = conn.cursor() 
cur.copy_from(f, 'written_by', columns=('author_id','article_id'), sep=',')
conn.commit()
cur.close()
