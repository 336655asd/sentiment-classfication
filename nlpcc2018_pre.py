# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:18:11 2019

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
import jieba

model_w2v = Word2Vec.load("../data/nlpcc2018/nlpcc2018.w2v")
model = keras.models.load_model("../data/nlpcc2018/bi/2018_bi_1.model")

words = jieba.lcut('今天真的很开心')
x = model_w2v[words]
x = x.reshape([1,x.shape[0],x.shape[1]])
x = pad_sequences(x,128)
y = model.predict(x)

print(np.argmax(y)) 