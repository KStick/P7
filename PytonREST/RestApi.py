from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

import psycopg2

def connect():
	try:
		return psycopg2.connect("dbname='user' user='user' host ='localhost' password='123'")
	except Exception as e:
		raise	
	
app = Flask(__name__)
CORS(app)

@app.cli.command()
def initdb():
	conn = connect()
	cur = conn.cursor()
	try:
		cur.execute("""CREATE TABLE users(id serial PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL);""")
	except Exception as e:
		pass
	try:
		cur.execute("""CREATE TABLE questions(id serial PRIMARY KEY, username TEXT NOT NULL REFERENCES users(username) , subject TEXT NOT NULL  ,question TEXT NOT NULL, date_time TIMESTAMP WITH TIME ZONE NOT NULL default CURRENT_TIMESTAMP); """)
	except Exception as e:
		pass
	try:
		cur.execute("""CREATE TABLE roles(id serial PRIMARY KEY, role TEXT UNIQUE NOT NULL); """)
	except Exception as e:
		pass
	try:
		cur.execute("""CREATE TABLE user_roles(id serial PRIMARY KEY, username TEXT NOT NULL UNIQUE REFERENCES users(username), role TEXT REFERENCES roles(role));""")
	except Exception as e:
		pass
	conn.commit()
	cur.close()
	conn.close()

@app.cli.command()
def seedData():
	conn = connect()
	cur = conn.cursor()
	cur.execute("""INSERT INTO users(username, password,email) VALUES('henry','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('pedro','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Kenneth','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Finn','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Max','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Morgan','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Henrik Vanderheim','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Mark','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Reggie','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Jim Sterling','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('OnePunch','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Joseph','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Megaman','123','123@a123.com');""")
	cur.execute("""INSERT INTO users(username, password,email) VALUES('Trent','123','123@a123.com');""")
	cur.execute("""INSERT INTO roles(role) VALUES('student');""")
	cur.execute("""INSERT INTO roles(role) VALUES('math_teacher');""")
	cur.execute("""INSERT INTO roles(role) VALUES('professor');""")
	cur.execute("""INSERT INTO roles(role) VALUES('high_school_teacher');""")
	cur.execute("""INSERT INTO roles(role) VALUES('toddler');""")
	conn.commit()
	cur.close()
	conn.close()


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
	query = "INSERT INTO questions(username, subject, question)" + " VALUES('" + str(username) + "','" + str(subject) + "','" + str(question) + "') RETURNING id;"
	cur.execute(query)
	sessionID = cur.fetchone()[0]
	conn.commit()
	cur.close()
	conn.close()
	return str(sessionID)

@app.route('/InsertRole', methods = ['POST'])
def insertRole():

	#format user:role

	data = request.form
	username = data['username']
	role = data['role']
	conn = connect()
	cur = conn.cursor()
	query = "INSERT INTO roles(username, role) " + "VALUES ('" + str(username) +"','" + str(role) + "');"
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()
