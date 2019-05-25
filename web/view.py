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
    #print(results_db)
    return render_template('table.html', results_db = results_db)    

@app.route('/retrain',methods=['GET','POST'])
def retrain():
    try:
        model.retrain(10)
    except:
        print("no need to update")
    results_db = sql.select()
    return render_template('table.html',results_db = results_db)    

@app.route('/feedback',methods=['GET'])
def feedback():
    item = sql.last_one()
    dic = {'id':item[0],'text':item[1],'label':[int(x) for x in item[2]],'relabel':[int(x) for x in item[3]],'flag':item[4]}
    print(dic)    
    return render_template('feedback.html',variable = dic)    

@app.route('/relabel',methods=['POST'])
def relabel():
    print(request.values.getlist('relabels'))
    relabels = [0,0,0,0,0]
    for i in request.values.getlist('relabels'):
        relabels[int(i)] = 1
    sql.update_label(relabels)
    print("relabels",relabels)
    return render_template('index.html', variable = variable)          

# api
@app.route('/query_api',methods=['POST'])
def query_api():
    text = request.values['text']
    classify(text)
    row = sql.last_one()
    result = {}
    result['text'] = text
    result['label'] = row[2]
    return json.dumps(result)
    
def classify(search_sentence=u'未知词语'):
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
