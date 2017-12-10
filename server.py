#!/usr/bin/env python2.7

"""
To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import atexit
from apscheduler.scheduler import Scheduler
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask,url_for
from flask import Flask, flash, redirect, render_template, request, session, abort,g
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
from werkzeug import secure_filename
import random
import time
import logging
logging.basicConfig()

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
cron = Scheduler(daemon=True)
UPLOAD_FOLDER = 'query'
ALLOWED_EXTENSIONS = set(['doc', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Explicitly kick off the background thread
cron.start()

DATABASEURI = "postgresql://localhost/big_data"
engine = create_engine(DATABASEURI)
f_name =""
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass



@app.route('/')
def index(): 
  if not session.get('logged_in'):
  	return render_template('signIn.html')
  else:
  	return main()


@app.route('/login', methods=['POST'])
def do_login():
  id = request.form['id']
  password = request.form['password']
  cursor = g.conn.execute("SELECT count(*) FROM account Where username='"+id+"' And password='"+password+"'")
  count =  cursor.scalar()
  if count != 0:
  	cursor = g.conn.execute("SELECT * FROM account Where username='"+id+"' And password='"+password+"'")
  	session['logged_in'] = True
  	session['id'] = id
  else:
  	flash('wrong password!')
  return index()



@app.route('/main')
def main():
  label = 'train'
  cursor = g.conn.execute("SELECT * FROM wiki where label='"+label+"' ORDER BY RANDOM() LIMIT 10")
  return render_template('index.html',randomList=cursor)


@app.route('/id/<int:id>')
def rating(id):
	cursor = g.conn.execute("SELECT * FROM wiki where id='"+str(id)+"'")
	return render_template('rating.html',id=id, content=cursor)

	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename("file.filename")
            f_name= str(random.randint(1,1010000)) + ".jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    return index()

def imageClassfication():
	queryPath = '/query/'+f_name
	descriptorName = 'SURF'
	k = 1
	treeIndex = '/ballTreeIndexes/ballTreeIndexes.pickle'
	pathVD = '/Users/zhanghao/Documents/BigData/project/CBIR/visualDictionary/visualDictionary.pickle'
	#load the index
	with open(treeIndex, 'rb') as f:
    	indexStructure=pickle.load(f)

	#load the visual dictionary
	with open(pathVD, 'rb') as f:
    	visualDictionary=pickle.load(f)     

	imageID=indexStructure[0]
	tree = indexStructure[1]
	pathImageData = indexStructure[2]
	imageClasses = indexStructure[3]

	print(pathImageData)
	#computing descriptors
	dist,ind = query(queryPath, k, descriptorName, visualDictionary, tree)

	#print(dist)
	ind=list(itertools.chain.from_iterable(ind))

	print(queryPath)
	results = list()
	for i in ind:
    	results = np.hstack((results,imageClasses[i]))
    	print(imageID[i])
	print('the query image class id is:')
	print(mode(results))



if __name__ == "__main__":
  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()




