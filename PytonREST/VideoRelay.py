import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import base64
import os
import time

import cv2 as cv


active_clients = set() 

fourcc = cv.VideoWriter_fourcc('M','J','P','G')
isColor = 1
fps     = 24  # or 30, frames per second
frameW  = 320 # images width
frameH  = 240 # images height
writer = cv.VideoWriter("video.avi",fourcc, 
fps,(frameW,frameH),isColor)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		active_clients.add(self)
		pass

	def on_message(self, message):
		start = time.time()
		fh = open(os.getcwd() + "/image.jpeg", "wb")
		fh.write(message.split(",")[1].decode("base64"))
		fh.close()
		img = cv.imread(os.getcwd() + "/image.jpeg")
		writer.write(img)
		for client in active_clients:
			client.write_message(message)
		print "frame sent and saved in " + str(time.time() - start) + "sec"
		#self.write_message(message)

 
	def on_close(self):
		active_clients.remove(self)
		pass

	def check_origin(self, origin):
		return True
 
 
class IndexPageHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")
 
 
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', IndexPageHandler),
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