# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:30:33 2019

@author: cc
"""

import tensorflow as tf
import pickle
import numpy as np
import multiprocessing
from gensim.models import Word2Vec

#%%
data_train = 0
data_evalution = 0
with open('../data/nlpcc2018/train.pkl','rb') as f:
    data_train = pickle.load(f)
with open('../data/nlpcc2018/dev.pkl','rb') as f:
    data_evalution = pickle.load(f)

w2v = []
w2v.extend(data_train[0])
w2v.extend(data_evalution[0])
model_w2v = Word2Vec(w2v,size = 128,min_count = 5)
model_w2v.save('../data/nlpcc2018/nlpcc2018.w2v')

x_train_embedding = []
for sentences in data_train[0]:
    embedding = []
    for word in sentences:
        try:
            embedding.append(model_w2v[word])
        except:
            continue
    x_train_embedding.append(embedding)
    
    
x_test_embedding = []
for sentences in data_evalution[0]:
    embedding = []
    for word in sentences:
        try:
            embedding.append(model_w2v[word])
        except:
            continue
    x_test_embedding.append(embedding)
    
with open('../data/nlpcc2018/train_embedding.pkl','wb') as f:
    pickle.dump(x_train_embedding,f)
    
with open('../data/nlpcc2018/test_embedding.pkl','wb') as f:
    pickle.dump(x_test_embedding,f)
    