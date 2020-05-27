import torch
import pandas as pd
import torch.nn as nn
from limit_dataset import LimitDataSet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
import numpy as np

# attempt at a neural network
# fails miserably 

class NeuralNet(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(NeuralNet, self).__init__()
        self.layer1 = nn.Linear(in_dim, in_dim)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(in_dim, out_dim)

    def forward(self, x):
        res = self.layer1(x)
        res = self.relu(res)
        res = self.layer2(res)
        return res

#######################

df = LimitDataSet.createDataFrame(10)


# we need to explicitly convert the type ids to ints
Y = pd.to_numeric(df['type_id'])
X = df['content']


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X)


tf_transformer = TfidfTransformer().fit(X_train_counts)
X = tf_transformer.transform(X_train_counts)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)

def func(x):
    if (x==0):
        return 0
    elif (x==1):
        return 1    
    elif (x==6):
        return 2
    elif (x==10):
        return 3
    elif (x==14):
        return 4
    elif (x==15):
        return 5
    elif (x==27):
        return 6
    elif (x==42):
        return 7               
    elif (x==132):
        return 8
    elif (x==136):
        return 9
    elif (x==351):
        return 10
    elif (x==397):
        return 11
    elif (x==628):
        return 12        

#######################
X_train = X_train.toarray()
y_train = y_train.map(func)
y_train = y_train.to_numpy()

X_test = X_test.toarray()
y_test = y_test.map(func)
y_test = y_test.to_numpy()

# print(type(X_train))
# print(type(y_train))
print(X_train.shape)
print(y_train.shape)
in_dim = X_train.shape[1]
out_dim = y_train.shape[0]
net = NeuralNet(in_dim, 13)           
loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr = 0.02)
# train
net.train()

x = torch.from_numpy(X_train)
y = torch.from_numpy(y_train)

acc=0.0
for t in range(1):
    print(y)
    # print(y)
    y_pred = net(x.float())
    print(y_pred.shape)
    print(y.shape)
    loss = loss_func(y_pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# test

net.eval()
loss_total = 0
y_pred = net(torch.from_numpy(X_test).float())
loss = loss_func(y_pred, torch.from_numpy(y_test))
loss_total += loss
print(loss_total/X_test.shape[0])
# print(y_test)
# print(y_pred)
print(y_pred[0])
value, index = torch.max(y_pred[0],0)
print(value)
print(index)
y_pred_real = []

for i in range(y_pred.shape[0]):
    y_pred[0]
    value, index = torch.max(y_pred[i],0)
    # ttt = index.numpy()[0]
    # print(index.numpy().item(0))
    y_pred_real.append(index.numpy().item(0))

print("real")
print(y_test)    
print("output")
print(y_pred_real)

sum=0
for j in range(len(y_pred_real)):
    if (y_pred_real[j] == y_test[j]):
        sum+=1
print(sum/len(y_pred_real))        