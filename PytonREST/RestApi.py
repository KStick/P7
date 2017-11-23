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
		pass
	try:
		cur.execute("""CREATE TABLE questions(
						id serial PRIMARY KEY,
						username TEXT NOT NULL REFERENCES users(username) ON UPDATE CASCADE , 
						subject TEXT NOT NULL,
						question TEXT NOT NULL,
						date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP::TIMESTAMP(0),
						answered BOOLEAN DEFAULT false,
						public BOOLEAN NOT NULL); 
					""")
	except Exception as e:
		pass
	try:
		cur.execute("""CREATE TABLE roles(
						role TEXT UNIQUE PRIMARY KEY NOT NULL); 
					""")
	except Exception as e:
		pass
	try:
		cur.execute("""CREATE TABLE user_roles(
						username TEXT NOT NULL UNIQUE REFERENCES users(username) ON UPDATE CASCADE, 
						role TEXT REFERENCES roles(role));
					""")
	except Exception as e:
		pass
	conn.commit()
	cur.close()
	conn.close()

@app.cli.command("seedData")
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
	cur.execute("""INSERT INTO roles(role) VALUES('tutor');""")
	cur.execute("""INSERT INTO roles(role) VALUES('professor');""")
	cur.execute("""INSERT INTO roles(role) VALUES('high_school_teacher');""")
	cur.execute("""INSERT INTO roles(role) VALUES('toddler');""")
	cur.execute("""INSERT INTO user_roles(username,role) VALUES('henry','student');""")
	cur.execute("""INSERT INTO user_roles(username,role) VALUES('Finn','tutor');""")
	conn.commit()
	cur.close()
	conn.close()


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    return 'Hello, World'

#Make it a bit more beautiful to look at. For example fix append
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
		print(access)
		query = "INSERT INTO questions(username, subject, question, public)" + " VALUES('" + str(username) + "','" + str(subject) + "','" + str(question) + "'," + str(str(access)=='public') + ") RETURNING id;"
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
		return re.sub(pattern=pattern, repl="\\1-\\2-\\3 \\4:\\5:\\6", string=str(question))
		conn.commit()
		cur.close()
		conn.close()
		return str(question)

	elif data['submit']=='no' and data['access']=='private':
		conn = connect()
		cur = conn.cursor()
		query = "SELECT * FROM questions WHERE answered = false AND public = false;"
		cur.execute(query)
		question = cur.fetchall()
		pattern = r"datetime\.datetime\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+)\)"
		return re.sub(pattern=pattern, repl="\\1-\\2-\\3 \\4:\\5:\\6", string=str(question))
		conn.commit()
		cur.close()
		conn.close()
		return str(question)

	else:
		return "What are you trying to do?"

@app.route('/QuestionAnswered', methods = ["POST"])
def QuestionAnswered():
	data = request.form
	sessionid = data['id']
	conn = connect()
	cur = conn.cursor()
	query = "UPDATE questions SET answered = true WHERE id = " + str(sessionid) + ";"
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()
	return "what are you doing here"
	

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

@app.route('/validateLogin', methods = {'POST'})
def validateLogin():
	#SELECT role FROM users,user_roles WHERE users.username = user_roles.username;

	data = request.form
	username = data['username']
	password = data['password']

	conn = connect()
	cur = conn.cursor()
	query = "SELECT role FROM users NATURAL JOIN user_roles WHERE users.username ='" + str(username) + "' " + "AND users.password = '" + str(password) + "';"
	cur.execute(query)
	role = cur.fetchone();
	conn.commit
	cur.close()
	conn.close()
	if role != None:
		return role[0]
	else:
		return "NULL"

@app.route('/CreateUser', methods = ['POST'])
def CreateUser():

	data = request.form
	username = data['username']
	password = data['key']
	email = data['email']
	role = data['role']
	salt = data['response']
	try:
		password = bcrypt.hashpw(password.encode('utf8'),salt.encode('utf8'))

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
	username = ['username']
	salt = bcrypt.gensalt(rounds=14)	
	conn = connect()
	cur = conn.cursor()
	#query = "UPDATE users SET salt ='" + str(salt) +"' WHERE username = '" + str(username) "';"
	return salt; 


