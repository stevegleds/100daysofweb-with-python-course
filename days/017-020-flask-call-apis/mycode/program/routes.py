from flask import render_template, request
from program import app
from datetime import datetime
import requests

timenow = str(datetime.today())


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Template Demo', time=timenow)


@app.route('/100Days')
def p100days():
    return render_template('100Days.html')


@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)


@app.route('/numbers')
def numbers():
    number = get_numbers()
    return render_template('numbers.html', number=number)


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []  # to store list of pokemon names
    allowed_colours = ['yellow', 'blue', 'red', 'black']
    if request.method == 'POST' and 'pokecolour' in request.form:  # user has POSTed a colour in the user form
        colour = request.form.get('pokecolour')  # this is link from front end to backend
        if colour in allowed_colours:
            pokemon = get_poke_colour(colour)  # get_poke_colour returns list of names
            #  pokemon_count = len(pokemon)
            return render_template('pokemon.html', pokemon=pokemon, pokemon_count=len(pokemon), colour=colour)
        else:
            error = "There is no " + colour + " Pokemon."
            return render_template('pokemon.html', error=error)


def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']


def get_numbers():
    r = requests.get('http://numbersapi.com/random/year?json')
    data = r.json()
    print(data)
    return data['text']


def get_poke_colour(colour):  # colour entered by user form
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + colour.lower())
    # pokemon api expects colour parameter
    pokedata = r.json()
    pokemon = []  # used to store list of pokemon chars with colour specified by user form

    for i in pokedata['pokemon_species']:  # 'name' is key in mini dictionary under 'pokemon_species' dictionary
        pokemon.append(i['name'])
    return sorted(pokemon)


