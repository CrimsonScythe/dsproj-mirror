import pandas as pd
import numpy as np
import csv
from limit_dataset import LimitDataSet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import scipy

# test file nothing important

def func(x):
    # pass
    if (x=="true" or x=="mostly-true" or x=="half-true"):
    #     print("yes")
        return 42
    elif(x=="false" or x=="half-true" or x=="barely-true" or x=="pants-fire"):
        return 27
    # elif x is None:
    #     return 1000    

df1 = pd.read_csv('test.tsv', sep='\t')
# print(df1.iloc[:,1])
# extracting labels
print(type(df1.iloc[:,1]))
# extracting text
print(type(df1.iloc[:,2]))

Xd = df1.iloc[:,2]
Yd = df1.iloc[:,1]


X_arr = Xd.to_numpy()
# Y_arr = Y.to_numpy()
# print(Y_arr)

# contentList = map(lambda x: x[0],content)
Y_arr = Yd.map(func)
print(Y_arr)
df = LimitDataSet.createDataFrame(1000)


# we need to explicitly convert the type ids to ints
Y = pd.to_numeric(df['type_id'])
X = df['content']

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X)
print(X_train_counts.shape)

tf_transformer = TfidfTransformer().fit(X_train_counts)
X = tf_transformer.transform(X_train_counts)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)

####################
# SVM CLASSIFIER 

SVM = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
SVM.fit(X_train, y_train)


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_arr)
print(X_train_counts.shape)
print(Y_arr.shape)

tf_transformer = TfidfTransformer().fit(X_train_counts)
X_arr = tf_transformer.transform(X_train_counts)
print(type(X_arr))
# value error becuase trained on the original dataset. the number of 
# features are 47905 which is actually the vocabulary size,
# however when running predict on a new dataset, the vocubalry size is only
# 4348, so we must fill in 0s to make it upto 47905

# we need to append these many zero columns
num_cols = X_train.shape[1] - X_arr.shape[1]
zeros = np.zeros((X_arr.shape[0], num_cols), dtype=np.int)
print(zeros)
X_res=scipy.sparse.hstack([X_arr, zeros]).toarray()
# X_res = np.concatenate((X_arr.toarray(), zeros), axis=1)

# print(X_arr)
score = SVM.score(X_res, Y_arr)
print(score)