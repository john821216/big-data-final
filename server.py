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
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,g
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
import time
import logging
logging.basicConfig()

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

DATABASEURI = "postgresql://localhost/big_data"
engine = create_engine(DATABASEURI)
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
  cursor = g.conn.execute("SELECT * FROM account")
  print cursor
  return render_template('signIn.html')

@app.route('/test')
def test():
  print "test"
  return ""


@cron.interval_schedule(seconds=10)
def job_function():
	#test
    count = 0
    print count

    #write update func here
    #https://stackoverflow.com/questions/4476373/simple-url-get-post-function-in-python
    #write post and get and update it to database



# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))


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




