import os
from flask import Flask, render_template, request, session, abort
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import simplejson as json
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *
# import pykemon

print(os.environ['APP_SETTINGS'])

# from flask_wtf.csrf import CsrfProtect

# CsrfProtect(app)

def pullStats(list):
    newList = []
    for item in list:
        newList.append(item['name'])
    return newList

def initMove(move, move_link):
    m = move.title().replace(' ','_')
    print(m)
    regType = re.compile('[a-zA-Z0-9_]+ \(type\)$')
    regCategory = re.compile('[a-zA-Z0-9_]+ move')

    t = requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text
    t = BeautifulSoup(t,'html.parser')
    move_type = t.find('a',title=regType)
    category = t.find('a',title=regCategory)

    if not move_type:
        if '-' in m:
            m = m.replace('-','_')
            t = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text, 'html.parser')
            move_type = t.find('a', title=regType)
            category = t.find('a',title=regCategory)
            if not move_type:
                return False
        return False

    move_stats = json.loads(requests.get('http://pokeapi.co'+move_link).text)
    new_move = Move(name=move_stats['name'], type=move_type.text.strip(), category=category.text.strip(), power=move_stats['power'], accuracy=move_stats['accuracy'], pp=move_stats['pp'], effect=move_stats['description'])
    return new_move

def getTypeMatchUp(move_type, target_types):
    match_up = {
        'normal': {
            'rock':0.5,
            'ghost':0,
            'steel':0.5
        },
        'fight': {
            'normal':2,
            'flying':0.5,
            'poison':0.5,
            'rock':2,
            'bug':0.5,
            'ghost':0,
            'steel':2,
            'psychic':0.5,
            'ice':2,
            'dark':2,
            'fairy':0.5
        },
        'flying': {
            'fighting':2,
            'rock':0.5,
            'bug':2,
            'steel':0.5,
            'grass':2,
            'electric':0.5
        },
        'poison': {
            'poison':0.5,
            'ground':0.5,
            'rock':0.5,
            'ghost':0.5,
            'steel':0,
            'grass':2,
            'fairy':2
        },
        'ground': {
            'flying':0,
            'poison':2,
            'rock':2,
            'bug':0.5,
            'steel':2,
            'fire':2,
            'grass':0.5,
            'electric':2
        },
        'rock': {
            'fighting':0.5,
            'flying':2,
            'ground':0.5,
            'bug':2,
            'steel':0.5,
            'fire':2,
            'ice':2
        },
        'bug': {
            'fighting':0.5,
            'flying':0.5,
            'poison':0.5,
            'ghost':0.5,
            'steel':0.5,
            'fire':0.5,
            'grass':2,
            'pyschic':2,
            'dark':2,
            'fairy':0.5
        },
        'ghost': {
            'normal':0,
            'ghost':2,
            'pyschic':2,
            'dark':0.5
        },
        'steel': {
            'rock':2,
            'steel':0.5,
            'fire':0.5,
            'water':0.5,
            'electric':0.5,
            'ice':2,
            'fairy':2
        },
        'fire': {
            'rock':0.5,
            'bug':2,
            'steel':2,
            'fire':0.5,
            'water':0.5,
            'grass':2,
            'ice':2,
            'dragon':0.5
        },
        'water': {
            'ground':2,
            'rock':2,
            'fire':2,
            'water':0.5,
            'grass':0.5,
            'dragon':0.5
        },
        'grass': {
            'flying':0.5,
            'poison':0.5,
            'ground':2,
            'rock':2,
            'bug':0.5,
            'steel':0.5,
            'fire':0.5,
            'water':2,
            'grass':0.5,
            'dragon':0.5
        },
        'electric': {
            'flying':2,
            'ground':0,
            'water':2,
            'grass':0.5,
            'electric':0.5,
            'dragon':0.5
        },
        'pyschic': {
            'fighting':2,
            'poison':2,
            'steel':0.5,
            'pyschic':0.5,
            'dark':0
        },
        'ice': {
            'flying':2,
            'ground':2,
            'steel':0.5,
            'fire':0.5,
            'water':0.5,
            'grass':2,
            'ice':0.5,
            'dragon':2
        },
        'dragon': {
            'steel':0.5,
            'dragon':2,
            'fairy':0
        },
        'dark': {
            'fighting':0.5,
            'ghost':2,
            'pyschic':2,
            'dark':0.5,
            'fairy':0.5
        },
        'fairy': {
            'fighting':2,
            'poison':0.5,
            'steel':0.5,
            'fire':0.5,
            'dragon':2,
            'dark':2
        },
    }
    mod = match_up[move_type][target_types[0]] if target_types[0] in match_up[move_type] else 1
    mod *= match_up[move_type][target_type[1]] if target_types[1] and target_types[1] in match_up[move_type] else 1
    return mod

