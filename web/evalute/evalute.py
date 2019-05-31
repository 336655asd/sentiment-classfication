# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:29:32 2019

@author: cc
"""

from __future__ import absolute_import, division, print_function
import tensorflow as tf
import pickle
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import keras

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

global graph
graph = tf.get_default_graph()


data_evalution = 0
with open('data/dev.pkl','rb') as f:
    data_evalution = pickle.load(f)
    
x_test_embedding = 0
with open('../data/nlpcc2018/test_embedding.pkl','rb') as f:
    x_test_embedding = pickle.load(f)
    
max_len = 128    
x_test = np.array(x_test_embedding)
x_test = pad_sequences(x_test,maxlen = max_len, dtype = 'float32')
x_test = np.reshape(x_test,(x_test.shape[0],max_len,128))


eva_y = data_evalution[1]

#pre_y = np.array(pre_y)
eva_y = np.array(eva_y)
#eva_y = np.reshape(eva_y,[eva_y.shape[1],eva_y.shape[2]])

def predict(model_type):
    model = 0
    y_list = []
    if model_type == 'en':
        model = keras.models.load_model("data/encode.model")  
        with graph.as_default():
            y = model.predict(x_test)
        y_ten = [np.argmax(y_temp) for y_temp in y]
        y_list_str = [np.binary_repr(y_temp,5) for y_temp in y_ten]
        y_list = [np.array([int(temp) for temp in y_temp]) for y_temp in y_list_str]
        
    if model_type == 're':
        model = keras.models.load_model("data/2018_2.model")
        with graph.as_default():
            pre = model.predict(x_test)
            y_list = []
            for i in range(len(pre)):
                res = [0,0,0,0,0]
                for j in range(5):
                    if pre[i][j]>0.1:
                        res[j] = 1
                y_list.append(res)
                
    if model_type == 'bi':
        model_bi = []
        for i in range(5):
            model_bi.append(keras.models.load_model("data/bi/bi_"+str(i+1)+".model"))
        for i in range(5):
            with graph.as_default():
                y = model_bi[i].predict(x_test)
                y_list.append([np.argmax(y_temp) for y_temp in y])
        return np.array(y_list).T
    return np.array(y_list)


def mix_model():
    y1 = predict('re')
    y2 = predict('bi')
    y3 = predict('en')
    y_sum = y1+y2+y3
    for i in range(len(y_sum)):
        for j in range(5):
            if y_sum[i][j]>1:
                y_sum[i][j] = 1
    return y_sum
    

def score(pre_y, eva_y):
    acc = np.ones(5)
    for emotion in range(5):
        acc[emotion] = accuracy_score(pre_y.T[emotion], eva_y.T[emotion])
    print("accuracy_score: ",acc)    
    pcs = np.ones(5)
    for emotion in range(5):
        pcs[emotion] = precision_score(pre_y.T[emotion], eva_y.T[emotion])
    print("precision_score: ",pcs)
    rec = np.ones(5)
    for emotion in range(5):
        rec[emotion] = recall_score(pre_y.T[emotion], eva_y.T[emotion])
    print("recall_score: ",rec)
    f1 = np.ones(5)
    for emotion in range(5):
        f1[emotion] = f1_score(pre_y.T[emotion], eva_y.T[emotion])
    print("f1_score: ",f1)
    return [acc,pcs,rec,f1]




#predict('bi')
#res, y_ten = predict('en')
"""
print("*"*10,"re_model","*"*10)
score(predict('re'),eva_y)

print("*"*10,"bi_model","*"*10)
score(predict('bi'),eva_y)

print("*"*10,"en_model","*"*10)
score(predict('en'),eva_y)
"""

print("*"*10,"mix_model","*"*10)
score(mix_model(),eva_y)




