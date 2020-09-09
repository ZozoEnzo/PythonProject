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
    results = []
    datalast = call(URL_YEAR_CINEMA + "1985")
    datanew = call(URL_YEAR_CINEMA + "2019")
    populations = call(URL_POPULATION)
    results.append(json.dumps(datalast['records'][0]['fields']))
    results.append(json.dumps(datanew['records'][0]['fields']))
    for population in populations:
        print(population.keys())
        if "1985" in population:
            results.append(json.dumps(population))
        if "2019" in population:
           results.append(json.dumps(population))
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
    url = URL_YEAR_CINEMA + year
    data = call(url)
    return json.dumps(data['records'][0]['fields'])


def call(url):
    response = requests.get(url)
    data = response.json()
    #if data['nhits'] < 1:
    #   abort(404)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')