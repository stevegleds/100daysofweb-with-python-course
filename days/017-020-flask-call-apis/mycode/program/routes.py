from flask import render_template
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


def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']