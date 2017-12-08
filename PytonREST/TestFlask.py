#!/usr/bin/python

from multiprocessing import Pool, TimeoutError
import time
import os
import random
import requests
import string

def startTest():
	username = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(19))
	password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(19))
	email = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8)) + "@hotmail.com"
	role = random.choice(['student', 'tutor'])
	subject = random.choice(['Math', 'Biology'])
	question = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(42)) + "?"
	access = random.choice(['public', 'private'])


	createUser(username, password,email,role)
	login(username, password)
	createQuestion(username, subject, question, access)

	getPrivateQuestions()


def createUser(username, password, email, role):
	response = requests.post("http://172.17.245.96:5000/GenerateSalt", data={'username':username})
	salt = response.text
	print salt
	role = requests.post("http://172.17.245.96:5000/CreateUser", data={'username':username, 'key':password, 'email':email, 'role':role, 'salt':salt})
	print role.text

def login(username, password):
	role = requests.post("http://172.17.245.96:5000/validateLogin", data={'username':username, 'HashedPassword':password})
	print role.text

def createQuestion(username, subject, question, access):
	id = requests.post("http://172.17.245.96:5000/Questions", data={'submit':'yes', 'username':username, 'subject':subject, 'question':question, 'access':access})
	print id.text

def getPrivateQuestions():
	res = requests.get('http://172.17.245.96:5000/Questions', data ={'submit':'no', 'access':'private'})
	print res.text
	
def spawnProcesses(num):
    pool = Pool(processes=num)              # start 4 worker processes
    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [pool.apply_async(startTest, ()) for i in range(num)]
    [res.get(timeout=360) for res in multiple_results]

if __name__ == '__main__':
	spawnProcesses(100)
	

	#spawnProcesses(50)