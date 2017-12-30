# set up test mysql db

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import numpy as np

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
#    dat20plot = get_plot(dat20, 21)
#    dat50plot = get_plot(dat50, 51)
    return dict

@app.route("/")
def hello():
    return "Welcome to Python Flask App!"

stats20 = get_stats(20)
stats50 = get_stats(50)
print(stats20, stats50)
print('Done')

#if __name__ == "__main__":
#    app.run()
