# This is a state capital quiz app developed with python, flask and SQLite3
from flask import Flask, render_template, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from capital_data import Capitals
from credentials import Credentials
import random, datetime, sqlite3
import matplotlib.pyplot as plt, mpld3, numpy as np

Capitals = Capitals()
Credentials = Credentials()

app = Flask(__name__)
key = Credentials['session_password']
app.secret_key = key

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="bdscheid",
    password=Credentials['database_password'],
    hostname="bdscheid.mysql.pythonanywhere-services.com",
    databasename="bdscheid$capital_db",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class scores(db.Model):

    __tablename__ = "Scores"

    ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String)
    Quiz = db.Column(db.Integer)
    Score = db.Column(db.Integer)

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
        # save quiz score to database unless there are zero answers
        if length > 0:
            save_result(total_correct, number)
        # return result template depending on score
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
    dat20, plot20 = get_stats(20)
    dat50, plot50 = get_stats(50)
    return render_template('stats_temp.html', dat20=dat20, dat50=dat50)
#    return render_template('stats.html', dat20=dat20, dat50=dat50, plot20=plot20, plot50=plot50)

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
    me = scores(Date=date, Quiz=number, Score=total_correct)
    db.session.add(me)
    db.session.commit()

def get_stats(n):
    dat = scores.query.filter_by(Quiz=n).all()
    data = []
    for score in dat:
        data.append(score.Score)
    dict = {}
    dict['mean'] = int(np.mean(data) + 0.5)
    dict['median'] = int(np.median(data) + 0.5)
    dict['std'] = int(np.std(data) + 0.5)
    dict['attempts'] = len(data)
    plot = get_plot(data, n+1)
    return dict, plot

def get_plot(data, bwidth):
    if bwidth == 50:
        step = 2
    else:
        step = 1
    counts = np.bincount(data)
    fig, ax = plt.subplots()
    ax.bar(range(bwidth), counts, width=1, align='center')
    ax.set(xticks=range(0, bwidth, step), xlim=[-1, bwidth])
    plt.title("Histogram of Quiz Scores")
    chart = mpld3.fig_to_html(fig, template_type="simple")
    return chart

if __name__ == '__main__':
    app.run()
