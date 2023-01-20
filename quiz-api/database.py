import sqlite3
from models import Answer, Question, Participation
from flask import jsonify




class ErrorHandler(Exception):
    def __init__(self, message: str, errorCode:int):
        self.message = message
        self.errorCode = errorCode
    def __str__(self):
        return "An error occured: " + str(self.errorCode) + f" {self.message}"

def dbCursor():
    db_connection = sqlite3.connect("quiz.db")
    db_connection.isolation_level = None

    cur = db_connection.cursor()
    cur.execute("begin")
    return cur


def GetQuizInfo():
    participations = getAllParticipations()
    scores = []

    quiz_size = getLastQuestionDb()
    if quiz_size == None:
        quiz_size = 0
    for participation in participations:
        scores.append({"playerName": participation.playerName, "score":participation.score})

    result = {"size": quiz_size, "scores": scores}


    return result




def postQuestionDb(question: Question):
    try:
        cur = dbCursor()


        missing_fields = []
        if question.text == None:
            missing_fields.append("text")
        if question.title == None:
            missing_fields.append("title")
        if question.position == None:
            missing_fields.append("position")
        if question.image == None:
            missing_fields.append("image")
        if len(missing_fields) > 0:
            return "Error, missing fields : "+ ''.join([str(a) + ", " for a in missing_fields]), 400

        try:
            question_position = getQuestionPosition(question.position)
        
            if question_position:
                cur.execute(
                    f"UPDATE Question SET position = position + 1 "
                    f"WHERE position >= {question.position!r}"
                )
        except Exception as e:
            print("didnt have to change positions !")
        

        data = (question.text, question.title, question.image, question.position)

        cur.execute("insert into Question (text,title,image,position) values (?,?,?,?)", data)




        cur.execute("commit")
        print("worked for question!")
        cur.close()

        return cur.lastrowid

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("insertion in DB failed:  " + str(e))


def postAnswerDb(answer: Answer, id_question: int):
    try:
        cur = dbCursor()



        missing_fields = []
        if answer.text == None:
            missing_fields.append("text")
        if answer.isCorrect == None:
            missing_fields.append("isCorrect")
        if len(missing_fields) > 0 :
            return "Error, missing fields : "+ ''.join([str(a) + ", " for a in missing_fields]), 400


        text = answer.text
        isCorrect = answer.isCorrect
        cur.execute("insert into Answer (text,isCorrect, id_question) values (?,?,?)", (text, isCorrect, id_question))
        cur.execute("commit")
        print("worked for answer!")
        cur.close()

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("insertion in DB failed:  " + str(e))


def postParticipationDb(participation: Participation):

    cur_participation = dbCursor()
    try:
        cur_participation.execute("insert into Participation (playerName, score) values (?,?)", (participation.playerName, participation.score))
        cur_participation.execute("commit")
        print("worked for participation!")
        cur_participation.close()

        return cur_participation.lastrowid


    except Exception as e:
        cur_participation.execute('rollback')
        cur_participation.close()
        raise Exception("insertion in DB failed:  " + str(e))


def getParticipation(playerName: str):
    try:
        cur = dbCursor()
        cur.execute("SELECT * FROM Participation where playerName = ?", (playerName,))
        result = cur.fetchone()
        playerScore = {"playerName": result[1], "score": result[2]}
        print(result)
        cur.close()

        return playerScore


    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("failed to get participation:  " + str(e))


def getScoreCorrect(list_answer):
    score = 0
    for elt in list_answer:
        if elt == 1:
            score+=1

    return score


def getScore(list_answer):
    score = 0
    for question_num in range(1, len(list_answer) + 1):
        question = getQuestionPosition(question_num)
        if question.isAnswerTrue(list_answer[question_num - 1]):
            score += 1

    return score
        
        

