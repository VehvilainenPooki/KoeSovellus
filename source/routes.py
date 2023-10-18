from app import app
import accountManager as aM
from flask import redirect, render_template, request, session

from os import getenv

app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def home():
    try:
        session["admin"]
    except:        
        session["admin"] = False
    
    return render_template("home-page.html")
    





#------------Account Management-------------

@app.route("/account-creation", methods=["GET","POST"])
def account_creation():
    if session["admin"]:
            
        if request.method == "GET":
            return render_template("account-creation.html")
        
        username = request.form["username"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        
        is_admin = request.form.get("is_admin")
        if is_admin:
            is_admin = 't'
        else:
            is_admin = 'f'

        if password == password_again:
            aM.create_account(username, password, is_admin)
            return render_template("account-creation.html")

        return render_template("account-creation.html")
    return render_template("not-admin.html")

@app.route("/login", methods=["GET","POST"])
def login():
    session["incorrectLogin"] = False
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form["username"]
    password = request.form["password"]

    if (aM.is_correct_user_password(username, password)):
        session["username"] = username
        if aM.is_user_admin(username):
            session["admin"] = True
        del session["incorrectLogin"]
        return redirect("/profile")

    session["incorrectLogin"] = True    
    return render_template("login.html")    

@app.route("/profile", methods=["GET","POST"])
def profile():
    try:
        if session["username"]:
            return render_template("profile.html")
    except:
        1
    return render_template("/not-logged-in.html")



@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    try:
        if session["username"]:
            if request.method == "GET":
                session["notMatching"] = False
                session["incorrectPassword"] = False
                session["changeSuccessful"] = False
                return render_template("change-password.html")
            

            oldPassword = request.form["oldPassword"]
            newPassword = request.form["newPassword"]
            newPasswordAgain = request.form["newPasswordAgain"]
            if newPassword == newPasswordAgain:
                if aM.is_correct_user_password(session["username"], oldPassword):
                    aM.change_user_password(session["username"], oldPassword, newPassword)
                    session["changeSuccessful"] = True
                else:
                    session["incorrectPassword"] = True
                return render_template("change-password.html")
            else:
                session["notMatching"] = True
    except:
        1
    return render_template("/not-logged-in.html")

@app.route("/logout")
def logout():
    session.clear()
    session["admin"] = False
    return redirect("/")