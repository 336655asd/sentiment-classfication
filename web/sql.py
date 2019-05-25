# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:42:04 2019

@author: cc
"""

import sqlite3
    
# add table
def create():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE rebuild
           (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
           text           TEXT    NOT NULL,
           label            TEXT     NOT NULL,
           relabel        TEXT,
           flag         int NOT NULL);''')
    print "Table created successfully";
    conn.commit()
    conn.close()    
   
# insert columns   
def insert(text, label,relabel,ifreabel='0'):
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    c = conn.cursor()
    c.execute("INSERT INTO results (text,label,relabel,flag) VALUES ("+"\'"+text+"\', "+"\'"+label+"\', "+"\'"+relabel+"\', "+ifreabel + ")")
    conn.commit()
    conn.close()

# select from tables
def select(table="results"):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")
    cursor = c.execute("SELECT id, text, label, relabel,flag from %s" %table)    
    results = {}
    index = 1
    for row in cursor:
        dic = {}
        dic['id'] = row[0]
        dic['text'] = row[1]
        dic['label'] = [int(x) for x in row[2]]
        dic['relabel'] = [int(x) for x in row[3]]
        dic['flag'] = row[4]
        results[str(index)]=dic
        index += 1
    results['length'] = index-1
    conn.commit()
    conn.close()
    return results

def select_train(table="rebuild"):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")
    cursor = c.execute("SELECT text, relabel from %s where flag = '1' "%table)    
    results = []
    for row in cursor:
        text = row[0]
        relabel = [int(x) for x in row[1]]
        results.append([text,relabel])
    #print(results)
    conn.commit()
    conn.close()
    return results
    
def update_train(table="rebuild"):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")
    cursor = c.execute("SELECT text, flag from rebuild where flag = '1' ")    
    for row in cursor:
        c.execute("UPDATE results set flag = '1' where ID='{0}'".format(row[4]))
    conn.commit()
    conn.close()

def update_label(relabels):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print("Opened database successfully")
    cursor = c.execute("select * from results order by id desc LIMIT 1")
    print(relabels)
    result = [str(x) for x in relabels]
    print(relabels)
    relabels = ''.join(result)
    print(relabels)
    rows = [x for x in cursor]
    item = rows[0]
    exe_str1 = "UPDATE results set relabel = '{0}' where ID='{1}'".format(relabels,item[0])
    print(exe_str1)
    c.execute(exe_str1)
    c.execute("UPDATE results set flag = '1' where ID='{0}'".format(item[0]))
    c.execute("INSERT INTO rebuild (text,label,relabel,flag) VALUES ("+"\'"+item[1]+"\', "+"\'"+item[2]+"\', "+"\'"+relabels+"\', "+"1" + ")")

    conn.commit()
    conn.close()
    #insert(text=item[1],label=item[2],relabel=relabels,ifreabel='1')

     
# delete acconding to the id
def delete(ID,table="results"):
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    c = conn.cursor()
    try:
        c.execute("delete from results where id="+ID+";)")
    except:
        print("not exisit")
    conn.commit()
    conn.close()

def last_one():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute("select * from results order by id desc LIMIT 1")
    result = []
    for row in cursor:    
        result=row
    return list(result)
    
def parse(label_str):
    labels = [int(x) for x in label_str]
    return labels


#insert(text, label,relabel)       
#select()