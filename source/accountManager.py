from sqlalchemy.sql import text

from werkzeug.security import check_password_hash, generate_password_hash


from db import db


'''
accountManager is an interface for (users) database.
'''




def get_user(username):
    '''get_user gets a user from db(users) with username:<username>'''
    
    print("[users] get user:", username)
    
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    
    if not user:
        print("--User does not exist")
        return False
    
    print("--User exists")
    return user



def __is_correct_password(hash, password):
    '''is_correct_password checks are <hash> and <password> the same password.'''
    
    print("-Correct password?")
    
    if check_password_hash(hash, password):
        print("--True")
        return True
    
    print("--False")
    return False



def is_correct_user_password(username, password):
    '''is_correct_user_password Checks'''
    
    user = get_user(username)
    
    if user:
        return __is_correct_password(user.password, password)

    return False


def __is_admin(user):
    '''__is_admin checks if user:<user> is admin.'''
    print("Is user admin:")
    if user.is_admin:
        print("True")
        return True
    print("False")
    return False

def is_user_admin(username):
    '''is_user_admin checks is a user with username:<username> an admin user.'''
    user = get_user(username)
    if user:
        return __is_admin(user)
    return False
    


def create_account(username, password, is_admin):
    print("Creating account:")
    if not get_user(username):
        print("Adding user to (users) database.")
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
        db.session.execute(text(sql), {"username":username, "password":hash_value, "is_admin":is_admin})
        db.session.commit()
        print("Account creation successful.")
        return True
    print("-Account creation failed. Username already in use.")
    return False



def __change_password(username, password):
    print("Changing password:")

    hash_value = generate_password_hash(password)
    sql = "UPDATE users SET password=:password WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username, "password":hash_value})
    return True

def change_password(username, oldPassword, newPassword):
    user = get_user(username)
    if not user:
        return False
    if __is_correct_password(user, oldPassword):
        return False

    return __change_password(username, newPassword)

def change_user_password_as_admin(admin_username, username, newPassword):
    print("[admin]Changing ", username, " password:")
    user = get_user(username)
    if is_user_admin(username=admin_username):
        return False
    if not user:
        return False
    
    return __change_password(username, newPassword)

#------------------OLD------------------

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
    print("Checking if password is correct:")
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
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

def change_password(username, oldPassword, newPassword):
    print("Changing password:")
    print("-Checking if password correct")
    if check_password_correct(username, oldPassword):
        print("--True")
        sql = "UPDATE users SET password=:password WHERE username=:username"
        result = db.session.execute(text(sql), {"username":username, "password":newPassword})
        return True
    print("--False")
    print("Password change failed")
    return False

def change_user_password_as_admin(admin_username, admin_password, username, newPassword):
    print("[admin]Changing users password:")
    print("-Checking if adminusercorrect")
    if check_password_correct(admin_username, admin_password) and check_admin(admin_username):
        print("True")
    
    
    print("False")
    return False

