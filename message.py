import pyrebase
import json
import os
import datetime



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

		self.exp_path = "experiments/{}/{}".format(self.user_api, self.name)
		if clear_old:
			self.clear()

		db.child(self.exp_path).set({	'start_time': datetime.datetime.now().isoformat(), 
						'latest_time': datetime.datetime.now().isoformat()})


	def clear(self):
		db.child(self.exp_path).remove()


	def metric(self, met, mss):
		db.child(self.exp_path).child('metric').child(met).push(float(mss))

	def param(self, par, mss):
		db.child(self.exp_path).child('param').child(par).set(json.dumps(mss))

	def log(self, mss):
		log_time = datetime.datetime.now().isoformat().split('.')[0]
		db.child(self.exp_path).child('logs').push(log_time + ': ' + mss)

	def command(self, mss):
		try:
			db.child(self.exp_path).child('eval').push(str(eval(mss)))
		except Exception as e:
			db.child(self.exp_path).child('eval').push(str(e))

	def capture_log(self):
		pass


test = Experiment('Exp_name_3')
test.param('newa', dict({'c': 1, 'd': 6}))
test.param('newb', dict({'c': 1, 'd': 6}))
test.param('newc', dict({'c': 1, 'd': 6}))

# for i in range(100):
# 	test.metric('acc', i)


# for i in range(100):
# 	test.metric('loss', (100 - i) / 100)


import time
import random
i = 0
while True:
	test.log('Hello' + str(time.time()))
	test.metric('acc', random.randint(0, 100))
	test.metric('loss', random.randint(0, 10))
	time.sleep(3)
	print(i, 'cc')
	i+=1