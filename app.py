import sys
import secrets

from flask import Flask
from flask import render_template, request, session, redirect

import users
import exams
import attempts
import config


app = Flask(__name__)

app.secret_key = config.secret_key

def not_logged_in():
    if "user_id" not in session:
        print("not_logged_in triggered")
        return False
    if "csrf_token" not in request.form:
        print("not_logged_in triggered")
        return False
    if request.form["csrf_token"] != session["csrf_token"]:
        print("not_logged_in triggered")
        return False

#-----------------Home Page---------------------
@app.route("/")
def home():
    if "admin" not in session:
        session["admin"] = False
    return render_template("home-page.html")

#-------------------User Management------------------------
@app.route("/create-account", methods=["GET","POST"])
def account_creation():
    if request.method == "GET":
        return render_template("create-account.html")
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]
    is_admin = 0
    if password == password_again:
        users.create_account(username, password, is_admin)
        return render_template("create-account.html")
    return render_template("create-account.html")

@app.route("/login", methods=["GET","POST"])
def login():
    session["incorrectLogin"] = False
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    if (users.is_correct_user_password(username, password)):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        if users.is_user_admin(username):
            session["admin"] = True
        del session["incorrectLogin"]
        return redirect("/profile")
    session["incorrectLogin"] = True    
    return render_template("login.html")    

@app.route("/profile", methods=["GET","POST"])
def profile():
    if not_logged_in():
        return render_template("/not-logged-in.html")
    try:
        if session["username"]:
            if session["admin"]:
                return render_template("profile.html", exams=exams.get_all_names())
            return render_template("profile.html")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if not_logged_in():
        return render_template("/not-logged-in.html")
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
                if users.is_correct_user_password(session["username"], oldPassword):
                    users.change_user_password(session["username"], oldPassword, newPassword)
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

#-------------------Exam Management------------------------
@app.route("/create-exam", methods=["GET", "POST"])
def create_exam():
    if not_logged_in():
        return render_template("/not-logged-in.html")
    if not session["admin"]:
        return render_template("not-admin.html")
    if request.method == "GET":
        return render_template("create-exam.html")
    else:
        examname = request.form["examname"]
        start_key = request.form["start_key"]
        if exams.create_exam(examname, start_key):
            session["exam-created"] = True
            return redirect("/profile")
        else:
            return render_template("create-exam.html", failed=True)

@app.route("/edit-exam/<string:examname>", methods=["GET", "POST"])
def edit_exam(examname):
    try:
        if session["username"] and session["admin"]:
            exam = exams.get_exam(examname)
            if exam:
                if request.method == "POST":
                    print(1)
                    addRemove = request.form["addRemove"]
                    print(2)
                    if addRemove == "add":
                        print(3)
                        exercise = request.form["exercise"]
                        points = request.form["points"]
                        exams.add_exercise(examname, exercise, points)
                    elif addRemove == "remove":
                        print(4)
                        index = int(request.form["index"]) + -1
                        print(5)
                        exams.remove_exercise(examname, index)
                    elif addRemove == "activate":
                        exams.activate_exam(examname)
                    else:
                        exams.deactivate_exam(examname)
                    print(6)
                    exam = exams.get_exam(examname)
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
            if exams.remove_exam(examname):
                1#TBD Add some way to communicate if removal failed.
            return redirect("/profile")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        raise
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

#------------Exam attempts-------------------
@app.route("/exam", methods=["POST"])
def exam():
    try:
        if session["username"]:
            examname = request.form["examname"]
            start_key = request.form["start_key"]
            exam = exams.get_exam(examname)
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
            exam = exams.get_exam(examname)
            if exam:
                if request.method == "POST":
                    answers = []
                    for i in range(len(exam.exercises)):
                        exercise = "exercise" + str(i)
                        answers.append(request.form[exercise])
                    answers = str(answers).replace("[","{").replace("]","}")
                    exams.submit_answers(exam.examname, session["username"], answers)
                else:
                    return render_template("exam.html", exam=examname, exercises=exam.exercises, points=exam.points)
            return redirect("/profile")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        error = ("Unexpected error:", sys.exc_info()[0])
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

#-----------Exam Review--------------
