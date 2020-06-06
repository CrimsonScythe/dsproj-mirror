import pandas as pd
from sklearn import linear_model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


class Baselines:
    def __init__(self):
        super().__init__()
    
        # prepare datasets
        dfTrain = pd.read_csv("train.csv")
        dfTest = pd.read_csv("valid.csv")
        dfliar = pd.read_csv("test.tsv", sep='\t')
        dfkaggle = pd.read_json("test_set.json")

        X_train = dfTrain['content']
        y_train = pd.to_numeric(dfTrain['type_id'])

        X_test_corp = dfTest['content']
        y_test_corp = pd.to_numeric(dfTest['type_id'])

        X_test_liar = dfliar.iloc[:, 2].to_numpy()
        y_test_liar = dfliar.iloc[:, 1]

        X_test_kaggle = dfkaggle.iloc[: , 1].to_numpy()
        ids_kaggle = dfkaggle.iloc[:, 0]
        
        self.X_train = self.vectorizeX(X_train)
        self.y_train = y_train

        self.X_test_corp = self.vectorizeX(X_test_corp)
        self.y_test_corp = y_test_corp

        self.X_test_liar = self.vectorizeX(X_test_liar)
        self.y_test_liar = y_test_liar.map(self.encodeLiar)

        self.X_test_kaggle = self.vectorizeX(X_test_kaggle)
        self.ids_kaggle = ids_kaggle

        # prepare models
        self.SVM = linear_model.SGDClassifier(max_iter=1000, tol=1e-3)
        self.NN = KNeighborsClassifier(n_neighbors=5)
        self.MNB = MultinomialNB()
        self.DT = DecisionTreeClassifier(max_depth=None)

    def vectorizeX(self, input):

        count_vect = CountVectorizer(ngram_range=(1,2))
        input_train_counts = count_vect.fit_transform(input)

        tf_transformer = TfidfTransformer().fit(input_train_counts)
        return tf_transformer.transform(input_train_counts)

    # 56% acc. if half-true is encoded as 1, 35% otherwise
    def encodeLiar(self, y):
        if (y=="true" or y=="mostly-true") or y=="half-true":
            return 1
        else:
            return 0

    def __train(self, model, Xtest):

      # we need to either append 0 columns to the test set,
        # so it matches the size of the training set
        # but that does not scale as the dataset is large,
        # so we truncate the training set instead.

        print(self.X_train.shape)
        print(Xtest.shape)

        trunc = self.X_train[:, :Xtest.shape[1]]

        print(trunc.shape)

        model.fit(trunc, self.y_train)

    
    def test_corp(self, modelName: str, model):

        # train on corp
        # truncating is handled by self.train see above
        self.__train(model, self.X_test_corp)

        score = model.score(self.X_test_corp, self.y_test_corp)
        print(modelName+'corpus accuracy:'+str(score))

    def test_liar(self, modelName: str, model):

        self.__train(model, self.X_test_liar)

        score = model.score(self.X_test_liar, self.y_test_liar)
        print(modelName+'liar accuracy:'+str(score))

    def decodeKaggle(self, x):
        if (x==0):
            return 'FAKE'
        else:
            return 'REAL'

    def test_kaggle(self, modelName: str, model):

        self.__train(model, self.X_test_kaggle)

        predictions = model.predict(self.X_test_kaggle)
        tr=0
        fl=0
        for x in predictions:
            if (x==0):
                fl+=1
            else:
                tr+=1
        print("reals"+str(tr))
        print("fakes"+str(fl))     

        labels = pd.DataFrame(data=predictions, columns=['label']).applymap(self.decodeKaggle)
        print(labels)

        self.ids_kaggle = self.ids_kaggle.to_frame()
        self.ids_kaggle.columns = ['id']

        kaggle_res = self.ids_kaggle.join(labels)

        kaggle_res.to_csv('predictions.csv', index=False)


'''
Note.
1.The string you pass for the model name can be anything.
It is only used in print statements.
2. Remember to pass the model from the instantiated class itself. i.e. baselines.SVM
'''

'''
Example usage below
'''
baselines = Baselines()
baselines.test_corp("SVM", baselines.SVM)
baselines.test_liar("SVM", baselines.SVM)
baselines.test_kaggle("SVM", baselines.SVM)
