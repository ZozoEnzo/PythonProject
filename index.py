from flask import Flask, abort
import requests
import json
from flask_cors  import CORS

app = Flask(__name__)
CORS(app)

URL_YEAR_CINEMA = "https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&facet=annee&refine.annee="
URL_POPULATION = "http://open-api.green-walk.fr/data.json"


@app.route('/lastandnew')
def lasttonew():
    # Calcul du nombre d'entré en fonction des années
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

    # Calcule de l'évolution
    evolution = round(((value_new - value_last) / value_last) * 100, 2)
    if value_last < value_new:
        value_evolve = '+' + str(evolution) + ' % entrées'
    else:
        value_evolve = '-' + str(evolution) + ' % entrées'
    results = {"title": "Evolution",
               "chart": {
                   "data": [{
                       "value": [value_last, value_new],
                       "label": value_label
                   }],
                   "labels": ["1985", "2019"]},
               "data": [value_evolve]}
    return json.dumps(results)


@app.route('/lasttonewseance')
def lasttonewseance():
    # Calcul du nombre d'entré en fonction des années
    datalast = call(URL_YEAR_CINEMA + "1985")
    data_list_last = json.dumps(datalast['records'][0]['fields'])
    alls_last = json.loads(data_list_last)
    list_key_last = list(alls_last.keys())
    list_val_last = list(alls_last.values())
    value_last_entrees = list_val_last[list_key_last.index('entrees_millions')]
    value_last_seance = list_val_last[list_key_last.index('seances_milliers')]
    datanew = call(URL_YEAR_CINEMA + "2019")
    data_list_new = json.dumps(datanew['records'][0]['fields'])
    alls_new = json.loads(data_list_new)
    list_key_new = list(alls_new.keys())
    list_val_new = list(alls_new.values())
    value_new_entrees = list_val_new[list_key_new.index('entrees_millions')]
    value_new_seance = list_val_new[list_key_new.index('seances_milliers')]
    value_entrees = 'Million d\'entrée'
    value_seances = 'Millier de seances'

    # Calcule de l'évolution
    personne_par_seance_avant = round((value_last_entrees * 1000000) / (value_last_seance * 1000), 1)
    personne_par_seance_mtn =  round((value_new_entrees * 1000000) / (value_new_seance * 1000), 1)
    evolution_entrees = round(((value_new_entrees - value_last_entrees) / value_last_entrees) * 100, 2)
    evolution_seance = round(((value_new_seance - value_last_seance) / value_last_seance) * 100, 2)
    pp_par_seance_av = str(personne_par_seance_avant) + " personnes en moyennes par seance en 1985"
    pp_par_seance_mtn =str(personne_par_seance_mtn) + " personnes en moyennes par seance en 2019"
    if value_last_entrees < value_new_entrees:
        value_evolve_entrees = '+' + str(evolution_entrees) + ' % entrées'
    else:
        value_evolve_entrees = '-' + str(evolution_entrees) + ' % entrées'
    if value_last_seance < value_new_seance:
        value_evolve_seance = '+' + str(evolution_seance) + ' % seances'
    else:
        value_evolve_seance = '-' + str(evolution_seance) + ' % entrées'
    results = {"title": "Evolution",
               "chart": {
                   "data": [{
                       "value": [value_last_entrees, value_new_entrees],
                       "label": value_entrees
                   }, {
                       "value": [value_last_seance, value_new_seance],
                       "label": value_seances
                   }],
                   "labels": ["1985", "2019"]},
               "data": [value_evolve_entrees, value_evolve_seance, pp_par_seance_av, pp_par_seance_mtn]}
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
        value_evolve = '+'+ str(evolution) + ' % entrées'
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
        value_evolve_pop = '+'+ str(evolution_pop) + ' % de population'
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
    if int(year) < 2015 and int(year) > 1990: 
        results = []

        #Récupération des données de 3 années, année exact, +5 et -5
        datamin = call(URL_YEAR_CINEMA + str(int(year)-5))
        dataminusfive = json.dumps(datamin['records'][0]['fields'])
        datanormal = call(URL_YEAR_CINEMA + str(int(year)))
        data = json.dumps(datanormal ['records'][0]['fields'])
        datamax = call(URL_YEAR_CINEMA + str(int(year)+5))
        dataplusfive = json.dumps(datamax['records'][0]['fields'])

        #Calcule des différentes données (recette)
        #Min
        alls_min = json.loads(dataminusfive)
        list_key_min = list(alls_min.keys())
        list_val_min = list(alls_min.values())
        value_min = (list_val_min[list_key_min.index('entrees_millions')] * list_val_min[list_key_min.index('recette_moyenne_par_entree_eu')])
        #Normal
        alls_normal = json.loads(data)
        list_key_normal = list(alls_normal.keys())
        list_val_normal = list(alls_normal.values())
        value_normal = (list_val_normal[list_key_normal.index('entrees_millions')] * list_val_normal[list_key_normal.index('recette_moyenne_par_entree_eu')])
        #Max
        alls_max = json.loads(dataplusfive)
        list_key_max = list(alls_max.keys())
        list_val_max = list(alls_max.values())
        value_max = (list_val_max[list_key_max.index('entrees_millions')] * list_val_max[list_key_max.index('recette_moyenne_par_entree_eu')])
        #Calcule de l'évolution des recettes
        #Min -> Normal
        recette_min_normal = round((((value_normal - value_min)/value_min)*100), 2)
        if value_min < value_normal:
            value_recette_min_normal =  '+'+ str(recette_min_normal) + ' % de recette entre '+ str(int(year)-5) + ' et '+ str(year)
        else: 
            value_recette_min_normal = '-'+ str(recette_min_normal)+' % de recette entre '+ str(int(year)-5) + ' et '+ str(year)
        #Normal -> Max
        recette_normal_max = round((((value_max - value_normal)/value_normal)*100), 2)
        if value_normal < value_max:
            value_recette_normal_max =  '+'+ str(recette_normal_max) + ' % de recette entre '+ str(year) + ' et '+ str(int(year)+5)
        else: 
            value_recette_normal_max = '-'+ str(recette_normal_max)+' % de recette entre '+ str(year) + ' et '+ str(int(year)+5)
        #Min -> Max
        recette_min_max = round((((value_max - value_min)/value_min)*100), 2)
        if value_min < value_max:
            value_recette_min_max =  '+'+ str(recette_min_max) + ' % de recette entre '+ str(int(year)-5) + ' et '+ str(int(year)+5)
        else: 
            value_recette_min_max = '-'+ str(recette_min_max)+' % de recette entre '+ str(int(year)-5) + ' et '+ str(int(year)+5)

        #Calcule des populations en fonction des années
        populations = call(URL_POPULATION)
        for item in populations: 
            if str(int(year)-5) in item:
                pop_min = int(item[str(int(year)-5)].replace(' ',''))
            if str(int(year)) in item:
                pop_normal = int(item[str(int(year))].replace(' ',''))
            if str(int(year)+5) in item:
                pop_max = int(item[str(int(year)+5)].replace(' ',''))
        #Calcule de l'évolution de la population en fonction des années 
        #Min -> Normal
        evolution_pop_min_normal = round((((pop_normal - pop_min)/pop_min)*100), 2)
        if pop_min < pop_normal:
            value_evolve_pop_min_normal =  '+'+ str(evolution_pop_min_normal) + ' % de population entre '+ str(int(year)-5) + ' et '+ str(year)
        else: 
            value_evolve_pop_min_normal = '-'+ str(evolution_pop_min_normal)+' % de population entre '+ str(int(year)-5) + ' et '+ str(year)
        #Normal -> Max
        evolution_pop_normal_max = round((((pop_max - pop_normal)/pop_normal)*100), 2)
        if pop_normal < pop_max:
            value_evolve_pop_normal_max =  '+'+ str(evolution_pop_normal_max) + ' % de population entre '+ str(year) + ' et '+ str(int(year)+5)
        else: 
            value_evolve_pop_normal_max = '-'+ str(evolution_pop_normal_max)+' % de population entre '+ str(year) + ' et '+ str(int(year)+5)
        #Min -> Max
        evolution_pop_min_max = round((((pop_max - pop_min)/pop_min)*100), 2)
        if pop_min < pop_max:
            value_evolve_pop_min_max =  '+'+ str(evolution_pop_min_max) + ' % de population entre '+ str(int(year)-5) + ' et '+ str(int(year)+5)
        else: 
            value_evolve_pop_min_max = '-'+ str(evolution_pop_min_max)+' % de population entre '+ str(int(year)-5) + ' et '+ str(int(year)+5)
        
        #Fabrication du tableau
        results = { "title" : "Recette global en fonction de l'année",
            "chart": 
            {
                "data":[
                {
                    "value" : [value_min, value_normal, value_max],
                    "label" : "Comparaison -5 & +5"
                }],
                "labels": [str(int(year)-5),str(year),str(int(year)+5)]
            },
            "data": [value_recette_min_normal,value_evolve_pop_min_normal,value_recette_normal_max,value_evolve_pop_normal_max,value_recette_min_max,value_evolve_pop_min_max]
        }
        return json.dumps(results)
    else:
        abort(404)

@app.route('/year/<path:year>')
def index(year):
    # Calcul du nombre d'entré en fonction des années
    datalast = call(URL_YEAR_CINEMA + year)
    data_list_last = json.dumps(datalast['records'][0]['fields'])
    alls_last = json.loads(data_list_last)
    list_key_last = list(alls_last.keys())
    list_val_last = list(alls_last.values())
    value_last = list_val_last[list_key_last.index('entrees_millions')]
    value_label = 'Million d\'entrée'
    results = {"title": "Evolution",
               "chart": {
                   "data": [{
                       "value": [value_last],
                       "label": value_label
                   }],
                   "labels": [year]}}
    return json.dumps(results)


def call(url):
    response = requests.get(url)
    data = response.json()
    #if data['nhits'] < 1:
    #   abort(404)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')