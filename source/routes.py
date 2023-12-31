from app import app
import accountManager as aM
import examManager as eM
from flask import redirect, render_template, request, session

from os import getenv

import sys


app.secret_key = getenv("SECRET_KEY")



#------------Home Page----------------------
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
            if session["admin"]:
                return render_template("profile.html", exams=eM.get_all_names())
            return render_template("profile.html")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
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
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

@app.route("/logout")
def logout():
    session.clear()
    session["admin"] = False
    return redirect("/")


#-----------Managing Exams-----------------
@app.route("/create-exam", methods=["GET", "POST"])
def create_exam():
    if session["admin"]:
        if request.method == "GET":
            return render_template("exam-creation.html")
        else:
            examname = request.form["examname"]
            start_key = request.form["start_key"]
            if eM.create_exam(examname, start_key):
                session["exam-created"] = True
                return redirect("/profile")
            else:
                return render_template("exam-creation.html", failed=True)
    return render_template("not-admin.html")

@app.route("/edit-exam/<string:examname>", methods=["GET", "POST"])
def edit_exam(examname):
    try:
        if session["username"] and session["admin"]:
            exam = eM.get_exam(examname)
            if exam:
                if request.method == "POST":
                    print(1)
                    addRemove = request.form["addRemove"]
                    print(2)
                    if addRemove == "add":
                        print(3)
                        exercise = request.form["exercise"]
                        points = request.form["points"]
                        eM.add_exercise(examname, exercise, points)
                    elif addRemove == "remove":
                        print(4)
                        index = int(request.form["index"]) + -1
                        print(5)
                        eM.remove_exercise(examname, index)
                    elif addRemove == "activate":
                        eM.activate_exam(examname)
                    else:
                        eM.deactivate_exam(examname)
                    print(6)
                    exam = eM.get_exam(examname)
                    print(7)
                    return render_template("exam-editing.html", exam=examname, exercises=exam.exercises, points=exam.points)
                else:
                    return render_template("exam-editing.html", exam=examname, exercises=exam.exercises, points=exam.points)
            return redirect("/profile")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

@app.route("/remove-exam/<string:examname>", methods=["GET", "POST"])
def remove_exam(examname):
    try:
        if session["username"] and session["admin"]:
            if eM.remove_exam(examname):
                1#TBD Add some way to communicate if removal failed.
            return redirect("/profile")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        raise
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

#------------Doing Exams-------------------
@app.route("/exam", methods=["POST"])
def exam():
    try:
        if session["username"]:
            examname = request.form["examname"]
            start_key = request.form["start_key"]
            exam = eM.get_exam(examname)
            if exam:
                if exam.start_key == start_key and exam.active:
                    url = "/exam/" + examname
                    return redirect(url)
            return redirect("/profile")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
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
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")


#-----------Reviewing Answers--------------


