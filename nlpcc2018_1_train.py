# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:58:58 2019

@author: cc
"""
from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pickle
import numpy as np
from gensim.models import Word2Vec
from keras.models import Sequential
from keras import layers
from keras.preprocessing.sequence import pad_sequences
import keras

#%%
data_train = 0
data_evalution = 0
with open('../data/nlpcc2018/train.pkl','rb') as f:
    data_train = pickle.load(f)
with open('../data/nlpcc2018/dev.pkl','rb') as f:
    data_evalution = pickle.load(f)

model_w2v = Word2Vec.load("../data/nlpcc2018/nlpcc2018.w2v")

x_train_embedding = 0
x_test_embedding = 0
with open('../data/nlpcc2018/train_embedding.pkl','rb') as f:
    x_train_embedding = pickle.load(f)
    
with open('../data/nlpcc2018/test_embedding.pkl','rb') as f:
    x_test_embedding = pickle.load(f)

max_len = max([len(x) for x in x_train_embedding[0]])
x_train = np.array(x_train_embedding)
X = pad_sequences(x_train, maxlen=max_len, dtype='float32')
X = np.reshape(X,(X.shape[0],max_len,128))    
y = np.array(data_train[1])

x_test = np.array(x_test_embedding)
x_test = pad_sequences(x_test,maxlen = max_len, dtype = 'float32')
x_test = np.reshape(x_test,(x_test.shape[0],max_len,128))
y_test = np.array(data_evalution[1])
#%%

epochs = 1000

model = Sequential()
model.add(layers.LSTM(64,input_shape=(X.shape[1],128)))
model.add(layers.Dense(5,activation='sigmoid'))
model.compile(loss = "binary_crossentropy", optimizer='adam', metrics=['accuracy'])

print("train"+'-'*20)
model.fit(X, y, validation_data=(x_test,y_test), epochs=epochs, batch_size=200, verbose=2)


scores = model.evaluate(x_test, y_test, verbose=0)
print("Model Accuracy: %.2f%%" % (scores[1]*100))

model.summary()
model.save('../data/nlpcc2018/2018_3.model')