@app.route('/')
def index():
    raw = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_name').text, 'html.parser')
    pokeList = []
    for poke in raw.find_all('a',title=re.compile('[a-zA-Z0-9_]+ \(Pokémon\)$')):
        pokeList.append(poke.text.lower())

    pokeList.sort()
    natures = Nature.query.all()
    return render_template('display.html', pokeList=json.dumps(pokeList), natures=natures)


@app.route('/api/pokemon', methods = ['POST'])
def get_pokemon():
    print("Request form: {}".format(request.form))
    pokemon_name = request.form['pokemon'].lower()

    print("Pokemon: {}".format(pokemon_name))

    if(pokemon_name != ''):
        pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
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
            pokemon = Pokemon(name=pokemon_name, stats=stats)
            db.session.add(pokemon)

            for move in pokestats['moves']:
                m = Move.query.filter_by(name=move['name']).first()
                if m:
                    pokemon.moves.append(m)
                else:
                    m = initMove(move['name'], move['resource_uri'])
                    if m:
                        pokemon.moves.append(m)

            db.session.commit()
            print("Pokemon model: {}".format(pokemon))
        pokejson = pokemon.serialize()
        pokejson['form'] = request.form['formId']
        return json.dumps(pokejson)
    else:
        return 'Error'

@app.route('/api/attack', methods=['PUT'])
def battle():
    move = Move.query.filter_by(name=request.form['move']).first()
    origin = Pokemon.query.filter_by(id=request.form['origin']['id']).first()
    target = Pokemon.query.filter_by(id=request.form['target']['id']).first()

    level = request.form['origin']['level']
    accuracy = request.form['origin']['accuracy'] if 'accuracy' in request.form['origin'] else 100
    evasion = request.form['target']['evasion'] if 'evasion' in request.form['target'] else 100
    crit_chance = request.form['target']['crit_chance'] if 'crit_chance' in request.form['target'] else 16

    if not move:
        return False
    else:
        result = {
            'origin': request.form['origin']['name'],
            'target': request.form['target']['name'],
            'move': move.name
        }

        hit = move.accuracy * (accuracy/evasion)
        if random() > hit/100:
            result['result'] = 'missed.'
            return json.dumps(result)

        mod = 1

        if random() > 1/crit_chance:
            result['crit'] = True
            mod = 1.5

        mod *= 1.5 if move.type in origin.stats['types'] else 1
        mod *= typeMatchUp(move.type,target.stats['types'])
        mod *= uniform(0.85,1)

        if move.category == 'Physical' and move.power > 0:
            attack = request.form['origin']['attack']
            defense = request.form['target']['defense']
            damage = (((((2 * level) + 10)/250) * (attack/defense) * move.power) + 2) * mod
            result['result'] = 'hit for {} damage'.format(int(damage))
        elif move.category == 'Special' and move.power > 0:
            sp_attack = request.form['origin']['sp_attack']
            sp_defense = request.form['target']['sp_defense']
            damage = (((((2 * level) + 10)/250) * (sp_attack/sp_defense) * move.power) + 2) * mod
            result['result'] = 'hit for {} damage'.format(int(damage))
        elif move.category == 'Status':
            result['result'] = move.effect
        else:
            result = False

        return json.dumps(result)


if __name__ == '__main__':
    app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT','8080')))