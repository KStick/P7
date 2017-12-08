import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import base64
import os
import time
import requests

import cv2 as cv



fourcc = cv.VideoWriter_fourcc('M','J','P','G')
isColor = 1
fps     = 24  # or 30, frames per second
frameW  = 320 # images width
frameH  = 240 # images height

class Session:

	def __init__(self, sessionID):
		self.sessionID = sessionID
		self.students = set()
		self.tutor = None
		self.studentWriter = None
		self.tutorWriter = None

	def addTutor(self, tutor):
		self.tutor = tutor

	def addStudent(self, student):
		self.students.add(student)

	def addStudentWriter(self, writer):
		self.studentWriter = writer

	def addTutorWriter(self, writer):
		self.tutorWriter = writer



sessionList = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		pass

	def on_message(self, message):
		if message.split(",")[0] == "data:image/jpeg;base64":
			sessionVar = None
			role = None
			for session in sessionList:
				if self in session.students:
					sessionVar = session
					role = "student"
				elif self == session.tutor:
					sessionVar = session
					role = "tutor"
			if sessionVar != None:
				if role == "tutor":
					start = time.time()
					fh = open(os.getcwd() + "/T" + sessionVar.sessionID + ".jpeg", "wb")
					fh.write(message.split(",")[1].decode("base64"))
					fh.close()
					img = cv.imread(os.getcwd() + "/T" + sessionVar.sessionID + ".jpeg")
					sessionVar.tutorWriter.write(img)
					for student in sessionVar.students:
						student.write_message(message)
					print "frame sent and saved in " + str(time.time() - start) + " sec"
				elif len(sessionVar.students) == 1:
						start = time.time()
						fh = open(os.getcwd() + "/S" + sessionVar.sessionID + ".jpeg", "wb")
						fh.write(message.split(",")[1].decode("base64"))
						fh.close()
						img = cv.imread(os.getcwd() + "/S" + sessionVar.sessionID + ".jpeg")
						sessionVar.studentWriter.write(img)
						if sessionVar.tutor != None:
							sessionVar.tutor.write_message(message)
						print "frame sent and saved in " + str(time.time() - start) + " sec"
				else:
					pass
		elif message.split(",")[0] == "tutor":
			print "tutor"
			new = True
			sessionVar = None
			for session in sessionList:
				if session.sessionID == message.split(",")[1]:
					new = False
					sessionVar = session
			if new:
				print "addtutor"
				sessionVar = Session(message.split(",")[1])
				sessionVar.addTutor(self)	
				writer = cv.VideoWriter("T"+str(message.split(",")[1]) + ".avi", fourcc, fps,(frameW,frameH),isColor)	
				sessionVar.addTutorWriter(writer)
				sessionList.append(sessionVar)
			else:
				sessionVar.addTutor(self)
				writer = cv.VideoWriter("T"+str(message.split(",")[1]) + ".avi", fourcc, fps,(frameW,frameH),isColor)	
				sessionVar.addTutorWriter(writer)
			
		elif message.split(",")[0] == "student":
			new = True
			sessionID = message.split(",")[1]
			for session in sessionList:
				if session.sessionID == sessionID:
					new = False
					sessionVar = session
			if new:
				session = Session(sessionID)
				session.addStudent(self)	
				writer = cv.VideoWriter("S"+str(sessionID) + ".avi", fourcc, fps,(frameW,frameH),isColor)	
				session.addStudentWriter(writer)
				sessionList.append(session)
				#r = requests.post("localhost:5000/JoinSession", data={'id': message.split(",")[1]})
			else:
				sessionVar.addStudent(self)
				if sessionVar.studentWriter == None:
					writer = cv.VideoWriter("S"+str(sessionID) + ".avi", fourcc, fps,(frameW,frameH),isColor)	
					sessionVar.addStudentWriter(writer)
		else:
			print message



 
	def on_close(self):
		for session in sessionList:
			if self == session.tutor:
				session.tutor = None
			elif self in session.students:
				session.students.remove(self)

	def check_origin(self, origin):
		return True
 
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/websocket', WebSocketHandler)
		]
 
		settings = {
			'template_path': 'templates'
		}
		tornado.web.Application.__init__(self, handlers, **settings)
 
 
if __name__ == '__main__':
	ws_app = Application()
	server = tornado.httpserver.HTTPServer(ws_app)
	server.listen(8080)
	tornado.ioloop.IOLoop.instance().start()