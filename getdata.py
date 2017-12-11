
import time
import subprocess
import os
dir = os.path.dirname(__file__)
starttime=time.time()
# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    while True:
        cur = conn.cursor()
        cur.execute( "SELECT * FROM account" )
        for i in cur :
            #userid
            an = subprocess.Popen("curl --data-binary @user_ratings" + i[0]+".file http://localhost:3030/" + i[0]+ "/ratings",shell=True)
            print an
            print i[0]
            with open("rating/user_ratings"+i[0]+".file","w") as fo:
               fo.write("")
        for i in cur:
            url = "http://localhost:5432/"+ i +"/ratings/top/20"
            r = requests.get(url)
            data = r.json()



        time.sleep(40.0 - ((time.time() - starttime) % 40.0))

import psycopg2
myConnection = psycopg2.connect( host="localhost", dbname="big_data" )
doQuery( myConnection )
myConnection.close()

   

