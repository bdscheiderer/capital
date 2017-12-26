from flask import Flask, render_template, url_for, request
from capital_data import Capitals
import random


app = Flask(__name__)

Capitals = Capitals()

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/quiz", methods = ["POST"])
def quiz():
    if request.method == "POST":
        if request.form['Submit'] == "20 Questions":
            n = 20
        else:
            n = 50
    total_correct = 0
    allstates = list(Capitals.keys())
    cities = []
    capitals_states = []
    if n < 50:
        states = random.sample(allstates, n)
    else:
        states = allstates
    for state in states:
        allcities = list(Capitals.values())
        # identify correct answer
        capital = Capitals[state]
        # get three more possible answers and random shuffle answers
        allcities.remove(capital)
        cities = random.sample(allcities, 3)
        cities.append(capital)
        random.shuffle(cities)
        # add state to list of cities at fifth index
        cities.append(state)
        # create list of cities and states to pass to quiz form
        capitals_states.append(cities)
        # shuffle the quesitons
        random.shuffle(capitals_states)
    return render_template("quiz.html", capitals_states = capitals_states)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/map')
def map():
    return render_template('map.html', capitals = Capitals)

@app.route('/result', methods = ["POST"])
def result():
    if request.method == "POST":
        answers = request.form
        correct = check(answers)
        return render_template('result.html', n = correct)

@app.route('/stats')
def stats():
    return render_template('stats.html')

def check(answers):
    for answer in answers: print(answers[answer], answer)
    return 99

if __name__ == '__main__':
    app.run(debug=True)
