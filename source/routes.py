from app import app
import accountManager as aM
from flask import redirect, render_template, request, session

from os import getenv

app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def home():
    session["admin"] = False
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
            if aM.check_admin(username):
                session["admin"] = True
            del session["incorrectLogin"]
            return redirect("/profile")

    session["incorrectLogin"] = True    
    return render_template("login.html")

    

@app.route("/account-creation", methods=["GET","POST"])
def account_creation():
    print(session["admin"]) 
    if session["admin"]:
            
        if request.method == "GET":
            return render_template("account-creation.html")
        
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        is_admin = request.form["is_admin"]

        if is_admin == "on":
            is_admin = 't'
        else:
            is_admin = 'f'

        if password == password_again:
            aM.create_account(username, password, is_admin)
            return render_template("account-creation.html")

        return render_template("account-creation.html")
    return render_template("not-admin.html")


    

@app.route("/profile", methods=["GET","POST"])
def profile():
    try:
        if session["username"]:
            return render_template("profile.html")
    except:
        1
    return redirect("/")

@app.route("/logout")
def logout():
    try:
        del session["username"]
    except:
        1
    return redirect("/")