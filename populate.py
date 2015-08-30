# import argparse
import sys
from app import generate_pokemon, initMove
import requests
from bs4 import BeautifulSoup
from models import Pokemon

def populate(arg):

    if '-u' in arg or '--update' in arg:
        pokeList = []
        for poke in Pokemon.query.all():
            for move in poke.stats['moves']:
                m = initMove(move['name'],move['resource_uri'])
                if not m in poke.moves:
                    poke.moves.append(m)
                    pokeList.append(poke)

        print("COMPLETED:\n{}".format(pokeList))
    if '-a' in arg or '--all' in arg:
        raw = BeautifulSoup(requests.get('http://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_name').text, 'html.parser')
        pokeList = []
        for poke in raw.find_all('a',title=re.compile('[a-zA-Z0-9_]+ \(Pokémon\)$')):
            pokeList.append(poke.text.lower())

        for i, poke in enumerate(pokeList):
            pokeList[i] = generate_pokemon(poke)

        print("COMPLETED:\n{}".format(pokeList))
    elif isinstance(arg, (list, tuple)):
        pokeList = []
        for poke in arg:
            if isinstance(poke, str):
                pokeList.append(generate_pokemon(poke.lower()))

        print("COMPLETED:\n{}".format(pokeList))
    elif isinstance(arg, str):
        pokemon = generate_pokemon(arg.lower())
        print("COMPLETED:\n{}".format(pokemon))
    else:
        print("Invalid argument(s)")

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Populate database with indicated/all pokemon.')
    # parser.add_argument('strings', type=str, nargs='+', help='a pokemon to populate into the database')
    # parser.add_argument(('-a','--all'), help='populate with complete list of pokemon as determined by bulbapedia')
    # args = parser.parse_args()
    # print(args.accumulate(args.strings))
    args = sys.argv[1:]
    if len(args) == 1:
        populate(args[0])
    elif len(args) == 0:
        print("Invalid number of arguments")
    else:
        populate(args)