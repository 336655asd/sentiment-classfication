# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:18:11 2019

@author: cc
"""

from __future__ import absolute_import, division, print_function
import numpy as np
from gensim.models import Word2Vec
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import keras
import jieba
import tensorflow as tf
import sql
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#%%
# load model
model_w2v = Word2Vec.load("model/nlpcc2018.w2v")
graph = tf.get_default_graph()
global graph

global model_encode
global model_bi
global model_re
model_encode = keras.models.load_model("model/encode.model")
model_bi = []
for i in range(5):
    model_bi.append(keras.models.load_model("model/bi_"+str(i+1)+".model"))
model_re = keras.models.load_model("model/re.model")    

#%%

def analyse(text):
    global model_encode
    global model_bi
    global model_re
    global graph
    
    words = jieba.lcut(text)
    x = model_w2v[words]
    x = x.reshape([1,x.shape[0],x.shape[1]])
    #model 1
    pre_x = pad_sequences(x, 128, dtype='float32')
    with graph.as_default():
        y1 = model_encode.predict(pre_x)
    y_temp = np.binary_repr(np.argmax(y1),5)
    y1 = np.array([int(temp) for temp in y_temp])
    #print(np.argmax(y1))
    print(y1)
    # model 2
    y2=[]
    for i in range(5):
        pre_x = pad_sequences(x, 128, dtype='float32')
        with graph.as_default():
            y_temp = model_bi[i].predict(pre_x)
            y2.append(np.argmax(y_temp))
        #print(np.argmax(y2))
    y2 = np.array(y2)
    print(y2)
    
    # model 3
    pre_x = pad_sequences(x, 128, dtype='float32')
    with graph.as_default():
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
    y = y.tolist()
    print("finally result: ", y)
    return y


def retrain(epochs = 100):
    train_source = sql.select_train()
    train_x = [x[0] for x in train_source]
    train_y = [x[1] for x in train_source]
    x_cut = [jieba.lcut(text) for text in train_x]
    train_x =[model_w2v[word] for word in x_cut]
    max_len = 128
    X = pad_sequences(np.array(train_x), maxlen=max_len, dtype='float32')
    del(train_x)
    y = np.array(train_y)
    # re
    with graph.as_default():
        model_re.fit(X,y, epochs = epochs)
        model_re.save("model/re.model")
    # bi
    for i in range(5):
        with graph.as_default():
            print(20*str(i))
            print(to_categorical(y.T[i],2))
            model_bi[i].fit(X,to_categorical(y.T[i],2), epochs = epochs)
            model_bi[i].save("model/bi_"+str(i+1)+".model")
    # encode        
    encode_y = gen_label(y)
    with graph.as_default():
        model_encode.fit(X,encode_y, epochs = epochs)
        model_encode.save("model/encode.model") 
    sql.update_train()                     
    return

def gen_label(labels):
    num_labels = labels.shape[0]
    num_types = labels.shape[1]
    label_array = np.zeros(num_labels)
    for i in range(num_labels):
        label_array[i] = int(''.join([str(x) for x in labels[i]]),2)
    return to_categorical(label_array,int(pow(2,num_types)))
    
#retrain(10)
