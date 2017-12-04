import requests
import json
import csv
url = 'http://localhost:5432/1/ratings/top/3'


#json_str = json.dumps(data)
with open('mydata.csv','w') as outf:
    for k in range(10):
        url = 'http://localhost:5432/%d/ratings/top/3' %(k)
        r = requests.get(url)
        data = r.json()
        dw = csv.writer(outf, delimiter=',')
        i = 0
        for row in data:
            i=i+1
            row.append(i)
            dw.writerow(row)
