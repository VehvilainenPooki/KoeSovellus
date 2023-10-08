from sqlalchemy.sql import text

from werkzeug.security import check_password_hash, generate_password_hash



from db import db



def check_account_exists(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print("Does account exist:")
    if not user:
        print("False")
        return False
    print("True")
    return True

def check_password_correct(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print("Is password correct:")
    hash_value = user.password
    if check_password_hash(hash_value, password):
        print("True")
        return True
    print("False")
    return False

def check_admin(username):
    sql = "SELECT is_admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user:
        if user.is_admin:
            return True
    return False


def create_account(username, password, is_admin):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print("Creating account:")

    print("Checking if username in use:")
    if not user:
        print("False")
        print("Adding user to (users) database.")
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
        db.session.execute(text(sql), {"username":username, "password":hash_value, "is_admin":is_admin})
        db.session.commit()
        print("Account creation successful.")
        return True
    print("True")
    print("Account creation failed. Username already in use.")
    return False