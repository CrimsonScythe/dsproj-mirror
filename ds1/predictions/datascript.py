from limit_dataset import LimitDataSet
import pandas as pd

df = LimitDataSet.createDataFrame(5000)

def func(x):
    # pass
    if (x=="true" or x=="mostly-true"):
    #     print("yes")
        return 1
    elif(x=="false" or x=="barely-true" or x=="pants-fire"  or x=="half-true"):
        return 0


# print(df.shape[0])
#
train_size = 0.8 * df.shape[0]
test_size = 0.1 * df.shape[0]
val_size = 0.1 * df.shape[0]
#
# # 0 ..
df_train = df.iloc[:int(train_size), :]
df_test = df.iloc[int(train_size):int(train_size)+int(test_size), :]
df_valid = df.iloc[int(train_size)+int(test_size):, :]
#
# print(df_train.shape)
# print(df_test.shape)
# print(df_valid.shape)
#
df_train.to_csv('train.csv', index=False)
df_test.to_csv('test.csv', index=False)
df_valid.to_csv('valid.csv', index=False)

df_liar = pd.read_csv('test.tsv', sep='\t')
# Xd = df_liar.iloc[:,2]
# Yd = df_liar.iloc[:,1]

# X_arr = Xd.to_numpy()
#
# Y_arr = Yd.map(func)
# Y_arr = Y_arr.to_numpy()
#
# print(X_arr)
# print(Y_arr)