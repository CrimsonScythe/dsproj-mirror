import pandas as pd
import psycopg2
import numpy as np
from collections import defaultdict


tf_dict = dict()
idf_dict = dict()
max_dict = dict()

l = list()

conn1 = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur1 = conn1.cursor() 
cur1.execute('SELECT content FROM article LIMIT 10000;')
content = cur1.fetchall()
# content is a list
# content[0] is a tuple
# content[0][0] is a str


for x in content:
    f_dict = dict()
    string=x[0] #convert from typle to str
    lst = string.split()
    wCount = len(lst)
    for y in lst:
        if y not in f_dict:
            f_dict[y]=1
        else:
            f_dict[y] = f_dict[y]+1    
    # we divide by total number of words which gives the tf score
    for key in f_dict:
        f_dict[key] = f_dict[key]/wCount

    # we append the dict to the list
    if len(f_dict) > len(max_dict):
        max_dict=f_dict

    l.append(f_dict)

# at this point the list l contains a dict for each document where each
# dict has unique words and tf scores for those words
# the list index corresponds to the document number


# we need to fill in the missing values for the dicts
# so that they that all contain the same keys, wit default value 0
# we use set operations 

for d in l:
    if (d==max_dict):
        continue
    missing_keys = set(max_dict.keys()) - set(d.keys())
    for k in missing_keys:
        d[k] = 0


# now we need to merge the dicts so that similar words are grouped together 

# the code is from here
# https://stackoverflow.com/questions/5946236/how-to-merge-multiple-dicts-with-same-key



dd = defaultdict(list)


for d in l: # you can list as many input dicts as you want here
    for key, value in d.items():
        dd[key].append(value)


   