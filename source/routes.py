from app import app
import accountManager as aM
import examManager as eM
from flask import redirect, render_template, request, session

from os import getenv

#debug
import sys


app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def home():
    try:
        session["admin"]
    except:        
        session["admin"] = False
    
    return render_template("home-page.html")
    
#
#
#----------------Testataan tätä seuraavaksi:
#
#
@app.route("/exam", methods=["POST"])
def exam():
    try:
        print(1)
        if session["username"]:
            print(2)
            examname = request.form["examname"]
            start_key = request.form["start_key"]
            print(3)
            exam = eM.get_exam(examname)
            print(4)
            if exam:
                print(5)
                if exam.start_key == start_key:
                    print(6)
                    url = "/exam/" + examname
                    return redirect(url)
            print(7)
            return redirect("/profile")
    except Exception:
        print(Exception)
    print(8)
    return render_template("/not-logged-in.html")

@app.route("/exam/<string:examname>", methods=["POST", "GET"])
def exam_num(examname):
    try:
        if session["username"]:
            #Would be great if this query could be removed. Passing the value from exam to here, but can't figure it out.
            exam = eM.get_exam(examname)
            if exam:
                if request.method == "POST":
                    answers = []
                    for i in range(len(exam.exercises)):
                        exercise = "exercise" + str(i)
                        answers.append(request.form[exercise])
                    answers = str(answers).replace("[","{").replace("]","}")
                    eM.submit_answers(exam.examname, session["username"], answers)
                else:
                    return render_template("exam.html", exam=examname, exercises=exam.exercises, points=exam.points)
            return redirect("/profile")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return render_template("/not-logged-in.html")

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