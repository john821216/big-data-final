from sqlalchemy import *
import csv
from sqlalchemy.pool import NullPool
#from flask import Flask
#from flask import Flask, flash, redirect, render_template, request, session, abort,g

DATABASEURI = "postgresql://localhost/big_data"
engine = create_engine(DATABASEURI)
try:
    conn = engine.connect()
except:
    print "uh oh, problem connecting to database"
    import traceback;
    traceback.print_exc()
    conn = None

id = 1
label = 'train'
with open('/Users/jenan/Documents/big_data_final/train.csv', 'r') as csvin:
    reader = csv.reader(csvin)
    for item in reader:
        if reader.line_num == 1:
            continue;
        title = item[0]
        content = item[2]
        title = title.replace("'"," ")
        title = title.replace("%", " ")
        content = content.replace("'"," ")
        content = content.replace("%"," ")
        print content
        cursor = conn.execute("INSERT INTO wiki(id,label,title,content) VALUES("+str(id)+",'"+str(label)+"','"+str(title)+"','"+str(content)+"')")
        id = id+1
        print (id,cursor)
    cursor.close()
print id

