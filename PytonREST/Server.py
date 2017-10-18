#!/usr/bin/pyton2.7.6
#
#
#

import psycopg2

def connect():
	try:
		return psycopg2.connect("dbname='test' user='sivash' host ='localhost' password='123'")
	except Exception as e:
		raise	

def CreateTables():
	#date_time TIMESTAMP WITH TIME ZONE NOT NULL default current_timestamp
	conn = connect()
	cur = conn.cursor()
	try:
		cur.execute("""CREATE TABLE users(id serial PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL);""")
	except Exception as e:
		pass
	try:	
		cur.execute("""CREATE TABLE questions(id serial PRIMARY KEY, username INTEGER REFERENCES users(id) , subject TEXT NOT NULL  ,question TEXT NOT NULL, date_time TIMESTAMP WITH TIME ZONE NOT NULL default CURRENT_TIMESTAMP); """)
	except Exception as e:
		pass
	conn.commit()
	cur.close()
	conn.close()

def SeedData():
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
	conn.commit()
	cur.close()
	conn.close()

def insertQuestion(username, subject, question):
	#"""CREATE TABLE questions(id serial PRIMARY KEY, username INTEGER REFERENCES users(id) , subject TEXT NOT NULL  ,question TEXT NOT NULL); """)
	conn = connect()
	cur = conn.cursor()
	query = "SELECT id FROM users WHERE username = '" + username + "';"
	cur.execute(query)
	id = cur.fetchone()
	query = "INSERT INTO questions(username, subject, question) VALUES(" + str(id[0]) + ", '" + subject + "', '" + question + "');"
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()

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
	print returnData
	conn.commit()
	cur.close()
	conn.close()


CreateTables()
SeedData()
insertQuestion("henry","Math","What is some math question i hope nobody is going to read this as i dont know what i am doing")
getQuestion(1)