def modifyQuestionDb(q_json, id_question):
    try:
        cur = dbCursor()
        possibleAnswers = q_json.get("possibleAnswers")
        list_answer = []
        for answer in possibleAnswers:
            list_answer.append(Answer(answer.get("text"), answer.get("isCorrect")))

        question = Question(q_json.get("text"), q_json.get("title"), q_json.get("image"), q_json.get("position")
        , list_answer)
        print("\n")
        print("INPUT QUESTION!!!! \n")
        print(question.to_json())
        

        question_json = getQuestionIdDb(id_question)
        

        print(cur)

        if question_json == None:
            raise ErrorHandler("Cannot find this question id: " + str(id_question), 404)

        print("\n")
        print("QUESTION ID!!!!! \n")
        print(question_json)
        print(question.position)
        print(question_json["position"])

        if int(question.position) < question_json["position"]:
            print("triggers if1")
            cur.execute(
                f"UPDATE Question SET position = -1 "
                f"WHERE id = {id_question!r}"
            )

            print("triggers if2")
            cur.execute(
                f"UPDATE Question SET position = position + 1 "
                f"WHERE position >= {question.position!r} and position < {question_json['position']!r}"
            )
            print("triggers if3")

        elif int(question.position) > question_json["position"] :
            print("triggers elif1")
            cur.execute(
                f"UPDATE Question SET position = -1 "
                f"WHERE id = {id_question!r}"
            )
            print("triggers elif2")
            cur.execute(
                f"UPDATE Question SET position = position - 1 "
                f"WHERE position <= {question.position!r} and position > {question_json['position']!r}"
            )
            print("triggers elif3")
        
        print("after IF")
        cur.execute(
            f"UPDATE Question SET position = {question.position!r},"
            f"title = {question.title!r},"
            f"text = {question.text!r},"
            f"image = {question.image!r} WHERE id = {id_question!r}"
        )
        print("after SET")
        cur.execute("DELETE FROM Answer WHERE id_question = ?",(id_question,))
        print("AFTER ANSWER DELETION")
        print("AFTER ANSWER DELETION")

        insert_answer_string = ""
        for answer in question.possibleAnswers:
            insert_answer_string += f"({id_question!r},{answer.text!r},{answer.isCorrect!r}),"

        print("INSERT STRIIIING")
        print("\n \n")

        print(insert_answer_string)

        cur.execute(
            f"insert into Answer (id_question,text,isCorrect) values"
            f"{insert_answer_string[:-1]}"
        )
        

        cur.execute("commit")
        cur.close()


    except ErrorHandler as e:
        cur.execute('rollback')
        cur.close()
        raise e

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("Failed trying to modify question:  " + str(e))


def getQuestionIdDb(id_question: int):
    try:
        cur = dbCursor()

        cur.execute(
            "SELECT * FROM Answer WHERE id_question = ?", (id_question,))
        result_answer = cur.fetchall()
        answers = [Answer(answer[1], answer[2]) for answer in result_answer]

        print("ok 1/2")

        cur.execute("SELECT * FROM Question WHERE id = ?", (id_question,))
        print("ok 2/2")

        result_question = cur.fetchone()
        print(result_question)

        print(cur.rowcount)

        if result_question == None:
            raise ErrorHandler("Cannot find this question id: " + str(id_question), 404)

        print("ok 3/2")

        question = Question(result_question[1],result_question[2],result_question[3],result_question[4], answers)
        print("ok 4/2")
        cur.execute('end')
        cur.close()

        return Question.to_json(question)
        
    except ErrorHandler as e:
        cur.execute('rollback')
        cur.close()
        raise e

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("Error, failed trying to get question by id:  " + str(e))

def getAllParticipations():

    try:
        cur = dbCursor()
            


        cur.execute("SELECT * FROM Participation ORDER BY score DESC")
        
        result = cur.fetchall()


        list_participation = []

        for participation in result:
            list_participation.append(Participation(participation[1], participation[2]))

        cur.execute('end')
        cur.close()

        return list_participation

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("Error, failed trying to get all participations:  " + str(e))


def getAllQuestions():

    try:
        cur = dbCursor()
        print("getting last question position:")
        last_question_pos= getLastQuestionDb()
        print("after last question position:")
        print(last_question_pos)
        cur = dbCursor()
        if last_question_pos == None:
            raise ErrorHandler("No question found in db!", 404)
        
        
        print("after exception:")
            
        
        print("new cursor: ")
        all_questions = []    

        for position in range(last_question_pos):
            cur.execute(f"SELECT * FROM Question WHERE position = {position+1}")

        
            result_question = cur.fetchone()

            if result_question == None:
                continue

            cur.execute(
                f"SELECT * FROM Answer WHERE id_question = {result_question[0]}")

            result_answer = cur.fetchall()
            answers = [Answer(answer[1], answer[2]) for answer in result_answer]

            question = Question(result_question[1],result_question[2],result_question[3],result_question[4], answers)

            all_questions.append(question.to_json())

        cur.execute('end')
        cur.close()

        return {"questions": all_questions}, 200

    except ErrorHandler as e:
        cur.execute('rollback')
        cur.close()
        raise e

    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("Error, failed trying to get all questions:  " + str(e))


