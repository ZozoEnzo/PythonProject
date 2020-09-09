from flask import Flask, render_template, jsonify, abort
import requests
import json
import numpy as np

app = Flask(__name__)

#@app.route('/year/<path:year>')
#def index(year):
#    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee="+year
#    response = requests.get(url)
#    tous = json.loads(response.text)
#    records = json.dumps(tous['records'])
#    posstart = records.find("fields")
#    posend = records.find("record_timestamp")
#    fields = records[posstart+10:posend-4]
#    if posstart == -1:
#        abort(404)
#    return fields

@app.route('/lasttonew')
def lasttoroute():
    result =  {}
    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee=1985"
    response = requests.get(url)
    tous = json.loads(response.text)
    record = tous.get('records')
    records = json.dumps(tous['records'])
    posstart = records.find("fields")
    posend = records.find("record_timestamp")
    fields = records[posstart+10:posend-4].split(',')

    url2 = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee=2019"
    response2 = requests.get(url2)
    tous2 = json.loads(response2.text)
    records2 = json.dumps(tous2['records'])
    posstart2 = records2.find("fields")
    posend2 = records2.find("record_timestamp")
    fields2 = records2[posstart+10:posend-4].split(',')

    result['1985'] = fields
    result['2019'] = fields2
    if posstart == -1:
        abort(404)
    print(result)

@app.route('/fivemorelessfive/<path:year>')
def fivemorelessfive(year):
    datas = []
    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee="+ str(int(year)-5)
    url1 = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee="+ str(int(year))
    url2 = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee="+ str(int(year)+5)
    data = call(url)
    data1 = call(url1)
    data2 = call(url2)
    datas.append(json.dumps(data['records'][0]['fields']))
    datas.append(json.dumps(data1['records'][0]['fields']))
    datas.append(json.dumps(data2['records'][0]['fields']))
    return json.dumps(datas)

@app.route('/year/<path:year>')
def index(year):
    url = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee=" + year
    data = call(url)
    return json.dumps(data['records'][0]['fields'])


def call(url):
    response = requests.get(url)
    data = response.json()
    if data['nhits'] < 1:
        abort(404)
    return data

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')