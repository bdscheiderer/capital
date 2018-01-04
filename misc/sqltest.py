# set up test mysql db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import matplotlib, datetime
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="bdscheid",
    password="password_db",
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
    # create histograms
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
    mpld3.show(chart)
    return chart

def insert_result(newdata):
    date = datetime.datetime.now().strftime("%y-%m-%d")
    print(newdata, date)
    me = scores(Date=date, Quiz=newdata[0], Score=newdata[1])
    db.session.add(me)
    db.session.commit()

@app.route("/")
def hello():
    return "Welcome to Python Flask App!"

newdata = [20,15]
insert_result(newdata)

print('Done')

#if __name__ == "__main__":
#    app.run()
