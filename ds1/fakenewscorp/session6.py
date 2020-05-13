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
num_docs=1000

conn1 = psycopg2.connect(host = "localhost", dbname="postgres", user="postgres", password="root")
cur1 = conn1.cursor() 
cur1.execute('SELECT content FROM article ORDER BY article_id LIMIT 1000;')
content = cur1.fetchall()
# content is a list
# content[0] is a tuple
# content[0][0] is a str

cur2 = conn1.cursor('foo')
cur2.execute('SELECT type_id FROM is_type ORDER BY article_id LIMIT 1000;')
types = cur2.fetchall()

t_list = map(lambda  x: x[0],types)
t_list=list(t_list)

print("\nMAP\n")

s_list = map(lambda x: x[0],content)
s_list = list(s_list)


for x in s_list:
    
    f_dict = dict()
    # string=x[0] #convert from typle to str
    lst = x.split()
    wCount = len(lst)
    # add words to vocabulary list
    counted = False
    tempList=list()

    
    for y in lst:
        if y not in tempList: # add words to templist
            tempList.append(y) # such that templist only contains unique words
        if y not in v_list:
            v_list.append(y)    # add the new word to the voc. list
            idf_l.append({'word':y, 'freq':0}) # add new word to dict
            zList=[0]*num_docs  #create empty list with zeroes for the new word
            zList[index] = 1    # the word has frequency 1 in the current doc
            l.append({'word': y, 'freq':zList, 'sfreq':0}) # add dict to list

            # idf_l.append({'word':y, 'freq':1})
            # print(v_list) 
            # print(l)
        else:
            # find the dict containing the word and update the frequency
            # print("1")
            l_index = next((i for i, item in enumerate(l) if item["word"] == y), None)
            l[l_index]['freq'][index]=l[l_index]['freq'][index]+1
            # print("2")
    
    # print("three")
    # calcualte  the inf value
    for dic in l:
        dic['freq'][index] = dic['freq'][index]/wCount
        

    # recall that templist contains all unique words from the current article
    # as it contains unique words we only count the occurence of any word once even if it appears multiple times in a document
    # print("four")
    for elem in tempList:
        if elem in v_list:
            # here we update the frequency of the word
            # so no matter how many tiems it appears in this particualr docuemnt
            # if it appears then we increment the frequency by one
            # ival = next((i for i, item in enumerate(idf_l) if item["word"] == elem), None)
            # idf_l[ival]['freq'] = idf_l[ival]['freq']+1 # update doc count 
            ival = next((i for i, item in enumerate(l) if item["word"] == elem), None)
            l[ival]['sfreq'] = l[ival]['sfreq']+1 # update doc count 

    # print("five")
    # print(str((index/5000)*100))
    index+=1


# at this point the list l contains dicts where the key of 
# each dict is a unique word. The value of each dict is a list
# containing the frequency of the word in the i'th document 
# the freq is divided by the total number of words in the doc
# so it actually contains the tf value

# for elem in content:
    string = elem[0]
    lst = string.split()
    lst = list(set(lst)) # remove duplicates
    for word in lst:
        if word in v_list: # then must also be in ldf
            ival = next((i for i, item in enumerate(idf_l) if item["word"] == word), None)
            idf_l[ival]['freq'] = idf_l[ival]['freq']+1 # update doc count 

# next we calculate the idf by dividng the frequency 
# of each word by the total number of docs and taking log of that
# for dicts in idf_l:
#     dicts['freq'] = math.log(num_docs/dicts['freq'])
print('1')
for dic in l:
    dic['sfreq'] = math.log(num_docs/dic['sfreq'])
    for elems in dic["freq"]:
        elems = elems * dic['sfreq'] # multiiiply tf value with inf value to get final result 

print('2')


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(s_list)
print(X_train_counts.shape)

tf_transformer = TfidfTransformer().fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
# print(X_train_tf.shape)

# X = X_train_tf
# Y = t_list
# clf = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
# clf.fit(X, Y)

# print(X)

# print("x shape"+str(X.shape))
# print("\n") 


X = list(map(lambda x: x['freq'], l))

numpy_array = np.array(X)
transpose = numpy_array.T


X=transpose.tolist()

# print("x1 shape"+str(X1.shape))

# X = X_train_tf

Y = t_list

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)

# print(X)

clf2 = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
clf2.fit(X_train, y_train)


# score1=clf.score(s_list, t_list)]

# this implicitly calls predict() 
score2=clf2.score(X_test, y_test)

# print("score1 "+str(score1))
print("score2 "+str(score2))
