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

def create_account(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print("Creating account:")

    print("Checking if username in use:")
    if not user:
        print("False")
        print("Adding user to (users) database.")
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
        print("Account creation successful.")
        return True
    print("True")
    print("Account creation failed. Username already in use.")
    return False