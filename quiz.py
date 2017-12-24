from flask import Flask, render_template, url_for, request
from capital_data import Capitals

app = Flask(__name__)

Capitals = Capitals()

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/quiz", methods = ["POST"])
def quiz():
    if request.form['Submit'] == "20 Questions":
        n = 20
    else:
        n = 50
    return render_template("quiz.html", n = n, capitals = Capitals)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/map')
def map():
    return render_template('map.html', capitals = Capitals)

@app.route('/stats')
def stats():
    return render_template('stats.html')

if __name__ == '__main__':
    app.run(debug=True)
