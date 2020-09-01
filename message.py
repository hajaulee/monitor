import pyrebase
import json
import os




config = {
  "apiKey": "AIzaSyBvSo1GFKS_XN6LYKC2QDkfm8o8UK2iJhE",
  "authDomain": "",
  "databaseURL": "https://dl-monitor.firebaseio.com/",
  "storageBucket": "",
  "serviceAccount": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()




class Experiment(object):
	"""docstring for Experiment"""
	def __init__(self, name, capture_log=False, clear_old=True):
		super(Experiment, self).__init__()
		self.name = name

		api_path = os.path.expanduser('~/.remote_log.api')
		with open(api_path) as file:
			self.user_api = file.read().strip()

		if clear_old:
			self.clear()


	def clear(self):
		db.child("experiments").child(self.user_api).child(self.name).remove()


	def metric(self, met, mss):
		db.child("experiments").child(self.user_api).child(self.name).child('metric').child(met).push(float(mss))

	def param(self, par, mss):
		db.child("experiments").child(self.user_api).child(self.name).child('param').child(par).set(json.dumps(mss))

	def capture_log(self):
		pass


test = Experiment('Hello')
test.param('new', dict({'c': 1, 'd': 6}))
test.param('newb', dict({'c': 1, 'd': 6}))
test.param('newc', dict({'c': 1, 'd': 6}))
test.metric('acc', 10)
test.metric('acc', 122)