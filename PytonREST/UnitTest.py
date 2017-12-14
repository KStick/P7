import unittest
import random
import string
import requests
import sys

def createUser(password, email, role):
   username = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(19))
   response = requests.post("http://localhost:5000/GenerateSalt", data={'username':username})
   salt = response.text
   role = requests.post("http://localhost:5000/CreateUser", data={'username':username, 'key':password, 'email':email, 'role':role, 'salt':salt})
   return role.text

def login(username, password):
   role = requests.post("http://localhost:5000/validateLogin", data={'username':username, 'HashedPassword':password})
   return role.text

def createQuestion(username, subject, question, access):
   id = requests.post("http://localhost:5000/Questions", data={'submit':'yes', 'username':username, 'subject':subject, 'question':question, 'access':access})
   return id.text

def getPrivateQuestions():
   res = requests.get('http://localhost:5000/Questions', data ={'submit':'no', 'access':'private'})
   return res.text

class TestStringMethods(unittest.TestCase):

   def test_createUser(self):
      self.assertEqual(createUser('123', 'email@email.com', 'student'), 'student')

   def test_createUser_fail(self):
      self.assertNotEqual(createUser('123', 'email@email.com', 'cook'), 'cook')

   def test_login(self):
      self.assertEqual(login('Finnur', 'JVV/g9NvloQK7qptOCL9wenJlEw4/APTCJmN/c+0rA8='), 'tutor')

   def test_login_fail(self):
      self.assertNotEqual(login('Finnu', 'JVV/g9NvloQK7qptOCL9wenJlEw4/APTCJmN/c+0rA8='), 'tutor')

   def test_createQuestion(self):
      self.assertTrue(createQuestion('Mark', 'Software', 'Unit Test?', 'private').isdigit())

   def test_createQuestion_fail(self):
      self.assertFalse(createQuestion('Noone', 'Software', 'Unit Test?', 'private').isdigit())

   def test_getQuestins(self):
      self.assertTrue(getPrivateQuestions().find('Unit Test?') != -1)

   def test_getQuestins_fail(self):
      self.assertFalse(getPrivateQuestions().find('Not Unit Test?') != -1)


suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)