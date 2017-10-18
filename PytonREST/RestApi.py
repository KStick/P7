from flask import Flask
from flask import request

import psycopg2

def connect():
	try:
		return psycopg2.connect("dbname='sivash' user='sivash' host ='localhost' password='123'")
	except Exception as e:
		raise	
	
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/getquestion/<int:id>')
def getQuestion(id):
	conn = connect()
	cur = conn.cursor()
	query = "SELECT * FROM questions WHERE id = " + str(id) + ";"
	cur.execute(query)
	question = cur.fetchone()
	query = "SELECT username FROM users WHERE id = " + str(question[1]) + ";"
	cur.execute(query)
	username = cur.fetchone() [0]
	returnData = []
	returnData.append(question[0])
	returnData.append(username)
	returnData.append(question[2])
	returnData.append(question[3])
	returnData.append(question[4])
	conn.commit()
	cur.close()
	conn.close()
	return str(returnData)

@app.route('/insertQuestion', methods = ['POST'])
def insertQuestion():
	
	#format user:subject:question
	
	data = request.form
	username = data['username']
	subject = data['subject']
	question = data['question']
	conn = connect()
	cur = conn.cursor()
	
	query = "SELECT id FROM users WHERE username = '" + str(username) + "';"
	cur.execute(query)
	userid = cur.fetchone() [0]
	
	query = "INSERT INTO questions(username, subject, question)" + " VALUES(" + str(userid) + ",'" + str(subject) + "','" + str(question) + "') RETURNING id;"
	cur.execute(query)
	sessionID = cur.fetchone()[0]
	conn.commit()
	cur.close()
	conn.close()
	return str(sessionID)
