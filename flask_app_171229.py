# This is a state capital quiz app developed with python, flask and SQLite3
from flask import Flask, render_template, session, url_for, request
from capital_data import Capitals
import random, datetime, sqlite3
import matplotlib.pyplot as plt, mpld3, numpy as np

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
#        save_result(total_correct, number)
        if length == 0:
            return render_template('result_error.html')
        elif total_correct == number:
            return render_template('result_perfect.html', total_correct = total_correct, number = number)
        elif total_correct / number > .699:
            return render_template('result.html', total_correct = total_correct, wrong = wrong)
        else:
            return render_template('result_warning.html', total_correct = total_correct, wrong = wrong)

@app.route('/stats')
def stats():
#    dat20avg, dat20plot, dat50avg, dat50plot = get_stats()
#    return render_template('stats.html', dat20avg = dat20avg, dat20plot = dat20plot, dat50avg = dat50avg, dat50plot = dat50plot)
    return render_template('stats_temp.html')


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

def get_stats():
    # open connection to database
    conn = sqlite3.connect('capital_db.sqlite')
    cur = conn.cursor()
    # get score data for 20 and 50 questions quizs
    cur.execute('SELECT score FROM Scores WHERE quiz=20')
    d20 = cur.fetchall()
    dt = np.dtype('int')
    dat20 = np.asarray(d20, dt)
    dat20 = np.reshape(dat20, -1)
    cur.execute('SELECT score FROM Scores WHERE quiz=50')
    d50 = cur.fetchall()
    dat50 = np.asarray(d50, dt)
    dat50 = np.reshape(dat50, -1)
    # calculate stats
    dat20avg = get_average(dat20)
    dat50avg = get_average(dat50)
    # create histograms
    dat20plot = get_plot(dat20, 21)
    dat50plot = get_plot(dat50, 51)
    # close database connection
    cur.close()
    conn.close()
    return dat20avg, dat20plot, dat50avg, dat50plot

def get_average(dat):
    dict = {}
    dict['mean'] = int(np.mean(dat) + 0.5)
    dict['median'] = int(np.median(dat) + 0.5)
    dict['std'] = int(np.std(dat) + 0.5)
    dict['attempts'] = len(dat)
    return dict

def get_plot(dat, bwidth):
    if bwidth <50:
        step = 1
    else:
        step = 2
    counts = np.bincount(dat)
    fig, ax = plt.subplots()
    ax.bar(range(bwidth), counts, width=1, align='center')
    ax.set(xticks=range(0, bwidth, step), xlim=[-1, bwidth])
    plt.title("Histogram of Quiz Scores")
    chart = mpld3.fig_to_html(fig)
    return chart

if __name__ == '__main__':
    app.run()
