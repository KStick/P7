##TODO##
#Fix redundancy such as conn in every function
# pip install bcrypt | if dependency errors use:
#				$ sudo apt-get install build-essential libffi-dev python-dev
#pip install Flask


from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import re
import base64
import  bcrypt

import psycopg2

def connect():
	try:
		return psycopg2.connect("dbname='postgres' user='postgres' host ='localhost' password='123'")
	except Exception as e:
		raise	
	
app = Flask(__name__)
CORS(app)

@app.cli.command("initdb")
def initdb():
	conn = connect()
	cur = conn.cursor()
	
	try:
		cur.execute("""CREATE TABLE users( 
						username TEXT UNIQUE NOT NULL, 
						password TEXT NOT NULL, 
						email TEXT NOT NULL,
						salt TEXT DEFAULT NULL);
					""")
	except Exception as e:
		print "users error"
		pass
	
	try:
		cur.execute("""CREATE TABLE questions(
						question_id serial PRIMARY KEY,
						username TEXT NOT NULL REFERENCES users(username) ON UPDATE CASCADE , 
						subject TEXT NOT NULL,
						question TEXT NOT NULL,
						date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP::TIMESTAMP(0),
						answered BOOLEAN DEFAULT false,
						public BOOLEAN NOT NULL,
						count Integer NOT NULL); 
					""")
	except Exception as e:
		print "questions error:"
		pass
	
	try:
		cur.execute("""CREATE TABLE roles(
						role TEXT UNIQUE PRIMARY KEY NOT NULL); 
					""")
	except Exception as e:
		print "roles error:"
		pass
	
	try:
		cur.execute("""CREATE TABLE user_roles(
						username TEXT NOT NULL UNIQUE REFERENCES users(username) ON UPDATE CASCADE, 
						role TEXT REFERENCES roles(role));
					""")
	except Exception as e:
		print "user_roles error: "
		pass

	try:
		cur.execute("""CREATE TABLE session_history(
						username TEXT NOT NULL UNIQUE REFERENCES users(username) ON UPDATE CASCADE, 
						question_id Integer REFERENCES questions(question_id));
					""")
	except Exception as e:
		print "Session_history error : "
		pass

	try:
		cur.execute("""CREATE TABLE tutor_subject(
			username TEXT NOT NULL REFERENCES users(username),
			subject TEXT NOT NULL); 
			""")
	except Exception as e:
		print "Tutor table error"
		pass	
	conn.commit()
	cur.close()
	conn.close()

@app.cli.command("seedData")
def seedData():
	conn = connect()
	cur = conn.cursor()
	cur.execute("""INSERT INTO users(username, password,email, salt) VALUES('henry','$2b$14$dgelyw4eIDf41V.uQ8fyzehy3jtAArO.nMSMxxzDCir/9Dd15mlxO','123@a123.com', '$2b$14$dgelyw4eIDf41V.uQ8fyze');""")
	cur.execute("""INSERT INTO users(username, password,email, salt) VALUES('Finn','$2b$14$bOi4M43fiPTTQ3yUmUdB4eJ5geRB9GDNIKDM777/RNZN/0A4v7vTq','123@a123.com', '$2b$14$bOi4M43fiPTTQ3yUmUdB4e');""")
	cur.execute("""INSERT INTO roles(role) VALUES('student');""")
	cur.execute("""INSERT INTO roles(role) VALUES('tutor');""")
	cur.execute("""INSERT INTO roles(role) VALUES('math_teacher');""")
	cur.execute("""INSERT INTO roles(role) VALUES('professor');""")
	cur.execute("""INSERT INTO roles(role) VALUES('high_school_teacher');""")
	cur.execute("""INSERT INTO roles(role) VALUES('toddler');""")
	cur.execute("""INSERT INTO user_roles(username,role) VALUES('henry','student');""")
	cur.execute("""INSERT INTO user_roles(username,role) VALUES('Finn','tutor');""")
	cur.execute("""INSERT INTO tutor_subject(username, subject) VALUES('Finn', 'Mathematics');""")
	cur.execute("""INSERT INTO tutor_subject(username, subject) VALUES('Finn', 'Software');""")
	cur.execute("""INSERT INTO tutor_subject(username, subject) VALUES('Finn', 'Biology');""")
	conn.commit()
	cur.close()
	conn.close()



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

#Work in progress
#def getQuestion(id):
#	conn = connect()
#	cur = conn.cursor()
#	query = """ SELECT questions.username,questions.question,questions.date_time,questions.count
#				FROM"""

