from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/hub-user", methods=["POST"])
def hubuser():
    return render_template("hub-user.html", kt=request.form["kt"])

@app.route("/hub-admin")
def hubadmin():
    return render_template("hub-admin.html")

@app.route("/kurssi/uusi")
def uusiKurssi():
    return render_template("exam-new.html")


@app.route("/kurssi/<int:id>", methods=["POST"])
def kurssi(id):
    if (int(request.form["mode"])==0):
        return render_template("exam-open.html", number=id)
    return render_template("exam-mod.html", number=id)
