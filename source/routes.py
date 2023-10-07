from app import app
import accountManager
from flask import render_template


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/account-creation")
def account_creation():
    return render_template("account-creation.html")
