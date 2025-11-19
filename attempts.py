import db

'''
attempts is an interface for exam_attempts database table.
'''
def submit_answers(examname, username, answers):
    '''submit_answers saves answers:<answers> into db(exam_results) with examname:<examname> and username:<username>. It leaves notes and points empty.'''
    print("[exam_results] Adding", username, "answers to" , examname, ".")
    sql = "INSERT INTO exam_results (examname, username, answers) VALUES ( :examname, :username, :answers)"
    db.execute(sql, {"examname":examname, "username":username, "answers":answers})
    print("Answers saved successfully.")
    return True