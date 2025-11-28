
import db

'''
exams is an interface for exams database table.
'''
def get_exam(examname):
    '''get_exam gets an exam from db(exams) with examname:<name>
    
    returns object with structure:
    exam {
        id: int unique
        examname: string unique
        start_key: string
        active: bool
        exercises [
            id: int unique
            exercise: string
            points: int
        ]
    }
    '''
    print("[exams] get exam:", examname)
    sql = """
        SELECT exam.id, exam.examname, exam.start_key, exam.active, exercise.id as exercise_id, exercise.exercise, exercise.points
        FROM exams exam
        LEFT JOIN exercises exercise ON exam.id = exercise.exam_id
        WHERE exam.examname = :examname
        ORDER BY exercise.id
    """
    result = db.query(sql, {"examname":examname})
    if not result:
        print("--exam does not exist")
        return False
    print("--exam exists")
    exam_data = {
        'id': result[0]['id'],
        'examname': result[0]['examname'],
        'start_key': result[0]['start_key'],
        'active': result[0]['active'],
        'exercises': []
    }
    for row in result:
        if row['exercise_id'] is not None:
            exam_data['exercises'].append({'id': row['exercise_id'], 'exercise': row['exercise'], 'points': row['points']})
    return exam_data

def get_all_exams_info(filter=None):
    '''get_all_exams_info returns all exam objects from db(exams) in a list
    
    returns:
    exams[ 
        {
            id: int unique
            examname: string unique
            start_key: string
            active: bool
        },,,
    ]
    '''
    print("[exams] getting all exams:")
    sql = "SELECT id, examname, start_key, active FROM exams WHERE (:filter IS NULL OR examname LIKE '%' || :filter || '%')"
    result = db.query(sql, {"filter":filter})
    if not result:
        print("--no exams exist")
        return False
    print("--at least one exam exists")
    exams = []
    for row in result:
        exam_data = {
            'id': row['id'],
            'examname': row['examname'],
            'start_key': row['start_key'],
            'active': row['active'],
        }
        exams.append(exam_data)
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
    exam = get_exam(examname)
    if exam:
        sql = "DELETE FROM exercises WHERE exam_id=:exam_id"
        db.execute(sql, {"exam_id":exam["id"]})
        sql = "DELETE FROM exams WHERE id=:id"
        db.execute(sql, {"id":exam["id"]})
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
    exam = get_exam(examname)
    if exam:
        sql = "INSERT INTO exercises (exam_id, exercise, points) VALUES ( :exam_id, :exercise, :points)"
        db.execute(sql, {"exam_id":exam['id'], "exercise":exercise, "points":points})
        print("Exercise added successfully.")
        return True
    return False

def remove_exercise(examname, index):
    '''remove_exercise removes exercice and points from exam with examname:<examname> and exercise[index]:<index>.'''
    print("[exams] Removing exercise from", examname)
    exam = get_exam(examname)
    if exam and len(exam['exercises']) > index and - 1 < index:
        sql = "DELETE FROM exercises WHERE id=:exercise_id"
        db.execute(sql, {"exercise_id":exam['exercises'][index]['id']})
        print("Exercise removed successfully.")
        return True
    return False