def getLastQuestionDb():
    try:
        cur = dbCursor()

        cur.execute("SELECT MAX(position) FROM Question")

        result = cur.fetchone()
        cur.execute('end')
        cur.close()

        return result[0]


    except Exception as e:
        cur.execute('rollback')
        cur.execute('end')
        cur.close()
        return e

def rebuildDb():
    createTableQuestion()
    createTableAnswer()
    createTableParticipation()


def createTableQuestion():
    try:
        cur = dbCursor()
        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS "Question" (
        "id"	INTEGER,
        "text"	TEXT,
        "title"	TEXT,
        "image"	TEXT,
        "position"	INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        )
        cur.execute("commit")
        cur.close()

    except Exception as e:
        print("error:")
        print(e)
        cur.execute("rollback")
        cur.close()
        raise e

def createTableAnswer():
    try:
        cur = dbCursor()
        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS "Answer" (
                "id"	INTEGER UNIQUE,
                "text"	TEXT,
                "isCorrect"	INTEGER,
                "id_question"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
                FOREIGN KEY("id_question") REFERENCES "Question"("id")
        );
        """
        )
        cur.execute("commit")
        cur.close()

    except Exception as e:
        print("error:")
        print(e)
        cur.execute("rollback")
        cur.close()
        raise e

def createTableParticipation():
    try:
        cur = dbCursor()
        cur.execute(
        """
        CREATE TABLE IF NOT EXISTS "Participation" (
            "id"	INTEGER UNIQUE,
            "playerName"	TEXT,
            "score"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        )
        cur.execute("commit")
        cur.close()

    except Exception as e:
        print("error:")
        print(e)
        cur.execute("rollback")
        cur.close()
        raise e


def getQuestionPosition(position: int):
    try:
        cur = dbCursor()
        


        cur.execute(f"SELECT * FROM Question WHERE position = {position}")

        
        result_question = cur.fetchone()
        if result_question == None:
            raise ErrorHandler("Question not Found!", 404)

        print("went through")
        cur.execute(
            f"SELECT * FROM Answer WHERE id_question = {result_question[0]}")

        result_answer = cur.fetchall()
        answers = [Answer(answer[1], answer[2]) for answer in result_answer]

        question = Question(result_question[1],result_question[2],result_question[3],result_question[4], answers)

        cur.execute('end')
        cur.close()
        return question



    except ErrorHandler as e:
        cur.execute('rollback')
        cur.close()
        raise e
        
    except Exception as e:
        cur.execute('rollback')
        cur.close()
        raise Exception("Error, failed trying to get question by position:  " + str(e))


def deleteQuestion(id_question: int):
    try:
        cur = dbCursor()
        question_json = getQuestionIdDb(id_question)
        
        cur.execute(
            f"DELETE FROM Question where id = {id_question}"
            )

        cur.execute(
            f"UPDATE Question SET position = position - 1 "
            f"WHERE position >= {question_json['position']!r}"
            )
        cur.execute("commit")
        cur.close()

    except ErrorHandler as e:
        cur.execute('rollback')
        cur.close()
        raise e

    except Exception as e:
        cur.execute("rollback")
        cur.close()
        raise Exception("Error: couldnt remove this question: " + str(e))



def deleteAnswer(id_question: int):
    try:
        cur = dbCursor()
        cur.execute("DELETE FROM Answer WHERE id_question = ?",(id_question,))
        cur.execute("commit")
        cur.close()

    except Exception as e:
        cur.execute("rollback")
        cur.close()
        raise Exception("Error: couldnt remove this answer" + str(e))


def  deleteAllQuestions():
    try:
        cur = dbCursor()
        cur.execute("DELETE FROM Question")
        cur.execute("DELETE FROM Answer")
        cur.execute("commit")
        cur.close()
    
    except Exception as e:
        cur.execute("rollback")
        cur.close()
        raise Exception("Error: couldnt remove all questions" + str(e))


def  deleteAllParticipations():
    try:
        cur = dbCursor()
        cur.execute("DELETE FROM Participation")
        cur.execute("commit")
        cur.close()
    
    except Exception as e:
        cur.execute("rollback")
        cur.close()
        raise Exception("Error: couldnt remove all questions" + str(e))

def idByPosition(position):
    try:
        cur = dbCursor()

        cur.execute(f"SELECT * FROM Question WHERE position = {position}")

                
        result_question = cur.fetchone()
        cur.execute('end')
        cur.close()
        

        return result_question[0]

    except Exception as e:
        cur.execute("rollback")
        cur.close()
        raise Exception("Error: couldnt remove all questions" + str(e))




