from sqlalchemy.sql import text

from werkzeug.security import check_password_hash, generate_password_hash



from db import db



def check_does_account_exist(username):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    print("Does account exist:")
    if not user:
        print("False")
        return False
    print("True")
    return True

def check_is_password_correct():
    1

def create_account():
    1#todo