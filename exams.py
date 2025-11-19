
import db

'''
exams is an interface for exams database table.
'''
def get_exam(examname):
    '''get_exam gets an exam from db(exams) with examname:<name>'''
    print("[exams] get exam:", examname)
    sql = "SELECT * FROM exams WHERE examname=:examname"
    result = db.query(sql, {"examname":examname})
    if not result:
        print("--exam does not exist")
        return False
    print("--exam exists")
    exam = result[0]
    return dict(exam)

def get_all_names():
    '''get_all_names returns all examname values from db(exams) in a list'''
    print("[exams] getting all exams:")
    sql = "SELECT examname FROM exams"
    result = db.query(sql)
    exams = [item[0] for item in result]
    if not exams:
        print("--The db(exams) has no data")
        return False
    print("--At least one exam exists")
    return exams

def create_exam(examname, start_key):
    '''create_exam creates exam with examname:<examname> start_key:<start_key> active:False into db(exams).'''
    print("[exams] Creating", examname, start_key)
    if not get_exam(examname):
        sql = "INSERT INTO exams (examname, start_key, active) VALUES ( :examname, :start_key, :active)"
        db.execute(sql, {"examname":examname, "start_key":start_key, "active":False})
        print("Exam created successfully.")
        return True
    return False

def remove_exam(examname):
    '''remove_exam removes exam from db(exams).'''
    print("[exams] Removing exam from", examname)
    if get_exam(examname):
        sql = "DELETE FROM exams WHERE examname=:examname"
        db.execute(sql, {"examname":examname})
        print("exam removed successfully.")
        return True
    return False

def activate_exam(examname):
    '''activate_exam activates exam so a user can do the exam.'''
    print("[exams] Activating ", examname)
    if get_exam(examname):
        sql = "UPDATE exams SET active = TRUE WHERE examname=:examname"
        db.execute(sql, {"examname":examname})
        print("Exam activated successfully.")
        return True
    return False

def deactivate_exam(examname):
    '''deactivate_exam deactivates exam so a user can not do the exam.'''
    print("[exams] Deactivating ", examname)
    if get_exam(examname):
        sql = "UPDATE exams SET active = FALSE WHERE examname=:examname"
        db.execute(sql, {"examname":examname})
        print("Exam deactivated successfully.")
        return True
    return False

def add_exercise(examname, exercise, points):
    '''add_exercise adds exercice and points to exam with examname:<examname>.'''
    print("[exams] Adding exercise to", examname)
    if get_exam(examname):
        sql = "UPDATE exams SET exercises = array_append(exercises, :exercise) WHERE examname=:examname"
        db.execute(sql, {"exercise":exercise, "examname":examname})
        sql = "UPDATE exams SET points = array_append(points, :point) WHERE examname=:examname"
        db.execute(sql, {"point":points, "examname":examname})
        print("Exercise added successfully.")
        return True
    return False

def remove_exercise(examname, index):
    '''remove_exercise removes exercice and points from exam with examname:<examname> and exercise[index]:<index>.'''
    print("[exams] Removing exercise from", examname)
    if get_exam(examname):
        indexminus = index -1
        indexplus = index +1
        sql = "UPDATE exams SET exercises = array_cat(exercises[\: :indexminus], exercises[:indexplus\:]) WHERE examname=:examname"
        db.execute(sql, {"indexminus":indexminus, "indexplus":indexplus, "examname":examname})
        sql = "UPDATE exams SET points = array_cat(points[\: :indexminus], points[:indexplus\:]) WHERE examname=:examname"
        db.execute(sql, {"indexminus":indexminus, "indexplus":indexplus, "examname":examname})
        print("Exercise removed successfully.")
        return True
    return False
