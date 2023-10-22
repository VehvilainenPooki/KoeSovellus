from sqlalchemy.sql import text

from db import db

'''
examManager is an interface for (exams) database.
'''


def get_exam(examname):
    '''get_exam gets an exam from db(exams) with examname:<name>'''
    
    print("[exams] get exam:", examname)
    
    sql = "SELECT * FROM exams WHERE examname=:examname"
    result = db.session.execute(text(sql), {"examname":examname})
    exam = result.fetchone()
    
    if not exam:
        print("--exam does not exist")
        return False
    
    print("--exam exists")
    return exam

def get_all_names():
    '''get_all_names returns all examname values from db(exams) in a list'''
    
    print("[exams] getting all exams:")
    
    sql = "SELECT examname FROM exams"
    result = db.session.execute(text(sql))
    exams = [item[0] for item in result.fetchall()]
    
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
        db.session.execute(text(sql), {"examname":examname, "start_key":start_key, "active":False})
        db.session.commit()
        print("Exam created successfully.")
        return True
    return False

def add_exercise(examname, exercise, points):
    '''add_exercise adds exercice and points to exam with examname:<examname>.'''
    print("[exams] Adding exercise to", examname)
    if get_exam(examname):
        sql = "UPDATE exams SET exercises = array_append(exercises, :exercise) WHERE examname=:examname"
        db.session.execute(text(sql), {"exercise":exercise, "examname":examname})
        sql = "UPDATE exams SET points = array_append(points, :point) WHERE examname=:examname"
        db.session.execute(text(sql), {"point":points, "examname":examname})
        db.session.commit()
        print("Exercise added successfully.")
        return True
    return False

def remove_exercise(examname, index):
    '''remove_exercise removes exercice and points from exam with examname:<examname> and exercise[index]:<index>.'''
    print("[exams] Removing exercise from", examname)
    print(1)
    if get_exam(examname):
        print(2)
        indexminus = index -1
        indexplus = index +1
        sql = "UPDATE exams SET exercises = array_cat(exercises[\: :indexminus], exercises[:indexplus\:]) WHERE examname=:examname"
        db.session.execute(text(sql), {"indexminus":indexminus, "indexplus":indexplus, "examname":examname})
        print(3)
        sql = "UPDATE exams SET points = array_cat(points[\: :indexminus], points[:indexplus\:]) WHERE examname=:examname"
        db.session.execute(text(sql), {"indexminus":indexminus, "indexplus":indexplus, "examname":examname})
        print(4)
        db.session.commit()
        print(5)
        print("Exercise removed successfully.")
        return True
    return False

def remove_exam(examname):
    '''remove_exam removes exam from db(exams).'''
    print("[exams] Removing exercise from", examname)
    print(1)
    if get_exam(examname):
        print(2)
        sql = "REMOVE * FROM exams WHERE examname=:examname"
        db.session.execute(text(sql), {"examname":examname})
        db.session.commit()
        print(5)
        print("exam removed successfully.")
        return True
    return False

#---------exam_results-------------

def submit_answers(examname, username, answers):
    '''submit_answers saves answers:<answers> into db(exam_results) with examname:<examname> and username:<username>. It leaves notes and points empty.'''
    print("[exam_results] Adding", username, "answers to" , examname, ".")
    sql = "INSERT INTO exam_results (examname, username, answers) VALUES ( :examname, :username, :answers)"
    db.session.execute(text(sql), {"examname":examname, "username":username, "answers":answers})
    db.session.commit()
    print("Answers saved successfully.")
    return True

