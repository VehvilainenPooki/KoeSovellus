from app import app
import accountManager
from flask import redirect, render_template, request, session


@app.route("/")
def home():
    return render_template("home-page.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        1#todo Login attempt

    return render_template("login.html")

@app.route("/account-creation", methods=["GET","POST"])
def account_creation():
    if request.method == "POST":
        1#todo account creation

    return render_template("account-creation.html")

@app.route("/profile", methods=["GET","POST"])
def profile():
    return render_template("profile.html")
