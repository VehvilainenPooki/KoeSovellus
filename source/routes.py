from app import app
import accountManager as aM
from flask import redirect, render_template, request, session

from os import getenv

app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def home():
    
    return render_template("home-page.html")

@app.route("/login", methods=["GET","POST"])
def login():
    session["incorrectLogin"] = False
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]
    if (aM.check_account_exists(username)):
        if (aM.check_password_correct(username, password)):
            session["username"] = username
            del session["incorrectLogin"]
            return redirect("/profile")

    session["incorrectLogin"] = True    
    return render_template("login.html")

    

@app.route("/account-creation", methods=["GET","POST"])
def account_creation():
    if request.method == "GET":
        return render_template("account-creation.html")
    
    username = request.form["username"]
    password = request.form["password"]

    return render_template("account-creation.html")


    

@app.route("/profile", methods=["GET","POST"])
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")