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
from sklearn.svm import SVC
import matplotlib.pyplot as plt

# visualization file, doesn't work

df = LimitDataSet.createDataFrame(50)


# we need to explicitly convert the type ids to ints
Y = pd.to_numeric(df['type_id'])
X = df['content']

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X)


tf_transformer = TfidfTransformer().fit(X_train_counts)
X = tf_transformer.transform(X_train_counts)

Xv = X.tocsr()[:,0]
print(Xv)

# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)
fig, ax = plt.subplots()
ax.scatter(X.tocsr()[:,0], X.tocsr()[:,1])
# set a title and labels
ax.set_title('Iris Dataset')
ax.set_xlabel('sepal_length')
ax.set_ylabel('sepal_width')
# Y.reshape(Y, (Y.shape[0],1))
