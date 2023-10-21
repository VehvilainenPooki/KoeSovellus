from sqlalchemy.sql import text

from db import db

'''
examManager is an interface for (exams) database.
'''


def get_exam(name):
    '''get_exam gets an exam from db(exams) with examname:<name>'''
    
    print("[exams] get exam:", name)
    
    sql = "SELECT * FROM exams WHERE examname=:examname"
    result = db.session.execute(text(sql), {"examname":name})
    exam = result.fetchone()
    
    if not exam:
        print("--exam does not exist")
        return False
    
    print("--exam exists")
    return exam