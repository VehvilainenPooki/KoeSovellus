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
    if "username" not in session:
        print("not_logged_in triggered")
        return True
    False

def check_csrf():
    if "csrf_token" not in request.form:
        print("csrf check 1 triggered")
        return True
    if request.form["csrf_token"] != session.get("csrf_token"):
        print("csrf check 2 triggered")
        return True
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

@app.route("/profile", methods=["GET"])
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
            if newPassword == newPasswordAgain and request.method == "POST":
                if check_csrf():
                    return render_template("/not-logged-in.html")
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

@app.route("/toggle-admin", methods=["GET", "POST"])
def toggle_admin():
    if not_logged_in():
        return render_template("/not-logged-in.html")
    if not session.get("admin"):
        return render_template("not-admin.html")
    if request.method == "GET":
        return render_template("toggle-admin.html", users=users.get_all_users_info())
    if request.method == "POST":
        if check_csrf():
            return render_template("/not-logged-in.html")
        argument = request.form["argument"]
        username = request.form["toggleUsername"]
        if argument and username:
            if argument == "add":
                print("add")
                users.add_admin(username)
            elif argument == "remove":
                print("remove")
                users.remove_admin(username)
            return render_template("toggle-admin.html", users=users.get_all_users_info())
    return render_template("/error.html", error="WRONG ARGS, if you see this error multiple times contact IT-support")

#-------------------Exam Management------------------------
@app.route("/create-exam", methods=["GET", "POST"])
def create_exam():
    if not_logged_in():
        return render_template("/not-logged-in.html")
    if not session.get("admin"):
        return render_template("not-admin.html")
    if request.method == "GET":
        return render_template("create-exam.html")
    elif request.method == "POST":
        if check_csrf():
            return render_template("/not-logged-in.html")
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
                if check_csrf():
                    return render_template("/not-logged-in.html")
                argument = request.form["argument"]
                if argument == "add":
                    exercise = request.form["exercise"]
                    points = request.form["points"]
                    exams.add_exercise(examname, exercise, points)
                elif argument == "remove":
                    index = int(request.form["index"]) + -1
                    exams.remove_exercise(examname, index)
                elif argument == "activate":
                    exams.activate_exam(examname)
                else:
                    exams.deactivate_exam(examname)
                exam = exams.get_exam(examname)
                return render_template("edit-exam.html", exam=exam)
            else:
                return render_template("edit-exam.html", exam=exam)
        return redirect("/profile")
    except:
        raise
        error = ("Unexpected error:", sys.exc_info())
        return render_template("error.html", error=error)

#TODO: /toggle-exam-activity might be also good to remove that feature from the edit-exam template

@app.route("/remove-exam/<string:examname>", methods=["POST"])
def remove_exam(examname):
    if not_logged_in():
        return render_template("/not-logged-in.html")
    if not session.get("admin"):
        return render_template("/not-admin.html")
    try:
        if request.method == "POST":
            if check_csrf():
                return render_template("/not-logged-in.html")
            if exams.remove_exam(examname):
                1#TODO Add some way to communicate if removal failed.
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
    if check_csrf():
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
                if check_csrf():
                    return render_template("/not-logged-in.html")
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
