# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:18:11 2019

@author: cc
"""

from __future__ import absolute_import, division, print_function
import numpy as np
from gensim.models import Word2Vec
from keras.preprocessing.sequence import pad_sequences
import keras
import jieba

model_w2v = Word2Vec.load("data/nlpcc2018/nlpcc2018.w2v")
print("load model")
words = jieba.lcut('今天心情真好')
model_encode = keras.models.load_model("data/nlpcc2018/encode.model")
model_bi = []
for i in range(5):
    model_bi.append(keras.models.load_model("data/nlpcc2018/bi/2018_bi_"+str(i+1)+".model"))
model_re = keras.models.load_model("data/nlpcc2018/2018_2.model")

def analyse(text):
    words = jieba.lcut(text)
    x = model_w2v[words]
    x = x.reshape([1,x.shape[0],x.shape[1]])
    
    pre_x = pad_sequences(x, 128, dtype='float32')
    y1 = model_encode.predict(pre_x)
    y_temp = np.binary_repr(np.argmax(y1),5)
    y1 = np.array([int(temp) for temp in y_temp])
    #print(np.argmax(y1))
    print(y1)
    
    y2=[]
    for i in range(5):
        pre_x = pad_sequences(x, 128, dtype='float32')
        y_temp = model_bi[i].predict(pre_x)
        y2.append(np.argmax(y_temp))
        #print(np.argmax(y2))
    y2 = np.array(y2)
    print(y2)
    
    pre_x = pad_sequences(x, 128, dtype='float32')
    y3_temp = model_re.predict(pre_x)[0]
    y3 = np.array([0,0,0,0,0])
    for i in range(len(y3_temp)):
        if y3_temp[i]>0.1:
            y3[i] = 1
    #print(np.argmax(y3))
    print(y3)
    y = y1+y2+y3
    for i in range(len(y)):
        if y[i]>1:
            y[i] = 1
        else:
            y[i] = 0
    
    return y.tolist()
