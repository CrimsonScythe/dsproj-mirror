import pandas as pd
import psycopg2
import numpy as np
from collections import defaultdict
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import linear_model
from sklearn.model_selection import train_test_split

tf_dict = dict()
idf_dict = dict()

v_list = list()
l = list()
idf_l = list()

index=0
num_docs=4000

conn1 = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur1 = conn1.cursor() 
cur1.execute('SELECT content FROM article ORDER BY article_id LIMIT 2000;')
content = cur1.fetchall()
# content is a list
# content[0] is a tuple
# content[0][0] is a str

cur2 = conn1.cursor('foo')
cur2.execute('SELECT type_id FROM is_type ORDER BY article_id LIMIT 2000;')
types = cur2.fetchall()

t_list = map(lambda  x: x[0],types)
t_list=list(t_list)

print("\nMAP\n")

contentList = map(lambda x: x[0],content)
contentList = list(contentList)

# print(s_list)
print(type(contentList[0]))

voc_set = set()

# voc_list = list()


for item in contentList:
    word_list = item.split()
    for word in word_list:
        voc_set.add(word)
    

# convert set to dict automatically assigning indexes as values
# 
dic = {k: v for v, k in enumerate(voc_set)}



# print("ddd")
voc_list = list(voc_set)
hello=""
for item in contentList: # for every document in the list of documents
    c_list = [0] * len(voc_set) # a list for every docuemnt containing count of every word in voc list
    word_list = item.split()
    for word in word_list:
        # index=0
        # index = voc_list.index(word) # we find the index of each word. As the index does not change in the voc list this remians consistent across all words in all docuemts
        index = dic[word] # this used to be a list, but it was super slow. Switched to dict and it seems like everything now runs in O(1) :)
        c_list[index]=c_list[index]+1 # update the frequency
        # we now have the frequencuies however we still need to 
        # calculate the TF score
        
        # we divide the frequencies in the 

print("done")