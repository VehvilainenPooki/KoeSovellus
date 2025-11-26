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

def get_full_attempt_info(attempt_id):
    '''get_full_attempt_info gets the complete joined object for the attempt_id
        structure:
        exam_attempt:
        {
            "attempt_id": 1,
            "exam_id": 1,
            "examname": "Final Exam",
            "start_key": "abc123",
            "active": true,
            "user_id": 1,
            "username": "john_doe",
            "is_admin": false,
            "exercises": [
                {
                "exercise_id": 1,
                "exercise_text": "What is SQL?",
                "points": 10,
                "answer": "Structured Query Language",
                "score": 8,
                "note": "Good answer"
                },
                {
                "exercise_id": 2,
                "exercise_text": "Explain joins",
                "points": 15,
                "answer": "JOINs combine rows from two or more tables",
                "score": 12,
                "note": "Excellent explanation"
                },
                ...
            ]
        }
    '''
    print("[exam_attempts] getting", attempt_id, " attempt full info.")
    sql = '''
        SELECT 
        exam_attempts.id,
        exam_attempts.exam_id,
        exams.examname,
        exams.start_key,
        exams.active,
        exam_attempts.user_id,
        users.username,
        users.is_admin,
        exercises.id as exercise_id,
        exercises.exercise,
        exercises.points,
        exercise_attempts.answer,
        exercise_attempts.score,
        exercise_attempts.note
        FROM exam_attempts
        JOIN exams ON exam_attempts.exam_id = exams.id
        JOIN users ON exam_attempts.user_id = users.id
        LEFT JOIN exercise_attempts ON exam_attempts.id = exercise_attempts.attempt_id
        LEFT JOIN exercises ON exercise_attempts.exercise_id = exercises.id
        WHERE exam_attempts.id = (?)
        ORDER BY exercises.id;
    '''
    result = db.query(sql, attempt_id)
    if not result:
        return False
    attempt_data = {
        'attempt_id': result[0]['id'],
        'exam_id': result[0]['exam_id'],
        'examname': result[0]['examname'],
        'start_key': result[0]['start_key'],
        'active': result[0]['active'],
        'user_id': result[0]['user_id'],
        'username': result[0]['username'],
        'is_admin': result[0]['is_admin'],
        'exercises': []
    }
    for row in result:
        if row['exercise_id']:
            exercise_data = {
                'exercise_id': row['exercise_id'],
                'exercise_text': row['exercise'],
                'points': row['points'],
                'answer': row['answer'],
                'score': row['score'],
                'note': row['note']
            }
            attempt_data['exercises'].append(exercise_data)
    print("attempt fetched successfully.")
    return attempt_data
