# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:56:33 2019

@author: cc
"""

from __future__ import absolute_import
import flask
from flask import render_template, Flask, request
import json

app = Flask(__name__)

f = open('static/list.json','r')
variable = json.load(f)
f.close()
variable['list0'] = {'text':'', 'label':[0,0,0,0,0]}

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
    

def classify(search_sentence):
    f = open('static/list.json','w')
    result = [1,0,0,0,1]
    variable['list3'] = variable['list2']
    variable['list2'] = variable['list1']
    variable['list1'] = {'text':search_sentence, 'label':result}
    variable['list0'] = {'text':search_sentence, 'label':result}
    json.dump(variable,f)
    f.close()
    return     
    
    
if __name__ == '__main__':
    app.run(debug=True)

