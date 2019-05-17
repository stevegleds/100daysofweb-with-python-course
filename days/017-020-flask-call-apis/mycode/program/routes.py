from flask import render_template
from program import app
from datetime import datetime

timenow = str(datetime.today())

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Template Demo', time=timenow)


@app.route('/100Days')
def p100days():
    return render_template('100Days.html')