@app.route('/Questions', methods = ['GET', 'POST'])
def Questions():
	data = request.form
	if data['submit']=='yes':
		username = data['username']
		subject = data['subject']
		question = data['question']
		access = data['access']
		conn = connect()
		cur = conn.cursor()
		query = "INSERT INTO questions(username, subject, question, public, count)" + " VALUES('" + str(username) + "','" + str(subject) + "','" + str(question) + "'," + str(str(access)=='public') + ", 1) RETURNING question_id;"
		cur.execute(query)
		sessionID = cur.fetchone()[0]
		conn.commit()
		cur.close()
		conn.close()
		return str(sessionID)

	elif data['submit']=='no' and data['access']=='public':
		conn = connect()
		cur = conn.cursor()
		query = "SELECT * FROM questions WHERE answered = false AND public = true;"
		cur.execute(query)
		question = cur.fetchall()
		pattern = r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\)"
		conn.commit()
		cur.close()
		conn.close()
		return re.sub(pattern=pattern, repl="\\1-\\2-\\3 \\4:\\5:\\6", string=str(question))[:-2]

	elif data['submit']=='no' and data['access']=='private':
		conn = connect()
		cur = conn.cursor()
		query = "SELECT * FROM questions WHERE answered = false AND public = false;"
		cur.execute(query)
		question = cur.fetchall()
		pattern = r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\)"
		conn.commit()
		cur.close()
		conn.close()
		return re.sub(pattern=pattern, repl="\\1-\\2-\\3 \\4:\\5:\\6", string=str(question))[:-2]

@app.route('/QuestionAnswered', methods = ["POST"])
def QuestionAnswered():
	data = request.form
	sessionid = data['id']
	conn = connect()
	cur = conn.cursor()
	query = "UPDATE questions SET answered = true WHERE question_id = " + str(sessionid) + ";"
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()
	return ""
	
@app.route('/JoinSession', methods = ["POST"])
def JoinSession():
	data = request.form
	sessionid = data['id']
	conn = connect()
	cur = conn.cursor()
	query = "UPDATE questions SET count = count+1 WHERE question_id = " + str(sessionid) + ";"
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()
	return ""

@app.route('/LeaveSession', methods = ["POST"])
def LeaveSession():
	data = request.form
	sessionid = data['id']
	conn = connect()
	cur = conn.cursor()
	query = "UPDATE questions SET count = count-1 WHERE question_id = " + str(sessionid) + ";"
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()
	return ""

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
	return ""

@app.route('/validateLogin', methods = {'POST'})
def validateLogin():
	#SELECT role FROM users,user_roles WHERE users.username = user_roles.username;

	data = request.form
	username = data['username']
	password = data['HashedPassword']

	print 0
	conn = connect()
	cur = conn.cursor()
	print 1
	query = "SELECT role,password FROM users NATURAL JOIN user_roles WHERE users.username ='" + str(username) + "';"
	cur.execute(query)
	result = cur.fetchone();
	conn.commit
	cur.close()
	conn.close()
	databasePassword = result[1]
	print 2
	salt = GetSalt()
	print 3
	inputPassword = bcrypt.hashpw(bytes(password),bytes(salt))

	#print databasePassword==inputPassword
	if databasePassword == inputPassword:
		if result[0] != None:
			return result[0]
		else:
			return "NULL"
	else:
		return "Login error"

@app.route('/CreateUser', methods = ['POST'])
def CreateUser():

	data = request.form
	username = data['username']
	password = data['key']
	email = data['email']
	role = data['role']
	salt = data['salt']
	try:
		password = bcrypt.hashpw(bytes(password),bytes(salt))

		conn = connect()
		cur = conn.cursor()
		query = "INSERT INTO users(username, password, email, salt) " + "VALUES ('" + str(username) + "','" + str(password) + "','" + str(email) + "','" + str(salt) + "');"
		cur.execute(query)
		conn.commit()
		query = "INSERT INTO user_roles(username, role) " + "VALUES ('" + str(username) +"','" + str(role) + "') RETURNING role;"
		cur.execute(query)
		conn.commit()
		assigned_role = cur.fetchone()[0]
		cur.close()
		conn.close()
		return str(assigned_role)
	except psycopg2.Error as e:
		print e
		return('username_taken')

@app.route('/GenerateSalt', methods = ['POST'])
def GenerateSalt():
	data = request.form
	username = data['username']
	salt = bcrypt.gensalt(rounds=14)	
	conn = connect()
	cur = conn.cursor()
	#query = "UPDATE users SET salt ='" + str(salt) +"' WHERE username = '" + str(username) "';"
	return salt; 

@app.route('/GetSalt', methods = ['POST'])
def GetSalt():
	data = request.form
	username = data['username']
	conn = connect()
	cur = conn.cursor()
	query = "SELECT salt FROM users WHERE username ='" + str(username) + "';"
	cur.execute(query)
	salt = cur.fetchone()
	cur.close()
	conn.close()
	if salt == None:
		return "usernameNotExist"	
	return salt[0]

@app.route('/GetRole/<string:username>')
def GetRole(username):
	conn = connect()
	cur = conn.cursor()
	query = "SELECT role FROM user_roles WHERE username = '" + str(username) + "';"
	cur.execute(query)
	role = cur.fetchone()[0]
	conn.commit()
	cur.close()
	conn.close()
	return role