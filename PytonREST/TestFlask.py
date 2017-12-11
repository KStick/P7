#!/usr/bin/python

from multiprocessing import Pool, TimeoutError
import threading
import time
import os
import random
import requests
import string
import Queue

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
	response = requests.post("http://localhost:5000/GenerateSalt", data={'username':username})
	salt = response.text
	role = requests.post("http://localhost:5000/CreateUser", data={'username':username, 'key':password, 'email':email, 'role':role, 'salt':salt})

def login(username, password):
	role = requests.post("http://localhost:5000/validateLogin", data={'username':username, 'HashedPassword':password})

def createQuestion(username, subject, question, access):
	id = requests.post("http://localhost:5000/Questions", data={'submit':'yes', 'username':username, 'subject':subject, 'question':question, 'access':access})

def getPrivateQuestions():
	res = requests.get('http://localhost:5000/Questions', data ={'submit':'no', 'access':'private'})
	
def spawnProcesses(num):
    pool = Pool(processes=num)              # start 4 worker processes
    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [pool.apply_async(startTest, ()) for i in range(num)]
    [res.get(timeout=360) for res in multiple_results]



exitFlag = True

class myThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.time = []
	def run(self):
		while exitFlag:
			start = time.time()
			startTest()
			self.time.append(time.time() - start)

if __name__ == '__main__':
	threads = []
	threadID = 1

	start = time.time()

	# Create new threads
	for i in range(0,20):
		thread = myThread()
		thread.start()
		threads.append(thread)
	while True:
		if time.time() - start >= 3 :
			exitFlag = False
			print "##################################################"
			print "Kenneth exit"
			print "##################################################"
			break

	# Wait for all threads to complete
	count = 0
	for t in threads:
		count+=1
		print len(t.time)
		t.join()
	print "Exiting Main Thread"
	print count