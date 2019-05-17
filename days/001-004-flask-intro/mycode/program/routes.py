from program import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/myresults')
def my_results():
    return render_template('my_results.html')


@app.route('/mypaceresults')
def my_pace_results():
    return render_template('my_pace_results.html')


if __name__ == '__main__':
    app.run()