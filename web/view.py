# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:56:33 2019

@author: cc
"""

from __future__ import absolute_import, division, print_function
from flask import render_template, Flask, request
import json
import numpy as np
import sql
import model

app = Flask(__name__)
print("from the title")

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
    
@app.route('/history',methods=['GET','POST'])
def history():
    results_db = sql.select()
    #results_db = json.dumps(results_db)
    print(results_db)
    return render_template('table.html', results_db = results_db)    
    
    
def classify(search_sentence=u'等待'):
    f = open('static/list.json','w')
    #result = analyse(search_sentence)
    try:
        result = model.analyse(search_sentence)
    except:
        print("*************error*****************")
        result = [0,0,0,0,0]
    variable['list3'] = variable['list2']
    variable['list2'] = variable['list1']
    variable['list1'] = {'text':search_sentence, 'label':result}
    variable['list0'] = {'text':search_sentence, 'label':result}
    json.dump(variable,f)
    f.close()
    result = [str(x) for x in result]
    label = ''.join(result)
    relabel = label
    sql.insert(search_sentence,label,relabel)
    return     
    


    
#%%
if __name__ == '__main__':
    print("web start")
    print("load model")
    #app.run(debug=True,use_reloader=False)
    app.run(debug=True)
