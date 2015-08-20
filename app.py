import os
from flask import Flask, render_template, request, session, abort
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import simplejson as json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

import models
# import pykemon

print(os.environ['APP_SETTINGS'])

# from flask_wtf.csrf import CsrfProtect

# CsrfProtect(app)

def pullStats(list):
    newList = []
    for item in list:
        newList.append(item['name'])
    return newList

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/pokemon', methods = ['POST'])
def get_pokemon():
    print("Request form: {}".format(request.form))
    pokemon_name = request.form['pokemon']

    print("Pokemon: {}".format(pokemon_name))

    if(pokemon_name != ''):
        pokemon = models.Pokemon.query.filter_by(name=pokemon_name).first()
        if pokemon is None:
            pokestats = json.loads(requests.get('http://pokeapi.co/api/v1/pokemon/' + pokemon_name).text)
            print("Pokestats: {}".format(pokestats))
            stats = {
                'hp': pokestats['hp'],
                'attack': pokestats['attack'],
                'defense': pokestats['defense'],
                'sp_attack': pokestats['sp_atk'],
                'sp_defense': pokestats['sp_def'],
                'speed': pokestats['speed'],
                'height': pokestats['height'],
                'weight': pokestats['weight'],
                'types': pullStats(pokestats['types']),
                'abilities': pullStats(pokestats['abilities']),
                'gender_ratio': pokestats['male_female_ratio'],
                'catch_rate': pokestats['catch_rate'],
                'moves': pullStats(pokestats['moves']),
            }
            print("Stats: {}".format(stats))
            pokemon = models.Pokemon(name=pokemon_name, stats=stats)
            print("Pokemon model: {}".format(pokemon))
            db.session.add(pokemon)
            db.session.commit()
        pokejson = pokemon.serialize()
        pokejson['form'] = request.form['formId']
        return json.dumps(pokejson)
    else:
        return 'Error'

if __name__ == '__main__':
    app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT','8080')))