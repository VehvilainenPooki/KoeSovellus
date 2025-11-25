import db

'''
attempts is an interface for exam_attempts database table.
'''
def submit_answers(exam_id, user_id, answers):
    '''submit_answers saves answers:<answers> into db(exam_attempts) with exam_id:<exam_id> and username:<username>. It leaves notes and points empty.'''
    print("[exam_attempts] Adding", user_id, "answers to exam with id" , exam_id, ".")
    sql = "INSERT INTO exam_attempts (exam_id, user_id) VALUES ( :exam_id, :user_id)"
    db.execute(sql, {"exam_id":exam_id, "user_id":user_id})
    sql = "SELECT MAX(id) FROM exam_attempts WHERE exam_id = :exam_id AND user_id = :user_id"
    result = db.query(sql, {"exam_id":exam_id, "user_id":user_id})
    attempt_id = result[0][0]
    for exercise in answers:
        exercise[0] = attempt_id
    sql = "INSERT INTO exercise_attempts (attempt_id, exercise_id, answer) VALUES (?, ?, ?)"
    db.executemany(sql, answers)
    print("Answers saved successfully.")
    return True