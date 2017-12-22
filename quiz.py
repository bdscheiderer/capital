from flask import Flask, render_template, url_for
from capital_data import Capitals

app = Flask(__name__)

Capitals = Capitals()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/map')
def map():
    return render_template('map.html', capitals = Capitals)

if __name__ == '__main__':
    app.run(debug=True)
