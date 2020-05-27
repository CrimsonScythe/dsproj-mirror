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
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

df = LimitDataSet.createDataFrame(1000)


# we need to explicitly convert the type ids to ints
Y = pd.to_numeric(df['type_id'])
X = df['content']

count_vect = CountVectorizer(ngram_range=(1,2))
X_train_counts = count_vect.fit_transform(X)
print(X_train_counts.shape)

tf_transformer = TfidfTransformer().fit(X_train_counts)
X = tf_transformer.transform(X_train_counts)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)

####################
# SVM CLASSIFIER WITH LINEAR KERNEL

SVM = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
SVM.fit(X_train, y_train)
score = SVM.score(X_test, y_test)

print("SVM score "+str(score))
# parameters = {'loss':('hinge', 'log', 'modified_huber'),
#  'penalty':('l2', 'l1', 'elasticnet')}
# clf = GridSearchCV(estimator=linear_model.SGDClassifier(), param_grid=parameters, n_jobs=-1)
# clf.fit(X_train, y_train)
# print("SVM best score" + str(clf.best_score_))
# print("best params" + str(clf.best_params_))
####################

####################
# SVM CLASSIFIER WITH NON-LINEAR KERNEL

# SVC = SVC(C=1.0, kernel='rbf', degree=4, gamma='scale', coef0=0.0)
# SVC.fit(X_train, y_train)
# score = SVC.score(X_test, y_test)

# print("SVC score" + str(score))

# parameters = {'C':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], 'kernel':('rbf', 'poly', 'sigmoid'),
#  'degree':[3], 'gamma':('scale', 'auto')}
# clf = GridSearchCV(estimator=SVC(), param_grid=parameters, n_jobs=-1)
# clf.fit(X_train, y_train)
# print("SVC best score" + str(clf.best_score_))
# print("best params" + str(clf.best_params_))

# parameters = {'kernel':('rbf', 'poly', 'sigmoid')}
# clf = GridSearchCV(estimator=SVC(), param_grid=parameters, n_jobs=-1)
# clf.fit(X_train, y_train)
# print("SVC best score" + str(clf.best_score_))
# print("best params" + str(clf.best_params_))


####################

####################
# NN classifier

# default n value is also 5
# NN = KNeighborsClassifier(n_neighbors=5)
# NN.fit(X_train, y_train)
# score = NN.score(X_test, y_test)



# print("NN score "+str(score))
# parameters = {'n_neighbors':[1,2,3,4,5], 'weights':('uniform', 'distance')}
# clf = GridSearchCV(estimator=KNeighborsClassifier(), param_grid=parameters, n_jobs=-1)
# clf.fit(X_train, y_train)
# print("NN best score" + str(clf.best_score_))
# print("best params" + str(clf.best_params_))
####################

# ####################
# # NB classifier

# # this is Multinomial Naive Bayes (Gaussian did not work as it required a dense matrix whereas the matrix we have is sparse
# # also it looks like Multinomial is better for text classification according to GHUB and SO)
# # there are also other variants which are perhaps better
# MNB = MultinomialNB() 
# MNB.fit(X_train, y_train)
# score = MNB.score(X_test, y_test)

# print("MNB score "+str(score))
# parameters = {'alpha':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], 'fit_prior':('True', 'False')}
# clf = GridSearchCV(estimator=MultinomialNB(),
#  param_grid=parameters, n_jobs=-1)
# clf.fit(X_train, y_train)
# print("MNB best score" + str(clf.best_score_))
# print("best params" + str(clf.best_params_))


####################

####################
# DT classifier


# DT = DecisionTreeClassifier(max_depth=None) 
# DT.fit(X_train, y_train)
# score = DT.score(X_test, y_test)

# print("DT score "+str(score))
# parameters = {'criterion':('gini', 'entropy'), 'splitter':('best', 'random')}
# clf = GridSearchCV(estimator=DecisionTreeClassifier(),
#  param_grid=parameters, n_jobs=-1)
# clf.fit(X_train, y_train)
# print("DT best score" + str(clf.best_score_))
# print("best params" + str(clf.best_params_))



# ####################

# ####################

# clf = AdaBoostClassifier(n_estimators=1000)
# clf.fit(X_train, y_train)
# score = clf.score(X_test, y_test)

# print("SCORE"+str(score))
# ####################


# ####################
# # Using grid search here

# GridSearchCV

# ####################