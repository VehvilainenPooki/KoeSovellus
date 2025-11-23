from werkzeug.security import check_password_hash, generate_password_hash

import db

'''
users is an interface for users database table.
'''
def get_user(username):
    '''get_user gets an user from db(users) with username:<username>'''
    print("[users] get user:", username)
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.query(sql, {"username":username})
    if not result:
        print("--User does not exist")
        return False
    print("--User exists")
    user = result[0]
    return dict(user)

def get_all_users_info(filter=False):
    '''get_all_users_info returns all user objects from db(users) in a list
    
    returns:
    exams[ 
        {
            id: int unique
            username: string unique
            is_admin: bool
        },,,
    ]
    '''
    print("[users] getting all users:")
    if filter:
        print("Filter exists and is:", filter)
        sql = "SELECT id, username, is_admin FROM users WHERE username LIKE ?"
        result = db.query(sql, ["%" + filter + "%"])
    else:
        print("No filter, getting all")
        sql = "SELECT id, username, is_admin FROM users"
        result = db.query(sql)
    if not result:
        print("--no users exist")
        return False
    print("--at least one user exists")
    users = []
    for row in result:
        user_data = {
            'id': row['id'],
            'username': row['username'],
            'is_admin': row['is_admin'],
        }
        users.append(user_data)
    return users

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
        print(user)
        return __is_correct_password(user["password"], password)
    return False

def __is_admin(user):
    '''__is_admin checks if user:<user> is admin.'''
    print("Is user admin:")
    if user["is_admin"]:
        print("True", user)
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
        db.execute(sql, {"username":username, "password":hash_value, "is_admin":is_admin})
        print("Account creation successful.")
        return True
    print("-Account creation failed. Username already in use.")
    return False

def __change_password(username, password):
    print("Changing password:")
    hash_value = generate_password_hash(password)
    sql = "UPDATE users SET password=:password WHERE username=:username"
    result = db.execute(sql, {"username":username, "password":hash_value})
    return True

def change_user_password(username, oldPassword, newPassword):
    user = get_user(username)
    if not user:
        return False
    if not __is_correct_password(user.password, oldPassword):
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

def add_admin(username):
    print("Change", username, "to ADMIN:")
    try:
        sql = "UPDATE users SET is_admin=:is_admin WHERE username=:username"
        result = db.execute(sql, {"username":username, "is_admin": True})
        print("--Success")
        return True
    except:
        return False

def remove_admin(username):
    print("Change", username, "to NOT BE ADMIN:")
    try:
        sql = "UPDATE users SET is_admin=:is_admin WHERE username=:username"
        result = db.execute(sql, {"username":username, "is_admin": False})
        print("--Success")
        return True
    except:
        return False
