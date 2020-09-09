from flask import Flask, render_template, jsonify, abort
import requests
import json
import numpy as np

app = Flask(__name__)

URL_YEAR_CINEMA = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee="
URL_POPULATION = "http://open-api.green-walk.fr/data.json"


@app.route('/lastandnew')
def lasttonew():
    results = []
    datalast = call(URL_YEAR_CINEMA + "1985")
    datanew = call(URL_YEAR_CINEMA + "2019")
    results.append(json.dumps(datalast['records'][0]['fields']))
    results.append(json.dumps(datanew['records'][0]['fields']))
    return json.dumps(results)


@app.route('/lastandnewpopulation')
def lastandnewpopulation():
    #Calcul du nombre d'entré en fonction des années
    datalast = call(URL_YEAR_CINEMA + "1985")
    data_list_last = json.dumps(datalast['records'][0]['fields'])
    alls_last = json.loads(data_list_last)
    list_key_last = list(alls_last.keys())
    list_val_last = list(alls_last.values())
    value_last = list_val_last[list_key_last.index('entrees_millions')]
    datanew = call(URL_YEAR_CINEMA + "2019")
    data_list_new = json.dumps(datanew['records'][0]['fields'])
    alls_new = json.loads(data_list_new)
    list_key_new = list(alls_new.keys())
    list_val_new = list(alls_new.values())
    value_new = list_val_new[list_key_new.index('entrees_millions')]
    value_label = 'Million d\'entrée'

    #Calcule de l'évolution
    evolution = round(((value_new - value_last)/value_last)*100,2)
    if value_last < value_new:
        value_evolve = str(evolution) + ' % entrées'
    else: 
        value_evolve = '-'+ str(evolution) +' % entrées'
    
    #Calcule des populations en fonction des années
    populations = call(URL_POPULATION)
    for item in populations: 
        if '1985' in item:
            last_pop = int(item['1985'].replace(' ',''))
        if '2019' in item:
            new_pop = int(item['2019'].replace(' ',''))
    #Calcule de l'évolution de la population en fonction des années
    evolution_pop = round((((new_pop - last_pop)/last_pop)*100), 2)
    if last_pop < new_pop:
        value_evolve_pop = str(evolution_pop) + ' % de population'
    else: 
        value_evolve_pop = '-'+ str(evolution_pop)+' % de population'
    
    results = { "title" : "Entrée en fonction de la population",
        "chart": {
        "data":[{
        "value" : [value_last, value_new],
        "label" : value_label
    }],
    "labels": ["1985","2019"]},
    "data": [value_evolve,value_evolve_pop]}
    return json.dumps(results)



@app.route('/fivemorelessfive/<path:year>')
def fivemorelessfive(year):
    results = []
    dataminusfive = call(URL_YEAR_CINEMA + str(int(year)-5))
    data = call(URL_YEAR_CINEMA + str(int(year)))
    dataplusfive = call(URL_YEAR_CINEMA + str(int(year)+5))
    results.append(json.dumps(dataminusfive['records'][0]['fields']))
    results.append(json.dumps(data['records'][0]['fields']))
    results.append(json.dumps(dataplusfive['records'][0]['fields']))
    return json.dumps(results)

@app.route('/year/<path:year>')
def index(year):
    result = []
    url = URL_YEAR_CINEMA + year
    data = call(url)
    data_list = json.dumps(data['records'][0]['fields'])
    alls = json.loads(data_list)
    list_key = list(alls.keys())
    list_val = list(alls.values())
    value = list_val[list_key.index('entrees_millions')]
    return json.dumps(value)


def call(url):
    response = requests.get(url)
    data = response.json()
    #if data['nhits'] < 1:
    #   abort(404)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')