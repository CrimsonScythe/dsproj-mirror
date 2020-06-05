# -*- coding: utf-8 -*-
"""predictor_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tFwLoXlCO-sv_VA0KdHq1_JyYRwqC1Fv
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import functools
import numpy as np
from limit_dataset import LimitDataSet
import pandas as pd
import tensorflow_datasets as tfds

# prepare LIAR dataset
# ##################

def func(x):
    if (x=="true" or x=="mostly-true" ):
        return 1
    elif(x=="false" or x=="barely-true" or x=="pants-fire" or x=="half-true"):
        return 0

df_liar = pd.read_csv('test.tsv', sep='\t')
Xd = df_liar.iloc[:,2]
Yd = df_liar.iloc[:,1]

X_arr = Xd.to_numpy()

Y_arr = Yd.map(func)
Y_arr = Y_arr.to_numpy()

liar_x = X_arr
liar_y = Y_arr

####################

BATCH_SIZE = 10

train_data = pd.read_csv("train.csv")
valid_data = pd.read_csv("valid.csv")
test_data = pd.read_csv("test.csv")


train_x = train_data['content'].to_numpy()
train_y = train_data['type_id'].to_numpy()

valid_x = valid_data['content'].to_numpy()
valid_y = valid_data['type_id'].to_numpy()

test_x = test_data['content'].to_numpy()
test_y = test_data['type_id'].to_numpy()



train_dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
valid_dataset = tf.data.Dataset.from_tensor_slices((valid_x, valid_y))
test_dataset = tf.data.Dataset.from_tensor_slices((test_x, test_y))
liar_dataset = tf.data.Dataset.from_tensor_slices((liar_x, liar_y))

# print(train_dataset)
# print(valid_dataset)
# print(test_dataset)

# for element, inde in train_dataset:
  # print(element.numpy())
  # print(inde)


tokenizer = tfds.features.text.Tokenizer()

vocabulary_set = set()

# only build vocabulary on training set
for content, _ in train_dataset:
  some_tokens = tokenizer.tokenize(content.numpy())
  vocabulary_set.update(some_tokens)

vocab_size = len(vocabulary_set)

encoder = tfds.features.text.TokenTextEncoder(vocabulary_set)

# example_text = next(iter(train_dataset))[0].numpy()
# encoded_example = encoder.encode(example_text)

# print(example_text)
# print(encoded_example)

def encode(text_tensor, label):
  encoded_text = encoder.encode(text_tensor.numpy())
  return encoded_text, label

def encode_map_fn(text, label):
  # py_func doesn't set the shape of the returned tensors.
  encoded_text, label = tf.py_function(encode, 
                                       inp=[text, label], 
                                       Tout=(tf.int64, tf.int64))

  # `tf.data.Datasets` work best if all components have a shape set
  #  so set the shapes manually: 
  encoded_text.set_shape([None])
  label.set_shape([])

  return encoded_text, label


train_encoded_data = train_dataset.map(encode_map_fn)  
valid_encoded_data = valid_dataset.map(encode_map_fn)  
test_encoded_data = test_dataset.map(encode_map_fn)
liar_encoded_data = liar_dataset.map(encode_map_fn)

train_batches = train_encoded_data.padded_batch(BATCH_SIZE)
valid_batches = valid_encoded_data.padded_batch(BATCH_SIZE)
test_batches = test_encoded_data.padded_batch(BATCH_SIZE)
liar_batches = liar_encoded_data.padded_batch(BATCH_SIZE)

embedding_dim=16

model = keras.Sequential([
  layers.Embedding(encoder.vocab_size, embedding_dim),
  layers.GlobalAveragePooling1D(),
  layers.Dense(16, activation='relu'),
  layers.Dense(1)
])

model.summary()


model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(
    train_batches,
    epochs=1,
    )


result = model.evaluate(test_batches)
dict(zip(model.metrics_names, result))

result_liar = model.evaluate(liar_batches)
dict(zip(model.metrics_names, result_liar))

# putting half-true in false gives much higher accuracy :)
# it is opposite in the SVM model
# please report this in the report

