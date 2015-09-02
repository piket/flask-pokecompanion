import os
from flask import Flask, render_template, request, session, abort
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import simplejson as json
from bs4 import BeautifulSoup
import re
from random import random, uniform

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from services import *
from models import *
# import pykemon

print(os.environ['APP_SETTINGS'])

# from flask_wtf.csrf import CsrfProtect

# CsrfProtect(app)

@app.route('/')
def index():
    raw = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_name').text, 'html.parser')
    pokeList = []
    for poke in raw.find_all('a',title=re.compile('[a-zA-Z0-9_]+ \(Pokémon\)$')):
        pokeList.append(poke.text.lower())

    pokeList.sort()
    natures = Nature.query.order_by(Nature.id)
    return render_template('display.html', pokeList=json.dumps(pokeList), natures=natures)


@app.route('/api/pokemon', methods = ['POST'])
def get_pokemon():
    print("Request form: {}".format(request.form))
    pokemon_name = request.form['pokemon'].lower()

    print("Pokemon: {}".format(pokemon_name))
    pokemon = generate_pokemon(pokemon_name)

    if pokemon:
        pokejson = pokemon.serialize()
        pokejson['form'] = request.form['formId']
        pokejson['moves'] = pokemon.get_moves()
        return json.dumps(pokejson)
    else:
        return 'Error'

@app.route('/api/attack', methods=['POST'])
def battle():
    # print(request)
    # data = request.get_json(silent=True,force=True)
    data = request.form
    print(request.mimetype)
    print("Data: {}".format(data))
    move = Move.query.filter_by(name=data['move']).first()
    print("move {}".format(move))
    origin = Pokemon.query.filter_by(id=data['origin[id]']).first()
    print("origin {}".format(origin))
    target = Pokemon.query.filter_by(id=data['target[id]']).first()
    print("target {}".format(target))

    # print("move {}, origin {}, target {}".format(move,origin,target))

    level = int(data['origin[level]'])
    accuracy = float(data['origin[accuracy]']) if 'origin[accuracy]' in data else 100
    evasion = float(data['target[evasion]']) if 'target[evasion]' in data else 100
    crit_chance = int(data['origin[crit_chance]']) if 'origin[crit_chance]' in data else 16

    if not move:
        print('No move: {}'.format(move))
        return json.dumps({'response':False})
    else:
        print("Move: {}".format(move))
        result = {
            'origin': data['origin[name]'],
            'target': data['target[name]'],
            'move': move.name,
            'response': True,
            'crit': False,
            'effective':1
        }

        hit = move.accuracy * (accuracy/evasion)
        if random() > hit/100:
            result['result'] = 'missed.'
            return json.dumps(result)

        mod = 1

        if random() <= 1/crit_chance:
            result['crit'] = True
            mod = 1.5

        print("Crit? {} Mod: {}".format(result['crit'],mod))

        mod *= 1.5 if move.type.lower() in origin.stats['types'] else 1
        typeMod = typeMatchUp(move.type,target.stats['types'])
        mod *= typeMod
        mod *= uniform(0.85,1)

        result['effective'] = typeMod

        print("Category: {}".format(move.category))

        if move.category == 'Physical' and move.power > 0:
            attack = int(request.form['origin[attack]'])
            defense = int(request.form['target[defense]'])
            damage = (((((2 * level) + 10)/250) * (attack/defense) * move.power) + 2) * mod
            result['result'] = 'hit for {} damage'.format(int(damage))
        elif move.category == 'Special' and move.power > 0:
            sp_attack = int(request.form['origin[sp_attack]'])
            sp_defense = int(request.form['target[sp_defense]'])
            damage = (((((2 * level) + 10)/250) * (sp_attack/sp_defense) * move.power) + 2) * mod
            result['result'] = 'hit for {} damage'.format(int(damage))
        elif move.category == 'Status':
            result['result'] = move.effect
        else:
            print('Invalid category: {}'.format(move.category))
            result = {'response':False}

        return json.dumps(result)


if __name__ == '__main__':
    app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT','8080')))