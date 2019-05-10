# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:58:58 2019

@author: cc
"""
from __future__ import absolute_import, division, print_function
import pickle
import numpy as np
from gensim.models import Word2Vec
from keras.models import Sequential
from keras import layers
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint
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

for i in range(5):
    epochs = 100
    
    model = Sequential()
    model.add(layers.LSTM(64,input_shape=(X.shape[1],128)))
    model.add(layers.Dense(2,activation='softmax'))
    model.compile(loss = "categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    
    tensorboad = TensorBoard(log_dir='log')
    checkpoint = ModelCheckpoint(filepath='../data/nlpcc2018/bi/2018_bi_'+str(i+1)+'.model',monitor='val_acc',mode='auto' ,save_best_only='True')

    callback_lists=[checkpoint]
    print("train"+'-'*20)
    model.fit(X, to_categorical(y.T[i]), validation_data=(x_test,to_categorical(y_test.T[i])), epochs=epochs, batch_size=200, verbose=2,callbacks=callback_lists)
    
    
    scores = model.evaluate(x_test, to_categorical(y_test.T[i]), verbose=0)
    print("Model Accuracy: %.2f%%" % (scores[1]*100))
    
    model.summary()
    #model.save('../data/nlpcc2018/bi/2018_bi_'+str(i+1)+'.model')
