# set up test mysql db

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

print('Done')

@app.route("/")
def hello():
    return "Welcome to Python Flask App!"

#if __name__ == "__main__":
#    app.run()
