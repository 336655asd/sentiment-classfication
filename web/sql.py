# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:42:04 2019

@author: cc
"""

import sqlite3
    
text = u"今天心情很好"
label = "10000"
relabel = "10000"

# add table
def create():
    conn = sqlite3.connect('test.db')
    print "Opened database successfully";
    c = conn.cursor()
    c.execute('''CREATE TABLE results
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
    print "Opened database successfully"
    c = conn.cursor()
    c.execute("INSERT INTO results (text,label,relabel,flag) VALUES ("+"\'"+text+"\', "+"\'"+label+"\', "+"\'"+relabel+"\', "+ifreabel + ")")
    conn.commit()
    conn.close()

# select from tables
def select():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print "Opened database successfully"
    cursor = c.execute("SELECT id, text, label, relabel,flag from results")    
    results = {}
    index = 1
    for row in cursor:
        dic = {}
        """
        print(row)
        print "ID = ", row[0]
        print "TEXT = ", row[1]
        labels = [int(x) for x in row[2]]
        print "label = ", labels
        relabels = [int(x) for x in row[3]]
        print "relabel = ", relabels
        print "flag = ", row[4], "\n"
        """
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

def select_train():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print "Opened database successfully"
    cursor = c.execute("SELECT text, relabel from results where flag = '0' ")    
    results = []
    for row in cursor:
        text = row[0]
        relabel = [int(x) for x in row[1]]
        results.append([text,relabel])
    print(results)
    conn.commit()
    conn.close()
    return results
    
def update_train():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    print "Opened database successfully"
    cursor = c.execute("SELECT text, flag from results where flag = '0' ")    
    for row in cursor:
        row[1] = 1
    conn.commit()
    conn.close()
    
# delete acconding to the id
def delete(ID):
    conn = sqlite3.connect('test.db')
    print "Opened database successfully"
    c = conn.cursor()
    try:
        c.execute("delete from results where id="+ID+";)")
    except:
        print("not exisit")
    conn.commit()
    conn.close()

    
def parse(label_str):
    labels = [int(x) for x in label_str]
    return labels


#insert(text, label,relabel)       
#select()