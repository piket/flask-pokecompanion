import os
from flask import Flask, render_template, request, session, abort
from flask.ext.sqlalchemy import SQLAlchemy
import requests
import simplejson as json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

# from models import Pokemon
# import pykemon

print(os.environ['APP_SETTINGS'])

from flask_wtf.csrf import CsrfProtect

CsrfProtect(app)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/api/pokemon', methods = ['POST'])
def get_pokemon():
    print("Request form: {}".format(request.form))
    pokemon = request.form['pokemon']
    
    print("Pokemon: {}".format(pokemon))
    
    if(pokemon != ''):
        pokestats = requests.get('http://pokeapi.co/api/v1/pokemon/' + pokemon).text
        # print("Pokestats: {}".format(pokestats))
        return pokestats
    else:
        return 'Error'
    
if __name__ == '__main__':
    app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT','8080')))