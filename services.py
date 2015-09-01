from app import db
from models import *
import re
import simplejson as json
from bs4 import BeautifulSoup

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

def getBulbaData(move):
    search = move
    existing = Move.query.filter_by(name=search.replace('_',' ')).first()
    if existing:
        print('vv Move found, not created: {}'.format(existing))
        return (existing, True)

    regType = re.compile('[a-zA-Z0-9_]+ \(type\)$')
    regCategory = re.compile('[a-zA-Z0-9_]+ move')

    t = requests.get('http://bulbapedia.bulbagarden.net/wiki/'+m+'_(move)').text
    t = BeautifulSoup(t,'html.parser')
    move_type = t.find('a',title=regType)
    category = t.find('a',title=regCategory)

    if not move_type:
        return (None, None)
    else:
        return (move_type, category)

def initMove(move, move_link):
    m = move.title().replace(' ','_')
    # print(m)
    move_type, category = getBulbaData(m)

    if not move_type:
        if '-' in m:
            m = m.replace('-','_')
            move_type, category = getBulbaData(m)
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'beam' in m and not '_Beam' in m:
            move_type, category = getBulbaData(m.replace('beam','_Beam'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'punch' in m and not '_Punch' in m:
            move_type, category = getBulbaData(m.replace('punch','_Punch'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'kick' in m and not '_Kick' in m:
            move_type, category = getBulbaData(m.replace('kick','_Kick'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'powder' in m and not '_Powder' in m:
            move_type, category = getBulbaData(m.replace('powder','_Powder'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'breath' in m and not '_Breath' in m:
            move_type, category = getBulbaData(m.replace('breath','_Breath'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'fang' in m and not '_Fang' in m:
            move_type, category = getBulbaData(m.replace('fang','_Fang'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'shock' in m and not '_Shock' in m:
            move_type, category = getBulbaData(m.replace('shock','_Shock'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'wave' in m and not '_Wave' in m:
            move_type, category = getBulbaData(m.replace('wave','_Wave'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'whistle' in m and not '_Whistle' in m:
            move_type, category = getBulbaData(m.replace('whistle','_Whistle'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        elif 'dance' in m and not '_Dance' in m:
            move_type, category = getBulbaData(m.replace('dance','_Dance'))
            if not move_type:
                return False
            elif isinstance(move_type,Move):
                return move_type
        else:
            return False

    move_stats = json.loads(requests.get('http://pokeapi.co'+move_link).text)
    new_move = Move(name=m.replace('_',' '), type=move_type.text.strip(), category=category.text.strip(), power=move_stats['power'], accuracy=move_stats['accuracy'], pp=move_stats['pp'], effect=move_stats['description'])
    return new_move

def generate_pokemon(pokemon_name):
    print("\n****************************************************************\nBEGIN: GENERATE_POKEMON\n****************************************************************\n\n")
    pokemon_name = pokemon_name.lower()
    search_name = pokemon_name

    if(pokemon_name != ''):
        pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
        if pokemon is None:
            json_data = requests.get('http://pokeapi.co/api/v1/pokemon/' + search_name.replace('♀','-f').replace('♂','-m')).text

            if json_data == '':
                return None
            else:
                pokestats = json.loads(json_data)
                if not 'name' in pokestats:
                    return None

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
                    'moves': pokestats['moves'],
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
                            else:
                                print("-- Invalid move: {}".format(move['name']))

                db.session.commit()
                print("Pokemon model: {}".format(pokemon))
                return pokemon
        else:
            print("Pokemon found {}".format(pokemon))
            return pokemon
    else:
        return None

def pullStats(list):
    newList = []
    for item in list:
        newList.append(item['name'])
    return newList
