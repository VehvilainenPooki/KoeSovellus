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

def submit_answers(examname, username, answers):
    print("Adding", username, "answers to" , examname, ".")
    sql = "INSERT INTO exam_results (examname, username, answers) VALUES ( :examname, :username, :answers)"
    db.session.execute(text(sql), {"examname":examname, "username":username, "answers":answers})
    db.session.commit()
    print("Answers saved successfully.")
    return True

