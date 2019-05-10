# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:21:29 2019

@author: cc
"""

import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
from bs4 import BeautifulSoup

path = '../data/nlpcc2018/dev.txt'


#%%
def tf_to_01(word):
    if word == 'F':
        return 0
    else:
        return 1

def parse(file_path):
    html_file = open(file_path,'rb')
    html_headle = html_file.read()
    print("start parse")
    soup = BeautifulSoup(html_headle,'lxml')
    print("finding")
    tweet_list = soup.find_all('tweet')
    html_file.close()
    data_x = []
    data_y = []
    print("pre-processing")
    for item in tweet_list:
        print tweet_list.index(item)
        happiness = ''.join(item.happiness.contents).replace('\n','').replace('\r','').replace('\t','')
        sadness = ''.join(item.sadness).replace('\n','').replace('\r','').replace('\t','')
        anger = ''.join(item.anger).replace('\n','').replace('\r','').replace('\t','')
        fear = ''.join(item.fear).replace('\n','').replace('\r','').replace('\t','')
        surprise = ''.join(item.surprise).replace('\n','').replace('\r','').replace('\t','')
        sentiment = [tf_to_01(happiness),tf_to_01(sadness),tf_to_01(anger),tf_to_01(fear),tf_to_01(surprise)]
        data_y.append(sentiment)
        sentense = ''.join(item.content.contents).replace('\n','').replace('\r','').replace('\t','')
        words = sentense.split()
        data_x.append(words)
    return [data_x,data_y]
    
data = parse('../data/nlpcc2018/dev.txt')    
f = open('../data/nlpcc2018/dev.pkl','wb')
pickle.dump(data,f)
f.close()