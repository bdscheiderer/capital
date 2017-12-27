from flask import Flask, render_template, session, redirect, url_for, escape, request
from capital_data import Capitals
import random, datetime, sqlite3

app = Flask(__name__)
app.secret_key = "anyrandomstring"

Capitals = Capitals()

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/quiz", methods = ["POST"])
def quiz():
    if request.method == "POST":
        if request.form['Submit'] == "20":
            n = 20
        else:
            n = 50
    session['number'] = n
    capitals_states = questions(n, Capitals)
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
        length = len(answers)
        number = session['number']
        total_correct, wrong = check(answers, Capitals)
        save_result(total_correct, number)
        if length == 0:
            return render_template('result_error.html')
        elif total_correct == number:
            return render_template('result_perfect.html', total_correct = total_correct, number = number)
        elif total_correct / number > .699:
            return render_template('result.html', total_correct = total_correct, message = "Greet score!", wrong = wrong)
        else:
            return render_template('result_warning.html', total_correct = total_correct, message = "Keep practicing", wrong = wrong)

@app.route('/stats')
def stats():
    return render_template('stats.html')

def questions(n, Capitals):
        allstates = list(Capitals.keys())
        cities = []
        capitals_states = []
        if n < 50:
            states = random.sample(allstates, n)
        else:
            states = allstates
        for state in states:
            # identify correct answer
            capital = Capitals[state]
            # get three more possible answers to create list of four
            allcities = list(Capitals.values())
            allcities.remove(capital)
            cities = random.sample(allcities, 3)
            cities.append(capital)
            # shuffle the four possible answers
            random.shuffle(cities)
            # add state to list of cities at fifth index
            cities.append(state)
            # create list of the list of four cities and state to pass to quiz
            capitals_states.append(cities)
        # shuffle the list of quesitons
        random.shuffle(capitals_states)
        return capitals_states

def check(answers, Capitals):
    total_correct = 0
    wrong = []
    # answers is a dict, keys are the states, and values are the capital guess
    for answer in answers:
        state = answer
        city_quess = answers[answer]
        city_correct = Capitals[state]
        if city_correct == city_quess:
            total_correct = total_correct + 1
        else:
            wrong.append([city_correct, state])
    print(total_correct, wrong)
    return total_correct, wrong

def save_result(total_correct, number):
    date = datetime.datetime.now().strftime("%y-%m-%d")
    conn = sqlite3.connect('capital_db.sqlite')
    cur = conn.cursor()
    cur.execute('INSERT INTO Scores (datestamp, quiz, score) VALUES (?, ?, ?)', (date, number, total_correct,))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
