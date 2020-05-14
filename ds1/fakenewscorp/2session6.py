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
num_docs=5000

conn1 = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur1 = conn1.cursor() 
cur1.execute('SELECT content FROM article ORDER BY article_id LIMIT 5000;')
content = cur1.fetchall()
# content is a list
# content[0] is a tuple
# content[0][0] is a str

cur2 = conn1.cursor('foo')
cur2.execute('SELECT type_id FROM is_type ORDER BY article_id LIMIT 5000;')
types = cur2.fetchall()

t_list = map(lambda  x: x[0],types)
Y=list(t_list)

print("\nMAP\n")

contentList = map(lambda x: x[0],content)
contentList = list(contentList)



# print(s_list)
print(type(contentList[0]))

voc_set = set()

# voc_list = list()

X = list()

for item in contentList:
    word_list = item.split()
    for word in word_list:
        voc_set.add(word)
    

# convert set to dict automatically assigning indexes as values
# 
dic = {k: v for v, k in enumerate(voc_set)}

np_idf = np.zeros((len(voc_set)))


# print("ddd")
voc_list = list(voc_set)
hello=""
for item in contentList: # for every document in the list of documents
    c_list = [0] * len(voc_set) # a list for every docuemnt containing count of every word in voc list
    word_list = item.split()
    num_words = len(word_list)
    temp_set = set()
    for word in word_list:
        # index=0
        # index = voc_list.index(word) # we find the index of each word. As the index does not change in the voc list this remians consistent across all words in all docuemts
        index = dic[word] # this used to be a list, but it was super slow. Switched to dict and it seems like everything now runs in O(1) :)
        c_list[index]=c_list[index]+1 # update the frequency
        
        if word not in temp_set:# if word has not been seen before then add 1
            np_idf[index]+=1

        temp_set.add(word) # add to set indicating that the word has been counted, so if it appears again in the same document it will njot be counted

    new_list = map(lambda x: x/num_words, c_list) # we calcualte the tf score
    X.append(c_list) # we append each c list to the master list

        # we divide the frequencies in the 

# this is fast
np_idf = np.log(np.divide(num_docs, np_idf))

# this takes slightly longer
np_arr = np.array(X)

# multiply each idf with value with the correspondig inf
# this gives the inf-df value
X_result = np.multiply(np_arr, np_idf)

print("done set up")

X_train, X_test, y_train, y_test = train_test_split(X_result, Y, test_size=0.33, random_state=1)

clf = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
clf.fit(X_train, y_train)

score = clf.score(X_test, y_test)

print("score "+str(score))

# got 73% accuracy