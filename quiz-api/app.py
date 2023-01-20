from flask import Flask
from flask_cors import CORS
from flask import Flask, request, session, jsonify
import jwt_utils
import json
import database
from models import Question, Answer, Participation




app = Flask(__name__)
CORS(app)




@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def getQuizInfo():
	result = database.GetQuizInfo()
	
	return result, 200


@app.route('/login', methods=['POST'])
def login():
	print("entering the login process")
	payload = request.get_json()
	print("payload")
	password = payload['password']
	print("password: "+ password)
	if password == "flask2023":
		token = jwt_utils.build_token()
		token = json.dumps({"token": f'{token}'})
		return token, 200
	else:
		return 'Unauthorized', 401
	
@app.route('/questions', methods=['POST'])
def postQuestion():
	try:
		token = request.headers.get('Authorization')
		print(token)
		if token == None:
			return "You need to authenticate!", 401
		
		print("HERE IS THE BEARER TOKEN:")
		print(token[7:])

		json = request.get_json()

		possibleAnswers = json.get("possibleAnswers")
		list_answer = []
		for answer in possibleAnswers:
			list_answer.append(Answer(answer.get("text"), answer.get("isCorrect")))

		question = Question(json.get("text"), json.get("title"), json.get("image"), json.get("position")
		, list_answer)

		id_question = database.postQuestionDb(question)

		for answer in question.possibleAnswers:
			database.postAnswerDb(answer, id_question)

		return str(id_question), 200
	except Exception as e:
		print(e)
		return str(e), 500


@app.route('/participations', methods=['GET'])
def getParticipation():
	try:
		playerName = request.args['name']
		participation = database.getParticipation(playerName)

		return participation, 200

	except Exception as e:
		print(e)
		return str(e), 500


@app.route('/participations', methods=['POST'])
def postParticipation():
	try:


		json = request.get_json()
		print("json is:")
		print(json)

		if len(json.get("answers")) != database.getLastQuestionDb():
			return "bad request, doesnt fit quiz size!", 400
		playerName = json.get("playerName")
		list_answer = [answer for answer in json.get("answers")]

        
		score = database.getScore(list_answer)
		print("score is:")
		print(score)

		participation = Participation(playerName, score)

		id_participation = database.postParticipationDb(participation)


		print("id is :" + str(id_participation))

		return participation.to_json(), 200


	except Exception as e:
		print(e)
		return str(e), 500
        

@app.route('/participations/all', methods=['DELETE'])
def deleteAllParticipations():
	try:
		token = request.headers.get('Authorization')
		print(token)
		if token == None:
			return "You need to authenticate!", 401
		
		print("HERE IS THE BEARER TOKEN:")
		print(token[7:])


		database.deleteAllParticipations()
		
		return "OK", 204
	

	except Exception as e:
		print(e)
		return str(e), 500


@app.route('/questions/<int:id_question>', methods=['GET'])
def getQuestion(id_question):
	try:

		result = database.getQuestionIdDb(id_question)

		print(type(result))
		print(result)
		return result, 200


	except database.ErrorHandler as e:
		return e.message, e.errorCode

	except Exception as e:
		print(e)
		return str(e), 500

@app.route('/questions/idpos', methods=['GET'])
def idByPosition():
	try:
		position = request.args['position']

		result = database.idByPosition(position)

		return {"id_question" : result}, 200

	
	except database.ErrorHandler as e:
		return e.message, e.errorCode

	except Exception as e:
		print(e)
		return str(e), 500


@app.route('/questions/<int:id_question>', methods=['PUT'])
def putQuestion(id_question):
	try:
		token = request.headers.get('Authorization')
		print(token)
		if token == None:
			return "You need to authenticate!", 401
		
		print("HERE IS THE BEARER TOKEN:")
		print(token[7:])

		question_json = request.get_json()


		database.modifyQuestionDb(question_json, id_question)

	
	except database.ErrorHandler as e:
		return e.message, e.errorCode

	except Exception as e:
		print(e)
		return str(e), 500

	return "worked", 204


@app.route('/questions', methods=['GET'])
def getQuestionPosition():
	try:

		position = request.args['position']
		print(position)
		result = database.getQuestionPosition(position)
		
		return Question.to_json(result), 200


	except database.ErrorHandler as e:
		return e.message, e.errorCode
	
	except Exception as e:
		print(e)
		return str(e), 500

@app.route('/questions/all', methods=['GET'])
def getAllQuestions():
	try:
		json_all_questions = database.getAllQuestions()

		
		return json_all_questions


	except database.ErrorHandler as e:
		return e.message, e.errorCode
	
	except Exception as e:
		print(e)
		return str(e), 500


@app.route('/questions/<int:id_question>', methods=['DELETE'])
def deleteQuestion(id_question):
	try:
		token = request.headers.get('Authorization')
		print(token)
		if token == None:
			return "You need to authenticate!", 401
		
		print("HERE IS THE BEARER TOKEN:")
		print(token[7:])
		
		database.deleteQuestion(id_question)
		database.deleteAnswer(id_question)

		return "OK", 204
	
	except database.ErrorHandler as e:
		return e.message, e.errorCode

	except Exception as e:
		print(e)
		return str(e), 500


@app.route('/questions/all', methods=['DELETE'])
def deleteAllQuestions():
	try:
		token = request.headers.get('Authorization')
		print(token)
		if token == None:
			return "You need to authenticate!", 401
		
		print(token[7:])
		
		database.deleteAllQuestions()

		return "OK", 204

	except Exception as e:
		print(e)
		return str(e), 500



@app.route('/rebuild-db', methods=['POST'])
def rebuildDb():


	database.rebuildDb()

	return "Ok", 200


if __name__ == "__main__":
    app.run()