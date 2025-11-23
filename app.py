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
        return True
    if "csrf_token" not in request.form:
        print("not_logged_in triggered")
        return True
    if request.form["csrf_token"] != session.get("csrf_token"):
        print("not_logged_in triggered")
        return True
    return False

#-----------------Home Page---------------------
@app.route("/")
def home():
    if "admin" not in session:
        session.get("admin") = False
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
        if session.get("username"):
            if session.get("admin"):
                return render_template("profile.html", exams=exams.get_all_exams_info())
            return render_template("profile.html")
    except KeyError:
        return render_template("/not-logged-in.html")
    except:
        raise
        error = ("Unexpected error:", sys.exc_info())
        return render_template("error.html", error=error)
    return render_template("/not-logged-in.html")

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if not_logged_in():
        return render_template("/not-logged-in.html")
    try:
        if session.get("username"):
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
        error = ("Unexpected error:", sys.exc_info())
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
    if not session.get("admin"):
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
    if not_logged_in():
        return render_template("/not-logged-in.html")
    if not session.get("admin"):
        return render_template("/not-admin.html")
    try:
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
                return render_template("edit-exam.html", exam=exam)
            else:
                return render_template("edit-exam.html", exam=exam)
        return redirect("/profile")
    except:
        raise
        error = ("Unexpected error:", sys.exc_info())
        return render_template("error.html", error=error)

@app.route("/remove-exam/<string:examname>", methods=["GET", "POST"])
def remove_exam(examname):
    if not_logged_in():
        return render_template("/not-logged-in.html")
    if not session.get("admin"):
        return render_template("/not-admin.html")
    try:
        if exams.remove_exam(examname):
            1#TBD Add some way to communicate if removal failed.
        return redirect("/profile")
    except:
        raise
        error = ("Unexpected error:", sys.exc_info())
        return render_template("error.html", error=error)

#------------Exam attempts-------------------
@app.route("/exam", methods=["POST"])
def exam():
    if not_logged_in():
        return render_template("/not-logged-in.html")
    try:
        examname = request.form["examname"]
        start_key = request.form["start_key"]
        exam = exams.get_exam(examname)
        if exam:
            if exam["start_key"] == start_key and exam["active"]:
                url = "/exam/" + examname
                return redirect(url)
        return redirect("/profile")
    except:
        raise
        error = ("Unexpected error:", sys.exc_info())
        return render_template("error.html", error=error)

@app.route("/exam/<string:examname>", methods=["POST", "GET"])
def exam_num(examname):
    if not_logged_in():
        return render_template("/not-logged-in.html")
    try:
        #Would be great if this query could be removed. Passing the value from /exam to here, but can't figure it out.
        exam = exams.get_exam(examname)
        if exam:
            if request.method == "POST":
                1
                #TODO: exercise attempt logic
            else:
                return render_template("exam.html", exam=examname, exercises=exam["exercises"])
        return redirect("/profile")
    except:
        raise
        error = ("Unexpected error:", sys.exc_info())
        return render_template("error.html", error=error)

#-----------Exam Review--------------
