# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:56:33 2019

@author: cc
"""

from __future__ import absolute_import, division, print_function
from flask import render_template, Flask, request
import json
import numpy as np
from gensim.models import Word2Vec
from keras.preprocessing.sequence import pad_sequences
import keras
import jieba

app = Flask(__name__)
print("from the title")
#%%
# laod model
model_w2v = Word2Vec.load("data/nlpcc2018/nlpcc2018.w2v")
model_bi=[]

#%%
f = open('static/list.json','r')
variable = json.load(f)
f.close()
variable['list0'] = {'text':'', 'label':[0,0,0,0,0]}

#%%
# web
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',variable = variable)

@app.route('/query',methods=['GET','POST'])
def query():
    print(request.values)
    print(request.values["search"])
    search_sentence = request.values["search"]
    classify(search_sentence)
    return render_template('index.html', variable = variable)
    

def classify(search_sentence=u'等待'):
    f = open('static/list.json','w')
    #result = analyse(search_sentence)
    try:
        result = analyse(search_sentence)
    except:
        print("*************error*****************")
        result = [0,0,0,0,0]
    variable['list3'] = variable['list2']
    variable['list2'] = variable['list1']
    variable['list1'] = {'text':search_sentence, 'label':result}
    variable['list0'] = {'text':search_sentence, 'label':result}
    json.dump(variable,f)
    f.close()
    return     
    
#%%
def analyse(text):
    words = jieba.lcut(text)
    model_encode = keras.models.load_model("data/nlpcc2018/encode.model")
    model_bi = []
    for i in range(5):
        model_bi.append(keras.models.load_model("data/nlpcc2018/bi/2018_bi_"+str(i+1)+".model"))
    model_re = keras.models.load_model("data/nlpcc2018/2018_2.model")    
    
    x = model_w2v[words]
    x = x.reshape([1,x.shape[0],x.shape[1]])
    #model 1
    pre_x = pad_sequences(x, 128, dtype='float32')
    y1 = model_encode.predict(pre_x)
    y_temp = np.binary_repr(np.argmax(y1),5)
    y1 = np.array([int(temp) for temp in y_temp])
    #print(np.argmax(y1))
    print(y1)
    # model 2
    y2=[]
    for i in range(5):
        pre_x = pad_sequences(x, 128, dtype='float32')
        y_temp = model_bi[i].predict(pre_x)
        y2.append(np.argmax(y_temp))
        #print(np.argmax(y2))
    y2 = np.array(y2)
    print(y2)
    
    # model 3
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
    y = y.tolist()
    print("finally result: ", y)
    return y
    
#%%
if __name__ == '__main__':
    print("web start")
    print("load model")
    app.run(debug=True)

