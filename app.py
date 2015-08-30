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
        elif 'beam' in m and not '_Beam' in m:
            m = m.replace('beam','_Beam')
            t = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text, 'html.parser')
            move_type = t.find('a', title=regType)
            category = t.find('a',title=regCategory)
            if not move_type:
                return False
        elif 'punch' in m and not '_Punch' in m:
            m = m.replace('punch','_Punch')
            t = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text, 'html.parser')
            move_type = t.find('a', title=regType)
            category = t.find('a',title=regCategory)
            if not move_type:
                return False
        elif 'powder' in m and not '_Powder' in m:
            m = m.replace('powder','_Powder')
            t = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text, 'html.parser')
            move_type = t.find('a', title=regType)
            category = t.find('a',title=regCategory)
            if not move_type:
                return False
        elif 'breath' in m and not '_Breath' in m:
            m = m.replace('breath','_Breath')
            t = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text, 'html.parser')
            move_type = t.find('a', title=regType)
            category = t.find('a',title=regCategory)
            if not move_type:
                return False
        else:
            return False

    move_stats = json.loads(requests.get('http://pokeapi.co'+move_link).text)
    new_move = Move(name=m.replace('_',' '), type=move_type.text.strip(), category=category.text.strip(), power=move_stats['power'], accuracy=move_stats['accuracy'], pp=move_stats['pp'], effect=move_stats['description'])
    return new_move

def typeMatchUp(move_type, target_types):
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
    mod = match_up[move_type.lower()][target_types[0].lower()] if target_types[0].lower() in match_up[move_type.lower()] else 1
    mod *= match_up[move_type.lower()][target_types[1].lower()] if len(target_types) > 1 and target_types[1].lower() in match_up[move_type.lower()] else 1
    return mod

def generate_pokemon(pokemon_name):
    print("\n****************************************************************\nBEGIN: GENERATE_POKEMON\n****************************************************************\n\n")
    pokemon_name = pokemon_name.lower()
    if(pokemon_name != ''):
        pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
        if pokemon is None:
            json_data = requests.get('http://pokeapi.co/api/v1/pokemon/' + pokemon_name).text

            if json_data == '':
                return None
            else:
                pokestats = json.loads(json_data)
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
                    m = Move.query.filter_by(name=move['name'].title()).first()
                    if m:
                        print("** {} found".format(m.name))
                        pokemon.moves.append(m)
                    else:
                        m = Move.query.filter_by(name=move['name'].replace('-',' ').title()).first()
                        if m:
                            print("** {} found".format(m.name))
                            pokemon.moves.append(m)
                        else:
                            m = initMove(move['name'], move['resource_uri'])
                            if m:
                                pokemon.moves.append(m)
                                print("Move created: {}".format(m.name))

                db.session.commit()
                print("Pokemon model: {}".format(pokemon))
                return pokemon
        else:
            print("Pokemon found {}".format(pokemon))
            return pokemon
    else:
        return None

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
            'crit': False
        }

        hit = move.accuracy * (accuracy/evasion)
        if random() > hit/100:
            result['result'] = 'missed.'
            return json.dumps(result)

        mod = 1

        if random() > 1/crit_chance:
            result['crit'] = True
            mod = 1.5

        print("Crit? {} Mod: {}".format(result['crit'],mod))

        mod *= 1.5 if move.type in origin.stats['types'] else 1
        mod *= typeMatchUp(move.type,target.stats['types'])
        mod *= uniform(0.85,1)

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